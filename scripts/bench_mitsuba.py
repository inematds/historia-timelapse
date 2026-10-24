"""Mede o Mitsuba 3 na GPU com os dados reais de uma cidade (prédios + relevo).

Uso: <venv-mitsuba>/bin/python -I scripts/bench_mitsuba.py <cidade> [spp] [saida.png]
Prédios viram caixas (lado = raiz da área, altura = alt) apoiadas no relevo; relevo = malha do chao.npy.
Câmera oblíqua sobre o recorte inteiro (pior caso: tudo na tela). 1920x1080.
"""
import json, sys, time
import numpy as np
import mitsuba as mi
import drjit as dr

cid = sys.argv[1]
spp = int(sys.argv[2]) if len(sys.argv) > 2 else 64
out = sys.argv[3] if len(sys.argv) > 3 else f"/tmp/claude-1000/bench-{cid}.png"
base = f"cidades/{cid}"
mi.set_variant("cuda_ad_rgb")

cfg = json.load(open(f"{base}/config.json"))
x0, y0, x1, y1 = cfg["bbox"]
lat0 = (y0 + y1) / 2
mx = 111320 * np.cos(np.radians(lat0)); my = 110540
W, H = (x1 - x0) * mx, (y1 - y0) * my

t0 = time.time()
chao = np.load(f"{base}/dados/chao.npy").astype(np.float32)
ny, nx = chao.shape
gx, gy = np.meshgrid(np.linspace(0, W, nx), np.linspace(H, 0, ny))  # linha 0 = norte
V = np.stack([gx.ravel(), chao.ravel(), -gy.ravel()], 1).astype(np.float32)
i = np.arange(ny * nx).reshape(ny, nx)
a, b, c, d = i[:-1, :-1].ravel(), i[:-1, 1:].ravel(), i[1:, :-1].ravel(), i[1:, 1:].ravel()
F = np.concatenate([np.stack([a, c, b], 1), np.stack([b, c, d], 1)]).astype(np.uint32)
terreno = mi.Mesh("terreno", len(V), len(F))
p = mi.traverse(terreno); p["vertex_positions"] = V.ravel(); p["faces"] = F.ravel(); p.update()

m = np.load(f"{base}/dados/predios_meta.npz", allow_pickle=True)
px = ((m["lon"] - x0) * mx).astype(np.float32); pz = ((m["lat"] - y0) * my).astype(np.float32)
ok = (px > 0) & (px < W) & (pz > 0) & (pz < H)
px, pz = px[ok], pz[ok]
s = (np.sqrt(np.maximum(m["area"][ok], 20)) / 2).astype(np.float32)
alt = np.maximum(m["alt"][ok], 3).astype(np.float32)
ix = np.clip((px / W * (nx - 1)).astype(int), 0, nx - 1); iy = np.clip(((H - pz) / H * (ny - 1)).astype(int), 0, ny - 1)
z0 = chao[iy, ix]
n = len(px)
cx = np.array([-1, 1, 1, -1, -1, 1, 1, -1], np.float32); cz = np.array([-1, -1, 1, 1, -1, -1, 1, 1], np.float32)
cy = np.array([0, 0, 0, 0, 1, 1, 1, 1], np.float32)
BV = np.stack([px[:, None] + s[:, None] * cx, z0[:, None] + alt[:, None] * cy, -(pz[:, None] + s[:, None] * cz)], 2).reshape(-1, 3)
caixa = np.array([[4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5], [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7]], np.uint32)
BF = (caixa[None] + (np.arange(n, dtype=np.uint32) * 8)[:, None, None]).reshape(-1, 3)
predios = mi.Mesh("predios", len(BV), len(BF))
p = mi.traverse(predios); p["vertex_positions"] = BV.astype(np.float32).ravel(); p["faces"] = BF.ravel(); p.update()
t_monta = time.time() - t0

alvo = [W / 2, 0, -H / 2]
dist = max(W, H) * 0.9
cena = mi.load_dict({
    "type": "scene",
    "integrator": {"type": "path", "max_depth": 4},
    "sensor": {"type": "perspective", "fov": 45, "near_clip": 10.0, "far_clip": 1e6,
               "to_world": mi.ScalarTransform4f().look_at(origin=[W / 2, dist * 0.6, -H / 2 + dist * 0.8], target=alvo, up=[0, 1, 0]),
               "film": {"type": "hdrfilm", "width": 1920, "height": 1080}},
    "sol": {"type": "directional", "direction": [-0.4, -1, 0.5], "irradiance": 3.0},
    "ceu": {"type": "constant", "radiance": 0.6},
    "terreno": terreno, "predios": predios,
})
mi.render(cena, spp=4); dr.sync_thread()  # aquece (compila kernel)
# timelapse: a cada quadro os prédios mudam de altura -> atualizar vértices e refazer a aceleração
pc = mi.traverse(cena); k = [x for x in pc.keys() if x.endswith("vertex_positions") and "predios" in x][0]
BV2 = BV.copy(); BV2[:, 1] *= 0.999
t = time.time(); pc[k] = BV2.astype(np.float32).ravel(); pc.update(); dr.sync_thread(); t_atualiza = time.time() - t
t = time.time(); img = mi.render(cena, spp=spp); dr.eval(img); dr.sync_thread(); t_render = time.time() - t
mi.util.write_bitmap(out, img)
print(json.dumps({"cidade": cid, "predios": int(n), "tri_predios": int(len(BF)), "tri_relevo": int(len(F)),
                  "spp": spp, "montar_s": round(t_monta, 1), "atualiza_s": round(t_atualiza, 2), "quadro_s": round(t_render, 2), "png": out}))
