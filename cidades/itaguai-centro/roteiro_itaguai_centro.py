"""Monta cidades/itaguai-centro/roteiro.json — versão CENTRO de Itaguaí (centro histórico, prédios históricos, cidade futura).
Não confundir com cidades/itaguai (história do município). Motor: centro/motor (cópia), cena: centro/scripts/gerar_cena.py.
Vídeo SEM narração (fase 1): o cartão conta a história. Padrão de cidades/itaguai/roteiro_itaguai.py.
Uso: python3 cidades/itaguai-centro/roteiro_itaguai_centro.py"""
import json
import math
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
PQ = json.load(open(f"{AQUI}/dados/pesquisa/eventos_centro.json"))
EV = {e["id"]: e for e in PQ["eventos"]}
ABREV = {"PM": "Prefeitura de Itaguaí", "PMimg": "Prefeitura de Itaguaí", "PM200": "Prefeitura de Itaguaí", "COL": "Coletânea de Nossas Memórias (SMEC, 2010)",
         "INEPAC": "INEPAC", "IBGE509": "IBGE", "DTB": "IBGE", "EFB": "Estações Ferroviárias do Brasil", "CAM": "Câmara de Itaguaí",
         "JA2019": "Jornal Atual", "JA2023": "Jornal Atual", "GRAHAM": "Wikimedia Commons", "PTDIO": "Wikipédia", "IPEA": "Mapa das OSCs (Ipea)"}


def fonte(e):
    nomes = []
    for u in e["fontes"]:
        n = ABREV.get(u, u)
        if n not in nomes:
            nomes.append(n)
    return "; ".join(nomes[:3])


def cam(lon, lat, zoom, pitch=58, bearing=-20):
    return {"lon": lon, "lat": lat, "zoom": zoom, "pitch": pitch, "bearing": bearing}


def ls(z, lat):
    return round(math.log(6371000 * 2 ** z / (156543 * math.cos(math.radians(lat)))), 3)


MZ = (-43.7792, -22.8676)                         # Matriz (aprox. ±50 m, pesquisa)
GERAL = cam(-43.7780, -22.8690, 16.2, 52, -15)    # o centro inteiro
CENTRO = cam(-43.7782, -22.8685, 16.4, 58, -25)
MORRO = cam(-43.7790, -22.8680, 17.6, 62, -60)    # Matriz no alto do morro, de lado
MORRO2 = cam(-43.7790, -22.8678, 17.9, 64, 30)
ADRO = cam(-43.7789, -22.8679, 18.4, 64, -100)
BOCAIUVA = cam(-43.7777, -22.8643, 17.9, 62, -35)  # chafariz, casarões, paço
PACO = cam(-43.7781, -22.8665, 17.7, 62, 10)
PRACAS = cam(-43.7783, -22.8700, 17.4, 60, -10)
ESTACAO = cam(-43.7775, -22.8746, 17.9, 62, -40)
ESTACAO2 = cam(-43.7776, -22.8744, 18.3, 64, 50)
CASAPAI = cam(-43.7724, -22.8737, 17.6, 62, -20)
ALTO = cam(-43.7780, -22.8690, 16.0, 50, -5)
FUTURO = cam(-43.7782, -22.8688, 16.0, 60, -35)
FUTURO2 = cam(-43.7779, -22.8695, 16.6, 64, 25)
FIM = cam(-43.7780, -22.8690, 16.2, 52, -10)


def titulo(e, n=1):
    pal = e["titulo"].capitalize().split()
    k = len(pal) - n
    return " ".join(pal[:k]) + " <b>" + " ".join(pal[k:]) + "</b>"


BASTIDOR = re.compile(r"não ach|Não ach|sem documento primário|provável erro|fontes divergem|sem foto|A fonte só diz")


def limpa(txt):   # tira da tela as frases de bastidor (a dúvida fica no RESUMO.md)
    txt = re.sub(r"\s*\((?:data|ano) não achad[ao]\)", "", txt)
    return " ".join(f for f in re.split(r"(?<=[.])\s+", txt) if not BASTIDOR.search(f)).strip()


