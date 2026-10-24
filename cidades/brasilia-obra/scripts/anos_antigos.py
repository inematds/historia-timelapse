"""Construção de Brasília: antes de 1956 só existia o núcleo antigo de Planaltina (arraial de 1859) — os prédios mais perto da praça
de São Sebastião ganham anos de 1859 a 1955 (do centro para fora). O resto fica com o ano do modelo (curva de população do DF, de 1957).
Lê assets/pred_ano.modelo.f32 (cópia do modelo_anos) e grava assets/pred_ano.orig.f32; depois rodar cidades/capitais/scripts/limpa.py.
Uso: CIDADE=brasilia-obra .venv/bin/python -I cidades/brasilia-obra/scripts/anos_antigos.py"""
import os, shutil, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from cidade import *  # noqa
NUCLEO = (-47.6615, -15.6212, 380, 1859.0, 1955.0)   # lon, lat (Museu Histórico de Planaltina, OSM), nº de prédios, ano 1º, ano último
mod = f"{ASSETS}/pred_ano.modelo.f32"
if not os.path.exists(mod):
    shutil.copy(f"{ASSETS}/pred_ano.orig.f32", mod)
ano = np.fromfile(mod, np.float32).copy()
m = np.load(f"{DADOS}/predios_meta.npz", allow_pickle=True)
lo, la, n, a0, a1 = NUCLEO
d = np.hypot((m["lon"] - lo) * 107000, (m["lat"] - la) * 111320)
idx = np.argsort(d)[:n]
k = np.arange(n)
NA = 70   # o arraial: as ~70 casas mais perto da igreja sobem de 1810 a 1859; o resto, de 1859 a 1955
ano[idx] = np.where(k < NA, 1810.6 + (a0 - 1810.6) * k / NA, a0 + (a1 - a0) * ((k - NA) / (n - NA)) ** 0.8)
ano.astype(np.float32).tofile(f"{ASSETS}/pred_ano.orig.f32")
print("núcleo antigo:", n, "prédios até", round(float(d[idx[-1]])), "m da praça;", [(y, int((ano < y).sum())) for y in (1860, 1900, 1956, 1958, 1960)])
