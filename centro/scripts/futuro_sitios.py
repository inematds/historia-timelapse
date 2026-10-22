"""Versão centro: escolhe onde fica a CIDADE FUTURA (visão, não é projeto) em lugares reais do recorte.
- VLT sobre a antiga linha do trem (efeitos.json, linha "trem") perto da estação-castelo
- parque linear no Canal do Viana (agua.geojson)
- ciclovia na rua principal mais próxima da Matriz
- torres de vidro moderadas e prédios de telhado verde sobre prédios grandes atuais (que somem em ANO_SOME)
- árvores nas calçadas das ruas principais
Saída: cidades/<id>/futuro_auto.json e assets/pred_fim.f32 (ano em que cada prédio comum some; 9e4 = nunca).
Roda depois de limpa_marcos.py. Uso: CIDADE=itaguai-centro .venv/bin/python -I centro/scripts/futuro_sitios.py"""
import json, math, os, sys
import numpy as np
from shapely.geometry import LineString, Point, shape
from shapely.ops import linemerge, unary_union
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa

ANO_SOME = 2026.0
MZ = tuple(CFG["centro_antigo"])
KL = 111320 * math.cos(math.radians(MZ[1]))
chao = np.load(f"{DADOS}/chao.npy"); H, Wd = chao.shape


def z(lon, lat):
    c = int(np.clip((lon - W) / (E - W) * Wd, 0, Wd - 1)); r = int(np.clip((N - lat) / (N - S) * H, 0, H - 1))
    return round(float(chao[r, c]), 2)


def m2ll(x, y):   # metros a partir da Matriz → lon, lat
    return (MZ[0] + x / KL, MZ[1] + y / 111320)


def ll2m(lon, lat):
    return ((lon - MZ[0]) * KL, (lat - MZ[1]) * 111320)


def dist(lon, lat):
    x, y = ll2m(lon, lat); return math.hypot(x, y)


def em_m(geom):   # shapely em metros
    from shapely.ops import transform
    return transform(lambda x, y, z=None: ll2m(x, y), geom)


def em_ll(geom):
    from shapely.ops import transform
    return transform(lambda x, y, z=None: m2ll(x, y), geom)


rot = json.load(open(f"{DIR}/roteiro.json"))
marcos = [ll2m(m["lon"], m["lat"]) for m in rot.get("marcos", [])]
meta = np.load(f"{DADOS}/predios_meta.npz", allow_pickle=True)
lon, lat, area = meta["lon"], meta["lat"], meta["area"]
xs, ys = ll2m(lon, lat)
d0 = np.hypot(xs, ys)
fim = np.full(len(lon), 9e4, np.float32)
elem, arv = [], []

# 1. VLT: linha do trem a até 900 m da Matriz
ef = json.load(open(f"{ASSETS}/efeitos.json"))
trem = unary_union([em_m(LineString([p[:2] for p in l])) for l in ef["linhas"]["trem"]])
trem = linemerge(trem) if trem.geom_type == "MultiLineString" else trem
perto = trem.intersection(Point(0, 0).buffer(900))
partes = list(perto.geoms) if hasattr(perto, "geoms") else [perto]
vlt = max(partes, key=lambda g: g.length)
est = Point(*ll2m(-43.777518, -22.874347))          # estação-castelo: o bonde passa por ela logo no começo
from shapely.ops import substring
pe = vlt.project(est); vlt = substring(vlt, max(0, pe - 110), min(vlt.length, pe + 650))
cam = [list(m2ll(*c)) for c in vlt.coords]
zv = round(float(np.median([z(*c) for c in cam])), 2)
elem.append({"id": "vlt", "tipo": "vlt", "caminho": cam, "vel": 6, "comp": 24, "z": zv})
corredor_vlt = vlt.buffer(9)

# 2. parque linear no Canal do Viana (trechos a até 900 m)
ag = [em_m(shape(f["geometry"])) for f in json.load(open(f"{BRUTOS}/agua.geojson"))["features"] if "Viana" in f["properties"].get("nome", "")]
canal = linemerge(unary_union(ag))
canal = canal.intersection(Point(0, 0).buffer(900))
pc = list(canal.geoms) if hasattr(canal, "geoms") else [canal]
rio = max(pc, key=lambda g: g.length).simplify(3)
parque = rio.buffer(28, cap_style=2).simplify(2)
cam_p = rio.parallel_offset(13, "left").simplify(3)
cam_p = max(cam_p.geoms, key=lambda g: g.length) if hasattr(cam_p, "geoms") else cam_p
zp = round(float(np.median([z(*m2ll(*c)) for c in rio.coords])), 2)
elem.append({"id": "parque", "tipo": "parque", "poligono": [list(m2ll(*c)) for c in parque.exterior.coords],
             "agua": [list(m2ll(*c)) for c in rio.coords], "agua_larg": 7, "caminho": [list(m2ll(*c)) for c in cam_p.coords],
             "arvores": int(parque.area / 260), "semente": 4, "z": zp})