def bloco(eid, anos, c0, c1, dur=9.0, **kw):
    e = EV[eid]
    kw.setdefault("chega", 0.3)
    loc = e.get("coord")
    b = {"id": eid, "anos": anos, "cam": [c0, c1], "dur": dur,
         "cartao": {"titulo": kw.pop("titulo", titulo(e, kw.pop("destaque", 1))), "numero": kw.pop("numero", str(int(anos[-2] if len(anos) == 3 else anos[0]))),
                    "legenda": kw.pop("legenda", e["legenda"]), "detalhe": limpa(kw.pop("detalhe", e.get("detalhe", ""))),
                    "fonte": kw.pop("fonte", fonte(e)), "de": kw.pop("cartao_de", 0.26), **({"local": loc} if loc else {})}}
    if not loc:
        b["pulso"] = False
    b.update(kw)
    return b


import numpy as np
CH = np.load(f"{AQUI}/dados/chao.npy"); CFG = json.load(open(f"{AQUI}/config.json")); BW, BS, BE, BN = CFG["bbox"]


def zc(lon, lat):   # chão (m) na grade do relevo
    c = int(np.clip((lon - BW) / (BE - BW) * CH.shape[1], 0, CH.shape[1] - 1)); r = int(np.clip((BN - lat) / (BN - BS) * CH.shape[0], 0, CH.shape[0] - 1))
    return round(float(CH[r, c]), 2)


# PRÉDIOS HISTÓRICOS modelados (centro/motor/marcos.js). rumo = para onde olha a fachada (graus, 0 = norte, 90 = leste).
# Medidas: estimativas do modelador tiradas das fotos (sem fonte métrica — RESUMO.md). Ano = quando aparece; "ate" = quando some.
MARCOS = [
    {"id": "matriz", "tipo": "igreja", "lon": MZ[0], "lat": MZ[1], "rumo": 90, "rumo_fixo": 90, "larg": 13, "comp": 30, "torres": 1, "torre_lado": "direita", "coroa": "cupula",
     "cor": "azul", "ano": 1718, "pronto": 1729, "rotulo": "Igreja Matriz", "sub": "1729 · tombada pelo INEPAC", "alt_rotulo": 26},
    {"id": "colegio", "tipo": "claustro", "lon": -43.77968, "lat": -22.86735, "rumo": 90, "larg": 28, "comp": 28, "cor": "azul",
     "ano": 1720, "pronto": 1729, "ate": 1961.45, "rotulo": "Colégio jesuíta", "sub": "1729 · demolido em 1961", "alt_rotulo": 14},
    {"id": "candeeiro", "tipo": "casa", "lon": -43.7774, "lat": -22.8644, "rumo": 240, "raio_limpa": 22, "larg": 14, "comp": 10, "cor": "vinho", "ano": 1841, "rotulo": "Casa do Candeeiro", "sub": "casa térrea colonial", "alt_rotulo": 10},
    {"id": "chafariz", "tipo": "chafariz", "lon": -43.7778, "lat": -22.8640, "rumo": 240, "raio_limpa": 12, "larg": 3.5, "comp": 3.5, "ano": 1847, "rotulo": "Chafariz", "sub": "1847 · Estrada Real", "alt_rotulo": 7},
    {"id": "paco", "tipo": "sobrado", "lon": -43.77815, "lat": -22.8663, "rumo": 60, "larg": 16, "comp": 12, "cor": "verde", "ano": 1880, "rotulo": "Paço da Câmara", "sub": "1880 · local aproximado", "alt_rotulo": 15},
    {"id": "estacao", "tipo": "estacao_castelo", "lon": -43.777518, "lat": -22.874347, "rumo": 30, "larg": 26, "comp": 10, "plataforma": True, "ano": 1910, "rotulo": "Estação-castelo", "sub": "1910 · hoje Casa de Cultura", "alt_rotulo": 16},
    {"id": "coreto", "tipo": "coreto", "lon": -43.7789, "lat": -22.8677, "rumo": 90, "rumo_fixo": 90, "raio": 4.2, "raio_limpa": 20, "ano": 1943, "rotulo": "Coreto", "sub": "1943 · adro da Matriz", "alt_rotulo": 9},
    {"id": "patronato", "tipo": "moderno", "lon": -43.77968, "lat": -22.86735, "rumo": 90, "larg": 26, "comp": 14, "andares": 3, "estatua": True, "ano": 1962, "pronto": 1968, "rotulo": "Patronato São José", "sub": "prédio de 1968", "alt_rotulo": 16},
    {"id": "catedral", "tipo": "catedral_moderna", "lon": -43.778562, "lat": -22.869189, "rumo": 90, "larg": 22, "comp": 30, "ano": 1985, "rotulo": "Catedral nova", "sub": "Rua Coronel Freitas", "alt_rotulo": 22},
    {"id": "casapai", "tipo": "casarao", "lon": -43.77224, "lat": -22.87337, "rumo": 0, "larg": 18, "comp": 13, "raio_limpa": 32, "cor": "verde", "ano": 2007, "rotulo": "Instituto Casa do Pai", "sub": "2007 · Monte Serrat", "alt_rotulo": 11},
]
from shapely.geometry import LineString, Point
KL = 111320 * math.cos(math.radians(MZ[1]))
RUAS = [LineString([((x - MZ[0]) * KL, (y - MZ[1]) * 111320) for x, y in f["geometry"]["coordinates"]])
        for f in json.load(open(f"{AQUI}/dados/brutos/ruas_todas.geojson"))["features"]
        if f["properties"]["hw"] in ("primary", "secondary", "tertiary", "residential", "unclassified", "living_street", "pedestrian")]
