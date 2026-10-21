"""Feições com nome para efeitos: pontes (bridge=yes + 'Ponte'), fortalezas (historic=fort/castle),
muros/diques e qualquer nome listado em config["feicoes_nomes"] → dados/brutos/feicoes.geojson"""
import json, sys
import osmium
from osmium.geom import GeoJSONFactory
from shapely.geometry import shape, box
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
geo = GeoJSONFactory(); CX = box(W, S, E, N)
NOMES = [n.lower() for n in CFG.get("feicoes_nomes", [])]
out = []
def tipo(t):
    nm = t.get("name", "").lower()
    if t.get("bridge") in ("yes", "suspension", "viaduct") and "ponte" in nm and t.get("highway"): return "ponte"
    if t.get("historic") in ("fort", "castle") or "fortaleza" in nm or "forte " in nm: return "forte"
    if t.get("barrier") in ("wall", "flood_wall") and "muro" in nm: return "muro"
    if t.get("man_made") in ("dyke",): return "dique"
    if any(n in nm for n in NOMES): return "nome"
    if "aterro" in nm: return "aterro"
    return None
class H(osmium.SimpleHandler):
    def way(self, w):
        k = tipo(w.tags)
        if not k or k == "forte": return
        try: g = shape(json.loads(geo.create_linestring(w)))
        except Exception: return
        if g.intersects(CX): out.append({"type": "Feature", "properties": {"tipo": k, "nome": w.tags.get("name", ""), "id": w.id}, "geometry": json.loads(json.dumps(g.__geo_interface__))})
    def area(self, a):
        k = tipo(a.tags)
        if not k: return
        try: g = shape(json.loads(geo.create_multipolygon(a)))
        except Exception: return
        if g.intersects(CX): out.append({"type": "Feature", "properties": {"tipo": k + "_area", "nome": a.tags.get("name", ""), "id": a.id}, "geometry": json.loads(json.dumps(g.__geo_interface__))})
H().apply_file(f"{RAIZ}/{CFG['pbf']}", locations=True)
json.dump({"type": "FeatureCollection", "features": out}, open(f"{BRUTOS}/feicoes.geojson", "w"))
import collections
for (k, n), c in sorted(collections.Counter((f["properties"]["tipo"], f["properties"]["nome"]) for f in out).items()): print(k, "|", n, "|", c)
