"""Versão centro: os prédios comuns (OSM/Microsoft) que caem sob um marco histórico nunca aparecem (ano 9999).
Roda depois do modelo_anos.py. Raio por tipo (m). Uso: CIDADE=itaguai-centro .venv/bin/python -I centro/scripts/limpa_marcos.py"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa
RAIO = {"igreja": 26, "claustro": 30, "estacao": 34, "estacao_castelo": 36, "catedral_moderna": 28, "moderno": 24, "sobrado": 16, "casa": 12, "casarao": 14,
        "chafariz": 7, "coreto": 9, "casa_ong": 14}
m = np.load(f"{DADOS}/predios_meta.npz", allow_pickle=True)
ano = np.fromfile(f"{ASSETS}/pred_ano.f32", np.float32)
rot = json.load(open(f"{DIR}/roteiro.json"))
kl = 111320 * math.cos(math.radians((S + N) / 2))
tot = 0
for mc in rot.get("marcos", []):
    r = mc.get("raio_limpa", RAIO.get(mc["tipo"], 15))
    d = np.hypot((m["lon"] - mc["lon"]) * kl, (m["lat"] - mc["lat"]) * 111320)
    sel = d < r
    ano[sel] = 9999; tot += int(sel.sum()); print(mc["id"], int(sel.sum()))
# praças do OSM são espaço aberto: prédio comum dentro delas não aparece
from shapely.geometry import shape, Point
af = f"{BRUTOS}/areas.geojson"
if os.path.exists(af):
    pr = [shape(f["geometry"]) for f in json.load(open(af))["features"] if f["properties"]["tipo"] in ("park", "square", "garden")]
    for g in pr:
        x0, y0, x1, y1 = g.bounds
        idx = np.where((m["lon"] > x0) & (m["lon"] < x1) & (m["lat"] > y0) & (m["lat"] < y1))[0]
        sel = [i for i in idx if g.contains(Point(m["lon"][i], m["lat"][i]))]
        ano[sel] = 9999; tot += len(sel)
ano.tofile(f"{ASSETS}/pred_ano.f32")
print("escondidos", tot)
