"""Folha de contato dos quadros q_*.jpg de uma cena: python folha.py <pasta-cena> <saida.jpg> [colunas]"""
import glob, sys
from PIL import Image, ImageDraw
fs = sorted(glob.glob(f"{sys.argv[1]}/q_*.jpg"), key=lambda f: float(f.split("q_")[1][:-4].replace("_", ".")))
nc = int(sys.argv[3]) if len(sys.argv) > 3 else 3; w, h = 640, 360
im = Image.new("RGB", (w * nc, h * ((len(fs) + nc - 1) // nc)), "black")
for i, f in enumerate(fs):
    q = Image.open(f).resize((w, h)); ImageDraw.Draw(q).text((8, 8), f.split("q_")[1][:-4], fill="yellow"); im.paste(q, ((i % nc) * w, (i // nc) * h))
im.save(sys.argv[2], quality=85); print(sys.argv[2], len(fs))
