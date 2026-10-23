"""Ato 3 de "As capitais do Brasil": BRASÍLIA (1956 → hoje). Gera cidades/capitais-bsb/roteiro.json.
Motor: versão centro (centro/motor + marcos-capitais.js). Prédios do poder desenhados (predios.json da pesquisa + contornos do OSM).
Uso: python3 cidades/capitais-bsb/roteiro_bsb.py   (depois centro/scripts/gerar_cena.py com CIDADE=capitais-bsb)"""
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

# ---------------------------------------------------------------- câmeras (bearing 106 = olhando para leste pelo Eixo Monumental)
C0 = cam(-47.86, -15.75, 10.75, 0, 0)               # DF de cima (fim do globo)
DF = cam(-47.87, -15.79, 11.2, 35, -10)
PLANO = cam(-47.875, -15.792, 12.4, 45, -14)
PLANO_A = cam(-47.882, -15.793, 12.9, 40, 106)
CATET = cam(-47.9882, -15.9468, 17.6, 58, -20)
CLIVRE = cam(-47.966, -15.866, 14.0, 52, -25)
MZERO = cam(-47.8835, -15.7930, 15.8, 58, 106)
CRUZ = cam(-47.9140, -15.7840, 15.8, 55, 106)
ALV = cam(-47.8228, -15.7928, 17.4, 60, 90)
TAGUA = cam(-48.050, -15.833, 13.3, 50, -15)
ESPL = cam(-47.8712, -15.7972, 16.2, 62, 106)
CONG = cam(-47.8645, -15.7994, 17.2, 64, 106)
CONG_N = cam(-47.8638, -15.7990, 17.0, 60, 196)
LAGO = cam(-47.835, -15.795, 12.3, 48, -25)
CATED = cam(-47.8754, -15.7988, 17.7, 56, 160)
PRACA = cam(-47.8625, -15.8003, 17.0, 60, 286)
TORRE = cam(-47.8936, -15.7902, 16.3, 45, 106)
UNB = cam(-47.8664, -15.7620, 15.0, 55, -20)
CEIL = cam(-48.085, -15.822, 13.2, 50, -35)
PONTE = cam(-47.829, -15.835, 14.6, 58, 0)
FIM = cam(-47.86, -15.77, 11.4, 42, -10)
FIM2 = cam(-47.86, -15.77, 11.2, 30, -4)

AZUL_FRIO = {"cor": "#5a6a8a", "forca": 0.25}