for m in MARCOS:
    m["z"] = zc(m["lon"], m["lat"])
    if m.get("rumo_fixo") is None:   # fachada virada para a rua mais próxima
        p = Point((m["lon"] - MZ[0]) * KL, (m["lat"] - MZ[1]) * 111320)
        r = min(RUAS, key=lambda l: l.distance(p)); q = r.interpolate(r.project(p))
        m["rumo"] = round(math.degrees(math.atan2(q.x - p.x, q.y - p.y)) % 360)
MK = {m["id"]: m for m in MARCOS}


def cm(mid, zoom=19.0, pitch=52, gira=0, dz=0.0):
    """câmera de frente para a fachada do marco (bearing = rumo − 180), girada `gira` graus."""
    m = MK[mid]
    return cam(m["lon"], m["lat"], zoom + dz, pitch, ((m["rumo"] - 180 + gira + 180) % 360) - 180)


MORRO = cm("matriz", 18.6, 50, -35)
MORRO2 = cm("matriz", 19.1, 54, 30)
ADRO = cm("coreto", 19.2, 50, 40)
BOCAIUVA = cm("chafariz", 19.4, 52, 20)
CANDEEIRO = cm("candeeiro", 19.2, 52, -25)
PACO = cm("paco", 19.1, 52, 15)
PRACAS = cam(-43.7783, -22.8700, 18.0, 52, -10)
ESTACAO = cm("estacao", 18.9, 52, -20)
ESTACAO2 = cm("estacao", 19.3, 56, 35)
CATEDRAL = cm("catedral", 18.9, 52, 15)
PATRONATO = cm("patronato", 18.9, 52, -30)
CASAPAI = cm("casapai", 19.4, 56, 20)
FUTURO = cam(-43.7774, -22.8736, 18.5, 60, -35)
FUTURO2 = cam(-43.7766, -22.8706, 18.6, 60, 25)
FUT = json.load(open(f"{AQUI}/futuro_auto.json")) if os.path.exists(f"{AQUI}/futuro_auto.json") else {"elementos": [], "arvores": []}

