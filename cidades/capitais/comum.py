"""Peças comuns dos 3 roteiros de "As capitais do Brasil" (Salvador → Rio → Brasília).
Cada ato é uma cidade do motor (cidades/capitais-ssa, capitais-rio, capitais-bsb) renderizada com o motor da versão centro
(centro/motor + marcos.js + marcos-capitais.js) e emendada em cidades/capitais/montar.py.
A linha do tempo do topo é a MESMA nos 3 atos (1549 → 2024) para a história parecer contínua."""
import json
import math
import os
import urllib.parse

import numpy as np

RAIZ_CAP = os.path.dirname(os.path.abspath(__file__))
LINHA = {"de": 1500, "ate": 2024}
FONTES = {"pt.wikipedia.org": "Wikipédia", "en.wikipedia.org": "Wikipédia", "fr.wikipedia.org": "Wikipédia", "biblioteca.ibge.gov.br": "IBGE",
          "www.ibge.gov.br": "IBGE", "cidades.ibge.gov.br": "IBGE", "commons.wikimedia.org": "Wikimedia Commons", "www.wikidata.org": "Wikidata",
          "www2.camara.leg.br": "Câmara dos Deputados", "www.camara.leg.br": "Câmara dos Deputados", "www.planalto.gov.br": "Planalto",
          "www12.senado.leg.br": "Senado", "www2.senado.leg.br": "Senado", "www.senado.leg.br": "Senado", "vitruvius.com.br": "Vitruvius",
          "www.vitruvius.com.br": "Vitruvius", "portal.iphan.gov.br": "IPHAN", "whc.unesco.org": "UNESCO"}
# faixas nacionais (o nome fica embaixo da bandeira); a bandeira usa os arquivos de motor/assets/bandeiras
REGIMES = [
    {"ano": 1500, "nome": "Brasil Colônia", "bandeira": "portugal"},
    {"ano": 1549.24, "nome": "Colônia · Governo-Geral", "bandeira": "portugal"},
    {"ano": 1763, "nome": "Colônia · sede do vice-rei", "bandeira": "portugal"},
    {"ano": 1808.18, "nome": "Sede da Corte portuguesa", "bandeira": "portugal"},
    {"ano": 1815.96, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
    {"ano": 1822.78, "nome": "Império do Brasil", "bandeira": "imperio"},
    {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
    {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
    {"ano": 1960, "nome": "República", "bandeira": "brasil"},
    {"ano": 1964.25, "nome": "Regime militar", "bandeira": "brasil"},
    {"ano": 1985.2, "nome": "Nova República", "bandeira": "brasil"},
]


def carrega(aqui):
    e = json.load(open(f"{aqui}/dados/pesquisa/eventos.json"))
    return {x["id"]: x for x in e["eventos"] + e.get("reserva", [])}


def fonte(e):
    nomes = []
    for u in e["fontes"]:
        h = urllib.parse.urlparse(u).netloc
        n = FONTES.get(h, h.removeprefix("www."))
        if n not in nomes:
            nomes.append(n)
    return "; ".join(nomes[:3])


def titulo(e, ultimas=1):
    pal = e["titulo_curto_PT"].split()
    k = max(1, len(pal) - ultimas)
    return " ".join(pal[:k]) + " <b>" + " ".join(pal[k:]) + "</b>"


class Chao:
    """altura do chão (m) da cidade, a partir de dados/chao.npy e do bbox do config"""
    def __init__(self, aqui):
        self.ch = np.load(f"{aqui}/dados/chao.npy"); cfg = json.load(open(f"{aqui}/config.json"))
        self.W, self.S, self.E, self.N = cfg["bbox"]; self.H, self.Wd = self.ch.shape

    def __call__(self, lon, lat, raio=0):
        c = int((lon - self.W) / (self.E - self.W) * self.Wd); r = int((self.N - lat) / (self.N - self.S) * self.H)
        c0, c1, r0, r1 = max(0, c - raio), min(self.Wd, c + raio + 1), max(0, r - raio), min(self.H, r + raio + 1)
        return float(max(np.median(self.ch[r0:r1, c0:c1]), 0.0))


def fazedor_cam(chao, exz):
    def cam(lon, lat, zoom, pitch=56, bearing=-20):
        return {"lon": lon, "lat": lat, "zoom": zoom, "pitch": pitch, "bearing": bearing, "z": round(chao(lon, lat, 3) * exz, 1)}
    return cam


def ls(z, lat):   # escala do globo (log de px por radiano) que bate com o zoom do mapa
    return round(math.log(6371000 * 2 ** z / (156543 * math.cos(math.radians(lat)))), 3)


def fazedor_bloco(EV):
    def bloco(eid, anos, c0, c1, dur=8.5, **kw):
        e = EV[eid]
        b = {"id": eid, "anos": anos, "cam": [c0, c1], "dur": dur,
             "cartao": {"titulo": kw.pop("titulo", titulo(e, kw.pop("destaque", 1))), "numero": kw.pop("numero", e.get("numero_impacto", "")),
                        "legenda": kw.pop("legenda", e["legenda"]), "detalhe": kw.pop("detalhe", e.get("detalhe", "")),
                        "fonte": fonte(e), "local": [e["local"]["lon"], e["local"]["lat"]]}}
        if "cartao_de" in kw:   # o cartão entra depois que a câmera chega (fração do bloco)
            b["cartao"]["de"] = kw.pop("cartao_de")
        b.update(kw)
        return b
    return bloco


def ajusta_anos(blocos):
    """o 3º ano do bloco (fim) não passa do ano do evento + 0,95 (contador mostra o ano certo enquanto o cartão está na tela)"""
    for b in blocos:
        a = b["anos"]
        if len(a) == 3 and "cartao" in b:
            a[2] = max(a[1] + 0.0001, min(a[2], math.floor(a[1]) + 0.95))


def marcas_do(blocos):
    return sorted({round(b["anos"][-2] if len(b["anos"]) == 3 else b["anos"][0]) for b in blocos if "cartao" in b})


def linha_completa():
    """marcas dos 3 atos juntas (gravadas por cada roteiro em cidades/capitais/marcas_<ato>.json)"""
    m = set()
    for ato in ("ssa", "rio", "bsb"):
        f = f"{RAIZ_CAP}/marcas_{ato}.json"
        if os.path.exists(f):
            m |= set(json.load(open(f)))
    return {**LINHA, "marcas": sorted(m)}


def grava_marcas(ato, blocos):
    json.dump(marcas_do(blocos), open(f"{RAIZ_CAP}/marcas_{ato}.json", "w"))


def imagem(aqui, i, legenda, autor_curto=None):
    L = json.load(open(f"{aqui}/dados/pesquisa/imagens.json"))
    L = L["imagens"] if isinstance(L, dict) else L
    x = L[i]; a = autor_curto or x["autor"].split("(")[0].split(" — ")[0].split(",")[0].strip().rstrip(",;")
    lic = "domínio público" if "úblico" in x.get("licenca", "") or "PD" in x.get("licenca", "") else x.get("licenca", "")
    return {"src": f"assets/epoca/e{i:02d}.jpg", "legenda": legenda, "credito": f"{a} · {x['ano']} · {lic} (Wikimedia Commons)"}
