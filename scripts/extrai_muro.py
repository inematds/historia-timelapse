"""Traçado do Muro da Mauá e diques (barrier=wall/flood_wall, man_made=dyke) em POA → dados/brutos/muro.geojson"""
import json, sys
import osmium
from osmium.geom import GeoJSONFactory
geo = GeoJSONFactory()
B = (-51.32, -30.12, -51.10, -29.95)
out = []
class H(osmium.SimpleHandler):
    def way(self, w):
        t = w.tags; nm = t.get("name", "")
        alvo = ("muro" in nm.lower()) or t.get("barrier") == "wall" and "mau" in nm.lower() or t.get("barrier") == "flood_wall" or t.get("man_made") in ("dyke", "flood_wall")
        if not alvo: return
        try: g = json.loads(geo.create_linestring(w))
        except Exception: return
        xs = [p[0] for p in g["coordinates"]]; ys = [p[1] for p in g["coordinates"]]
        if max(xs) < B[0] or min(xs) > B[2] or max(ys) < B[1] or min(ys) > B[3]: return
        out.append({"type": "Feature", "properties": {"nome": nm, "barrier": t.get("barrier"), "man_made": t.get("man_made"), "id": w.id}, "geometry": g})
H().apply_file(sys.argv[1], locations=True)
json.dump({"type": "FeatureCollection", "features": out}, open(sys.argv[2], "w"))
for f in out: print(f["properties"], len(f["geometry"]["coordinates"]))