C0 = cam(-43.7780, -22.8690, 16.0, 0, 0)
blocos = [
    {"id": "capa", "anos": [1680, 1680], "cam": [C0, C0], "dur": 5.5,
     "capa": {"kicker": "Itaguaí · Rio de Janeiro", "titulo": "O <b>centro</b> de Itaguaí", "sub": "A Matriz, os casarões, a estação-castelo e a cidade que pode vir", "segura": 5.5, "some": 0.8}},
    {"id": "globo", "anos": [1680, 1680], "cam": [C0, C0], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "uf": "RJ", "uf_de": 1500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -30, "lat": -6, "ls": 5.95}], [0.3, {"lon": -42, "lat": -16, "ls": 6.6}],
                          [0.62, {"lon": -43.6, "lat": -22.6, "ls": 8.8}], [1, {"lon": -43.7780, "lat": -22.8690, "ls": ls(16.0, -22.869)}]],
               "rotulos": [{"lon": -51, "lat": -11, "texto": "BRASIL", "de": 380, "ate": 3500, "tam": 84},
                           {"lon": -42.6, "lat": -22.15, "texto": "RIO DE JANEIRO", "de": 2600, "ate": 40000, "tam": 64},
                           {"lon": -43.778, "lat": -22.845, "texto": "ITAGUAÍ", "de": 30000, "ate": 3e5, "tam": 72, "ponto": True},
                           {"lon": -43.778, "lat": -22.862, "texto": "CENTRO", "de": 2.5e5, "ate": 2e7, "tam": 64}]}},
    bloco("capela-1688", [1680, 1688, 1689], C0, GERAL, 9.0, pulo=0.8, numero="1688",
          detalhe="A 1ª igreja ficava fora do centro de hoje, perto do mar ou ao norte do rio Itaguaí."),
    bloco("obra-1718", [1689, 1718, 1719], GERAL, MORRO, 9.0, pulo=1.0, destaque=2, numero="1718", destaca=["marco:matriz"]),
    bloco("matriz-1729", [1719, 1729, 1730], MORRO, MORRO2, 10.0, pulo=1.0, titulo="A Matriz fica <b>pronta</b>", destaca=["marco:matriz"]),
    bloco("expulsao-1759", [1730, 1759, 1760], MORRO2, cm("colegio", 18.9, 52, 25), 9.0, pulo=1.0, destaca=["marco:colegio"], tom={"cor": "#8a6a6a", "forca": 0.22}),
    bloco("freguesia-1795", [1760, 1795, 1796], ADRO, CENTRO, 8.5, pulo=1.0, destaca=["marco:matriz"]),
    bloco("vila-1818", [1796, 1818.5, 1819], CENTRO, MORRO, 9.0, pulo=1.0, destaca=["marco:matriz"]),
    bloco("aclamacao-1822", [1819, 1822.55, 1822.66], MORRO, ADRO, 9.0, pulo=0.8, titulo="D. Pedro <b>no adro</b>", destaque=2),
    bloco("graham-1823", [1822.66, 1823, 1823.5], ADRO, MORRO2, 9.5, pulo=0.3, titulo="O desenho de <b>Maria Graham</b>", destaque=2),
    bloco("porto-1841", [1823.5, 1841.2, 1842], MORRO2, CANDEEIRO, 9.5, pulo=1.2, numero="36 → 132", titulo="Porto Real e <b>132 casas</b>", destaque=2,
          destaca=["marco:candeeiro"]),
    bloco("chafariz-1847", [1842, 1847, 1848], CENTRO, BOCAIUVA, 9.0, pulo=0.6, titulo="O <b>chafariz</b>", destaca=["marco:chafariz"]),
    bloco("caridade-1858", [1848, 1858.8, 1859], BOCAIUVA, CENTRO, 8.5, pulo=0.6, titulo="Casa de <b>Caridade</b>"),
    bloco("quintino-casa-1873", [1859, 1873, 1874], CENTRO, BOCAIUVA, 9.0, pulo=0.8, titulo="O sobrado de <b>Quintino</b>",
          detalhe="Sobrado de 2 andares e 11 janelas, com balcão de ferro. A tradição o liga a Quintino Bocaiúva e à Guarda do Imperador."),
    bloco("biblioteca-1880", [1874, 1880.9, 1881], BOCAIUVA, PACO, 9.0, pulo=0.6, titulo="A casa <b>de leitura</b>", destaque=2, destaca=["marco:paco"]),
    bloco("cidade-1892", [1881, 1892.4, 1893], PACO, CENTRO, 8.5, pulo=0.8, titulo="Vira <b>cidade</b>",
          detalhe="Decreto estadual 1-A, de 3 de junho de 1892. Com o fim do café, as febres e a perda de terras, o município encolhe: de 17 mil para menos de 13 mil moradores."),
    bloco("estacao-1910", [1893, 1910.87, 1911], CENTRO, ESTACAO, 10.0, pulo=1.2, titulo="A estação-<b>castelo</b>", destaca=["marco:estacao", "linha:trem"]),
    bloco("coreto-1943", [1911, 1943, 1944], ESTACAO, ADRO, 9.0, pulo=1.2, titulo="O <b>coreto</b>", destaca=["marco:coreto"]),
    bloco("patronato-1953", [1944, 1953.5, 1954], ADRO, MORRO, 9.0, pulo=0.6, titulo="Patronato <b>São José</b>", destaque=2, destaca=["marco:colegio"]),
    bloco("pracas-anos50", [1954, 1955, 1956], MORRO, PRACAS, 9.0, pulo=0.3,
          chamadas=[{"lon": -43.77868, "lat": -22.86989, "z": 3, "texto": "Praça Vicente Cicarino", "sub": "antiga Praça 5 de Julho"},
                    {"lon": -43.777913, "lat": -22.870063, "z": 3, "texto": "Praça Barão de Tefé", "sub": "anos 1950"}], numero="ANOS 1950", titulo="As praças <b>novas</b>",
          detalhe="Praça Barão de Teffé e Praça 5 de Julho (hoje Vicente Cicarino), no pé do morro da Matriz."),
    bloco("colegio-demolido-1961", [1956, 1961, 1962], PRACAS, PATRONATO, 9.5, pulo=0.6, titulo="O colégio vem <b>abaixo</b>", destaque=2,
          destaca=["marco:colegio", "marco:patronato"], tom={"cor": "#6a5a5a", "forca": 0.22}),
    bloco("relogio-1967", [1962, 1967, 1968], MORRO2, cam(-43.7796, -22.8676, 19.3, 50, 60), 8.5, pulo=0.6, titulo="O relógio <b>de sol</b>", destaque=2,
          chamadas=[{"lon": -43.7796, "lat": -22.8676, "z": 3, "texto": "Relógio de sol", "sub": "1967 · diante do cemitério"}]),
    bloco("se-1980", [1968, 1980, 1980.3], ADRO, MORRO, 9.0, pulo=1.0, titulo="A Matriz vira <b>Sé</b>", destaca=["marco:matriz"]),
    bloco("trem-fim-1980", [1980.3, 1980.6, 1981], MORRO, ESTACAO, 9.0, pulo=0.3, titulo="O último <b>trem</b>", destaca=["marco:estacao"],
          tom={"cor": "#5a5a6a", "forca": 0.2}),
    bloco("casa-cultura-2006", [1981, 2006.1, 2006.3], ESTACAO, ESTACAO2, 9.5, pulo=1.4, titulo="Casa de <b>Cultura</b>", destaca=["marco:estacao"]),
    bloco("tombamento-2006", [2006.3, 2006.4, 2006.6], ESTACAO2, MORRO2, 9.0, pulo=0.3, titulo="Matriz <b>tombada</b>", destaca=["marco:matriz"]),
    {"id": "casa-do-pai-2007", "anos": [2006.6, 2007.45, 2008], "pulo": 0.4, "cam": [MORRO2, CASAPAI], "dur": 9.0, "destaca": ["marco:casapai"],
     "cartao": {"numero": "2007", "titulo": "Instituto <b>Casa do Pai</b>",
                "legenda": "Associação social fundada em 11 de junho de 2007 no Monte Serrat, a 600 m da Matriz",
                "detalhe": "Não é prédio histórico: é uma obra social do bairro, na Rua Prefeito José Maria de Brito, no Monte Serrat.",
                "fonte": "Mapa das OSCs (Ipea); site do Instituto", "local": [-43.77224, -22.87337]}},
    bloco("fachadas-2019", [2008, 2019, 2020], CASAPAI, BOCAIUVA, 9.0, pulo=1.0, titulo="Fachadas <b>pintadas</b>", destaca=["marco:chafariz"]),
    bloco("quintino-interdita-2023", [2020, 2023.4, 2024], BOCAIUVA, cam(-43.7776, -22.8650, 18.4, 55, -20), 9.0, pulo=0.6, titulo="A casa de Quintino <b>cai</b>", destaque=2,
          tom={"cor": "#6a4a4a", "forca": 0.25}),
    {"id": "hoje", "anos": [2024, 2025], "cam": [CENTRO, ALTO], "dur": 9.0,
     "cartao": {"numero": "116.841", "titulo": "Itaguaí <b>hoje</b>", "legenda": "Habitantes do município no Censo 2022; o centro cabe num raio de 700 m em volta da Matriz",
                "detalhe": "No mapa, cada prédio do OpenStreetMap e da Microsoft nasce no ano estimado do bairro; os marcos históricos são desenhos a partir de fotos, sem medidas oficiais.",
                "fonte": "IBGE, Censo 2022; OpenStreetMap; Microsoft Building Footprints", "local": list(MZ)}, "pulso": False},
    {"id": "futuro", "anos": [2025, 2050, 2050], "pulo": 1.5, "cam": [ALTO, FUTURO2], "dur": 16.0, "chega": 0.25,
     "futuro": {"de": 0.05, "nasce": 3.0, "atraso": 0.6, "fica_ate_fim": True, "elementos": FUT["elementos"]},
     "cartao": {"numero": "2050", "titulo": "Como <b>poderia ser</b>", "legenda": "Uma visão imaginada, não é projeto oficial: o centro com sombra, trem e casarões vivos",
                "detalhe": "Árvores nas ruas, telhados verdes e painéis solares, um VLT até a estação-castelo e a Matriz restaurada. Oficial hoje é o porto: terminal ITG02 e a ampliação do Tecar.",
                "fonte": "visão INEMA (imaginação); planos do porto: Jornal de Brasília, Datamar News", "local": list(MZ)}, "pulso": False},
    {"id": "fecho", "anos": [2050, 2050], "cam": [FUTURO2, FUTURO], "dur": 14.0},
]
ROT = {"capela-1688": None, "caridade-1858": None,
       "relogio-1967": ("RELÓGIO DE SOL", -43.7796, -22.8676), 
       "aclamacao-1822": ("ADRO DA MATRIZ", -43.77903, -22.86762)}
