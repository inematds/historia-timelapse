"""Prédios do OSM → binários para o deck.gl (SolidPolygonLayer em modo binário).

Saída em motor/assets/:
  pred_pos.f32   vértices [lon, lat, z_chão] (anel externo, sem repetir o 1º ponto)
  pred_ini.u32   índice inicial de cada prédio (n+1 valores)
  pred_alt.f32   altura real em metros (OSM height / levels*3 / padrão pelo tipo)
dados/predios_meta.npz  lon, lat, area, alt, municipio(bool POA), bairro(idx) para o modelo de anos
Uso: .venv/bin/python -I scripts/prep_predios.py
"""
import json
import os

import numpy as np
from shapely import STRtree, points
from shapely.geometry import shape

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, S, E, N = -51.36, -30.30, -50.95, -29.90
chao = np.load(f"{raiz}/dados/chao.npy")
H, Wd = chao.shape
PADRAO = {"house": 6, "residential": 7, "detached": 6, "garage": 3, "shed": 3, "roof": 4, "industrial": 9,
          "warehouse": 9, "commercial": 10, "retail": 7, "apartments": 15, "church": 16, "school": 8,
          "hospital": 18, "university": 14, "office": 20, "hotel": 20, "cathedral": 40}


def z_chao(lon, lat):
    c = np.clip(((lon - W) / (E - W) * Wd).astype(int), 0, Wd - 1)
    r = np.clip(((N - lat) / (N - S) * H).astype(int), 0, H - 1)
    return chao[r, c]


def main():
    pred = json.load(open(f"{raiz}/dados/brutos/predios.json"))
    pred = [p for p in pred if p["area"] >= 12 and len(p["poly"]) >= 4]
    lon = np.array([p["lon"] for p in pred]); lat = np.array([p["lat"] for p in pred])
    alt = []
    for p in pred:
        if p["h"]:
            a = p["h"]
        elif p["lv"]:
            a = p["lv"] * 3.0 + 1
        else:
            a = PADRAO.get(p["tipo"], 6.0)
        alt.append(min(max(a, 3.0), 180.0))
    alt = np.array(alt, np.float32)
    zc = z_chao(lon, lat)

    pos, ini = [], [0]
    for p, z in zip(pred, zc):
        anel = p["poly"][:-1]
        if len(anel) > 24:  # simplifica anéis muito detalhados
            anel = anel[:: int(np.ceil(len(anel) / 24))]
        for x, y in anel:
            pos += [x, y, float(z)]
        ini.append(ini[-1] + len(anel))
    np.array(pos, np.float32).tofile(f"{raiz}/motor/assets/pred_pos.f32")
    np.array(ini, np.uint32).tofile(f"{raiz}/motor/assets/pred_ini.u32")
    alt.tofile(f"{raiz}/motor/assets/pred_alt.f32")

    muni = shape(json.load(open(f"{raiz}/dados/brutos/municipio.geojson"))["features"][0]["geometry"])
    pts = points(lon, lat)
    em_poa = np.array([muni.contains(pt) for pt in pts])
    bfeat = json.load(open(f"{raiz}/dados/brutos/bairros.geojson"))["features"]
    bgeo = [shape(f["geometry"]) for f in bfeat]
    nomes = [f["properties"]["nome"] for f in bfeat]
    arv = STRtree(bgeo)
    bidx = np.full(len(pred), -1, np.int32)
    ip, ig = arv.query(pts, predicate="within")
    bidx[ip] = ig
    np.savez(f"{raiz}/dados/predios_meta.npz", lon=lon, lat=lat, alt=alt, area=np.array([p["area"] for p in pred]),
             poa=em_poa, bairro=bidx, nomes=np.array(nomes, dtype=object),
             tipo=np.array([p["tipo"] or "" for p in pred], dtype=object))
    print(f"predios={len(pred)} vertices={len(pos)//3} em_poa={em_poa.sum()} com_bairro={(bidx>=0).sum()} "
          f"alt_media={alt.mean():.1f} m · MB={len(pos)*4/1e6:.0f}")


if __name__ == "__main__":
    main()
