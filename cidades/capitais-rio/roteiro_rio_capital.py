"""Ato 2 de "As capitais do Brasil": o RIO DE JANEIRO como capital (1763 → 1956). Gera cidades/capitais-rio/roteiro.json.
Foco: os prédios do poder (Paço, Cadeia Velha → Palácio Tiradentes, Senado, São Cristóvão, Itamaraty, Catete, Monroe, Theatro)
e, dentro deles, a IDEIA de levar a capital para o Planalto (1823 → 1956). O ato termina na lei da Novacap (19/9/1956, no Catete);
o ato 3 começa na primeira visita de JK ao cerrado (2/10/1956), para a linha do tempo não voltar.
assets/ e dados/chao.npy foram copiados de cidades/rio (não rodar extrai_*/prep_* aqui).
Uso: python3 cidades/capitais-rio/roteiro_rio_capital.py"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "capitais"))
from comum import *  # noqa

EV = carrega(AQUI)
# cartão-síntese do porquê de 1960 (fontes lidas na pesquisa: RESUMO.md, "O porquê da mudança para Brasília")
EV["porque-planalto-1956"] = {"id": "porque-planalto-1956", "titulo_curto_PT": "POR QUE O PLANALTO?", "numero_impacto": "3 MOTIVOS",
    "legenda": "Tirar a sede do litoral exposto, ocupar o interior e unir o país em volta de um centro",
    "detalhe": "Defesa, coesão do território e ocupação do Centro-Oeste: os argumentos vêm de Hipólito da Costa (1813) e da Missão Cruls (1892). JK somou o '50 anos em 5' e cumpriu a Constituição.",
    "local": {"lon": -43.1762278, "lat": -22.9258639}, "fontes": ["https://pt.wikipedia.org/wiki/Hist%C3%B3ria_de_Bras%C3%ADlia", "https://pt.wikipedia.org/wiki/Miss%C3%A3o_Cruls"]}
EXZ = 1.6
zc = Chao(AQUI)
cam = fazedor_cam(zc, EXZ)
bloco = fazedor_bloco(EV)

# ---------------------------------------------------------------- câmeras: olhando a fachada (bearing = rumo da fachada + 180)
C0 = cam(-43.30, -22.90, 11.2, 0, 0)
CIDADE = cam(-43.25, -22.92, 11.9, 40, -5)
BAIA = cam(-43.17, -22.90, 13.0, 50, -20)
PACO = cam(-43.1738, -22.9038, 18.2, 60, 143)
PACO_L = cam(-43.1735, -22.9030, 17.5, 56, 110)
PACO_B = cam(-43.1720, -22.9020, 15.6, 55, 190)
CADEIA = cam(-43.1732, -22.9035, 18.3, 60, 55)
CAMPO = cam(-43.1895, -22.9070, 16.0, 55, 60)
SENADO = cam(-43.1898, -22.9075, 18.2, 58, 250)
MUNI = cam(-43.30, -22.92, 11.6, 35, -5)
ITAM = cam(-43.1878, -22.9036, 18.3, 58, 160)
SCRIST = cam(-43.2258, -22.9080, 16.0, 52, 348)
CASTELO = cam(-43.1735, -22.9080, 16.0, 55, -20)
CATETE = cam(-43.1757, -22.9259, 18.5, 58, 85)
AVENIDA = cam(-43.1765, -22.9080, 15.9, 60, 340)
THEATRO = cam(-43.1764, -22.9095, 18.2, 58, 338)
MONROE = cam(-43.1755, -22.9131, 18.3, 58, 170)
FIM = cam(-43.20, -22.91, 12.6, 45, -30)

AMB = [250, 204, 21]
blocos = [
    {"id": "globo", "anos": [1763.55, 1763.55], "cam": [C0, C0], "dur": 9.5, "corte": True,
     "globo": {"raster": True, "uf": "RJ", "uf_de": 2500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -38.51, "lat": -12.97, "ls": 7.6}], [0.3, {"lon": -41.2, "lat": -17.8, "ls": 6.35}],
                          [0.65, {"lon": -43.25, "lat": -22.75, "ls": 8.6}], [1, {"lon": C0["lon"], "lat": C0["lat"], "ls": ls(C0["zoom"], C0["lat"])}]],
               "rotulos": [{"lon": -38.51, "lat": -12.97, "texto": "SALVADOR", "de": 300, "ate": 4500, "tam": 50, "ponto": True},
                           {"lon": -44.4, "lat": -18.6, "texto": "MINAS · OURO", "de": 400, "ate": 4000, "tam": 48},
                           {"lon": -43.20, "lat": -22.90, "texto": "RIO DE JANEIRO", "de": 4000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco("capital-1763", [1763.55, 1763.56, 1763.9], C0, PACO, 11.0, pulo=0.2, destaque=1, destaca=["marco:paco"], chega=0.3, cartao_de=0.3),
    bloco("corte-1808", [1763.9, 1808.18, 1808.3], PACO, BAIA, 10.0, pulo=1.6, destaque=2,
          frota={"de": [-43.13, -23.05], "para": [-43.170, -22.905], "n": 17, "r": 110, "espalha_km": 3, "cor": [30, 120, 60], "dura": 7,
                 "rotulo": "A frota da Corte", "sub": "1808 · de Lisboa"}),
    bloco("reino-unido-1815", [1808.3, 1815.96, 1816.1], BAIA, PACO_L, 8.5, pulo=0.8, destaque=2, destaca=["marco:paco", "marco:paco_alto"]),
    bloco("fico-1822", [1816.1, 1822.02, 1822.1], PACO_L, PACO, 8.0, pulo=0.6, destaque=1),
    bloco("imperio-1822", [1822.1, 1822.78, 1822.9], PACO, CAMPO, 8.5, pulo=0.3, destaque=1),
    bloco("constituinte-1823", [1822.9, 1823.34, 1823.38], CAMPO, CADEIA, 8.5, pulo=0.3, destaque=1, destaca=["marco:cadeia"]),
    bloco("brasilia-nome-1823", [1823.38, 1823.43, 1823.6], CADEIA, CADEIA, 10.0, pulo=0.2, destaque=2, destaca=["marco:cadeia"]),
    bloco("parlamento-1826", [1823.6, 1826.35, 1826.5], CADEIA, SENADO, 8.5, pulo=0.5, destaque=2, destaca=["marco:senado"]),
    bloco("municipio-neutro-1834", [1826.5, 1834.61, 1835], SENADO, MUNI, 8.5, pulo=0.6, destaque=2),
    bloco("republica-1889", [1835, 1889.87, 1889.88], MUNI, CAMPO, 9.0, pulo=1.6, destaque=1),
    bloco("itamaraty-1889", [1889.88, 1889.9, 1890.5], CAMPO, ITAM, 8.0, pulo=0.2, destaque=1, destaca=["marco:itamaraty"]),
    bloco("constituicao-1891", [1890.5, 1891.15, 1891.4], ITAM, SCRIST, 10.0, pulo=0.4, destaque=2, destaca=["marco:scristovao"]),
    bloco("cruls-1892", [1891.4, 1892.5, 1892.9], SCRIST, CASTELO, 10.0, pulo=0.4, destaque=2,
          rotulos=[{"lon": -43.1930, "lat": -22.8905, "texto": "↖ PLANALTO CENTRAL · RETÂNGULO CRULS", "z": 450, "tam": 38}]),
    bloco("catete-1897", [1892.9, 1897.15, 1897.4], CASTELO, CATETE, 8.5, pulo=0.6, destaque=1, destaca=["marco:catete"]),
    bloco("avenida-central-1904", [1897.4, 1904.2, 1904.6], CATETE, AVENIDA, 8.5, pulo=0.6, destaque=1),
    bloco("municipal-1909", [1904.6, 1909.53, 1909.7], AVENIDA, THEATRO, 8.5, pulo=0.6, destaque=1, destaca=["marco:theatro"]),
    bloco("pedra-fundamental-1922", [1909.7, 1922.05, 1922.3], THEATRO, CATETE, 10.0, pulo=1.2, destaque=1, destaca=["marco:catete"],
          rotulos=[{"lon": -43.1752, "lat": -22.9256, "texto": "↙ PLANALTO CENTRAL (PLANALTINA)", "z": 70, "tam": 38}]),
    bloco("monroe-1925", [1922.3, 1925, 1925.3], CATETE, MONROE, 8.5, pulo=0.6, destaque=1, destaca=["marco:monroe"]),
    bloco("tiradentes-1926", [1925.3, 1926.34, 1926.6], MONROE, CADEIA, 9.0, pulo=0.4, destaque=1, destaca=["marco:tiradentes"]),
    bloco("constituicao-1946", [1926.6, 1946.71, 1946.9], CADEIA, CADEIA, 10.0, pulo=1.4, destaque=2, destaca=["marco:tiradentes"]),
    bloco("vargas-1954", [1946.9, 1954.65, 1954.8], CADEIA, CATETE, 8.5, pulo=0.8, destaque=2, tom={"cor": "#3a3a4a", "forca": 0.3}),
    bloco("belcher-1955", [1954.8, 1955.3, 1955.6], CATETE, CATETE, 9.0, pulo=0.3, destaque=2,
          rotulos=[{"lon": -43.1752, "lat": -22.9256, "texto": "↙ SÍTIO CASTANHO · PLANALTO CENTRAL", "z": 70, "tam": 38}]),
    bloco("porque-planalto-1956", [1955.6, 1956.1, 1956.3], CATETE, CIDADE, 11.0, pulo=0.4, destaque=2, chega=0.3, cartao_de=0.3,
          rotulos=[{"lon": -43.31, "lat": -22.86, "texto": "↖ PLANALTO CENTRAL", "z": 700, "tam": 44}]),
    bloco("novacap-1956", [1956.3, 1956.72, 1956.74], CIDADE, FIM, 11.0, pulo=0.5, destaque=2, chega=0.6, destaca=["marco:catete"]),
]

IMGS = {"capital-1763": (0, "A baía e a cidade de São Sebastião, mapa de 1775"), "corte-1808": (1, "Desembarque de D. Leopoldina diante do Paço, 1817"),
        "imperio-1822": (2, "Coroação de D. Pedro I, 1822 (Debret)"), "brasilia-nome-1823": (3, "José Bonifácio de Andrada e Silva"),
        "fico-1822": (4, "O Largo do Paço e o Paço Imperial"), "constituicao-1891": (5, "O Palácio de São Cristóvão, c. 1862"),
        "republica-1889": (6, "A Proclamação da República, 1889 (Benedito Calixto)"), "cruls-1892": (7, "A Comissão Cruls no Planalto Central, 1894"),
        "catete-1897": (8, "O Palácio do Catete com as águias, 1895"), "avenida-central-1904": (9, "A Avenida Central recém-aberta, 1906"),
        "monroe-1925": (10, "O Palácio Monroe no fim da Avenida Central"), "tiradentes-1926": (11, "O Palácio Tiradentes recém-construído"),
        "novacap-1956": (12, "O Congresso em obra em Brasília, 1959")}
for b in blocos:
    if b["id"] in IMGS:
        i, leg = IMGS[b["id"]]
        b["imagem"] = imagem(AQUI, i, leg)
ROT = {"imperio-1822": ("CAMPO DE SANTANA", -43.188563, -22.906701), "republica-1889": ("CAMPO DE SANTANA", -43.188563, -22.906701),
       "avenida-central-1904": ("AVENIDA CENTRAL", -43.1775, -22.9047),
       "municipio-neutro-1834": ("MUNICÍPIO NEUTRO DA CORTE", -43.33, -22.90)}
for b in blocos:
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b.setdefault("rotulos", []).append({"lon": lo, "lat": la, "texto": nm, "z": round(zc(lo, la, 6) * EXZ + (500 if b["id"] == "municipio-neutro-1834" else 60), 1), "tam": 30})
ajusta_anos(blocos)
grava_marcas("rio", blocos)


def M(id_, tipo, lon, lat, rumo, ano, pronto=None, **kw):
    m = {"id": id_, "tipo": tipo, "lon": lon, "lat": lat, "rumo": rumo, "ano": ano, "z": round(zc(lon, lat, 1), 1), **kw}
    if pronto:
        m["pronto"] = pronto
    return m


EZ = 1.25   # marcos_ez
MARCOS = [
    # Paço (1743): casa senhorial de 2 pavimentos, telha em 4 águas, cantaria cinza; em 1808 ganha o corpo central de 3 andares na frente
    M("paco", "palacio", -43.1742333, -22.9035083, 323, 1700, larg=90.7, comp=33, andares=2, pe=6, platibanda=0, telhado_visivel=True, avanco=22,
      escadaria=False, parede="#EEEAE0", cor="#8E8A82", rotulo="Paço", sub="dos Vice-Reis · Real · Imperial", sempre=True),
    M("paco_alto", "sobrado", -43.1742333 + 0.00008, -22.9035083 - 0.00011, 323, 1808.25, larg=22, comp=12, andares=1, pe=5, cor="#8E8A82", sacadas=False),
    # Cadeia Velha (1640): sobrado de 3 pavimentos com platibanda; demolida em 1922 para o Palácio Tiradentes
    M("cadeia", "palacio", -43.173877, -22.90387, 235, 1700, larg=50, comp=25, andares=3, pe=5, platibanda=1.2, avanco=0, escadaria=False,
      parede="#D9D1C2", cor="#B8B0A2", ate=1922.2, rotulo="Cadeia Velha", sub="Constituinte de 1823", sempre_ate=True),
    M("tiradentes", "palacio", -43.173877, -22.90387, 235, 1922.4, 1926.34, larg=71, comp=37, andares=4, pe=6.5, platibanda=1.8, avanco=24,
      parede="#D6CBB6", cor="#CFC5B0", portico={"n": 6, "larg": 22, "alt": 16, "frontao": False}, estatuas_canto=True,
      cupula={"r": 9, "h": 12, "tambor": 4, "cor": "cinza", "estatua": True}, rotulo="Palácio Tiradentes", sub="Câmara · 1926"),
    M("senado", "palacio", -43.19057, -22.90713, 70, 1700, larg=48, comp=46, andares=2, pe=6, platibanda=1.0, telhado_visivel=True, avanco=0,
      parede="#EDE6D6", cor="#8F8477", rotulo="Senado do Império", sub="Palácio Conde dos Arcos · 1826", sempre=True),
    M("scristovao", "palacio", -43.22611, -22.90583, 168, 1700, larg=105, comp=74, andares=3, pe=6, platibanda=1.6, avanco=30,
      parede="#E9D9B8", cor="#F4F0E8", torres_canto={"larg": 12, "alt": 6}, estatuas_canto=True,
      rotulo="Palácio de São Cristóvão", sub="Constituinte de 1891", sempre=True),
    M("itamaraty", "palacio", -43.18806, -22.903056, 340, 1851, 1855, larg=56, comp=43, andares=2, pe=6.5, platibanda=1.4, avanco=18,
      parede="#E6B8B4", cor="#F1EEE8", rotulo="Palácio Itamaraty", sub="governo · 1889–1897"),
    M("catete", "palacio", -43.1762278, -22.9258639, 265, 1858, 1866, larg=33, comp=26, andares=3, pe=6, platibanda=1.4, avanco=0,
      parede="#C9C2B6", cor="#F2EFE8", estatuas_canto=True, rotulo="Palácio do Catete", sub="Presidência · 1897–1960"),
    M("theatro", "palacio", -43.17667, -22.90889, 158, 1905.3, 1909.5, larg=68, comp=84, andares=3, pe=7, platibanda=1.6, avanco=34,
      parede="#E8DFC9", cor="#C9A227", portico={"n": 8, "larg": 30, "alt": 14, "frontao": False},
      cupula={"r": 10, "h": 11, "tambor": 3, "cor": "verde", "cor2": "#C9A227", "estatua": True, "dy": 8}, torres_canto={"larg": 9, "alt": 5},
      rotulo="Theatro Municipal", sub="1909"),
    M("monroe", "palacio", -43.17545, -22.91245, 350, 1905.5, 1906.5, larg=46, comp=38, andares=2, pe=7.5, platibanda=1.8, avanco=16,
      parede="#F0ECE3", cor="#F4F1EA", portico={"n": 6, "larg": 18, "alt": 13, "frontao": False}, estatuas_canto=True,
      cupula={"r": 7.5, "h": 10, "tambor": 4, "cor": "bronze", "estatua": True}, rotulo="Palácio Monroe", sub="Senado · 1925–1960"),
]
# a Cadeia Velha existe desde antes do ato: aparece pronta no começo e só "desmonta" em 1922
for m in MARCOS:
    if m.pop("sempre_ate", False):
        m["sempre"] = True
    if m["id"] == "paco_alto":
        m["z"] = round(m["z"] + 12 * EZ / EXZ, 2)   # em cima do corpo de 2 pavimentos (12 m × exagero dos marcos)

roteiro = {
    "titulo": "As capitais do Brasil · ato 2: Rio de Janeiro",
    "exz": EXZ, "exb": 1.5, "marcos_ez": EZ, "predios_neutros": True, "voo_alto": True, "cartaoDireita": 660, "cartaoEsquerda": 500,
    "hud_de_bloco": "capital-1763",
    "linha": linha_completa(),
    "popRotulo": "habitantes no Rio",
    "longe": {"auto": True},
    "regimes": REGIMES,
    "marcos": MARCOS,
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro rio", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