EPD = "assets/epoca"
IMG = {"graham-1823": {"src": f"{EPD}/graham_1823.jpg", "legenda": "A vila de Itaguaí por Maria Graham, 1823", "credito": "Maria Graham · 1823 · domínio público (Wikimedia Commons)"},
       "vila-1818": {"src": f"{EPD}/graham_1823.jpg", "legenda": "Igreja e colégio no alto, 1823", "credito": "Maria Graham · 1823 · domínio público (Wikimedia Commons)"},
       "cidade-1892": {"src": f"{EPD}/carta_1870.jpg", "legenda": "Carta náutica da Baía de Sepetiba, 1870", "credito": "Almirantado britânico · 1870 · domínio público (Wikimedia Commons)"},
       "estacao-1910": {"src": f"{EPD}/planta_efcb_1890.jpg", "legenda": "Planta da Estrada de Ferro Central, 1890", "credito": "Arquivo Nacional · 1890 · domínio público (Wikimedia Commons)"},
       "casa-cultura-2006": {"src": f"{EPD}/castelo_2021.jpg", "legenda": "A estação-castelo, hoje Casa de Cultura (2021)", "credito": "Almanaque Lusofonista · 2021 · domínio público (Wikimedia Commons)"},
       "se-1980": {"src": f"{EPD}/catedral_2017.jpg", "legenda": "A catedral nova, Rua Coronel Freitas (2017)", "credito": "Hierarchicus · 2017 · CC BY-SA 4.0 (Wikimedia Commons)"}}
