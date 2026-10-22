"""Monta cidades/itaguai/roteiro.json a partir de dados/pesquisa/eventos.json + direção visual de cada evento.
Vídeo SEM narração: o cartão conta a história (título, número de impacto, legenda, detalhe, fonte).
Padrão copiado de cidades/floripa/roteiro_floripa.py (aprovado em 22/10/2026).
Uso: python3 cidades/itaguai/roteiro_itaguai.py"""
import json
import math
import os
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
EV = {e["id"]: e for e in json.load(open(f"{AQUI}/dados/pesquisa/eventos.json"))["eventos"]}
FONTES = {"pt.wikipedia.org": "Wikipédia", "en.wikipedia.org": "Wikipédia", "biblioteca.ibge.gov.br": "IBGE", "www.ibge.gov.br": "IBGE",
          "cidades.ibge.gov.br": "IBGE", "commons.wikimedia.org": "Wikimedia Commons", "www.marinha.mil.br": "Marinha do Brasil",
          "www.gov.br": "Governo Federal", "www.itaguai.rj.gov.br": "Prefeitura de Itaguaí", "itaguai.rj.gov.br": "Prefeitura de Itaguaí"}


def fonte(e):
    nomes = []
    for u in e["fontes"]:
        h = urllib.parse.urlparse(u).netloc
        n = FONTES.get(h, h.removeprefix("www."))
        if n not in nomes:
            nomes.append(n)
    return "; ".join(nomes[:3])


def cam(lon, lat, zoom, pitch=56, bearing=-20):
    return {"lon": lon, "lat": lat, "zoom": zoom, "pitch": pitch, "bearing": bearing}


def ls(z, lat):   # escala do globo (log de px por radiano) que bate com o zoom do mapa
    return round(math.log(6371000 * 2 ** z / (156543 * math.cos(math.radians(lat)))), 3)


TOPO = cam(-43.83, -22.875, 11.45, 0, 0)
REGIAO = cam(-43.84, -22.93, 11.3, 50, -8)
BAIA = cam(-43.88, -22.96, 11.9, 52, -10)
CENTRO = cam(-43.776, -22.858, 14.3, 58, -25)
CENTRO_L = cam(-43.776, -22.862, 13.2, 56, -15)
SANTACRUZ = cam(-43.688, -22.915, 13.5, 57, -30)
PONTE_J = cam(-43.6768, -22.8745, 15.6, 60, 0)
ITACURUCA = cam(-43.90, -22.935, 12.9, 55, -10)
MANGARATIBA = cam(-44.02, -22.96, 12.4, 55, 15)
BAIXADA = cam(-43.75, -22.83, 12.3, 52, -15)
NORTE = cam(-43.73, -22.79, 12.2, 52, -10)
SEROPEDICA = cam(-43.71, -22.765, 12.5, 55, -20)
NUCLEP = cam(-43.828, -22.893, 14.4, 58, -35)
PORTO = cam(-43.835, -22.935, 13.7, 60, -25)
ILHA_M = cam(-43.845, -22.935, 14.4, 60, -10)
FIM = cam(-43.82, -22.90, 11.6, 45, -8)


def titulo(e, destaque_ultimas=1):
    pal = e["titulo_curto_PT"].split()
    k = len(pal) - destaque_ultimas
    return " ".join(pal[:k]) + " <b>" + " ".join(pal[k:]) + "</b>"


def bloco(eid, anos, c0, c1, dur=8.5, **kw):
    e = EV[eid]
    b = {"id": eid, "anos": anos, "cam": [c0, c1], "dur": dur,
         "cartao": {"titulo": kw.pop("titulo", titulo(e, kw.pop("destaque", 1))), "numero": kw.pop("numero", e.get("numero_impacto", "")),
                    "legenda": kw.pop("legenda", e["legenda"]), "detalhe": kw.pop("detalhe", e.get("detalhe", "")),
                    "fonte": fonte(e), "local": [e["local"]["lon"], e["local"]["lat"]]}}
    b.update(kw)
    return b


