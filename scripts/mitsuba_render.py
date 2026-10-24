"""Render com luz real (Mitsuba 3, GPU) para o motor do historia-timelapse.

O motor (motor/render.mjs --camada) grava, por quadro, a camada transparente (HUD, cartões, globo, efeitos) e a câmera.
Este script desenha relevo + prédios no Mitsuba com a MESMA câmera (sol, sombra e luz do céu), prédios subindo no ano
deles, e monta: céu → Mitsuba → tom → camada. Nada é preso a uma cidade: lê cena.js e cidades/<id>/assets.

Uso:
  .venv/bin/python -I scripts/mitsuba_render.py <pasta-da-cena> <pasta-da-camada> <saida.mp4|pasta-jpg> [--spp 32] [--fps 30]
  (pasta-jpg: grava q_NNNNN.jpg, para conferir quadros-chave)
"""
import json, re, sys, time, subprocess, os
from pathlib import Path
import numpy as np
from PIL import Image
import mitsuba as mi
import drjit as dr
import mapbox_earcut as earcut

mi.set_variant("cuda_ad_rgb")
args = sys.argv[1:]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
CENA, CAMADA, SAIDA = Path(args[0]), Path(args[1]), Path(args[2])
SPP, FPS = int(opt("--spp", 32)), int(opt("--fps", 30))
W, H = 1920, 1080
ASSETS = CENA.parent / "assets"
C = json.loads(re.sub(r"^window.CENA = |;\s*$", "", (CENA / "cena.js").read_text()))
T = json.loads((ASSETS / "terreno.json").read_text())
w0, s0, e0, n0 = T["bbox"]
lon0, lat0 = (w0 + e0) / 2, (s0 + n0) / 2
RT, RAD = 6378137.0, np.pi / 180
K = np.cos(lat0 * RAD)                       # Mercator em metros na latitude do centro (o modelo do deck.gl)
merc = lambda lat: np.log(np.tan(np.pi / 4 + np.asarray(lat) * RAD / 2))
Y0 = merc(lat0)


def M(lon, lat, z):
    """lon/lat/z (m) -> coordenadas do Mitsuba (x leste, y cima, z sul), em metros."""
    x = RT * (np.asarray(lon) - lon0) * RAD * K
    n = RT * (merc(lat) - Y0) * K
    return np.stack([x, np.asarray(z, dtype=np.float64) * np.ones_like(x), -n], -1)


lin = lambda c: np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
srgb = lambda x: np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.maximum(x, 0), 1 / 2.4) - 0.055)
t0 = time.time()

# ---------- relevo: elev.png decodificado como no motor (z × EXZ), textura do satélite ----------
EXZ, EXB, NASCER = C.get("exz", 1.6), C.get("exb", 1.5), C.get("nascer", 2.5)
el = np.asarray(Image.open(ASSETS / "elev.png").convert("RGB")).astype(np.float64)
z = (el[..., 0] * 256 + el[..., 1] + el[..., 2] / 256 - 32768) * EXZ
ny, nx = z.shape
LON = np.linspace(w0, e0, nx)[None, :].repeat(ny, 0)
LAT = np.linspace(n0, s0, ny)[:, None].repeat(nx, 1)
V = M(LON.ravel(), LAT.ravel(), z.ravel()).astype(np.float32)
UV = np.stack([np.linspace(0, 1, nx)[None, :].repeat(ny, 0).ravel(), np.linspace(0, 1, ny)[:, None].repeat(nx, 1).ravel()], 1).astype(np.float32)
i = np.arange(ny * nx).reshape(ny, nx)
a, b, c_, d = i[:-1, :-1].ravel(), i[:-1, 1:].ravel(), i[1:, :-1].ravel(), i[1:, 1:].ravel()
F = np.concatenate([np.stack([a, c_, b], 1), np.stack([b, c_, d], 1)]).astype(np.uint32)
terreno = mi.Mesh("terreno", len(V), len(F), has_vertex_normals=True, has_vertex_texcoords=True)
p = mi.traverse(terreno)
p["vertex_positions"] = V.ravel(); p["faces"] = F.ravel(); p["vertex_texcoords"] = UV.ravel(); p.update()
terreno.recompute_vertex_normals()

