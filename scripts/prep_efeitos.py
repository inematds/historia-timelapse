"""Efeitos geográficos da cidade → assets/efeitos.json

config["efeitos"]:
  linhas: {id: {nome_osm}}                      pontes/ferrovias (linhas do OSM com esse nome, em feicoes.geojson)
  fortes: {id: {nome_osm} | {ponto:[lon,lat], lado_m}}   polígonos para extrudar
  areas:  {id: {faixa: {bbox:[w,s,e,n], dist_m, zmax}, faixas: n}}   aterro = terra baixa junto ao mar atual,
          fatiada da margem antiga (longe do mar) até a costa atual
Legado POA: config["feicoes"] = {muro: {nome_osm}, aterro: {bairros_osm: [...]}}
"""
import json
import math

import numpy as np
from scipy import ndimage
from shapely.geometry import box, shape, Polygon
from shapely.ops import unary_union, linemerge
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa

ch = np.load(f"{DADOS}/chao.npy"); H, Wd = ch.shape
PXX, PXY = (E - W) / Wd, (N - S) / H


def z(lon, lat):
    c = min(max(int((lon - W) / (E - W) * Wd), 0), Wd - 1); r = min(max(int((N - lat) / (N - S) * H), 0), H - 1)
    return float(max(ch[r, c], 0.0))


def anel3d(pol):
    return [[x, y, z(x, y)] for x, y in pol.exterior.coords]


def poligonos(g):
    return list(g.geoms) if g.geom_type in ("MultiPolygon", "GeometryCollection") else [g]


out = {}
EF = CFG.get("efeitos", {})
fe = json.load(open(f"{BRUTOS}/feicoes.geojson"))["features"] if (EF.get("linhas") or EF.get("fortes")) else []

if EF.get("linhas"):
    out["linhas"] = {}
    for lid, spec in EF["linhas"].items():
        geoms = [shape(f["geometry"]) for f in fe if f["properties"]["nome"] == spec["nome_osm"] and f["properties"]["tipo"] == "ponte"]
        u = unary_union(geoms) if geoms else None
        m = (linemerge(u) if u is not None and u.geom_type == "MultiLineString" else u)
        linhas = list(m.geoms) if m is not None and m.geom_type == "MultiLineString" else ([m] if m is not None else [])
        out["linhas"][lid] = [[[x, y, z(x, y)] for x, y in l.coords] for l in linhas]
        print("linha", lid, len(linhas), "trechos", sum(len(l.coords) for l in linhas), "pontos")

if EF.get("fortes"):
    out["fortes"] = {}
    for fid, spec in EF["fortes"].items():
        if "ponto" in spec:
            x, y = spec["ponto"]; d = spec.get("lado_m", 60) / 2
            g = box(x - d / 96000 / math.cos(math.radians(-y)) * 0.9, y - d / 111000, x + d / 96000 * 0.9, y + d / 111000)
        else:
            gs = [shape(f["geometry"]) for f in fe if f["properties"]["nome"] == spec["nome_osm"] and f["properties"]["tipo"].endswith("_area")]
            g = unary_union(gs) if gs else None
        out["fortes"][fid] = [anel3d(p) for p in poligonos(g) if p.geom_type == "Polygon"] if g is not None else []
        print("forte", fid, len(out["fortes"][fid]))

if EF.get("areas"):
    out["areas"] = {}
    mar = ch < -0.5
    dist = ndimage.distance_transform_edt(~mar) * 30.0   # metros até o mar atual
    for aid, spec in EF["areas"].items():
        fx = spec["faixa"]; w_, s_, e_, n_ = fx["bbox"]
        c0, c1 = int((w_ - W) / PXX), int((e_ - W) / PXX); r0, r1 = int((N - n_) / PXY), int((N - s_) / PXY)
        sel = np.zeros_like(mar); sel[r0:r1, c0:c1] = True
        terra = sel & ~mar & (dist <= fx["dist_m"]) & (ch <= fx.get("zmax", 4.0))
        nf = spec.get("faixas", 6)
        faixas = []
        for k in range(nf):   # k=0: mais longe do mar (margem antiga) → nasce primeiro
            hi = fx["dist_m"] * (1 - k / nf); lo = fx["dist_m"] * (1 - (k + 1) / nf)
            msk = terra & (dist <= hi) & (dist > lo)
            rr, cc = np.nonzero(msk)
            px = [box(W + c * PXX, N - (r + 1) * PXY, W + (c + 1) * PXX, N - r * PXY) for r, c in zip(rr, cc)]
            if not px:
                continue
            g = unary_union(px).buffer(PXX * 0.6).buffer(-PXX * 0.6).simplify(PXX * 0.4)
            faixas += [[[x, y] for x, y in p.exterior.coords] for p in poligonos(g) if p.geom_type == "Polygon" and p.area > PXX * PXY]
        out["areas"][aid] = faixas
        area_ha = terra.sum() * 30 * 30 / 1e4
        print("area", aid, "faixas", len(faixas), f"{area_ha:.0f} ha")

# legado POA (muro + aterro por bairro)
FE = CFG.get("feicoes", {})
if FE.get("muro"):
    out["muro"] = []
    for f in json.load(open(f"{BRUTOS}/muro.geojson"))["features"]:
        if f["properties"]["nome"] != FE["muro"]["nome_osm"]:
            continue
        g = shape(f["geometry"]).buffer(0.00009, cap_style=2)
        out["muro"].append(anel3d(g))
if FE.get("aterro"):
    bairros = json.load(open(f"{BRUTOS}/bairros.geojson"))["features"]
    ater = unary_union([shape(f["geometry"]) for f in bairros if f["properties"]["nome"] in FE["aterro"]["bairros_osm"]])
    out["aterro"] = [[[x, y] for x, y in p.exterior.coords] for p in poligonos(ater)]
    out["aterro_z"] = max(z(x, y) for p in poligonos(ater) for x, y in p.exterior.coords)
json.dump(out, open(f"{ASSETS}/efeitos.json", "w"))
print("ok", list(out))