C0 = cam(-43.83, -22.875, 11.45, 0, 0)
blocos = [
    {"id": "capa", "anos": [1500, 1500], "cam": [C0, C0], "dur": 5.5, "capa": {"imagem": "assets/capa_full.jpg", "segura": 5.5, "some": 0.8}},
    {"id": "globo", "anos": [1500, 1500], "cam": [C0, C0], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "uf": "RJ", "uf_de": 1500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -30, "lat": -6, "ls": 5.95}], [0.3, {"lon": -42, "lat": -16, "ls": 6.6}],
                          [0.65, {"lon": -43.5, "lat": -22.5, "ls": 8.6}], [1, {"lon": -43.83, "lat": -22.875, "ls": ls(11.45, -22.875)}]],
               "rotulos": [{"lon": -51, "lat": -11, "texto": "BRASIL", "de": 380, "ate": 3500, "tam": 84},
                           {"lon": -42.6, "lat": -22.15, "texto": "RIO DE JANEIRO", "de": 2600, "ate": 40000, "tam": 64},
                           {"lon": -43.775, "lat": -22.80, "texto": "ITAGUAÍ", "de": 30000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco("tupinambas", [1500, 1500], C0, BAIA, 9.5, numero="SÉC. XVI", titulo="A terra dos <b>tupinambás</b>", pulso_r=2500),
    bloco("nome-tupi", [1500, 1500], BAIA, CENTRO_L, 9.0, numero="ITÁ · KÛÁ · 'Y", titulo="Itaguaí, nome <b>tupi</b>"),
    bloco("sesmaria-1556", [1500, 1556, 1557], CENTRO_L, SANTACRUZ, 8.5, pulo=1.5, destaque=2,
          frota={"de": [-43.62, -23.06], "para": [-43.70, -22.96], "n": 1, "r": 110, "dura": 6, "rotulo": "Cristóvão Monteiro", "sub": "1556 · sesmaria"}),
    bloco("jesuitas-1589", [1557, 1589, 1590], SANTACRUZ, SANTACRUZ, 8.5, pulo=1.2, destaque=2),
    bloco("jaguaramenom", [1590, 1620, 1621], SANTACRUZ, ITACURUCA, 9.0, pulo=1.0, destaque=1,
          frota={"de": [-43.95, -22.97], "para": [-43.90, -22.925], "n": 5, "r": 40, "dura": 5, "icone": "canoa", "rotulo": "Aldeia indígena", "sub": "da ilha para o continente"}),
    bloco("aldeia-itinga", [1621, 1627, 1628], ITACURUCA, CENTRO_L, 8.5, pulo=0.8, destaque=1),
    bloco("aldeia-desce-1718", [1628, 1718, 1719], CENTRO_L, CENTRO, 8.5, pulo=1.6, numero="ANTES DE 1718", titulo="A aldeia desce para <b>perto do mar</b>"),
    bloco("caminho-1725", [1719, 1725, 1726], CENTRO, BAIXADA, 8.5, pulo=0.6, destaque=2),
    bloco("igreja-1729", [1726, 1729, 1730], BAIXADA, CENTRO, 8.5, pulo=0.5, titulo="Igreja de S. Francisco <b>Xavier</b>"),
    bloco("ponte-jesuitas-1752", [1730, 1752, 1753], CENTRO, PONTE_J, 9.5, pulo=1.2, destaque=2, destaca=["forte:ponte_jes"]),
    bloco("expulsao-1759", [1753, 1759, 1760], PONTE_J, SANTACRUZ, 8.5, pulo=0.6, destaque=1, destaca=["forte:palacio"],
          tom={"cor": "#8a6a6a", "forca": 0.25}),
    bloco("freguesia-1795", [1760, 1795, 1796], SANTACRUZ, CENTRO, 8.0, pulo=1.2, destaque=1),
    bloco("corte-1808", [1796, 1808.2, 1809], CENTRO, SANTACRUZ, 9.0, pulo=1.0, destaque=2, destaca=["forte:palacio"]),
    bloco("vila-1818", [1809, 1818.5, 1819], SANTACRUZ, CENTRO, 9.0, pulo=1.0, destaque=1),
    bloco("dom-pedro-1822", [1819, 1822.62, 1822.8], CENTRO, CENTRO_L, 8.5, pulo=0.8, destaque=1),
    bloco("mangaratiba-1831", [1822.8, 1831.8, 1832], CENTRO_L, MANGARATIBA, 8.5, pulo=0.8, destaque=1),
    bloco("fim-aldeia-1834", [1832, 1834, 1835], MANGARATIBA, CENTRO_L, 8.5, pulo=0.5, destaque=1),
    bloco("quintino-1836", [1835, 1836.9, 1837], CENTRO_L, CENTRO, 8.0, pulo=0.5, destaque=1),
    bloco("cafe-1850", [1837, 1850, 1851], CENTRO, BAIXADA, 8.5, pulo=1.0, destaque=1),
    bloco("abolicao-1888", [1851, 1888.37, 1889], BAIXADA, CENTRO_L, 9.0, pulo=1.5, destaque=1, tom={"cor": "#7a6a5a", "forca": 0.2}),
    bloco("cidade-1892", [1889, 1892.42, 1893], CENTRO_L, CENTRO, 8.0, pulo=0.6, destaque=1),
    bloco("trem-1910", [1893, 1910.87, 1911], CENTRO, BAIXADA, 9.0, pulo=1.2, destaca=["linha:trem_a", "linha:trem_b", "linha:trem_c"]),
    bloco("rio-sp-1928", [1911, 1928.34, 1929], BAIXADA, NORTE, 9.0, pulo=1.2, destaque=2, destaca=["linha:riosp"]),
    bloco("japoneses-1938", [1929, 1938, 1939], NORTE, BAIXADA, 8.5, pulo=0.8, destaque=1),
    bloco("paracambi-1960", [1939, 1960.6, 1961], BAIXADA, NORTE, 8.5, pulo=1.2, destaque=2),
    bloco("inga-1962", [1961, 1962, 1963], NORTE, ILHA_M, 9.0, pulo=0.5, destaque=2, destaca=["forte:inga"]),
    bloco("rio-santos-1974", [1963, 1974, 1975], ILHA_M, ITACURUCA, 9.0, pulo=1.0, destaque=1, destaca=["linha:riosantos"]),
    bloco("nuclep-1975", [1975, 1975.5, 1976], ITACURUCA, NUCLEP, 8.5, pulo=0.4, destaque=1, destaca=["forte:nuclep"]),
    bloco("porto-1982", [1976, 1982, 1983], NUCLEP, PORTO, 10.0, pulo=1.0, destaque=1, destaca=["area:porto"],
          detalhe="Dragagem e aterro desde 1977 (área aproximada no mapa). Em 2021, 51,7 milhões de toneladas e 8 berços."),
    bloco("seropedica-1995", [1983, 1995.78, 1996], PORTO, SEROPEDICA, 9.0, pulo=1.2, destaque=2),
    bloco("dique-inga-1996", [1996, 1996.1, 1997], SEROPEDICA, ILHA_M, 9.0, pulo=0.3, titulo="Veneno na <b>baía</b>", destaca=["forte:inga"],
          tom={"cor": "#6a4a4a", "forca": 0.3}),
    bloco("prosub-2008", [1997, 2008, 2009], ILHA_M, ILHA_M, 8.5, pulo=1.0, destaque=2),
    bloco("arco-2014", [2009, 2014, 2015], ILHA_M, NORTE, 9.0, pulo=0.6, destaque=1, destaca=["linha:arco"]),
    bloco("riachuelo-2018", [2015, 2018.95, 2019], NORTE, ILHA_M, 9.0, pulo=0.6, destaque=1,
          frota={"de": [-43.845, -22.935], "para": [-43.86, -22.99], "n": 1, "r": 60, "cor": [40, 40, 40], "dura": 6, "rotulo": "Submarino Riachuelo", "sub": "S40 · 2018"}),
    bloco("censo-2022", [2019, 2022, 2024], ILHA_M, REGIAO, 10.0, pulo=1.5, titulo="<b>116 mil</b> itaguaienses"),
    {"id": "fecho", "anos": [2024, 2024], "cam": [REGIAO, FIM], "dur": 14.0},
]
ROT = {"aldeia-itinga": ("ALDEIA DE ITINGA", -43.775, -22.852), "aldeia-desce-1718": ("ITAGUAÍ", -43.775, -22.852),
       "sesmaria-1556": ("SANTA CRUZ", -43.6846, -22.9068), "jesuitas-1589": ("FAZENDA DE SANTA CRUZ", -43.6846, -22.9068),
       "jaguaramenom": ("ILHA DE ITACURUÇÁ", -43.905, -22.952), "igreja-1729": ("MATRIZ", -43.775, -22.852),
       "ponte-jesuitas-1752": ("PONTE DOS JESUÍTAS", -43.6768, -22.8725), "corte-1808": ("PALÁCIO DE SANTA CRUZ", -43.6846, -22.9068),
       "mangaratiba-1831": ("MANGARATIBA", -44.0406, -22.9597), "seropedica-1995": ("SEROPÉDICA", -43.7078, -22.7439),
       "paracambi-1960": ("PARACAMBI ↑", -43.72, -22.64), "inga-1962": ("INGÁ", -43.8469, -22.9295),
       "nuclep-1975": ("NUCLEP", -43.8282, -22.8832), "porto-1982": ("PORTO DE ITAGUAÍ", -43.835, -22.925),
       "prosub-2008": ("BASE DE SUBMARINOS", -43.8469, -22.9295), "rio-sp-1928": ("RIO–SÃO PAULO", -43.70, -22.765),
       "rio-santos-1974": ("RIO–SANTOS", -43.86, -22.89), "arco-2014": ("ARCO METROPOLITANO", -43.74, -22.78)}
ALTO = {"jaguaramenom": 320, "porto-1982": 300, "prosub-2008": 200}   # rótulos acima dos morros
EP = json.load(open(f"{AQUI}/assets/epoca/indice.json"))


def ep(i, leg):
    x = EP[i]
    return {"src": f"assets/epoca/e{i:02d}.jpg", "legenda": leg,
            "credito": f"{x['autor'].split('(')[0].strip().rstrip(',;')} · {x['ano']} · domínio público (Wikimedia Commons)"}


IMG = {"caminho-1725": ep(0, "A capitania do Rio de Janeiro, 1757"), "expulsao-1759": ep(1, "A baía e a Marambaia, 1767"),
       "freguesia-1795": ep(2, "A costa e a Baía de Sepetiba, 1785"), "corte-1808": ep(3, "Projeto do Palácio de Santa Cruz, 1817"),
       "vila-1818": ep(4, "A vila de Itaguaí por Maria Graham, 1823"), "dom-pedro-1822": ep(5, "O Palácio de Santa Cruz, 1823"),
       "mangaratiba-1831": ep(6, "Mata perto de Mangaratiba (Rugendas)"), "cafe-1850": ep(7, "Sede da Fazenda de Santa Cruz, 1848"),
       "abolicao-1888": ep(11, "A província do Rio de Janeiro, 1887"), "cidade-1892": ep(9, "Carta náutica da Baía de Sepetiba, 1870"),
       "trem-1910": ep(12, "Planta da Estrada de Ferro Central, 1890")}
for b in blocos:
    if b["id"] in IMG:
        b["imagem"] = IMG[b["id"]]
    if b["id"] == "fecho":
        b["galeria"] = {"fica": True, "titulo": "Imagens <b>da época</b>", "itens": [f"assets/epoca/e{i:02d}.jpg" for i in (0, 3, 4, 5, 6, 7, 9, 12)],
                        "creditos": "M. Leveux, John Johnson, Maria Graham, Rugendas, C. J. de Niemeyer, Almirantado britânico, Arquivo Nacional · domínio público, via Wikimedia Commons"}
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b["rotulos"] = [{"lon": lo, "lat": la, "texto": nm, "z": ALTO.get(b["id"], 70), "tam": 32}]

roteiro = {
    "titulo": "Itaguaí — da aldeia ao porto, em 3D",
    "hud_de_bloco": "sesmaria-1556",
    "linha": {"de": 1500, "ate": 2024},
    "fim": {"titulo": "Itaguaí", "sub": "1818 – 2024", "marca": "INEMA<span>.CLUB</span>", "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"auto": True},
    "regimes": [
        {"ano": 1500, "nome": "Terra dos tupinambás", "bandeira": "portugal"},
        {"ano": 1556, "nome": "Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1815.95, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
        {"ano": 1822.7, "nome": "Império do Brasil", "bandeira": "imperio"},
        {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
        {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
        {"ano": 1960, "nome": "República", "bandeira": "brasil"}],
    "fortes": [{"id": "ponte_jes", "ano": 1752, "alt": 14, "rotulo": "Ponte dos Jesuítas", "sub": "1752 · rio Guandu"},
               {"id": "palacio", "ano": 1589.5, "alt": 22, "rotulo": "Fazenda de Santa Cruz", "sub": "sede dos jesuítas · palácio em 1808"},
               {"id": "inga", "ano": 1962, "alt": 40, "rotulo": "Fábrica da Ingá", "sub": "zinco · Ilha da Madeira (aprox.)"},
               {"id": "nuclep", "ano": 1975.5, "alt": 30, "rotulo": "NUCLEP", "sub": "1975"}],
    "linhas": [*({"id": t, "ano": 1910.87, "desenha": 0.12, "sobe": 4, "cor": [60, 40, 30], "largura": 5} for t in ("trem_a", "trem_b", "trem_c")),
               {"id": "riosp", "ano": 1928.34, "desenha": 0.5, "sobe": 3, "cor": [190, 150, 90], "largura": 4},
               {"id": "riosantos", "ano": 1974, "desenha": 0.9, "sobe": 4, "cor": [236, 236, 236], "largura": 5},
               {"id": "arco", "ano": 2014, "desenha": 0.9, "sobe": 6, "cor": [255, 150, 60], "largura": 6}],
    "areas": [{"id": "porto", "ano0": 1977, "ano1": 1982.8, "sai": 8}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
