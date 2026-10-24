"""Brasília: os dois eixos do Plano Piloto ("o sinal da cruz") como 4 linhas que saem do Marco Zero (Rodoviária)
→ acrescentadas a assets/efeitos.json (linhas eixo_l, eixo_o, eixo_n, eixo_s), com z do chão.
Eixo Rodoviário: geometria do OSM (ways 'Eixo Rodoviário*', DF-002); Eixo Monumental: pontos de dados/pesquisa/eixos.json.
Rodar depois de scripts/prep_efeitos.py. Uso: CIDADE=capitais-bsb .venv/bin/python -I cidades/capitais-bsb/scripts/eixos.py"""
import json, math, os, sys
import numpy as np
import osmium
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from cidade import *  # noqa
ch = np.load(f"{DADOS}/chao.npy"); H, Wd = ch.shape
def z(lon, lat):
    c = min(max(int((lon - W) / (E - W) * Wd), 0), Wd - 1); r = min(max(int((N - lat) / (N - S) * H), 0), H - 1)
    return round(float(max(ch[r, c], 0.0)), 1)
EX = json.load(open(f"{PESQ}/eixos.json"))
Z0 = (-47.882611, -15.793389)                     # Rodoviária = Marco Zero (eixos.json)
KX = 111320 * math.cos(math.radians(Z0[1]))
pts = []
for o in osmium.FileProcessor(f"{RAIZ}/{CFG['pbf']}").with_filter(osmium.filter.KeyFilter("highway")).with_locations():
    if o.is_way() and o.tags.get("name", "").startswith("Eixo Rodoviário") and o.tags.get("highway") == "trunk":
        pts += [(n.lon, n.lat) for n in o.nodes]
P = np.array(pts); d = np.hypot((P[:, 0] - Z0[0]) * KX, (P[:, 1] - Z0[1]) * 111320)
def asa(sel):
    Q, dd = P[sel], d[sel]; o = np.argsort(dd); Q, dd = Q[o], dd[o]
    out = [list(Z0)]
    for k in np.arange(150, dd.max(), 250):       # média dos nós (as duas pistas) a cada 250 m de distância do Marco Zero
        m = (dd > k - 125) & (dd <= k + 125)
        if m.any(): out.append([round(float(Q[m, 0].mean()), 6), round(float(Q[m, 1].mean()), 6)])
    return out
norte, sul = asa(P[:, 1] > Z0[1]), asa(P[:, 1] < Z0[1])
mon = [(p["lon"], p["lat"]) for p in EX["eixo_monumental"]["pontos"] if p.get("lon")]
leste = [list(Z0)] + [[x, y] for x, y in sorted([q for q in mon if q[0] > Z0[0]], key=lambda q: q[0])]
oeste = [list(Z0)] + [[x, y] for x, y in sorted([q for q in mon if q[0] < Z0[0]], key=lambda q: -q[0])]
ef = json.load(open(f"{ASSETS}/efeitos.json")); ef.setdefault("linhas", {})
for k, l in (("eixo_n", norte), ("eixo_s", sul), ("eixo_l", leste), ("eixo_o", oeste)):
    ef["linhas"][k] = [[[x, y, z(x, y)] for x, y in l]]
    print(k, len(l), "pontos", round(sum(math.hypot((l[i][0] - l[i-1][0]) * KX, (l[i][1] - l[i-1][1]) * 111320) for i in range(1, len(l)))), "m")
json.dump(ef, open(f"{ASSETS}/efeitos.json", "w"))
