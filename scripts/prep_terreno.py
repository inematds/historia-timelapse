"""Relevo + textura do terreno para o motor deck.gl.

Entrada: dl/dem_*.tif (Copernicus GLO-30, 1"), dados/brutos/agua.geojson
Saída em motor/assets/: elev.png (Terrarium), textura.jpg, terreno.json (bbox, tamanhos)
         dados/chao.npy (altitude do chão em metros, grade do elev.png, para apoiar os prédios)
Uso: .venv/bin/python -I scripts/prep_terreno.py
"""
import json
import os

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from shapely.geometry import shape

PX = 1 / 3600  # 1 segundo de arco
TEX = 3  # textura 3x a grade do relevo
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa


def bloco(lat_ll, lon_ll):
    return f"{RAIZ}/dl/dem_S{-lat_ll:02d}_W{-lon_ll:03d}.tif"


def mosaico():
    import math
    lats = range(math.floor(S), math.floor(N) + 1)        # canto inferior de cada bloco de 1°
    lons = range(math.floor(W), math.floor(E) + 1)
    top_lat, left_lon = max(lats) + 1, min(lons)
    big = np.zeros((3600 * len(lats), 3600 * len(lons)), np.float32)
    for i, la in enumerate(sorted(lats, reverse=True)):
        for j, lo in enumerate(lons):
            big[i * 3600:(i + 1) * 3600, j * 3600:(j + 1) * 3600] = tifffile.imread(bloco(la, lo))
    c0 = int(round((W - left_lon) / PX)); c1 = int(round((E - left_lon) / PX))
    r0 = int(round((top_lat - N) / PX)); r1 = int(round((top_lat - S) / PX))
    return big[r0:r1, c0:c1]


def mascara_agua(h, w, escala):
    img = Image.new("L", (w * escala, h * escala), 0)
    dr = ImageDraw.Draw(img)

    def xy(lon, lat):
        return ((lon - W) / (E - W) * w * escala, (N - lat) / (N - S) * h * escala)

    for f in json.load(open(f"{BRUTOS}/agua.geojson"))["features"]:
        g = shape(f["geometry"])
        if f["properties"]["tipo"] == "linha":
            largura = max(1, int(1.2 * escala))
            dr.line([xy(*p) for p in g.coords], fill=255, width=largura)
            continue
        for pol in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            if pol.geom_type != "Polygon":
                continue
            dr.polygon([xy(*p) for p in pol.exterior.coords], fill=255)
            for it in pol.interiors:
                dr.polygon([xy(*p) for p in it.coords], fill=0)
    return np.asarray(img) > 127


def mar(dsm):
    # oceano no Copernicus = 0 m; componentes ligados à borda ou com mais de ~1 km²
    z = ndimage.binary_opening(dsm <= 0.15, iterations=1)
    lab, n = ndimage.label(z)
    if n == 0:
        return z
    tam = ndimage.sum(z, lab, range(1, n + 1))
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    ok = [i + 1 for i in range(n) if tam[i] > 1100 or (i + 1) in borda]
    return np.isin(lab, ok)


def main():
    dsm = mosaico()
    h, w = dsm.shape
    agua = mascara_agua(h, w, 1) | mar(dsm)
    # chão aproximado: abertura morfológica tira prédios e copas (~150 m), depois suaviza
    chao = ndimage.grey_opening(dsm, size=(5, 5))
    chao = ndimage.grey_closing(chao, size=(7, 7))   # fecha covas (açudes, cavas) que viram poços escuros
    chao = ndimage.gaussian_filter(chao, 1.2)
    baixa = agua & (chao < CFG.get("agua_baixa_m", 6.0))                     # só rebaixa água das áreas baixas (lago, rios, delta)
    chao = np.where(baixa, -1.0, np.maximum(chao, 1.0))
    chao = ndimage.gaussian_filter(chao, 0.6)
    np.save(f"{DADOS}/chao.npy", chao.astype(np.float32))

    v = chao + 32768.0
    r = np.floor(v / 256); g = np.floor(v - r * 256); b = np.floor((v - np.floor(v)) * 256)
    Image.fromarray(np.dstack([r, g, b]).astype(np.uint8)).save(f"{ASSETS}/elev.png")

    # textura
    hs = ndimage.zoom(chao, TEX, order=1)
    aguaT = mascara_agua(h, w, TEX) | (ndimage.zoom(mar(dsm).astype(np.uint8), TEX, order=0) > 0)
    gy, gx = np.gradient(hs, 30.0 / TEX)
    az, alt = np.radians(315), np.radians(40)
    sl = np.arctan(np.hypot(gx, gy) * 2.0)
    asp = np.arctan2(-gx, gy)
    sombra = np.clip(np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp), 0, 1)
    rng = np.random.default_rng(7)
    ruido = ndimage.gaussian_filter(rng.random(hs.shape), 14)
    ruido = (ruido - ruido.mean()) / ruido.std()
    mata = ndimage.gaussian_filter(rng.random(hs.shape), 1.2)
    mata = np.clip((mata - mata.mean()) / mata.std() * 0.25 + 0.5, 0, 1)
    t = np.clip(hs / 250.0, 0, 1)[..., None]
    campo = np.array([122, 160, 78]) * (1 - t) + np.array([84, 122, 60]) * t
    floresta = np.array([48, 86, 44])
    k = np.clip((ruido + 2.0 * t[..., 0] - 0.35) * 0.9, 0, 0.95)[..., None]
    k = k * (0.6 + 0.4 * mata[..., None])
    terra = campo * (1 - k) + floresta * k
    terra = terra * (0.62 + 0.45 * sombra[..., None])
    # água: mais escura no fundo, margem clara
    dist = ndimage.distance_transform_edt(aguaT)
    m = np.clip(dist / (12 * TEX), 0, 1)[..., None]
    cor_agua = np.array([86, 140, 168]) * (1 - m) + np.array([38, 82, 118]) * m
    img = np.where(aguaT[..., None], cor_agua, terra)
    img = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(img).filter(ImageFilter.SMOOTH).save(f"{ASSETS}/textura.jpg", quality=90)
    json.dump({"bbox": [W, S, E, N], "w": w, "h": h, "tex": [w * TEX, h * TEX],
               "zmin": float(chao.min()), "zmax": float(chao.max())},
              open(f"{ASSETS}/terreno.json", "w"))
    print(f"ok relevo {w}x{h} z {chao.min():.1f}..{chao.max():.1f} m · textura {w*TEX}x{h*TEX} · água {agua.mean()*100:.1f}%")


if __name__ == "__main__":
    main()
