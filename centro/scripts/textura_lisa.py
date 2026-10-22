"""Versão centro: chão limpo para ver de perto (zoom 18–20) — campo verde com relevo sombreado e variação suave,
sem as manchas de mata borradas da textura padrão (que de perto parecem erro de carregamento). Água dos canais em azul.
Saída: assets/textura.jpg (a lisa original fica em textura_lisa.jpg). Uso: CIDADE=itaguai-centro .venv/bin/python -I centro/scripts/textura_lisa.py"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from shapely.geometry import shape
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa

TEX = CFG.get("tex", 20)
chao = np.load(f"{DADOS}/chao.npy")
hs = ndimage.zoom(chao, TEX, order=3)
H, Wd = hs.shape
gy, gx = np.gradient(hs, 30.0 / TEX)
az, alt = np.radians(315), np.radians(45)
sl = np.arctan(np.hypot(gx, gy) * 1.6); asp = np.arctan2(-gx, gy)
sombra = np.clip(np.sin(alt) * np.cos(sl) + np.cos(alt) * np.sin(sl) * np.cos(az - asp), 0, 1)
rng = np.random.default_rng(3)
largo = ndimage.gaussian_filter(rng.random((H // 8, Wd // 8)), 6); largo = ndimage.zoom((largo - largo.mean()) / largo.std(), 8, order=1)
largo = np.pad(largo, ((0, H - largo.shape[0]), (0, Wd - largo.shape[1])), mode="edge")[:H, :Wd]
fino = ndimage.gaussian_filter(rng.random((H, Wd)), 1.0); fino = (fino - fino.mean()) / fino.std()
t = np.clip(hs / 40.0, 0, 1)[..., None]
campo = np.array([118, 146, 84]) * (1 - t) + np.array([96, 128, 70]) * t           # várzea → morro
img = campo * (1 + 0.05 * largo[..., None] + 0.025 * fino[..., None])
img = img * (0.72 + 0.36 * sombra[..., None])
# água: canais e rios (linhas) e lagoas (polígonos)
ag = Image.new("L", (Wd, H), 0); dr = ImageDraw.Draw(ag)
xy = lambda lo, la: ((lo - W) / (E - W) * Wd, (N - la) / (N - S) * H)
mpx = (E - W) * 111320 * np.cos(np.radians((S + N) / 2)) / Wd
for f in json.load(open(f"{BRUTOS}/agua.geojson"))["features"]:
    g = shape(f["geometry"])
    if f["properties"]["tipo"] == "linha":
        dr.line([xy(*p[:2]) for p in g.coords], fill=255, width=max(2, round(7 / mpx)), joint="curve")
    else:
        for pol in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            if pol.geom_type == "Polygon":
                dr.polygon([xy(*p[:2]) for p in pol.exterior.coords], fill=255)
m = ndimage.gaussian_filter(np.asarray(ag).astype(np.float32) / 255, 0.8)[..., None]
img = img * (1 - m) + np.array([62, 108, 140]) * m
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(f"{ASSETS}/textura.jpg", quality=93)
print(f"textura lisa {Wd}x{H} {mpx:.2f} m/px")