for b in blocos:
    if b["id"] in IMG:
        b["imagem"] = IMG[b["id"]]
    if b["id"] in ROT and ROT[b["id"]]:
        nm, lo, la = ROT[b["id"]]
        b["rotulos"] = [{"lon": lo, "lat": la, "texto": nm, "z": 14, "tam": 28}]
    if b["id"] == "fecho":
        b["galeria"] = {"fica": True, "titulo": "O centro de Itaguaí · <b>imagens</b>",
                        "itens": [f"{EPD}/{x}" for x in ("graham_1823.jpg", "carta_1870.jpg", "planta_efcb_1890.jpg", "castelo_2021.jpg", "catedral_2017.jpg")],
                        "creditos": "Maria Graham (1823), Almirantado britânico (1870), Arquivo Nacional (1890), Almanaque Lusofonista (2021), Hierarchicus (2017, CC BY-SA 4.0) · via Wikimedia Commons"}

# câmera mira a altura do chão (position z no viewState), senão prédio em morro sai do quadro
for b in blocos:
    for c in b["cam"]:
        c["z"] = round(zc(c["lon"], c["lat"]) * 1.6, 2)
    for c in b.get("chamadas", []):
        c["z"] = round(zc(c["lon"], c["lat"]) + c.get("z", 3), 2)
