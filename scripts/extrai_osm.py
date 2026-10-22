"""Recorta do OSM (recorte regional do config "pbf") o que o timelapse da cidade precisa.
Níveis administrativos do config: "nivel_municipio" (padrão "8") e "nivel_bairro" (padrão "10", convenção do Brasil).

Saída em dados/brutos/: predios.json, agua.geojson, ruas.geojson, bairros.geojson, municipio.geojson
Uso: CIDADE=<id> .venv/bin/python -I scripts/extrai_osm.py [pbf] [saida]
"""
import json
import sys

import osmium
from osmium.geom import GeoJSONFactory
from shapely.geometry import box, mapping, shape

import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
BBOX = (W, S, E, N)
CAIXA = box(*BBOX)
geo = GeoJSONFactory()
NIV_MUNI, NIV_BAIRRO = str(CFG.get("nivel_municipio", "8")), str(CFG.get("nivel_bairro", "10"))
RUAS = {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link"}


def dentro(g):
    return g.intersects(CAIXA)


class Coleta(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.predios, self.agua, self.ruas, self.bairros, self.muni = [], [], [], [], []

    def way(self, w):
        t = w.tags
        hw = t.get("highway")
        if hw in RUAS:
            try:
                g = shape(json.loads(geo.create_linestring(w)))
            except Exception:
                return
            if dentro(g):
                self.ruas.append({"type": "Feature", "properties": {"hw": hw, "nome": t.get("name", "")},
                                  "geometry": mapping(g)})
        if t.get("waterway") in ("river", "stream", "canal") and t.get("name"):
            try:
                g = shape(json.loads(geo.create_linestring(w)))
            except Exception:
                return
            if dentro(g):
                self.agua.append({"type": "Feature", "properties": {"tipo": "linha", "nome": t.get("name", "")},
                                  "geometry": mapping(g)})

    def area(self, a):
        t = a.tags
        is_b = "building" in t
        is_w = t.get("natural") == "water" or t.get("water") is not None or t.get("waterway") == "riverbank" \
            or t.get("landuse") in ("reservoir", "basin")
        adm = t.get("boundary") == "administrative" and t.get("admin_level") in (NIV_MUNI, NIV_BAIRRO)
        if not (is_b or is_w or adm):
            return
        try:
            g = shape(json.loads(geo.create_multipolygon(a)))
        except Exception:
            return
        if not dentro(g):
            return
        if is_b:
            c = g.centroid
            lv = t.get("building:levels")
            try:
                lv = float(lv) if lv else None
            except ValueError:
                lv = None
            h = t.get("height")
            try:
                h = float(str(h).split()[0]) if h else None
            except ValueError:
                h = None
            self.predios.append({"lon": round(c.x, 6), "lat": round(c.y, 6), "area": round(g.area * 1e10, 1),
                                 "lv": lv, "h": h, "tipo": t.get("building"),
                                 "data": t.get("start_date"), "nome": t.get("name"),
                                 "poly": [[round(x, 6), round(y, 6)] for x, y in
                                          (g.geoms[0] if g.geom_type == "MultiPolygon" else g).exterior.coords]})
        elif is_w:
            g = g.intersection(CAIXA)
            if g.area > 1e-7:
                self.agua.append({"type": "Feature", "properties": {"tipo": "area", "nome": t.get("name", "")},
                                  "geometry": mapping(g.simplify(0.00005))})
        elif adm:
            f = {"type": "Feature", "properties": {"nome": t.get("name", ""), "nivel": t.get("admin_level")},
                 "geometry": mapping(g.simplify(0.00005))}
            if t.get("admin_level") == NIV_BAIRRO:
                self.bairros.append(f)
            elif t.get("name") == CFG["municipio_osm"] and t.get("admin_level") == NIV_MUNI:
                self.muni.append(f)


def grava(path, feats):
    json.dump({"type": "FeatureCollection", "features": feats}, open(path, "w"))


if __name__ == "__main__":
    pbf = sys.argv[1] if len(sys.argv) > 1 else f"{RAIZ}/{CFG['pbf']}"
    out = sys.argv[2] if len(sys.argv) > 2 else BRUTOS
    h = Coleta()
    h.apply_file(pbf, locations=True)
    json.dump(h.predios, open(f"{out}/predios.json", "w"))
    grava(f"{out}/agua.geojson", h.agua)
    grava(f"{out}/ruas.geojson", h.ruas)
    grava(f"{out}/bairros.geojson", h.bairros)
    grava(f"{out}/municipio.geojson", h.muni)
    datas = sum(1 for p in h.predios if p["data"])
    print(f"predios={len(h.predios)} com_data={datas} agua={len(h.agua)} ruas={len(h.ruas)} "
          f"bairros={len(h.bairros)} municipio={len(h.muni)}")