blocos = [
    {"id": "globo", "anos": [1956.74, 1956.74], "cam": [C0, C0], "dur": 9.5, "corte": True,
     "globo": {"raster": True, "uf": "DF", "uf_de": 2500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -43.2, "lat": -22.9, "ls": 7.6}], [0.3, {"lon": -45.6, "lat": -19.0, "ls": 6.3}],
                          [0.65, {"lon": -47.7, "lat": -15.9, "ls": 8.4}], [1, {"lon": C0["lon"], "lat": C0["lat"], "ls": ls(C0["zoom"], C0["lat"])}]],
               "rotulos": [{"lon": -43.20, "lat": -22.90, "texto": "RIO DE JANEIRO", "de": 300, "ate": 4500, "tam": 50, "ponto": True},
                           {"lon": -47.3, "lat": -14.6, "texto": "PLANALTO CENTRAL", "de": 600, "ate": 6000, "tam": 56},
                           {"lon": -47.88, "lat": -15.79, "texto": "BRASÍLIA", "de": 5000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco("jk-primeira-visita-1956", [1956.74, 1956.75, 1956.8], C0, DF, 9.5, pulo=0.2, destaque=2, pulso_r=1500),
    bloco("catetinho-1956", [1956.8, 1956.86, 1956.95], DF, CATET, 9.0, pulo=0.3, destaque=2, destaca=["marco:catetinho"]),
    bloco("cidade-livre-1956", [1956.95, 1956.97, 1957.05], CATET, CLIVRE, 8.0, pulo=0.2, destaque=1),
    bloco("plano-piloto-1957", [1957.05, 1957.2, 1957.3], CLIVRE, PLANO, 11.0, pulo=0.5, destaque=2, chega=0.3,
          destaca=["linha:eixo_l", "linha:eixo_o", "linha:eixo_n", "linha:eixo_s"]),
    bloco("primeira-missa-1957", [1957.3, 1957.337, 1957.45], PLANO, CRUZ, 8.5, pulo=0.2, destaque=2),
    bloco("corte-rodoviaria-1957", [1957.45, 1957.5, 1957.9], CRUZ, MZERO, 8.5, pulo=0.2, destaque=2),
    bloco("alvorada-1958", [1957.9, 1958.49, 1958.6], MZERO, ALV, 10.0, pulo=0.8, destaque=2, destaca=["marco:alvorada"]),
    bloco("taguatinga-1958", [1958.6, 1958.65, 1958.95], ALV, TAGUA, 8.5, pulo=0.3, destaque=1, numero="1958"),
    bloco("censo-experimental-1959", [1958.95, 1959.37, 1959.45], TAGUA, PLANO_A, 8.5, pulo=0.4, destaque=2),
    bloco("congresso-obra-1959", [1959.45, 1959.5, 1959.65], PLANO_A, CONG, 10.0, pulo=0.2, destaque=2, destaca=["marco:congresso"]),
    bloco("lago-paranoa-1959", [1959.65, 1959.7, 1959.85], CONG, LAGO, 10.0, pulo=0.2, destaque=1),
    bloco("esplanada-1959", [1959.85, 1959.9, 1960.1], LAGO, ESPL, 9.5, pulo=0.2, destaque=2),
    bloco("catedral-estrutura-1960", [1960.1, 1960.29, 1960.295], ESPL, CATED, 9.0, pulo=0.3, destaque=2, destaca=["marco:catedral"]),
    bloco("inauguracao-1960", [1960.295, 1960.3, 1960.6], CATED, PRACA, 12.0, pulo=0.2, destaque=2,
          destaca=["marco:congresso", "marco:planalto"]),
    bloco("censo-1960", [1960.6, 1960.67, 1960.95], PRACA, DF, 8.5, pulo=0.2, destaque=2),
    bloco("unb-1962", [1960.95, 1962.3, 1962.5], DF, UNB, 8.0, pulo=0.8, destaque=2),
    bloco("golpe-1964", [1962.5, 1964.25, 1964.5], UNB, CONG_N, 9.0, pulo=0.8, destaque=2, tom=AZUL_FRIO),
    bloco("torre-tv-1967", [1964.5, 1967.5, 1967.7], CONG_N, TORRE, 9.0, pulo=1.0, destaque=2, destaca=["marco:torre"]),
    bloco("catedral-itamaraty-1970", [1967.7, 1970.3, 1970.5], TORRE, CATED, 10.0, pulo=1.0, destaque=2, destaca=["marco:vitral", "marco:itamaraty"]),
    bloco("ceilandia-1971", [1970.5, 1971.24, 1971.5], CATED, CEIL, 9.0, pulo=0.5, destaque=1),
    bloco("diretas-1984", [1971.5, 1984.32, 1984.5], CEIL, CONG, 9.0, pulo=1.4, destaque=2, tom=AZUL_FRIO),
    bloco("unesco-1987", [1984.5, 1987.93, 1987.97], CONG, PLANO, 9.0, pulo=1.0, destaque=2,
          destaca=["linha:eixo_l", "linha:eixo_o", "linha:eixo_n", "linha:eixo_s"]),
    bloco("constituicao-1988", [1987.97, 1988.76, 1988.9], PLANO, PRACA, 9.0, pulo=0.6, destaque=2, destaca=["marco:congresso"]),
    bloco("ponte-jk-2002", [1988.9, 2002.95, 2002.99], PRACA, PONTE, 9.5, pulo=1.4, destaque=3, destaca=["linha:ponte_jk"]),
    bloco("censo-2022", [2003, 2022.6, 2024], PONTE, FIM, 10.0, pulo=1.5, destaque=2),
    {"id": "fecho", "anos": [2024, 2024], "cam": [FIM, FIM2], "dur": 14.0},
]

# ---------------------------------------------------------------- imagens de época (índices de dados/pesquisa/imagens.json)
IMGS = {"catetinho-1956": (0, "O Catetinho, o 'palácio de tábuas', em 1956"),
        "cidade-livre-1956": (3, "Acampamento e galpões no cerrado, 1957"),
        "primeira-missa-1957": (2, "A primeira missa de Brasília, 3/5/1957"),
        "plano-piloto-1957": (4, "Os eixos riscados no cerrado, foto aérea de 1958"),
        "alvorada-1958": (5, "O Alvorada recém-concluído, 1958"),
        "censo-experimental-1959": (1, "Candangos no refeitório da obra"),
        "congresso-obra-1959": (7, "As torres do Congresso em estrutura, 1959"),
        "lago-paranoa-1959": (9, "O Lago Paranoá enchendo, com troncos na água"),
        "esplanada-1959": (8, "Os blocos dos ministérios em obra"),
        "inauguracao-1960": (12, "JK hasteia a bandeira na inauguração, 21/4/1960"),
        "catedral-itamaraty-1970": (13, "A Catedral pronta, 1970")}
for b in blocos:
    if b["id"] in IMGS:
        i, leg = IMGS[b["id"]]
        b["imagem"] = imagem(AQUI, i, leg)
    if b["id"] == "fecho":
        b["galeria"] = {"fica": True, "titulo": "Imagens <b>da época</b>", "itens": [f"assets/epoca/e{i:02d}.jpg" for i in (0, 2, 4, 5, 7, 9, 12, 13)],
                        "creditos": "Arquivo Nacional · domínio público (Wikimedia Commons)"}
ROT = {"jk-primeira-visita-1956": ("FAZENDA DO GAMA", -47.988333, -15.9475), "cidade-livre-1956": ("CIDADE LIVRE (NÚCLEO BANDEIRANTE)", -47.967778, -15.87),
       "primeira-missa-1957": ("PRAÇA DO CRUZEIRO", -47.913081, -15.784358), "corte-rodoviaria-1957": ("MARCO ZERO (RODOVIÁRIA)", -47.882611, -15.793389),
       "taguatinga-1958": ("TAGUATINGA", -48.056389, -15.833333), "lago-paranoa-1959": ("LAGO PARANOÁ", -47.84, -15.78),
       "unb-1962": ("UNB", -47.866389, -15.761389), "ceilandia-1971": ("CEILÂNDIA", -48.1083, -15.819167),
       "plano-piloto-1957": ("EIXO MONUMENTAL", -47.905, -15.787)}
for b in blocos:
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b["rotulos"] = [{"lon": lo, "lat": la, "texto": nm, "z": round(zc(lo, la) * EXZ + 60, 1), "tam": 30}]
ajusta_anos(blocos)
grava_marcas("bsb", blocos)

# ---------------------------------------------------------------- prédios do poder (marcos-capitais.js); rumo = para onde olha a fachada
def M(id_, tipo, lon, lat, rumo, ano, pronto=None, **kw):
    m = {"id": id_, "tipo": tipo, "lon": lon, "lat": lat, "rumo": rumo, "ano": ano, "z": round(zc(lon, lat, 2), 1), **kw}
    if pronto:
        m["pronto"] = pronto
    return m


MIN_N = [(-47.874635, -15.79435), (-47.873813, -15.794615), (-47.872954, -15.794797), (-47.872156, -15.795093), (-47.871358, -15.795481),
         (-47.870559, -15.795755), (-47.869677, -15.795869), (-47.868849, -15.796191), (-47.868075, -15.796489), (-47.867316, -15.796737)]
MIN_S = [(-47.873473, -15.798697), (-47.872584, -15.79892), (-47.871736, -15.799163), (-47.87091, -15.799433), (-47.870183, -15.799881),
         (-47.869284, -15.800015), (-47.868455, -15.800242)]
MARCOS = [
    M("catetinho", "catetinho", -47.988333, -15.9475, 180, 1956.84, larg=34, comp=10, rotulo="Catetinho", sub="1956 · 10 dias"),
    M("alvorada", "palacio_colunas", -47.822175, -15.792772, 270, 1957.25, 1958.49, larg=110, comp=31, pisos=2, pe=3.6, colunas="alvorada", col_n=11,
      rotulo="Palácio da Alvorada", sub="1958"),
    M("congresso", "congresso", -47.864167, -15.799722, 286, 1958.2, 1960.25, larg=160, comp=65, rotulo="Congresso Nacional", sub="cúpula, cuia e 2 torres de 28 andares"),
    M("planalto", "palacio_colunas", -47.860677, -15.799138, 196, 1958.52, 1960.25, larg=120, comp=60, pisos=4, pe=4.4, colunas="planalto", rampa=True,
      rotulo="Palácio do Planalto", sub="1960"),
    M("stf", "palacio_colunas", -47.861925, -15.802236, 16, 1958.6, 1960.25, larg=66, comp=40, pisos=3, pe=4.2, colunas="stf", rotulo="STF", sub="1960"),
    M("catedral", "catedral_bsb", -47.875557, -15.798332, 286, 1958.7, 1960.29, raio=30, alt=42, larg=60, comp=60, vitral=False, campanario=False,
      rotulo="Catedral", sub="16 colunas"),
    M("vitral", "catedral_bsb", -47.875557, -15.798332, 286, 1969.8, 1970.3, raio=30, alt=42, larg=60, comp=60, so_vitral=True, rotulo="Catedral", sub="vitrais · 1970"),
    M("itamaraty", "itamaraty", -47.867295, -15.80078, 16, 1963, 1970.3, larg=84, comp=84, rotulo="Itamaraty", sub="1970 · 14 arcos por face"),
    M("torre", "torre_tv", -47.892977, -15.790499, 106, 1965, 1967.5, larg=45, comp=41, rotulo="Torre de TV", sub="1967"),
    M("teatro", "teatro_piramide", -47.880344, -15.79196, 106, 1960.6, 1966, larg=136, comp=70, alt=24.5),
] + [M(f"min_n{i}", "ministerio", lo, la, 288, 1958.6 + i * 0.12, 1959.9 + i * 0.03, larg=104, comp=18) for i, (lo, la) in enumerate(MIN_N)] \
  + [M(f"min_s{i}", "ministerio", lo, la, 288, 1958.7 + i * 0.12, 1960.0 + i * 0.03, larg=104, comp=18) for i, (lo, la) in enumerate(MIN_S)]

# lago: polígono do OSM (sem as ilhas), enche de 12/9/1959 até a inauguração
lago = json.load(open(f"{AQUI}/dados/lago.json"))

roteiro = {
    "titulo": "As capitais do Brasil · ato 3: Brasília",
    "exz": EXZ, "exb": 1.5, "marcos_ez": 1.25, "predios_neutros": True, "cartaoDireita": 660, "cartaoEsquerda": 500,
    "hud_de_bloco": "jk-primeira-visita-1956",
    "linha": linha_completa(),
    "popRotulo": "habitantes no DF",
    "fim": {"titulo": "As 3 capitais do Brasil", "sub": "Salvador 1549 · Rio de Janeiro 1763 · Brasília 1960", "marca": "INEMA<span>.CLUB</span>",
            "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"auto": True},
    "regimes": REGIMES,
    "marcos": MARCOS,
    "aguas": [{"id": "paranoa", "ano0": 1959.7, "ano1": 1959.83, "poligonos": lago["poligonos"]}],
    "linhas": [{"id": "eixo_l", "ano": 1957.2, "desenha": 0.04, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_o", "ano": 1957.2, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_n", "ano": 1957.24, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_s", "ano": 1957.24, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "ponte_costa", "ano": 1976, "desenha": 0.5, "sobe": 8, "cor": [236, 236, 236], "largura": 6},
               {"id": "ponte_bragueto", "ano": 1960, "desenha": 0.3, "sobe": 6, "cor": [236, 236, 236], "largura": 5},
               {"id": "ponte_jk", "ano": 2002.95, "desenha": 0.035, "sobe": 12, "cor": [236, 236, 236], "largura": 8, "torres": False}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro bsb", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