# RUAS vetoriais (nítidas de perto): calçada + asfalto, todas do recorte; cada uma nasce com as casas em volta
_PM = np.load(f"{AQUI}/dados/predios_meta.npz", allow_pickle=True); PLON, PLAT = _PM["lon"], _PM["lat"]
ANO_P = np.fromfile(f"{AQUI}/assets/pred_ano.f32", np.float32)
LARG = {"primary": 12, "secondary": 11, "tertiary": 9, "residential": 7, "unclassified": 6, "living_street": 5, "pedestrian": 5, "service": 4}
RV = []
for f in json.load(open(f"{AQUI}/dados/brutos/ruas_todas.geojson"))["features"]:
    hw = f["properties"]["hw"].replace("_link", "")
    if hw not in LARG:
        continue
    cs = f["geometry"]["coordinates"]
    cam_ = [[round(x, 7), round(y, 7), zc(x, y)] for x, y in cs]
    mx, my = sum(x for x, _ in cs) / len(cs), sum(y for _, y in cs) / len(cs)
    perto = ANO_P[np.hypot((PLON - mx) * KL, (PLAT - my) * 111320) < 70]
    perto = perto[perto < 3000]
    a = float(np.percentile(perto, 15)) - 2 if len(perto) >= 3 else 1950.0   # a rua chega pouco antes das primeiras casas dela
    RV.append({"id": f"c{len(RV)}", "caminho": cam_, "larg": LARG[hw] + 3.2, "cor": [168, 162, 150], "ano": round(a, 1)})
for f in json.load(open(f"{AQUI}/dados/brutos/agua.geojson"))["features"]:
    if f["geometry"]["type"] == "LineString":
        RV.append({"id": f"w{len(RV)}", "caminho": [[round(x, 7), round(y, 7), zc(x, y)] for x, y in f["geometry"]["coordinates"]], "larg": 8, "cor": [58, 104, 138], "ano": 1500, "agua": True})
RV_A = [{"id": "a" + r["id"][1:], "caminho": r["caminho"], "larg": r["larg"] - 3.2, "cor": [88, 88, 94], "ano": r["ano"]} for r in RV if not r.get("agua")]
roteiro = {
    "titulo": "O centro de Itaguaí, em 3D",
    "hud_de_bloco": "capela-1688",
    "linha": {"de": 1680, "ate": 2050},
    "fim": {"titulo": "Centro de Itaguaí", "sub": "1729 – 2050?", "marca": "INEMA<span>.CLUB</span>", "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"auto": True},
    "popRotulo": "hab. no município",
    "teto": [[1680, 8], [1900, 10], [1940, 14], [1970, 24], [2000, 40]],
    "regimes": [
        {"ano": 1556, "nome": "Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1815.95, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
        {"ano": 1822.7, "nome": "Império do Brasil", "bandeira": "imperio"},
        {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
        {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
        {"ano": 1960, "nome": "República", "bandeira": "brasil"}],
    "linhas": [{"id": "trem", "ano": 1910.87, "desenha": 0.12, "sobe": 3, "cor": [60, 40, 30], "largura": 6}],
    "marcos": MARCOS,
    "predios_neutros": True,
    "ruas": RV + RV_A,
    "marcos_ez": 1.25,
    "arvores": FUT["arvores"],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
