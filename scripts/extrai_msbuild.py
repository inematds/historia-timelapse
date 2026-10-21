"""Junta prédios da Microsoft Global ML Building Footprints (arquivos .csv.gz em dl/msbuild/) aos do OSM.
OSM tem prioridade; prédio MS cujo centro cai a < 6 m de um prédio OSM é descartado.
Uso: CIDADE=floripa .venv/bin/python -I scripts/extrai_msbuild.py"""
import gzip, json, glob
import numpy as np
from shapely.geometry import shape
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
osm = json.load(open(f"{BRUTOS}/predios.json"))
grade = {(round(p["lon"] / 6e-5), round(p["lat"] / 6e-5)) for p in osm}
novos = 0
for f in sorted(glob.glob(f"{RAIZ}/dl/msbuild/*.csv.gz")):
    for linha in gzip.open(f, "rt"):
        ft = json.loads(linha)
        g = ft["geometry"]
        if g["type"] != "Polygon":
            continue
        anel = g["coordinates"][0]
        xs = [c[0] for c in anel]; ys = [c[1] for c in anel]
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        if not (W <= cx <= E and S <= cy <= N):
            continue
        if (round(cx / 6e-5), round(cy / 6e-5)) in grade:
            continue
        pol = shape(g)
        h = ft.get("properties", {}).get("height", -1)
        osm.append({"lon": round(cx, 6), "lat": round(cy, 6), "area": round(pol.area * 1e10, 1), "lv": None,
                    "h": float(h) if h and h > 0 else None, "tipo": "ms", "data": None, "nome": None,
                    "poly": [[round(x, 6), round(y, 6)] for x, y in anel]})
        novos += 1
json.dump(osm, open(f"{BRUTOS}/predios.json", "w"))
print(f"MS novos={novos} total={len(osm)}")
