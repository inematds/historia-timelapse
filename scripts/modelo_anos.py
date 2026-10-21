"""Ano de "nascimento" de cada prédio → motor/assets/pred_ano.f32

Ordem espacial: ano de ocupação do bairro (pesquisa) + distância dentro do bairro ao ponto mais antigo.
Depois a ordem é remapeada na curva de população, para que a mancha cresça no mesmo ritmo do contador.
Sem dados/pesquisa/bairros_epocas.json usa só a distância à Praça da Matriz (versão provisória).
Uso: .venv/bin/python -I scripts/modelo_anos.py
"""
import json
import os
import unicodedata

import numpy as np

import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
MATRIZ = tuple(CFG["centro_antigo"])
KM_LON, KM_LAT = 96.3, 111.0


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return " ".join(s.replace("-", " ").replace("'", " ").split())


def curva_pop():
    f = f"{PESQ}/populacao.json"
    if os.path.exists(f):
        pts = sorted((int(p["ano"]), float(p["pop"])) for p in json.load(open(f))["serie"])
    else:
        pts = [(1772, 1500), (1803, 3900), (1858, 20000), (1872, 43998), (1900, 73674), (1920, 179263),
               (1940, 272232), (1950, 394151), (1960, 641173), (1970, 885545), (1980, 1125477),
               (1991, 1263403), (2000, 1360590), (2010, 1409351), (2022, 1332845)]
    anos = np.array([a for a, _ in pts], float)
    pop = np.maximum.accumulate(np.array([p for _, p in pts], float))  # nunca "desconstrói"
    return anos, pop


def main():
    m = np.load(f"{DADOS}/predios_meta.npz", allow_pickle=True)
    lon, lat, poa, bairro, nomes = m["lon"], m["lat"], m["poa"], m["bairro"], m["nomes"]
    d = np.hypot((lon - MATRIZ[0]) * KM_LON, (lat - MATRIZ[1]) * KM_LAT)
    rng = np.random.default_rng(11)

    f = f"{PESQ}/bairros_epocas.json"
    if os.path.exists(f):
        bj = json.load(open(f))
        tab = {norm(b["bairro"]): float(b["ano_aprox_ocupacao"]) for b in bj["bairros"] if b.get("ano_aprox_ocupacao")}
        for lei, nomes_lei in bj.get("bairros_so_com_lei", {}).items():
            if lei.startswith("_"):
                continue
            for nm in nomes_lei:  # lei = limite superior; ocupação ~15 anos antes
                tab.setdefault(norm(nm), float(lei[:4]) - 15)
        base = np.array([tab.get(norm(nomes[b]), np.nan) if b >= 0 else np.nan for b in bairro])
        sem = sorted({str(nomes[b]) for b in bairro[poa & np.isnan(base)] if b >= 0})
        print("bairros de POA sem data:", len(sem), sem[:30])
        ok = ~np.isnan(base) & poa
        a, b0 = np.polyfit(d[ok], base[ok], 1)
        base = np.where(np.isnan(base), b0 + a * d, base)
        # dentro do bairro: do ponto mais perto do centro antigo para fora, ao longo de ~metade do tempo restante
        score = base.copy()
        for bi in np.unique(bairro[poa]):
            m_ = poa & (bairro == bi)
            dd = d[m_]
            r = (dd - dd.min()) / (np.ptp(dd) + 1e-9)
            espalha = np.clip((2020 - base[m_]) * 0.45, 5, 70)
            score[m_] = base[m_] + r * espalha
        score += rng.normal(0, 2.5, len(d))
        fonte = "bairros"
    anos, pop = curva_pop()
    ano = np.full(len(d), 2030.0, np.float32)
    # Porto Alegre: rank → fração da população final → ano
    idx = np.where(poa)[0]
    ordem = idx[np.argsort(score[idx])]
    frac = (np.arange(len(ordem)) + 1) / len(ordem)
    ano[ordem] = np.interp(frac * pop[-1], pop, anos)
    # vizinhos (Canoas, Viamão, Guaíba...): crescem de 1930 a 2020 pela distância ao próprio centro mais denso
    fora = np.where(~poa)[0]
    ordf = fora[np.argsort(d[fora] + rng.normal(0, 1.5, len(fora)))]
    ano[ordf] = 1930 + 90 * ((np.arange(len(ordf)) + 1) / len(ordf)) ** 1.3
    ano.astype(np.float32).tofile(f"{ASSETS}/pred_ano.f32")
    for y in (1772, 1800, 1850, 1900, 1941, 1970, 2000, 2024):
        print(y, int((ano[poa] <= y).sum()), end=" · ")
    print(f"\nfonte={fonte} n={len(ano)}")


if __name__ == "__main__":
    main()
