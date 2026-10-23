"""Ato 1 de "As capitais do Brasil": SALVADOR, primeira capital (1549 → 1763). Gera cidades/capitais-ssa/roteiro.json.
Abre com a capa e o globo; conta por que o rei criou uma capital, por que na Bahia, como a cidade foi erguida no alto da escarpa,
e — nos eventos 'porque-*' — por que a capital foi para o Rio. Prédios do poder em centro/motor/marcos-capitais.js.
Uso: python3 cidades/capitais-ssa/roteiro_ssa.py"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "capitais"))
from comum import *  # noqa

EV = carrega(AQUI)
EXZ = 1.6
zc = Chao(AQUI)
cam = fazedor_cam(zc, EXZ)
bloco = fazedor_bloco(EV)

C0 = cam(-38.48, -12.885, 11.2, 0, 0)
BAIA = cam(-38.56, -12.93, 11.9, 48, 290)
RECON = cam(-38.56, -12.86, 11.7, 42, 320)
VILAV = cam(-38.5325, -13.0005, 16.4, 58, 190)
BARRA = cam(-38.531, -13.004, 15.2, 56, 200)
ESCARPA = cam(-38.5140, -12.9745, 16.4, 60, 90)
PRACA = cam(-38.5128, -12.9748, 17.7, 60, 135)
PRACA_L = cam(-38.5126, -12.9745, 17.0, 56, 100)
TERREIRO = cam(-38.5103, -12.9729, 17.7, 58, 315)
SE = cam(-38.5120, -12.9733, 17.8, 58, 90)
PORTO = cam(-38.5170, -12.9720, 15.4, 55, 80)
LONGE = cam(-38.515, -12.975, 12.9, 48, 215)     # da cidade para o sul/sudoeste, onde ficam Minas, o Rio e o Prata
FIM = cam(-38.515, -12.965, 12.6, 42, 250)

PT = [40, 110, 70]       # navios portugueses
NL = [235, 120, 30]      # holandeses (Companhia das Índias Ocidentais)
IB = [200, 40, 40]       # armada luso-espanhola de 1625


def seta(texto, lon=-38.528, lat=-12.988):
    return [{"lon": lon, "lat": lat, "texto": texto, "z": 250, "tam": 40}]


blocos = [
    {"id": "capa", "anos": [1500, 1500], "cam": [C0, C0], "dur": 5.5, "capa": {"imagem": "assets/capa_full.jpg", "segura": 5.5, "some": 0.8}},
    {"id": "globo", "anos": [1500, 1500], "cam": [C0, C0], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "uf": "BA", "uf_de": 1500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -25, "lat": -8, "ls": 5.95}], [0.3, {"lon": -38, "lat": -11, "ls": 6.6}],
                          [0.65, {"lon": -38.6, "lat": -12.8, "ls": 8.7}], [1, {"lon": C0["lon"], "lat": C0["lat"], "ls": ls(C0["zoom"], C0["lat"])}]],
               "rotulos": [{"lon": -51, "lat": -11, "texto": "BRASIL", "de": 380, "ate": 3500, "tam": 84},
                           {"lon": -41.5, "lat": -12.3, "texto": "BAHIA", "de": 2600, "ate": 40000, "tam": 60},
                           {"lon": -38.51, "lat": -12.97, "texto": "SALVADOR", "de": 30000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco("tupinambas-1500", [1500, 1500], C0, BAIA, 9.0, destaque=1, pulso_r=3000),
    bloco("todos-os-santos-1501", [1500, 1501.83, 1501.9], BAIA, BAIA, 9.0, pulo=0.6, destaque=3,
          frota={"de": [-38.62, -13.08], "para": [-38.60, -12.93], "n": 3, "r": 120, "cor": PT, "dura": 6, "rotulo": "Expedição portuguesa", "sub": "1º/11/1501"}),
    bloco("caramuru-1510", [1501.9, 1510, 1510.5], BAIA, VILAV, 8.5, pulo=0.6, destaque=1),
    bloco("vila-do-pereira-1536", [1510.5, 1536.85, 1537], VILAV, VILAV, 8.5, pulo=0.8, destaque=1),
    bloco("coutinho-1547", [1537, 1547, 1547.5], VILAV, BARRA, 8.5, pulo=0.6, destaque=1, tom={"cor": "#a15050", "forca": 0.3},
          tropas={"lon": -38.5333, "lat": -13.0033, "n": 70, "raio_km": 0.7, "a0": 0.3, "a1": 2.8, "cor": [200, 60, 40]}),
    bloco("porque-regimento-1548", [1547.5, 1548.96, 1549.0], BARRA, C0, 9.0, pulo=0.5, destaque=2),
    bloco("porque-bahia-1549", [1549.0, 1549.1, 1549.2], C0, BAIA, 9.0, pulo=0.2, destaque=1),
    bloco("tome-de-sousa-1549", [1549.2, 1549.24, 1549.28], BAIA, BARRA, 9.5, pulo=0.2, destaque=2,
          frota={"de": [-38.56, -13.08], "para": [-38.535, -13.006], "n": 6, "r": 110, "cor": PT, "dura": 6.5, "rotulo": "Armada de Tomé de Sousa", "sub": "3 naus, 2 caravelas, 1 bergantim"}),
    bloco("cidade-alta-1549", [1549.28, 1549.3, 1549.4], BARRA, ESCARPA, 9.5, pulo=0.2, destaque=2, destaca=["linha:muralha"]),
    bloco("primeiros-predios-1549", [1549.4, 1549.5, 1549.58], ESCARPA, PRACA, 9.0, pulo=0.2, destaque=2, destaca=["marco:palacio", "marco:camara"]),
    bloco("jesuitas-1549", [1549.58, 1549.6, 1549.9], PRACA, TERREIRO, 8.5, pulo=0.2, destaque=1, destaca=["marco:colegio"]),
    bloco("bispado-1551", [1549.9, 1551.15, 1551.4], TERREIRO, SE, 8.5, pulo=0.4, destaque=2, destaca=["marco:se"]),
    bloco("engenhos-1587", [1551.4, 1587, 1587.5], SE, RECON, 9.0, pulo=1.4, destaque=2),
    bloco("relacao-1609", [1587.5, 1609.18, 1609.4], RECON, PRACA_L, 8.5, pulo=1.0, destaque=1),
    bloco("holandeses-1624", [1609.4, 1624.35, 1624.4], PRACA_L, PORTO, 10.0, pulo=0.8, destaque=2, tom={"cor": "#a15050", "forca": 0.3},
          frota={"de": [-38.60, -13.03], "para": [-38.522, -12.968], "n": 35, "r": 90, "espalha_km": 3, "cor": NL, "dura": 7, "rotulo": "Frota holandesa", "sub": "1624 · 35 navios"}),
    bloco("jornada-vassalos-1625", [1624.4, 1625.33, 1625.4], PORTO, PORTO, 10.0, pulo=0.3, destaque=2, tom={"cor": "#a15050", "forca": 0.25},
          frota={"de": [-38.62, -13.05], "para": [-38.53, -12.965], "n": 52, "r": 90, "espalha_km": 4, "cor": IB, "dura": 7, "rotulo": "Jornada dos Vassalos", "sub": "1625 · 52 navios"}),
    bloco("catedral-1672", [1625.4, 1672.49, 1672.6], PORTO, TERREIRO, 8.5, pulo=1.2, destaque=2, destaca=["marco:jesus"]),
    bloco("porque-sacramento-1680", [1672.6, 1680.06, 1680.3], TERREIRO, LONGE, 9.0, pulo=0.6, destaque=2, rotulos=seta("↖ COLÔNIA DO SACRAMENTO · RIO DA PRATA")),
    bloco("porque-ouro-1695", [1680.3, 1695, 1695.4], LONGE, LONGE, 9.0, pulo=0.8, destaque=2, rotulos=seta("↑ MINAS GERAIS · OURO")),
    bloco("porque-moeda-1699", [1695.4, 1699, 1699.4], LONGE, PRACA, 9.0, pulo=0.5, destaque=2),
    bloco("porque-caminho-novo-1707", [1699.4, 1707, 1707.4], PRACA, LONGE, 9.0, pulo=0.6, destaque=2, rotulos=seta("↑ RIO DE JANEIRO · PORTO DO OURO")),
    bloco("vice-rei-1720", [1707.4, 1720.89, 1720.95], LONGE, PRACA, 8.5, pulo=0.8, destaque=2, destaca=["marco:palacio"]),
    bloco("porque-madri-1750", [1720.95, 1750.04, 1750.3], PRACA, LONGE, 9.0, pulo=1.2, destaque=2, rotulos=seta("↖ SETE POVOS · FRONTEIRA SUL")),
    bloco("porque-jesuitas-1759", [1750.3, 1759.67, 1759.8], LONGE, TERREIRO, 8.5, pulo=0.6, destaque=2, destaca=["marco:colegio", "marco:jesus"]),
    bloco("porque-sacramento-cai-1762", [1759.8, 1762.83, 1762.9], TERREIRO, LONGE, 9.0, pulo=0.5, destaque=2, rotulos=seta("↖ COLÔNIA DO SACRAMENTO · RIO DA PRATA"),
          tom={"cor": "#a15050", "forca": 0.2}),
    bloco("porque-capital-rio-1763", [1762.9, 1763.5, 1763.55], LONGE, FIM, 11.0, pulo=0.4, destaque=2, chega=0.55, destaca=["marco:palacio"],
          frota={"de": [-38.522, -12.968], "para": [-38.60, -13.10], "n": 1, "r": 130, "cor": PT, "dura": 8, "rotulo": "A sede vai para o Rio", "sub": "1763"}),
]
IMGS = {"porque-regimento-1548": (0, "D. João III, o rei que criou o Governo-Geral"), "tome-de-sousa-1549": (1, "Tomé de Sousa (ilustração imaginada, séc. XX)"),
        "cidade-alta-1549": (3, "São Salvador no alto do morro, vista de 1644"), "porque-bahia-1549": (8, "A Baía de Todos os Santos, carta de 1647"),
        "holandeses-1624": (4, "O ataque holandês a São Salvador, 1624"), "jornada-vassalos-1625": (7, "A recuperação da Bahia, 1625 (Maino)"),
        "engenhos-1587": (9, "Engenhos de açúcar do Recôncavo (gravura de 1645)"), "relacao-1609": (6, "A cidade murada, planta de 1631"),
        "catedral-1672": (10, "Vista e planta de São Salvador, 1714"), "porque-jesuitas-1759": (12, "O Marquês de Pombal"),
        "porque-capital-rio-1763": (13, "O Conde da Cunha, 1º vice-rei no Rio")}
for b in blocos:
    if b["id"] in IMGS:
        i, leg = IMGS[b["id"]]
        b["imagem"] = imagem(AQUI, i, leg)
ROT = {"vila-do-pereira-1536": ("VILA VELHA (DO PEREIRA)", -38.5333, -13.0033), "caramuru-1510": ("PORTO DA BARRA", -38.5333, -13.0033),
       "engenhos-1587": ("RECÔNCAVO", -38.60, -12.80), "cidade-alta-1549": ("CIDADE ALTA", -38.5115, -12.9735),
       "holandeses-1624": ("CIDADE BAIXA · PORTO", -38.5150, -12.9710)}
for b in blocos:
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b.setdefault("rotulos", []).append({"lon": lo, "lat": la, "texto": nm, "z": round(zc(lo, la) * EXZ + 60, 1), "tam": 30})
ajusta_anos(blocos)
grava_marcas("ssa", blocos)


def M(id_, tipo, lon, lat, rumo, ano, pronto=None, **kw):
    m = {"id": id_, "tipo": tipo, "lon": lon, "lat": lat, "rumo": rumo, "ano": ano, "z": round(zc(lon, lat, 1), 1), **kw}
    if pronto:
        m["pronto"] = pronto
    return m


EZ = 1.25
MARCOS = [
    # Praça do Palácio (Tomé de Sousa): casas dos governadores ao sul (fachada para o norte), Câmara a leste (fachada para o oeste)
    M("palacio", "palacio", -38.51306, -12.975026, 0, 1549.42, 1549.56, larg=43, comp=30, andares=2, pe=5.5, platibanda=0, telhado_visivel=True, avanco=12,
      escadaria=False, parede="#EFE6CF", cor="#B8AE98", rotulo="Casa dos governadores", sub="1549 · hoje Palácio Rio Branco"),
    M("camara", "palacio", -38.51252, -12.974877, 270, 1549.44, 1549.56, larg=42, comp=16, andares=2, pe=5.0, platibanda=0, telhado_visivel=True, avanco=0,
      escadaria=False, parede="#F2EEE4", cor="#B8AE98", rotulo="Casa de Câmara e Cadeia", sub="1549"),
    M("camara_torre", "sobrado", -38.51252 - 0.00009, -12.974877, 270, 1698, larg=6.5, comp=6.5, andares=4, pe=3.8, cor="#B8AE98", sacadas=False),
    M("se", "igreja", -38.5118, -12.9732, 270, 1551.3, 1553, larg=18, comp=50, pe=12, torres=2, coroa="piramide", cor="azul", rotulo="Sé", sub="1552 · demolida em 1933"),
    M("colegio", "claustro", -38.509771, -12.972282, 135, 1549.62, 1590, lado=56, ala_larg=9, andares=2, cor="azul", rotulo="Colégio dos Jesuítas", sub="1549 → 1590"),
    M("jesus", "igreja", -38.510533, -12.972633, 135, 1657, 1672.49, larg=25, comp=58, pe=17, torres=2, coroa="piramide", cor="ocre",
      rotulo="Igreja dos Jesuítas", sub="1672 · hoje Catedral Basílica"),
    M("misericordia", "igreja", -38.511982, -12.973867, 40, 1550, 1552, larg=9, comp=28, pe=9, torres=1, cor="vinho"),
    M("sfrancisco", "igreja", -38.509053, -12.974631, 300, 1686, 1720, larg=27, comp=62, pe=14, torres=2, coroa="piramide", cor="ocre",
      rotulo="São Francisco", sub="1686–1720"),
    M("conceicao", "igreja", -38.514292, -12.975305, 303, 1739, 1765, larg=30, comp=56, pe=16, torres=2, cor="ocre"),
    M("smarcelo", "forte_redondo", -38.517846, -12.969924, 90, 1612, 1623, raio=36, alt=8, torreao_r=0.42, larg=76, comp=76,
      rotulo="Forte de São Marcelo", sub="1623 · no mar"),
    M("barra", "forte_redondo", -38.532778, -13.010278, 200, 1583, 1587, raio=24, alt=7, lados=10, torreao=False, parede="#E6E0D2", larg=50, comp=50,
      rotulo="Forte de Santo Antônio da Barra", sub="1583"),
    M("farol", "farol", -38.53291, -13.01036, 0, 1698, raio=3.4, alt=22, larg=8, comp=8, rotulo="Farol da Barra", sub="1698 · 1º das Américas"),
    M("monteserrat", "forte_redondo", -38.517719, -12.929965, 300, 1583, 1586, raio=18, alt=7, lados=6, torreao=False, parede="#E6E0D2", larg=38, comp=38),
    M("santamaria", "forte_redondo", -38.5339883, -13.0045093, 260, 1614, 1627, raio=16, alt=6, lados=7, torreao=False, parede="#E6E0D2", larg=34, comp=34),
    M("saobento", "claustro", -38.51388889, -12.97916667, 90, 1582, 1584, lado=44, ala_larg=8, andares=2, cor="azul"),
]

REG = [{"ano": 1500, "nome": "Terra dos tupinambás", "bandeira": "portugal"},
       {"ano": 1501.83, "nome": "Brasil Colônia", "bandeira": "portugal"},
       {"ano": 1534, "nome": "Capitania da Baía", "bandeira": "portugal"},
       {"ano": 1549.24, "nome": "Colônia · Governo-Geral", "bandeira": "portugal"},
       {"ano": 1624.35, "nome": "Ocupada pelos holandeses", "bandeira": "holanda"},
       {"ano": 1625.33, "nome": "Colônia · Governo-Geral", "bandeira": "portugal"},
       {"ano": 1720.89, "nome": "Colônia · sede do vice-rei", "bandeira": "portugal"}]

roteiro = {
    "titulo": "As capitais do Brasil · ato 1: Salvador",
    "exz": EXZ, "exb": 1.5, "marcos_ez": EZ, "predios_neutros": True, "cartaoDireita": 660, "cartaoEsquerda": 500,
    "hud_de_bloco": "tupinambas-1500",
    "linha": linha_completa(),
    "popRotulo": "habitantes em Salvador",
    "longe": {"auto": True},
    "regimes": REG,
    "marcos": MARCOS,
    "linhas": [{"id": "muralha", "ano": 1549.3, "desenha": 0.06, "sobe": 4, "cor": [196, 150, 100], "largura": 7}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro ssa", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
