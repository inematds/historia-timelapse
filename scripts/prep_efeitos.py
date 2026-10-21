"""Muro da Mauá (paredes) e área do aterro da Praia de Belas → motor/assets/efeitos.json"""
import json, os
import numpy as np
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, S, E, N = -51.36, -30.30, -50.95, -29.90
ch = np.load(f"{raiz}/dados/chao.npy"); H, Wd = ch.shape
def z(lon, lat):
    c = min(max(int((lon - W) / (E - W) * Wd), 0), Wd - 1); r = min(max(int((N - lat) / (N - S) * H), 0), H - 1)
    return float(ch[r, c])
muro = []
for f in json.load(open(f"{raiz}/dados/brutos/muro.geojson"))["features"]:
    if f["properties"]["nome"] != "Muro da Mauá": continue
    g = shape(f["geometry"]).buffer(0.00009, cap_style=2)  # ~5 m de espessura
    muro.append([[x, y, z(x, y)] for x, y in g.exterior.coords])
bairros = json.load(open(f"{raiz}/dados/brutos/bairros.geojson"))["features"]
pb = [shape(f["geometry"]) for f in bairros if f["properties"]["nome"] == "Praia de Belas"]
ater = unary_union(pb)
pts = [p for p in (ater.geoms if ater.geom_type == "MultiPolygon" else [ater])]
zt = max(z(x, y) for p in pts for x, y in p.exterior.coords)
aterro = [[[x, y] for x, y in p.exterior.coords] for p in pts]
json.dump({"muro": muro, "aterro": aterro, "aterro_z": zt}, open(f"{raiz}/motor/assets/efeitos.json", "w"))
print("muro trechos", len(muro), "aterro polígonos", len(aterro), "z topo aterro", round(zt, 1), "área km2", round(ater.area * 111 * 96.3, 2))
