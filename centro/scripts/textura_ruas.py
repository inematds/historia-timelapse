"""Versão centro: pinta as ruas do OSM (dados/brutos/ruas.geojson) e as praças (config "pracas") sobre assets/textura.jpg.
Roda depois do prep_terreno.py (que gera a textura lisa). Guarda a lisa em textura_lisa.jpg na 1ª vez.
Uso: CIDADE=itaguai-centro .venv/bin/python -I centro/scripts/textura_ruas.py"""
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa

LARG_M = {"motorway": 22, "trunk": 18, "primary": 14, "secondary": 12, "tertiary": 10, "residential": 8,
          "unclassified": 7, "living_street": 6, "service": 4.5, "pedestrian": 6, "track": 3.5}
lisa = f"{ASSETS}/textura_lisa.jpg"
if not os.path.exists(lisa):
    shutil.copy(f"{ASSETS}/textura.jpg", lisa)
img = Image.open(lisa).convert("RGB")
w, h = img.size
mpx = (E - W) * 111320 * np.cos(np.radians((S + N) / 2)) / w   # metros por pixel


def xy(lon, lat):
    return ((lon - W) / (E - W) * w, (N - lat) / (N - S) * h)


rf = f"{BRUTOS}/ruas_todas.geojson"
ruas = json.load(open(rf if os.path.exists(rf) else f"{BRUTOS}/ruas.geojson"))["features"]
calc = Image.new("L", (w, h), 0); asf = Image.new("L", (w, h), 0)
dc, da = ImageDraw.Draw(calc), ImageDraw.Draw(asf)
n = 0
for f in ruas:
    tipo = (f["properties"].get("hw") or "").replace("_link", "")
    if os.environ.get("SO_PRACAS") or tipo not in LARG_M:   # SO_PRACAS=1: ruas vão como vetor (C.ruas), a textura leva só as praças
        continue
    g = f["geometry"]
    linhas = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"] if g["type"] == "MultiLineString" else []
    for ln in linhas:
        pts = [xy(*p[:2]) for p in ln]
        if all(not (-50 < x < w + 50 and -50 < y < h + 50) for x, y in pts):
            continue
        lw = max(1, round(LARG_M[tipo] / mpx))
        dc.line(pts, fill=255, width=lw + max(2, round(3 / mpx)), joint="curve")   # calçada
        da.line(pts, fill=255, width=lw, joint="curve")
        n += 1
for p in CFG.get("pracas", []):   # praças: [[lon,lat],...]
    dc.polygon([xy(*q) for q in p["poly"]], fill=255)
a = np.asarray(img).astype(np.float32)
mc = np.asarray(calc.filter(ImageFilter.GaussianBlur(0.3))).astype(np.float32)[..., None] / 255
ma = np.asarray(asf.filter(ImageFilter.GaussianBlur(0.5))).astype(np.float32)[..., None] / 255
a = a * (1 - mc) + np.array([150, 146, 136]) * mc        # calçada clara
a = a * (1 - ma) + np.array([78, 80, 86]) * ma           # asfalto
pr = Image.new("L", (w, h), 0); dp = ImageDraw.Draw(pr)
for p in CFG.get("pracas", []):
    dp.polygon([xy(*q) for q in p["poly"]], fill=255)
af = f"{BRUTOS}/areas.geojson"
for f in (json.load(open(af))["features"] if os.path.exists(af) else []):
    if f["properties"]["tipo"] in ("park", "pitch", "garden", "cemetery"):
        dp.polygon([xy(*q) for q in f["geometry"]["coordinates"][0]], fill=255)
mp = np.asarray(pr.filter(ImageFilter.GaussianBlur(1))).astype(np.float32)[..., None] / 255
a = a * (1 - mp) + np.array([104, 150, 82]) * mp         # gramado das praças
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(f"{ASSETS}/textura.jpg", quality=92)
print(f"ruas={n} textura {w}x{h} {mpx:.2f} m/px")