fim[[parque.contains(Point(x, y)) for x, y in zip(xs, ys)]] = ANO_SOME

# 3. ruas principais (ciclovia + árvores de calçada)
ruas = [f for f in json.load(open(f"{BRUTOS}/ruas_todas.geojson"))["features"] if f["properties"]["hw"] in ("primary", "secondary", "tertiary", "residential")]
linhas = [em_m(LineString(f["geometry"]["coordinates"])) for f in ruas]
linhas = [l.intersection(Point(0, 0).buffer(650)) for l in linhas]
linhas = [g for l in linhas for g in (l.geoms if hasattr(l, "geoms") else [l]) if not l.is_empty and g.length > 30]
if linhas:
    cic = max(linhas, key=lambda g: g.length - 0.5 * g.distance(Point(0, 0)))
    off = cic.parallel_offset(5.5, "right")
    off = max(off.geoms, key=lambda g: g.length) if hasattr(off, "geoms") else off
    elem.append({"id": "ciclovia", "tipo": "ciclovia", "caminho": [list(m2ll(*c)) for c in off.coords], "z": round(z(*m2ll(*cic.centroid.coords[0])), 2)})
rng = np.random.default_rng(5)
usadas = []
for l in linhas:
    for lado in (6.5, -6.5):
        o = l.parallel_offset(abs(lado), "left" if lado > 0 else "right")
        for g in (o.geoms if hasattr(o, "geoms") else [o]):
            n = int(g.length // 12)
            for i in range(n):
                p = g.interpolate((i + 0.5) * 12)
                if corredor_vlt.contains(p) or any(math.hypot(p.x - a, p.y - b) < 8 for a, b in usadas[-40:]):
                    continue
                usadas.append((p.x, p.y)); lo, la = m2ll(p.x, p.y)
                arv.append({"lon": round(lo, 7), "lat": round(la, 7), "z": z(lo, la), "esc": round(float(rng.uniform(.8, 1.15)), 2),
                            "giro": int(rng.integers(0, 360)), "tipo": "palmeira" if rng.random() < .2 else "redonda",
                            "ano": round(float(2026 + rng.uniform(0, 14)), 2), "dura": 3})

# 4. torres de vidro (3) e telhado verde (5): prédios grandes, 180–650 m da Matriz, longe dos marcos, do parque e do VLT
cand = np.where((area > 220) & (area < 1600) & (d0 > 180) & (d0 < 650))[0]
cand = cand[np.argsort(-area[cand])]
esc = []
for i in cand:
    p = Point(xs[i], ys[i])
    if any(math.hypot(xs[i] - a, ys[i] - b) < 70 for a, b in marcos) or parque.buffer(15).contains(p) or corredor_vlt.buffer(10).contains(p):
        continue
    if any(math.hypot(xs[i] - xs[j], ys[i] - ys[j]) < 80 for j in esc):
        continue
    esc.append(i)
    if len(esc) == 14:
        break
for k, i in enumerate(esc):
    lo, la = float(lon[i]), float(lat[i]); lado = float(np.clip(math.sqrt(area[i]), 14, 24))
    tipo = "torre_vidro" if k < 4 else "telhado_verde"
    e = {"id": f"f{k}", "tipo": tipo, "lon": lo, "lat": la, "z": z(lo, la), "rumo": int(rng.integers(0, 4)) * 90 + 10,
         "larg": round(lado, 1), "comp": round(lado * (1 if tipo == "torre_vidro" else .7), 1), "andares": [10, 8, 9, 7][k] if tipo == "torre_vidro" else int(rng.integers(4, 6))}
    elem.append(e)
    fim[np.hypot(xs - xs[i], ys - ys[i]) < lado * 0.85] = ANO_SOME
fim.tofile(f"{ASSETS}/pred_fim.f32")
# ordem de nascimento: parque e ciclovia, VLT, telhados verdes, torres por último
ordem = {"parque": 0, "ciclovia": 1, "vlt": 2, "telhado_verde": 3, "torre_vidro": 4}
elem.sort(key=lambda e: ordem.get(e["tipo"], 9))
json.dump({"elementos": elem, "arvores": arv, "_nota": "visão imaginada (não é projeto); gerado por centro/scripts/futuro_sitios.py"},
          open(f"{DIR}/futuro_auto.json", "w"), ensure_ascii=False)
print(f"futuro: {len(elem)} elementos ({[e['tipo'] for e in elem]}), {len(arv)} árvores, somem {int((fim < 9e4).sum())} prédios, vlt {vlt.length:.0f} m, parque {parque.area:.0f} m²")
