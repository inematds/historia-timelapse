"""Versão centro: TODAS as ruas (highway=*) e praças/parques/igrejas do recorte → dados/brutos/ruas_todas.geojson, areas.geojson
Uso: CIDADE=itaguai-centro .venv/bin/python -I centro/scripts/extrai_ruas.py"""
import json, os, sys
import osmium
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa
ruas, areas = [], []
fp = osmium.FileProcessor(f"{RAIZ}/{CFG['pbf']}").with_filter(osmium.filter.KeyFilter("highway", "leisure", "landuse", "amenity", "natural", "waterway", "place", "railway")).with_locations()
for o in fp:
    if not o.is_way():
        continue
    try:
        pts = [(n.lon, n.lat) for n in o.nodes]
    except Exception:
        continue
    if not pts or not any(W < x < E and S < y < N for x, y in pts):
        continue
    t = dict(o.tags)
    if "highway" in t and pts[0] != pts[-1] or ("highway" in t and t.get("area") != "yes"):
        ruas.append({"type": "Feature", "properties": {"hw": t["highway"], "nome": t.get("name", "")}, "geometry": {"type": "LineString", "coordinates": pts}})
    elif pts[0] == pts[-1] and len(pts) > 3:
        k = t.get("leisure") or t.get("landuse") or t.get("amenity") or t.get("natural") or t.get("place") or t.get("highway")
        areas.append({"type": "Feature", "properties": {"tipo": k, "nome": t.get("name", "")}, "geometry": {"type": "Polygon", "coordinates": [pts]}})
json.dump({"type": "FeatureCollection", "features": ruas}, open(f"{BRUTOS}/ruas_todas.geojson", "w"))
json.dump({"type": "FeatureCollection", "features": areas}, open(f"{BRUTOS}/areas.geojson", "w"), ensure_ascii=False)
import collections
print("ruas", len(ruas), collections.Counter(r["properties"]["hw"] for r in ruas).most_common(8))
print("areas", len(areas), collections.Counter(a["properties"]["tipo"] for a in areas).most_common(12))
print([a["properties"]["nome"] for a in areas if a["properties"]["nome"]][:40])
