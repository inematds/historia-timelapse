"""Capitais: esconde (ano 9999) os prédios comuns do OSM/Microsoft que caem no lote de cada marco do roteiro.
Parte sempre do pred_ano.orig.f32 (cópia intocada), então pode rodar de novo quando o roteiro mudar.
Lote = retângulo larg × comp girado pelo rumo + folga (m), ou círculo `raio_limpa`.
Uso: CIDADE=capitais-rio .venv/bin/python -I cidades/capitais/scripts/limpa.py"""
import json, math, os, shutil, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from cidade import *  # noqa
orig = f"{ASSETS}/pred_ano.orig.f32"
if not os.path.exists(orig):
    shutil.copy(f"{ASSETS}/pred_ano.f32", orig)
m = np.load(f"{DADOS}/predios_meta.npz", allow_pickle=True)
ano = np.fromfile(orig, np.float32)
rot = json.load(open(f"{DIR}/roteiro.json"))
tot = 0
for mc in rot.get("marcos", []):
    kl = 111320 * math.cos(math.radians(mc["lat"]))
    dx, dy = (m["lon"] - mc["lon"]) * kl, (m["lat"] - mc["lat"]) * 111320
    if "raio_limpa" in mc:
        sel = np.hypot(dx, dy) < mc["raio_limpa"]
    else:
        th = math.radians(mc.get("rumo", 180) - 180)          # gira o mundo para o referencial do prédio
        x = math.cos(th) * dx - math.sin(th) * dy; y = math.sin(th) * dx + math.cos(th) * dy
        f = mc.get("folga", 6)
        sel = (np.abs(x) <= mc.get("larg", 20) / 2 + f) & (np.abs(y) <= mc.get("comp", 20) / 2 + f)
    ano[sel] = 9999; tot += int(sel.sum()); print(mc["id"], int(sel.sum()))
ano.tofile(f"{ASSETS}/pred_ano.f32")
print("escondidos", tot)
