"""A CONSTRUÇÃO DE BRASÍLIA (1810 → 1960): o que existia no planalto, o planejamento (Cruls, pedra de 1922, Sítio Castanho),
de onde a obra era comandada (Rio, Catetinho, sede da Novacap, acampamentos) e a obra até a inauguração.
Motor: versão centro (centro/motor + marcos-capitais.js). Dados do DF copiados de cidades/capitais-bsb.
Uso: python3 cidades/brasilia-obra/roteiro_obra.py; CIDADE=brasilia-obra .venv/bin/python -I cidades/capitais/scripts/limpa.py;
     CIDADE=brasilia-obra .venv/bin/python -I centro/scripts/gerar_cena.py"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "capitais"))
from comum import carrega, fonte, titulo, Chao, fazedor_cam, fazedor_bloco, ls, ajusta_anos, imagem  # noqa

EV = carrega(AQUI)
NOV = json.load(open(f"{AQUI}/dados/pesquisa/eventos_novos.json"))
EV.update({x["id"]: x for x in NOV["eventos"] + NOV["reserva"]})
RIO = {x["id"]: x for x in json.load(open(f"{AQUI}/../capitais-rio/dados/pesquisa/eventos.json"))["eventos"]}
PLANALTO = {"nome": "Planalto Central", "lat": -15.7939, "lon": -47.8828, "coord_fonte": "ponto do Plano Piloto (o ato aconteceu no Rio)"}
for k in ("constituicao-1946", "novacap-1956"):   # atos assinados no Rio: o cartão fica no planalto, com seta para o Rio
    EV[k] = {**RIO[k], "local": PLANALTO}
# cartões montados a partir de fatos já lidos (fontes dos eventos de origem)
EV["comando-1957"] = {"titulo_curto_PT": "DE ONDE SE MANDAVA", "numero_impacto": "3 LUGARES",
                      "legenda": "Rio: as leis e o governo · Catetinho: as visitas de JK · Novacap: o canteiro, todo dia",
                      "detalhe": "JK ia ao Catetinho e voltava ao Rio no mesmo dia. No barracão da Candangolândia, Israel Pinheiro e os diretores Bernardo Sayão, Ernesto Silva e Íris Meinberg tocavam a obra.",
                      "local": {"lon": -47.9498, "lat": -15.8539}, "fontes": EV["novacap-sede-1956"]["fontes"] + EV["lei-3273-1957"]["fontes"]}
EV["fazenda-bananal-1955"]["local"] = {"lon": -47.8828, "lat": -15.7939}

EXZ = 1.6
zc = Chao(AQUI)
cam = fazedor_cam(zc, EXZ)
bloco = fazedor_bloco(EV)

# ---------------------------------------------------------------- câmeras (Planaltina fica a 8 km da borda norte do mapa: olhar para o sul)
C0 = cam(-47.80, -15.74, 12.4, 0, 0)                 # DF de cima (fim do globo)
DF = cam(-47.86, -15.77, 12.4, 30, -10)
DFTOP = cam(-47.86, -15.75, 12.4, 0, 0)
PLAN_I = cam(-47.66222, -15.62233, 18.2, 55, 160)     # igreja de São Sebastião
PLAN = cam(-47.6618, -15.6185, 15.6, 50, 170)
PLAN_L = cam(-47.664, -15.612, 14.6, 48, 175)
VALE = cam(-47.86, -15.73, 13.2, 48, 160)            # vale do Paranoá, visto do norte
PEDRA = cam(-47.679135, -15.68555, 19.0, 45, 180)
OESTE = cam(-47.98, -15.78, 12.9, 45, 260)          # olhando para Brazlândia
CAST = cam(-47.905, -15.790, 13.6, 50, -20)          # Sítio Castanho / Cruzeiro
PLANO = cam(-47.875, -15.792, 12.6, 45, -14)
GAMA = cam(-47.978, -15.912, 14.2, 50, -20)
CATET = cam(-47.9883, -15.9472, 18.7, 55, -20)
NOVA = cam(-47.9499, -15.8543, 18.4, 56, -30)        # sede da Novacap
COMANDO = cam(-47.9500, -15.8546, 17.4, 52, -30)
CLIVRE = cam(-47.966, -15.866, 14.6, 52, -25)
VPLAN = cam(-47.8508, -15.7938, 17.2, 56, 0)
CRUZ = cam(-47.9140, -15.7840, 15.8, 55, 106)
MZERO = cam(-47.8835, -15.7930, 15.8, 58, 106)
BARR = cam(-47.7900, -15.8030, 15.6, 55, 40)
AMAURY = cam(-47.858, -15.775, 14.6, 52, 120)
HJKO = cam(-47.9596, -15.8608, 18.2, 56, -30)
ALV = cam(-47.8226, -15.7928, 18.3, 56, 90)
FATIMA = cam(-47.9038, -15.8145, 17.6, 56, -20)
SUDOESTE = cam(-47.95, -15.85, 13.0, 50, 230)       # olhando para Anápolis
TAGUA = cam(-48.0564, -15.8333, 13.6, 50, -15)
PLANO_A = cam(-47.882, -15.793, 12.9, 40, 106)
CONG = cam(-47.8645, -15.7994, 17.2, 64, 106)
LAGO = cam(-47.835, -15.795, 12.3, 48, -25)
ESPL = cam(-47.8712, -15.7972, 16.2, 62, 106)
PRACA = cam(-47.8625, -15.8003, 17.0, 60, 286)
FIM = cam(-47.8700, -15.7968, 15.4, 55, 106)    # fecho sobre a Esplanada: a cidade inaugurada fica na tela
FIM2 = cam(-47.8735, -15.7958, 15.1, 50, 106)

# rios do vale antes do lago (braço sul: Gama e Riacho Fundo; braço norte: Torto e Bananal; saída: Paranoá) — onde hoje é o lago
RIOS = [{"lon": lo, "lat": la, "texto": t, "z": round(zc(lo, la) + 150, 1), "tam": 28} for t, lo, la in
        [("RIACHO FUNDO · GAMA", -47.885, -15.838), ("TORTO · BANANAL", -47.850, -15.745), ("RIO PARANOÁ", -47.795, -15.800)]]
AZUL_FRIO = {"cor": "#5a6a8a", "forca": 0.25}
VERMELHO = {"cor": "#a15050", "forca": 0.3}
CRULS = [[-48.854167, -15.333333], [-47.354167, -15.333333], [-47.354167, -16.143056], [-48.854167, -16.143056]]


LADO = {"↘": (1440, 600), "↙": (60, 560), "←": (60, 520), "↖": (60, 420), "↗": (1440, 420)}


def seta(texto, sub=None):   # lugar fora do mapa: etiqueta fixa na tela, no lado da direção da seta
    x, y = LADO[texto[0]]
    return {"setas_tela": [{"texto": texto, "sub": sub, "x": x, "y": y}]}   # o motor multiplica z pelo exagero


# v4 (26/10/2026, Nei: "perdeu muito tempo indo para lá e para cá"): um ato por região, vista média, cartões trocando com
# a câmera quase parada (chega 0,3); só 4 viagens longas (Planaltina → Plano → Gama/Novacap → Plano). Final: revelação do Plano.
PLAN_I = cam(-47.66222, -15.62233, 17.6, 55, 160)
PEDRA_W = cam(-47.672, -15.668, 14.4, 48, 185)        # Planaltina e o morro da pedra no mesmo quadro
PEDRA = cam(-47.679135, -15.68555, 17.6, 45, 180)
PLANO_W = cam(-47.885, -15.790, 13.0, 45, -14)
SUL_W = cam(-47.965, -15.895, 13.6, 50, 170)          # Gama, Catetinho, Candangolândia e Cidade Livre juntos
GAMA_W = cam(-47.986, -15.940, 14.6, 38, 165)        # Catetinho fica a 300 m da borda sul do mapa: vista de perto ou de longe, nunca média
CATET = cam(-47.9883, -15.9472, 18.0, 55, 165)
NOVA = cam(-47.9499, -15.8543, 17.4, 56, 175)
CLIVRE = cam(-47.966, -15.874, 15.4, 50, 178)
COMANDO_W = cam(-47.969, -15.900, 13.15, 30, 112)        # Novacap e Catetinho juntos no quadro, quase de cima
VPLAN = cam(-47.8508, -15.7938, 16.4, 56, 0)
CRUZ = cam(-47.9100, -15.7900, 15.2, 55, 106)
PLANO_A = cam(-47.885, -15.795, 13.4, 42, 106)
FATIMA = cam(-47.9038, -15.8145, 16.8, 56, -20)
ALV = cam(-47.8226, -15.7928, 17.2, 56, 90)
CONG = cam(-47.8645, -15.7994, 16.6, 62, 106)
REVELA = cam(-47.865, -15.790, 12.55, 18, 106)          # o Plano de cima: eixos em cruz, Asa Sul e o lago inteiro
REVELA2 = cam(-47.880, -15.800, 12.3, 22, 112)          # epílogo: o DF de hoje, com as satélites
REVELA3 = cam(-47.880, -15.800, 12.2, 20, 116)

blocos = [
    {"id": "capa", "anos": [1810, 1810], "cam": [C0, C0], "dur": 5.0, "capa": {"imagem": "assets/capa_ilust.jpg", "segura": 5.0, "some": 0.8}},
    {"id": "globo", "anos": [1810, 1810], "cam": [C0, C0], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -43.2, "lat": -22.9, "ls": 7.6}], [0.3, {"lon": -45.6, "lat": -19.0, "ls": 6.3}],
                          [0.65, {"lon": -47.7, "lat": -15.8, "ls": 8.6}], [1, {"lon": C0["lon"], "lat": C0["lat"], "ls": ls(C0["zoom"], C0["lat"])}]],
               "rotulos": [{"lon": -43.20, "lat": -22.90, "texto": "RIO DE JANEIRO", "de": 300, "ate": 4500, "tam": 50, "ponto": True},
                           {"lon": -47.3, "lat": -14.6, "texto": "PLANALTO CENTRAL", "de": 1500, "ate": 9000, "tam": 56},
                           {"lon": -47.662, "lat": -15.622, "texto": "MESTRE D'ARMAS", "de": 6000, "ate": 2e6, "tam": 56, "ponto": True}]}},
    # ------------------------------------------------ 1. o que existia e o planejamento (Planaltina)
    bloco("igreja-sao-sebastiao-planaltina", [1810, 1810.5, 1810.9], C0, PLAN_I, 9.0, pulo=0.3, destaque=3,
          legenda="Erguida em 1810, a capela de São Sebastião, em Planaltina, é a igreja mais antiga do atual Distrito Federal", destaca=["marco:igreja_ss"], pulso_r=900),
    bloco("mestre-darmas-1859", [1810.9, 1859.63, 1859.9], PLAN_I, PLAN, 7.5, pulo=0.9, destaque=2, chega=0.3,
          detalhe="A data de fundação adotada é 19/8/1859. Junto à capela de São Sebastião, um ferreiro, mestre em consertar armas, deu nome à vila. Já havia cemitério em 1812."),
    bloco("cruls-mestre-darmas-1892", [1859.9, 1892.72, 1892.8], PLAN, PLAN_L, 7.5, pulo=0.9, destaque=2, chega=0.3),
    {**bloco("quadrilatero-cruls-1892", [1892.8, 1892.85, 1892.95], PLAN_L, PEDRA_W, 11.0, pulo=0.2, destaque=2, pulso=False),
     "globo": {"raster": True, "entra": 1.0, "some": 1.3, "br_ate": 9000, "uf": None,
               "chaves": [[0, {"lon": PLAN_L["lon"], "lat": PLAN_L["lat"], "ls": ls(14.3, PLAN_L["lat"])}],
                          [0.32, {"lon": -48.104, "lat": -15.738, "ls": 10.55}], [0.72, {"lon": -48.104, "lat": -15.738, "ls": 10.55}],
                          [1, {"lon": PEDRA_W["lon"], "lat": PEDRA_W["lat"], "ls": ls(PEDRA_W["zoom"], PEDRA_W["lat"])}]],
               "poligonos": [{"coords": CRULS, "de": 9000, "ate": 52000, "cor": "#FACC15", "preench": "rgba(250,204,21,.12)", "largura": 5}],
               "rotulos": [{"lon": -46.98, "lat": -15.74, "texto": "160 × 90 KM", "de": 14000, "ate": 52000, "tam": 44, "cor": "#FACC15"},
                           {"lon": -47.662, "lat": -15.622, "texto": "MESTRE D'ARMAS", "de": 14000, "ate": 90000, "tam": 34, "ponto": True},
                           {"lon": -47.86, "lat": -15.85, "texto": "ESTE MAPA", "de": 14000, "ate": 90000, "tam": 34}]}},
    bloco("pedra-fundamental-planalto-1922", [1892.95, 1922.68, 1922.8], PEDRA_W, PEDRA, 8.5, pulo=0.9, destaque=2, chega=0.3, destaca=["marco:pedra"]),
    # ------------------------------------------------ 2. a escolha do sítio (uma viagem: Planaltina → Plano)
    bloco("constituicao-1946", [1922.8, 1946.71, 1946.8], PEDRA, PLANO_W, 8.5, pulo=0.8, destaque=1, **seta("↘ RIO DE JANEIRO", "a capital do país")),
    bloco("sitio-castanho-1955", [1946.8, 1955.29, 1955.35], PLANO_W, CAST, 8.5, pulo=0.8, destaque=2, pulso_r=2500, chega=0.3),
    # ------------------------------------------------ 3. o comando da obra (Gama, Candangolândia, Cidade Livre: tudo a ~10 km)
    bloco("novacap-1956", [1955.35, 1956.72, 1956.74], CAST, SUL_W, 8.5, pulo=0.4, destaque=2, **seta("↖ RIO DE JANEIRO", "JK assina a lei no Catete")),
    bloco("jk-primeira-visita-1956", [1956.74, 1956.75, 1956.79], SUL_W, GAMA_W, 7.5, pulo=0.2, destaque=2, chega=0.3),
    bloco("catetinho-1956", [1956.79, 1956.86, 1956.88], GAMA_W, CATET, 8.0, pulo=0.2, destaque=2, chega=0.3, destaca=["marco:catetinho"]),
    bloco("novacap-sede-1956", [1956.88, 1956.885, 1956.9], CATET, NOVA, 8.5, pulo=0.2, destaque=2, destaca=["marco:novacap"]),
    bloco("cidade-livre-1956", [1956.9, 1956.97, 1957.0], NOVA, CLIVRE, 7.5, pulo=0.2, destaque=1, chega=0.3),
    bloco("comando-1957", [1957.0, 1957.02, 1957.05], CLIVRE, COMANDO_W, 12.5, pulo=0.2, destaque=2, numero="3 LUGARES", pulso=False, chega=0.25,
          setas_tela=[{"texto": "↗ RIO DE JANEIRO", "sub": "as leis e o governo · 930 km", "x": 1440, "y": 660}]),
    # ------------------------------------------------ 4. a obra, no Plano (vista média, poucos metros de câmera)
    bloco("vila-planalto-1957", [1957.05, 1957.09, 1957.15], COMANDO_W, VPLAN, 9.0, pulo=0.2, destaque=2, destaca=["marco:vp1", "marco:vp2", "marco:vp3"]),
    bloco("plano-piloto-1957", [1957.15, 1957.2, 1957.3], VPLAN, PLANO, 9.5, pulo=0.2, destaque=2, chega=0.3,
          destaca=["linha:eixo_l", "linha:eixo_o", "linha:eixo_n", "linha:eixo_s"]),
    bloco("primeira-missa-1957", [1957.3, 1957.337, 1957.4], PLANO, CRUZ, 7.5, pulo=0.2, destaque=2, chega=0.3),
    bloco("lei-3273-1957", [1957.4, 1957.75, 1958.1], CRUZ, PLANO_A, 7.5, pulo=0.3, destaque=2, numero="1/10/1957", chega=0.3, **seta("↘ RIO DE JANEIRO", "JK sanciona a lei")),
    bloco("contagem-1958", [1958.1, 1958.2, 1958.2], PLANO_A, PLANO_A, 7.0, pulo=0.3, destaque=1, numero="28.804", titulo="A CONTAGEM DE 1958"),
    bloco("fatima-1958", [1958.2, 1958.488, 1958.489], PLANO_A, FATIMA, 8.0, pulo=0.3, destaque=2, chega=0.3, destaca=["marco:fatima"]),
    bloco("alvorada-1958", [1958.489, 1958.494, 1958.6], FATIMA, ALV, 9.0, pulo=0.2, destaque=2,
          legenda="O 1º palácio de concreto da nova capital: a residência do presidente, à beira do futuro lago",
          detalhe="Barra de vidro de 110 × 30,75 m cercada pelas colunas que só tocam o chão.", destaca=["marco:alvorada"]),
    bloco("massacre-geb-1959", [1958.6, 1959.1, 1959.3], ALV, VPLAN, 8.5, pulo=0.3, destaque=2, tom=VERMELHO, chega=0.3),
    bloco("censo-experimental-1959", [1959.3, 1959.37, 1959.3701], VPLAN, PLANO_A, 7.5, pulo=0.2, destaque=2, chega=0.3),
    bloco("congresso-obra-1959", [1959.3701, 1959.5, 1959.65], PLANO_A, CONG, 8.5, pulo=0.2, destaque=2, chega=0.3, destaca=["marco:congresso"]),
    bloco("vila-amaury-1957", [1959.65, 1959.66, 1959.69], CONG, AMAURY, 7.5, pulo=0.2, destaque=2, numero="1957–1959", chega=0.3,
          legenda="A Vila Amaury, de operários com família, cresceu na beira do Bananal: chegou a cerca de 16 mil"),
    bloco("lago-paranoa-1959", [1959.69, 1959.7, 1959.76], AMAURY, LAGO, 9.5, pulo=0.2, destaque=1, chega=0.3),
    bloco("esplanada-1959", [1959.85, 1959.9, 1960.1], LAGO, ESPL, 8.5, pulo=0.2, destaque=2, chega=0.3),
    # ------------------------------------------------ 5. ápice: a inauguração e a cidade inteira de cima
    bloco("inauguracao-1960", [1960.1, 1960.3, 1960.6], ESPL, PRACA, 12.0, pulo=0.3, destaque=2, numero="41 MESES", chega=0.3,
          destaca=["marco:congresso", "marco:planalto", "marco:stf", "marco:catedral"],
          detalhe="A data é o Dia de Tiradentes. Inauguram juntos o Congresso, o Planalto, o STF e a Esplanada; a Catedral ainda era só a estrutura das colunas.",),
    bloco("censo-1960", [1960.6, 1960.67, 1960.6701], PRACA, REVELA, 11.0, pulo=0.2, destaque=2, chega=0.55,
          rotulos=[{"lon": lo, "lat": la, "texto": t, "z": round(zc(lo, la) + 150, 1), "tam": 40} for t, lo, la in
                   [("ASA SUL", -47.897, -15.818), ("EIXO MONUMENTAL", -47.893, -15.776), ("PRAÇA DOS TRÊS PODERES", -47.861, -15.801),
                    ("LAGO PARANOÁ", -47.835, -15.770)]]),
    # epílogo: a cruz riscada em 1960 vira a cidade de hoje (os prédios nascem no ano do bairro até 2022)
    bloco("censo-2022", [1960.6701, 2022.6, 2022.6], REVELA, REVELA2, 11.0, pulo=3.5, destaque=2, chega=0.5),
    {"id": "fecho", "anos": [2022.6, 2022.6], "cam": [REVELA2, REVELA3], "dur": 12.0},
]

# ---------------------------------------------------------------- imagens de época
IMG_N = {x["arquivo"]: x for x in (lambda L: L["imagens"] if isinstance(L, dict) else L)(json.load(open(f"{AQUI}/dados/pesquisa/imagens_novas.json")))}


def img_n(n, legenda):
    x = IMG_N[f"n{n:02d}.jpg"]; a = x["autor"].split("(")[0].split(" — ")[0].split(",")[0].split("/")[0].strip().rstrip(",;")
    lic = "domínio público" if "úblico" in x.get("licenca", "") else x.get("licenca", "").split("(")[0].strip()
    return {"src": f"assets/epoca/n{n:02d}.jpg", "legenda": legenda, "credito": f"{a} · {x['ano']} · {lic} (Wikimedia Commons)"}


IMGS = {"igreja-sao-sebastiao-planaltina": img_n(4, "A Igreja de São Sebastião hoje (foto de 2015)"),
        "cruls-mestre-darmas-1892": img_n(0, "Os membros da Missão Cruls"),
        "quadrilatero-cruls-1892": img_n(2, "O retângulo demarcado, mapa de 1894"),
        "acampamento-cruls-1894": img_n(1, "Um acampamento da Comissão Exploradora"),
        "pedra-fundamental-planalto-1922": img_n(3, "O obelisco de 1922 hoje (foto de 2015)"),
        "novacap-sede-1956": img_n(5, "Um barracão de madeira da Novacap, 1958"),
        "catetinho-1956": imagem(AQUI, 0, "O Catetinho, o 'palácio de tábuas', em 1956"),
        "cidade-livre-1956": img_n(12, "A primeira igreja da Cidade Livre, 1957"),
        "vila-planalto-1957": imagem(AQUI, 3, "Casas e galpões de acampamento no cerrado, 1957"),
        "plano-piloto-1957": imagem(AQUI, 4, "Os eixos riscados no cerrado, foto aérea de 1958"),
        "primeira-missa-1957": imagem(AQUI, 2, "A primeira missa de Brasília, 1957"),
        "barragem-paranoa-obra-1957": img_n(7, "A crista da barragem pronta, 1960"),
        "hjko-1957": img_n(13, "Os galpões do Hospital JK hoje (foto de 2017)"),
        "lei-3273-1957": img_n(14, "JK depois de sancionar a lei da data, 1957"),
        "alvorada-1958": imagem(AQUI, 5, "O Alvorada recém-concluído, 1958"),
        "fatima-1958": img_n(9, "A Igrejinha recém-pronta, 1958"),
        "rota-anapolis": img_n(11, "A estação de Anápolis, ponta dos trilhos, 1958"),
        "censo-experimental-1959": imagem(AQUI, 1, "Candangos no refeitório da obra"),
        "congresso-obra-1959": imagem(AQUI, 7, "As torres do Congresso em estrutura, 1959"),
        "lago-paranoa-1959": img_n(8, "O lago formado e a barragem ao fundo, 1960"),
        "esplanada-1959": imagem(AQUI, 8, "Os blocos dos ministérios em obra"),
        "inauguracao-1960": imagem(AQUI, 12, "JK hasteia a bandeira na inauguração, 21/4/1960")}
for b in blocos:
    if b["id"] in IMGS:
        b["imagem"] = IMGS[b["id"]]
    if b["id"] == "fecho":
        b["galeria"] = {"fica": True, "titulo": "Imagens <b>da época</b>",
                        "itens": [f"assets/epoca/n{i:02d}.jpg" for i in (0, 2, 5, 11)] + [f"assets/epoca/e{i:02d}.jpg" for i in (0, 4, 7, 12)],
                        "creditos": "Fotos e mapas em domínio público (Arquivo Nacional; Missão Cruls, 1894) · Wikimedia Commons"}
ROT = {"igreja-sao-sebastiao-planaltina": ("SÃO SEBASTIÃO · 1810", -47.66222, -15.62333),
       "mestre-darmas-1859": ("MESTRE D'ARMAS (PLANALTINA)", -47.6615, -15.6200),
       "acampamento-cruls-1894": ("VALE DO PARANOÁ · ONDE GLAZIOU QUER O LAGO", -47.85, -15.79),
       "sitio-castanho-1955": ("SÍTIO CASTANHO · 1.172 M (HOJE O CRUZEIRO)", -47.915365, -15.783374),
       "fazenda-bananal-1955": ("FAZENDA BANANAL", -47.88, -15.79),
       "jk-primeira-visita-1956": ("FAZENDA DO GAMA", -47.988333, -15.9475),
       "cidade-livre-1956": ("CIDADE LIVRE", -47.967778, -15.87),
       "vila-planalto-1957": ("ACAMPAMENTOS · VILA PLANALTO", -47.8503, -15.7927),
       "primeira-missa-1957": ("PRAÇA DO CRUZEIRO", -47.913081, -15.784358),
       "barragem-paranoa-obra-1957": ("BARRAGEM DO PARANOÁ", -47.784798, -15.799752),
       "vila-amaury-1957": ("VILA AMAURY", -47.856, -15.781),
       "taguatinga-1958": ("TAGUATINGA", -48.056389, -15.833333),
       "lago-paranoa-1959": ("LAGO PARANOÁ", -47.84, -15.78),
       "plano-piloto-1957": ("EIXO MONUMENTAL", -47.905, -15.787)}
for b in blocos:
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b.setdefault("rotulos", []).append({"lon": lo, "lat": la, "texto": nm, "z": round(zc(lo, la) + 150, 1), "tam": 30})
# o cartão "de onde se mandava" aponta os dois lugares no mapa
for b in blocos:
    if b["id"] == "comando-1957":
        b["chamadas"] = [{"lon": -47.949839, "lat": -15.853872, "z": round(zc(-47.949839, -15.853872) + 15, 1), "texto": "Sede da Novacap", "sub": "o canteiro, todo dia"},
                         {"lon": -47.988333, "lat": -15.9475, "z": round(zc(-47.988333, -15.9475) + 15, 1), "texto": "Catetinho", "sub": "as visitas de JK · 11 km"}]
ajusta_anos(blocos)
for b in blocos:   # contagens e censos: o contador fica parado no número do cartão
    if b["id"] in ("contagem-1958", "censo-experimental-1959", "censo-1960"):
        b["anos"][2] = b["anos"][1]


# ---------------------------------------------------------------- prédios desenhados; rumo = para onde olha a fachada
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
    M("igreja_ss", "igreja", -47.66222, -15.62333, 180, 1810.45, 1810.7, larg=9, comp=20, pe=6.5, torres=0, cor="ocre",
      rotulo="Igreja de São Sebastião", sub="1810 · a mais antiga do DF"),
    {**M("pedra", "obelisco", -47.679135, -15.685365, 180, 1922.66, 1922.72, alt=3.75, base=2.2, rotulo="Pedra Fundamental", sub="7/9/1922 · obelisco de 3,75 m"), "z": 1023.5},   # topo do morro: a mediana enterra o obelisco na encosta
    M("catetinho", "catetinho", -47.988333, -15.9475, 180, 1956.84, larg=34, comp=10, rotulo="Catetinho", sub="1956 · 10 dias"),
    M("novacap", "galpao", -47.949839, -15.853872, 160, 1956.79, 1956.84, larg=46, comp=10, n=3, vao=17, rotulo="Sede da Novacap", sub="1956–1959 · o QG da obra"),
    M("hjko", "galpao", -47.959553, -15.860222, 160, 1957.505, 1957.6, larg=30, comp=8, n=6, vao=13, madeira="#B98A5E",
      rotulo="Hospital JK", sub="1957 · 23 prédios de madeira"),
    M("vp1", "galpao", -47.8512, -15.7918, 90, 1957.07, 1957.12, larg=40, comp=9, n=4, vao=15),
    M("vp2", "galpao", -47.8488, -15.7934, 90, 1957.08, 1957.13, larg=36, comp=9, n=3, vao=15),
    M("vp3", "galpao", -47.8525, -15.7948, 90, 1957.09, 1957.14, larg=34, comp=9, n=3, vao=15, rotulo="Acampamentos", sub="22 construtoras"),
    M("fatima", "igrejinha", -47.903762, -15.813973, 200, 1958.2, 1958.49, lado=22, pe=4.5, alt=19, larg=24, comp=24,
      rotulo="Igrejinha de Fátima", sub="1958 · 100 dias"),
    M("alvorada", "palacio_colunas", -47.822175, -15.792772, 270, 1957.25, 1958.49, larg=110, comp=31, pisos=2, pe=3.6, colunas="alvorada", col_n=11,
      rotulo="Palácio da Alvorada", sub="1958"),
    M("congresso", "congresso", -47.864167, -15.799722, 286, 1958.2, 1960.25, larg=160, comp=65, rotulo="Congresso Nacional", sub="cúpula, cuia e 2 torres de 28 andares"),
    M("planalto", "palacio_colunas", -47.860677, -15.799138, 196, 1958.52, 1960.25, larg=120, comp=60, pisos=4, pe=4.4, colunas="planalto", rampa=True,
      rotulo="Palácio do Planalto", sub="1960"),
    M("stf", "palacio_colunas", -47.861925, -15.802236, 16, 1958.6, 1960.25, larg=66, comp=40, pisos=3, pe=4.2, colunas="stf", rotulo="STF", sub="1960"),
    M("catedral", "catedral_bsb", -47.875557, -15.798332, 286, 1958.7, 1960.29, raio=30, alt=42, larg=60, comp=60, vitral=False, campanario=False, espelho=False,
      rotulo="Catedral", sub="em 1960, só a estrutura"),
] + [M(f"min_n{i}", "ministerio", lo, la, 288, 1958.6 + i * 0.12, 1959.9 + i * 0.03, larg=104, comp=18) for i, (lo, la) in enumerate(MIN_N)] \
  + [M(f"min_s{i}", "ministerio", lo, la, 288, 1958.7 + i * 0.12, 1960.0 + i * 0.03, larg=104, comp=18) for i, (lo, la) in enumerate(MIN_S)]

REG = [{"ano": 1800, "nome": "Capitania de Goiás", "bandeira": "portugal"},
       {"ano": 1815.96, "nome": "Reino Unido · Goiás", "bandeira": "reino"},
       {"ano": 1822.78, "nome": "Império · Província de Goiás", "bandeira": "imperio"},
       {"ano": 1870, "nome": "Império · Província de Goiás", "bandeira": "imperio2"},
       {"ano": 1889.87, "nome": "República · Estado de Goiás", "bandeira": "republica"},
       {"ano": 1956.72, "nome": "Goiás · canteiro da Novacap", "bandeira": "republica"},
       {"ano": 1960.3, "nome": "Distrito Federal", "bandeira": "brasil"}]

lago = json.load(open(f"{AQUI}/dados/lago.json"))
roteiro = {
    "titulo": "A construção de Brasília",
    "exz": EXZ, "exb": 1.5, "marcos_ez": 1.25, "predios_neutros": True, "voo_alto": True, "cartaoDireita": 660, "cartaoEsquerda": 500,
    "hud_de_bloco": "igreja-sao-sebastiao-planaltina",
    "linha": {"de": 1800, "ate": 2023},
    "popRotulo": "habitantes na área do DF",
    "fim": {"titulo": "A construção de Brasília", "sub": "1892 Cruls demarca → 1956 Novacap → 41 meses de obra → 21/4/1960 → 2,8 milhões em 2022",
            "marca": "INEMA<span>.CLUB</span>", "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"auto": True},
    "regimes": REG,
    "marcos": MARCOS,
    "aguas": [{"id": "paranoa", "ano0": 1959.7, "ano1": 1959.95, "poligonos": lago["poligonos"]}],
    "linhas": [{"id": "eixo_l", "ano": 1957.2, "desenha": 0.04, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_o", "ano": 1957.2, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_n", "ano": 1957.24, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "eixo_s", "ano": 1957.24, "desenha": 0.05, "sobe": 3, "cor": [236, 232, 220], "largura": 6},
               {"id": "ponte_bragueto", "ano": 1960, "desenha": 0.3, "sobe": 6, "cor": [236, 236, 236], "largura": 5}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro obra", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
