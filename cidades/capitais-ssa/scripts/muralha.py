"""Salvador: a linha da muralha de taipa de 1549 (Portas de São Bento → Praça Tomé de Sousa → Portas do Carmo), traçado APROXIMADO
de dados/pesquisa/predios.json (muralha-1549.tracado_aproximado) → linha 'muralha' em assets/efeitos.json, com z do chão.
Uso: CIDADE=capitais-ssa .venv/bin/python -I cidades/capitais-ssa/scripts/muralha.py (depois do prep_efeitos.py)"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from cidade import *  # noqa
ch = np.load(f"{DADOS}/chao.npy"); H, Wd = ch.shape
def z(lon, lat):
    c = min(max(int((lon - W) / (E - W) * Wd), 0), Wd - 1); r = min(max(int((N - lat) / (N - S) * H), 0), H - 1)
    return round(float(max(ch[r, c], 0.0)), 1)
P = json.load(open(f"{PESQ}/predios.json")); P = P["predios"] if isinstance(P, dict) else P
mur = [p for p in P if p["id"] == "muralha-1549"][0]["tracado_aproximado"]["pontos"]   # [lat, lon]
pts = []
for (la0, lo0), (la1, lo1) in zip(mur, mur[1:]):           # densifica para o traço acompanhar o chão
    for k in range(12):
        la, lo = la0 + (la1 - la0) * k / 12, lo0 + (lo1 - lo0) * k / 12; pts.append([lo, la, z(lo, la)])
pts.append([mur[-1][1], mur[-1][0], z(mur[-1][1], mur[-1][0])])
ef = json.load(open(f"{ASSETS}/efeitos.json")); ef.setdefault("linhas", {})["muralha"] = [pts]
json.dump(ef, open(f"{ASSETS}/efeitos.json", "w")); print("muralha", len(pts), "pontos")