# ---------- prédios: contornos reais (pred_pos/pred_ini), teto = chão; paredes + telhado (earcut) ----------
POS = np.fromfile(ASSETS / "pred_pos.f32", np.float32).reshape(-1, 3).astype(np.float64)
INI = np.fromfile(ASSETS / "pred_ini.u32", np.uint32).astype(np.int64)
ALT = np.fromfile(ASSETS / "pred_alt.f32", np.float32)
ANO = np.fromfile(ASSETS / "pred_ano.f32", np.float32)
n = len(ALT); nv = len(POS)
cache = ASSETS / "mitsuba_predios.npz"
P2 = M(POS[:, 0], POS[:, 1], 0)[:, [0, 2]]
if cache.exists() and np.load(cache)["nv"] == nv:
    TRI = np.load(cache)["tri"]
else:
    tri = []
    for k in range(n):
        s, e = INI[k], INI[k + 1]
        t = earcut.triangulate_float64(P2[s:e], np.array([e - s], np.uint32))
        tri.append(t.astype(np.int64) + s)
    TRI = np.concatenate(tri).reshape(-1, 3)
    np.savez(cache, tri=TRI, nv=nv)
dono = np.repeat(np.arange(n), np.diff(INI))                    # prédio de cada vértice
prox = np.arange(nv) + 1; prox[INI[1:] - 1] = INI[:-1]          # vértice seguinte no mesmo anel
base = np.arange(nv); topo = base + nv                           # anéis: 0..nv-1 base, nv..2nv-1 topo
PAR = np.concatenate([np.stack([base, prox, prox + nv], 1), np.stack([base, prox + nv, topo], 1)])
# telhado com a orientação para cima (earcut devolve a ordem do anel; corrigir pela normal)
q = M(POS[:, 0], POS[:, 1], 0)
nrm = np.cross(q[TRI[:, 1]] - q[TRI[:, 0]], q[TRI[:, 2]] - q[TRI[:, 0]])[:, 1]
TRI = np.where((nrm < 0)[:, None], TRI[:, [0, 2, 1]], TRI)
# paredes para fora: anel horário/anti-horário pela área com sinal
ar = np.zeros(n); np.add.at(ar, dono, P2[:, 0] * P2[prox, 1] - P2[prox, 0] * P2[:, 1])
inv = (ar[dono] < 0)
PAR[:nv][inv] = PAR[:nv][inv][:, [0, 2, 1]]; PAR[nv:][inv] = PAR[nv:][inv][:, [0, 2, 1]]
# sem triângulos degenerados (vértices repetidos no contorno): eles dão NaN no render (pontos pretos)
lado = np.hypot(*(P2[prox] - P2).T) > 0.05
u_, v_ = P2[TRI[:, 1]] - P2[TRI[:, 0]], P2[TRI[:, 2]] - P2[TRI[:, 0]]
area = np.abs(u_[:, 0] * v_[:, 1] - u_[:, 1] * v_[:, 0]) > 0.01
FP = np.concatenate([PAR[np.concatenate([lado, lado])], TRI[area] + nv]).astype(np.uint32)
XY = M(POS[:, 0], POS[:, 1], 0).astype(np.float32)
ZB = (POS[:, 2] * EXZ).astype(np.float32)
hsh = ((np.arange(n, dtype=np.uint64) * 2654435761) % 2**32) / 4294967296   # mesma cor do motor
alto = np.minimum(1, ALT / 40)
cor = np.stack([226 + (238 - 226) * hsh + alto * 10, 122 + (150 - 122) * hsh + alto * 70, 58 + (82 - 58) * hsh + alto * 80], 1)
# cor por prédio via paleta (textura 1024x1, 32 tons x 32 alturas); mesh_attribute do Mitsuba gera NaN (pontos pretos)
NP = 32
idx = (np.minimum(NP - 1, (hsh * NP).astype(int)) * NP + np.minimum(NP - 1, (alto * NP).astype(int)))
hq, aq = (np.arange(NP * NP) // NP + 0.5) / NP, (np.arange(NP * NP) % NP + 0.5) / NP
pal_ = np.stack([226 + 12 * hq + aq * 10, 122 + 28 * hq + aq * 70, 58 + 24 * hq + aq * 80], 1)
PAL = mi.Bitmap(lin(np.clip(pal_, 0, 255) / 255).astype(np.float32).reshape(1, NP * NP, 3))
UVP = np.stack([(idx + 0.5) / (NP * NP), np.full(n, 0.5)], 1).astype(np.float32)[dono]
predios = mi.Mesh("predios", 2 * nv, len(FP), has_vertex_texcoords=True)
predios_uv = np.concatenate([UVP, UVP]).ravel()
pp = mi.traverse(predios); pp["faces"] = FP.ravel(); pp["vertex_texcoords"] = predios_uv


def alturas(ano, teto):
    s = np.clip((ano - ANO) / NASCER, 0, 1)                      # nasce subindo ao longo de "nascer" anos
    h = np.minimum(ALT, teto) * EXB * s
    vivo = (ANO <= ano)[dono]
    pos = np.empty((2 * nv, 3), np.float32)
    pos[:nv] = XY; pos[nv:] = XY
    pos[:nv, 1] = np.where(vivo, ZB - 3, -5000)                  # base um pouco enterrada; quem não nasceu fica no fundo
    pos[nv:, 1] = np.where(vivo, ZB + np.maximum(h[dono], 0.3), -5000)
    return pos


pp["vertex_positions"] = alturas(9999, 999).ravel(); pp.update()

# ---------- fundo além do recorte (o motor desenha chao-longe a z = -3) ----------
corLonge = np.array(C.get("corLonge", [150, 172, 168])) / 255
R = 200e3
longe = {"type": "rectangle", "to_world": mi.ScalarTransform4f().translate([0, -3.0, 0]).rotate([1, 0, 0], -90).scale(R),
         "bsdf": {"type": "diffuse", "reflectance": {"type": "rgb", "value": lin(corLonge).tolist()}}}

SOL = np.array([-2.0, -4.0, 3.0]); SOL /= np.linalg.norm(SOL)    # mesmo sol do motor: vem do nordeste, alto
terreno_bsdf = mi.load_dict({"type": "twosided", "bsdf": {"type": "diffuse", "reflectance": {"type": "bitmap", "filename": str(ASSETS / "textura.jpg"), "filter_type": "bilinear"}}})
predio_bsdf = mi.load_dict({"type": "twosided", "bsdf": {"type": "diffuse", "reflectance": {"type": "bitmap", "bitmap": PAL, "filter_type": "nearest", "raw": True}}})
terreno.set_bsdf(terreno_bsdf); predios.set_bsdf(predio_bsdf)
cena = mi.load_dict({
    "type": "scene",
    "integrator": {"type": "path", "max_depth": 4, "hide_emitters": True},
    "sol": {"type": "directional", "direction": SOL.tolist(), "irradiance": {"type": "rgb", "value": [3.3, 3.15, 2.95]}},
    "ceu": {"type": "constant", "radiance": {"type": "rgb", "value": [0.62, 0.70, 0.80]}},
    "terreno": terreno, "predios": predios, "longe": longe,
})
params = mi.traverse(cena)
KP = [k for k in params.keys() if k.endswith("vertex_positions") and "predios" in k][0]
print(f"montado em {time.time() - t0:.1f} s · {n} prédios · {len(FP)} triângulos de prédio · relevo {nx}x{ny}", file=sys.stderr)

# céu do motor (#ceu: gradiente vertical)
yy = np.linspace(0, 1, H)[:, None]
pal = [(0, (0x7f, 0xb0, 0xd6)), (.38, (0xb9, 0xd4, 0xe6)), (.60, (0xdf, 0xe8, 0xe2)), (1, (0xdf, 0xe8, 0xe2))]
CEU = np.zeros((H, 1, 3))
for ch in range(3):
    CEU[:, 0, ch] = np.interp(yy[:, 0], [q_[0] for q_ in pal], [q_[1][ch] for q_ in pal]) / 255
CEU = np.repeat(CEU, W, 1)
denoiser = mi.OptixDenoiser(input_size=[W, H], albedo=False, normals=False, temporal=False)
hexrgb = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255


k_dbg = "--debug" in args


def quadro(info):
    if info["globo"] >= 0.999 or info["fim"] >= 0.999:
        base = np.zeros((H, W, 3))
    else:
        o, c, u = M(*info["cam"]), M(*info["centro"]), M(*info["cima"])
        up = u - c; up /= np.linalg.norm(up)
        sensor = mi.load_dict({"type": "perspective", "fov": info["fovy"], "fov_axis": "y", "near_clip": 5.0, "far_clip": 2e6,
                               "to_world": mi.ScalarTransform4f().look_at(origin=o.tolist(), target=c.tolist(), up=up.tolist()),
                               "film": {"type": "hdrfilm", "width": W, "height": H, "pixel_format": "rgba", "rfilter": {"type": "gaussian"}},
                               "sampler": {"type": "independent", "sample_count": SPP}})
        params[KP] = alturas(info["ano"], info["teto"]).ravel(); params.update()
        img = mi.render(cena, sensor=sensor, spp=SPP, seed=0)
        nan = int(dr.count(dr.isnan(img.array))[0]) if hasattr(dr, "count") else 0
        if nan and k_dbg:
            print("NaN", nan, file=sys.stderr)
            al_ = np.asarray(img[:, :, 3]); m_ = np.isnan(np.asarray(img[:, :, 0]))
            print("  alfa nos NaN:", np.unique(np.round(al_[m_], 2))[:5], file=sys.stderr)
            pos0 = params[KP]; params[KP] = np.full(2 * nv * 3, -5000, np.float32); params.update()
            im2 = mi.render(cena, sensor=sensor, spp=SPP, seed=0); print("  sem prédios NaN:", int(dr.count(dr.isnan(im2.array))[0]), file=sys.stderr)
            params[KP] = pos0; params.update()
        rgb = denoiser(img[:, :, :3]) if SPP < 256 else img[:, :, :3]
        rgb = np.nan_to_num(np.asarray(rgb, dtype=np.float64), nan=0.0, posinf=0.0); al = np.clip(np.asarray(img[:, :, 3], dtype=np.float64), 0, 1)[..., None]
        base = CEU * (1 - al) + srgb(np.clip(rgb, 0, 64)) .clip(0, 1) * al
        if info.get("tom"):
            f = info["tom"]["forca"]; base = base * (1 - f + f * hexrgb(info["tom"]["cor"]))
    ov = np.asarray(Image.open(CAMADA / f"c_{info['i']:05d}.png").convert("RGBA"), dtype=np.float64) / 255
    out = ov[..., :3] * ov[..., 3:] + base * (1 - ov[..., 3:])
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


infos = [json.loads(l) for l in (CAMADA / "info.jsonl").read_text().splitlines() if l.strip()]
infos = list({x["i"]: x for x in infos}.values()); infos.sort(key=lambda x: x["i"])
video = SAIDA.suffix == ".mp4"
if video:
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium", str(SAIDA)], stdin=subprocess.PIPE)
else:
    SAIDA.mkdir(parents=True, exist_ok=True)
ti = time.time()
for k, info in enumerate(infos):
    q_ = quadro(info)
    if video: ff.stdin.write(q_.tobytes())
    else: Image.fromarray(q_).save(SAIDA / f"q_{info['i']:05d}.jpg", quality=92)
    if k % 30 == 0: print(f"quadro {k}/{len(infos)} {(time.time() - ti) / (k + 1):.2f} s/quadro", file=sys.stderr, flush=True)
if video:
    ff.stdin.close(); ff.wait()
print(f"ok {SAIDA} ({len(infos)} quadros, {time.time() - ti:.0f} s)", file=sys.stderr)
