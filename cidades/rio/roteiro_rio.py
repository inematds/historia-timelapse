"""Monta cidades/rio/roteiro.json a partir de dados/pesquisa/eventos.json + direção visual de cada evento.
Vídeo SEM narração: o cartão conta a história (título, número de impacto, legenda, detalhe, fonte).
Padrão copiado de cidades/floripa/roteiro_floripa.py e cidades/itaguai/roteiro_itaguai.py (aprovados em 22/10/2026).
Uso: python3 cidades/rio/roteiro_rio.py"""
import json
import math
import os
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
EV = {e["id"]: e for e in json.load(open(f"{AQUI}/dados/pesquisa/eventos.json"))["eventos"]}
FONTES = {"pt.wikipedia.org": "Wikipédia", "en.wikipedia.org": "Wikipédia", "fr.wikipedia.org": "Wikipédia", "biblioteca.ibge.gov.br": "IBGE",
          "www.ibge.gov.br": "IBGE", "cidades.ibge.gov.br": "IBGE", "commons.wikimedia.org": "Wikimedia Commons", "www.wikidata.org": "Wikidata"}


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


C0 = cam(-43.43, -22.91, 10.75, 0, 0)            # mapa todo de cima (fim do globo)
CIDADE = cam(-43.42, -22.94, 10.95, 44, -5)      # município inteiro
BAIA = cam(-43.19, -22.89, 12.0, 44, -20)         # a Baía de Guanabara
BAIA_S = cam(-43.165, -22.935, 12.6, 56, -10)    # entrada da baía + centro
ENTRADA = cam(-43.158, -22.958, 13.7, 60, -10)   # Pão de Açúcar
URCA = cam(-43.157, -22.950, 14.6, 62, -15)
VILLEG = cam(-43.163, -22.925, 14.4, 60, -20)
GLORIA = cam(-43.172, -22.935, 14.1, 58, -20)
CENTRO = cam(-43.178, -22.914, 14.6, 58, -30)
CENTRO_L = cam(-43.180, -22.918, 13.6, 56, -20)
PACO = cam(-43.1735, -22.9075, 15.2, 60, -35)
PACO_B = cam(-43.1700, -22.9040, 15.0, 58, -110)   # o Paço visto da baía
PACO_C = cam(-43.1760, -22.9030, 15.6, 60, 20)
PACO_D = cam(-43.1780, -22.9060, 14.2, 55, -65)
ARCOS = cam(-43.1795, -22.9165, 15.4, 60, -10)
CAMPO = cam(-43.1880, -22.9115, 14.9, 58, -20)
VALONGO = cam(-43.1860, -22.9010, 15.4, 60, -40)
COBRAS = cam(-43.1720, -22.9020, 14.6, 60, -15)
NITEROI = cam(-43.135, -22.905, 13.2, 56, 40)
LAGOA = cam(-43.2117, -22.986, 13.5, 55, -15)
JB = cam(-43.2225, -22.983, 13.9, 52, -25)
TREM = cam(-43.255, -22.925, 12.4, 55, -75)
COPA = cam(-43.1875, -22.9815, 15.6, 62, 165)
CRISTO = cam(-43.2105, -22.9560, 13.7, 48, -10)
MARACANA = cam(-43.2302, -22.9180, 15.0, 58, -10)
FLAMENGO = cam(-43.170, -22.938, 13.9, 60, -25)
PONTE = cam(-43.165, -22.893, 13.0, 62, 0)
BARRA = cam(-43.40, -23.005, 12.8, 56, -10)
FIM = cam(-43.42, -22.94, 11.0, 40, -5)


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


VERM, AZUL, CINZA = [220, 40, 40], [40, 70, 190], [60, 60, 60]
blocos = [
    {"id": "capa", "anos": [1500, 1500], "cam": [C0, C0], "dur": 5.5, "capa": {"imagem": "assets/capa_full.jpg", "segura": 5.5, "some": 0.8}},
    {"id": "globo", "anos": [1500, 1500], "cam": [C0, C0], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "uf": "RJ", "uf_de": 1500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -30, "lat": -6, "ls": 5.95}], [0.3, {"lon": -42, "lat": -16, "ls": 6.6}],
                          [0.65, {"lon": -43.3, "lat": -22.6, "ls": 8.6}], [1, {"lon": C0["lon"], "lat": C0["lat"], "ls": ls(C0["zoom"], C0["lat"])}]],
               "rotulos": [{"lon": -51, "lat": -11, "texto": "BRASIL", "de": 380, "ate": 3500, "tam": 84},
                           {"lon": -42.3, "lat": -21.9, "texto": "ESTADO DO RIO", "de": 2600, "ate": 40000, "tam": 60},
                           {"lon": -43.30, "lat": -22.86, "texto": "RIO DE JANEIRO", "de": 30000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco("tupinambas-1500", [1500, 1500], C0, BAIA, 9.5, titulo="A baía dos <b>tupinambás</b>", pulso_r=3000),
    bloco("rio-de-janeiro-1502", [1500, 1502, 1502.1], BAIA, ENTRADA, 9.0, pulo=1.0, titulo="Um rio em <b>janeiro</b>",
          frota={"de": [-43.14, -23.06], "para": [-43.158, -22.94], "n": 3, "r": 110, "dura": 6, "rotulo": "Expedição portuguesa", "sub": "1º/1/1502"}),
    bloco("feitoria-1504", [1502.1, 1504, 1505], ENTRADA, GLORIA, 8.5, pulo=0.6, destaque=1),
    bloco("franca-antartica-1555", [1505, 1555.86, 1556.2], GLORIA, VILLEG, 9.5, pulo=1.6, destaque=2,
          frota={"de": [-43.14, -23.05], "para": [-43.16, -22.918], "n": 2, "r": 110, "cor": AZUL, "dura": 6, "rotulo": "Naus de Villegagnon", "sub": "1555 · franceses"}),
    bloco("forte-coligny-1560", [1556.2, 1560.2, 1560.4], VILLEG, BAIA_S, 9.5, pulo=0.8, destaque=2, destaca=["forte:coligny"],
          frota={"de": [-43.13, -23.04], "para": [-43.16, -22.93], "n": 26, "r": 90, "espalha_km": 3, "dura": 6.5, "rotulo": "Esquadra de Mem de Sá", "sub": "1560"},
          tom={"cor": "#a15050", "forca": 0.3}),
    bloco("fundacao-1565", [1560.4, 1565.16, 1565.3], BAIA_S, URCA, 9.5, pulo=0.8, titulo="Nasce São Sebastião <b>do Rio</b>", numero="1º/3/1565",
          frota={"de": [-43.14, -23.02], "para": [-43.154, -22.945], "n": 4, "r": 70, "dura": 5.5, "rotulo": "Estácio de Sá", "sub": "1565"}),
    bloco("urucumirim-1567", [1565.3, 1567.05, 1567.15], URCA, GLORIA, 9.0, pulo=0.6, destaque=1, tom={"cor": "#a15050", "forca": 0.3}),
    bloco("castelo-1567", [1567.15, 1567.3, 1568], GLORIA, CENTRO, 8.5, pulo=0.4, destaque=1),
    bloco("niteroi-1573", [1568, 1573.89, 1574.5], CENTRO, NITEROI, 8.5, pulo=0.8, destaque=1),
    bloco("engenho-lagoa-1575", [1574.5, 1575, 1580], NITEROI, LAGOA, 8.5, pulo=0.5, destaque=2),
    bloco("santo-antonio-1608", [1580, 1608.42, 1609], LAGOA, CENTRO, 8.5, pulo=1.2, destaque=2),
    bloco("duclerc-1710", [1609, 1710.72, 1710.9], CENTRO, CENTRO_L, 9.0, pulo=1.6, destaque=2,
          tom={"cor": "#a15050", "forca": 0.25}),
    bloco("duguay-trouin-1711", [1710.9, 1711.7, 1711.9], CENTRO_L, BAIA_S, 10.0, pulo=0.5, destaque=1,
          frota={"de": [-43.13, -23.05], "para": [-43.165, -22.905], "n": 17, "r": 110, "espalha_km": 3, "cor": AZUL, "dura": 7, "rotulo": "Esquadra de Duguay-Trouin", "sub": "1711 · 16 a 18 navios"},
          tom={"cor": "#a15050", "forca": 0.3}),
    bloco("arcos-1750", [1711.9, 1750, 1751], BAIA_S, ARCOS, 9.0, pulo=1.2, destaque=2, destaca=["forte:arcos"]),
    bloco("capital-1763", [1751, 1763, 1764], ARCOS, PACO, 8.5, pulo=0.8, destaque=1, destaca=["forte:paco"]),
    bloco("corte-1808", [1764, 1808.18, 1808.3], PACO, BAIA_S, 10.0, pulo=1.4, destaque=2,
          frota={"de": [-43.13, -23.05], "para": [-43.170, -22.905], "n": 17, "r": 110, "espalha_km": 3, "cor": [30, 120, 60], "dura": 7, "rotulo": "A frota da Corte", "sub": "1808 · de Lisboa"}),
    bloco("jardim-botanico-1808", [1808.3, 1808.45, 1808.6], BAIA_S, JB, 8.5, pulo=0.3, destaque=2),
    bloco("valongo-1811", [1808.6, 1811, 1812], JB, VALONGO, 9.5, pulo=0.6, destaque=1, destaca=["forte:valongo"], tom={"cor": "#6a4a4a", "forca": 0.3}),
    bloco("reino-unido-1815", [1812, 1815.96, 1816.1], VALONGO, PACO_B, 8.5, pulo=0.6, destaque=2, destaca=["forte:paco"]),
    bloco("fico-1822", [1816.1, 1822.02, 1822.1], PACO_B, PACO_C, 8.0, pulo=0.6, destaque=1),
    bloco("imperio-1822", [1822.1, 1822.78, 1822.9], PACO_C, CAMPO, 8.5, pulo=0.4, destaque=1),
    bloco("municipio-neutro-1834", [1822.9, 1834.61, 1835], CAMPO, CIDADE, 9.0, pulo=0.8, destaque=2),
    bloco("ferrovia-1858", [1835, 1858.24, 1859], CIDADE, TREM, 9.5, pulo=1.2, destaque=1, destaca=["linha:trem"]),
    bloco("abolicao-1888", [1859, 1888.36, 1888.5], TREM, PACO_D, 8.5, pulo=1.4, destaque=1),
    bloco("republica-1889", [1888.5, 1889.87, 1890], PACO_D, CAMPO, 8.5, pulo=0.4, destaque=1),
    bloco("armada-1893", [1890, 1893.68, 1894.2], CAMPO, BAIA_S, 9.0, pulo=0.6, destaque=2,
          frota={"de": [-43.15, -22.86], "para": [-43.165, -22.91], "n": 5, "r": 70, "cor": CINZA, "dura": 6, "rotulo": "Navios rebeldes", "sub": "1893"},
          tom={"cor": "#8a6a6a", "forca": 0.25}),
    bloco("avenida-central-1904", [1894.2, 1904.2, 1904.5], BAIA_S, CENTRO, 8.5, pulo=0.8, destaque=1),
    bloco("vacina-1904", [1904.5, 1904.86, 1905], CENTRO, CAMPO, 8.5, pulo=0.3, destaque=1, tom={"cor": "#8a5a5a", "forca": 0.25}),
    bloco("chibata-1910", [1905, 1910.89, 1911], CAMPO, COBRAS, 8.5, pulo=0.6, destaque=1, numero="1.500 A 2.000 MARUJOS",
          frota={"de": [-43.16, -22.90], "para": [-43.165, -22.91], "n": 4, "r": 80, "cor": CINZA, "dura": 6, "rotulo": "Navios rebelados", "sub": "1910 · Minas Geraes e São Paulo"}, tom={"cor": "#8a6a6a", "forca": 0.2}),
    bloco("forte-copacabana-1922", [1911, 1922.51, 1922.6], COBRAS, COPA, 9.0, pulo=0.8, destaque=2, destaca=["forte:copacabana"], tom={"cor": "#8a5a5a", "forca": 0.2}),
    bloco("castelo-1922", [1922.6, 1922.68, 1923], COPA, CENTRO, 9.0, pulo=0.3, destaque=2),
    bloco("cristo-1931", [1923, 1931.78, 1932], CENTRO, CRISTO, 9.0, pulo=0.8, destaque=1, destaca=["forte:cristo"]),
    bloco("maracana-1950", [1932, 1950.54, 1950.95], CRISTO, MARACANA, 9.0, pulo=1.0, destaque=1, destaca=["forte:maracana"],
          legenda="No jogo decisivo da Copa, um público recorde até hoje vê o Uruguai vencer o Brasil por 2 a 1",
          detalhe="O estádio foi erguido para a Copa de 1950. No jogo decisivo, foram 199.854 presentes, dos quais 173.850 pagantes."),
    bloco("guanabara-1960", [1951, 1960.3, 1961], MARACANA, CIDADE, 8.5, pulo=0.8, destaque=1),
    bloco("aterro-1965", [1961, 1965.79, 1966], CIDADE, FLAMENGO, 9.5, pulo=0.8, destaque=2, destaca=["area:flamengo"],
          detalhe="Terra dos morros desmontados vira parque à beira da baía, de 1961 a 1965 (área aproximada no mapa)."),
    bloco("ponte-1974", [1966, 1974.17, 1974.6], FLAMENGO, PONTE, 10.5, pulo=0.8, destaque=2, destaca=["linha:ponte"],
          detalhe="A ponte tem 26,6 m de largura e um vão central de 300 m para os navios passarem. As obras começaram em 1969."),
    bloco("fusao-1975", [1974.6, 1975.2, 1975.9], PONTE, CIDADE, 8.5, pulo=0.4, titulo="A <b>fusão</b>",
          detalhe="Niterói deixou de ser a capital fluminense, e o Rio passou a ser um município do novo estado."),
    bloco("eco92-1992", [1976, 1992.43, 1992.9], CIDADE, BARRA, 8.5, pulo=1.0, titulo="A <b>Eco-92</b>",
          detalhe="A Rio-92 ajudou a espalhar a ideia de desenvolvimento sustentável e gerou as convenções do clima e da biodiversidade."),
    bloco("olimpiadas-2016", [1993, 2016.6, 2017], BARRA, BARRA, 8.5, pulo=1.2, destaque=1),
    bloco("censo-2022", [2017, 2022, 2024], BARRA, CIDADE, 10.0, pulo=1.5, titulo="<b>6,2 milhões</b> de cariocas"),
    {"id": "fecho", "anos": [2024, 2024], "cam": [CIDADE, FIM], "dur": 14.0},
]
ROT = {"feitoria-1504": ("FOZ DO CARIOCA", -43.1694, -22.9356),
       
       "urucumirim-1567": ("URUÇUMIRIM (GLÓRIA)", -43.1756, -22.9214), "castelo-1567": ("MORRO DO CASTELO (ARRASADO EM 1922)", -43.1745, -22.9069),
       "niteroi-1573": ("NITERÓI", -43.1250, -22.8950), "engenho-lagoa-1575": ("LAGOA", -43.2117, -22.9711),
       "santo-antonio-1608": ("CONVENTO DE SANTO ANTÔNIO", -43.1791, -22.9073), 
       "capital-1763": ("PAÇO DOS VICE-REIS", -43.1742, -22.9035), "jardim-botanico-1808": ("JARDIM BOTÂNICO", -43.2239, -22.9675),
       "imperio-1822": ("CAMPO DE SANTANA", -43.1886, -22.9067),
       "ferrovia-1858": ("CENTRAL DO BRASIL", -43.1927, -22.9037), "republica-1889": ("CAMPO DE SANTANA", -43.1886, -22.9067),
       
       "castelo-1922": ("ONDE ERA O CASTELO", -43.1745, -22.9069), "cristo-1931": ("CORCOVADO", -43.2105, -22.9519),
       "aterro-1965": ("ATERRO DO FLAMENGO", -43.170, -22.9211),
       "ponte-1974": ("PONTE RIO–NITERÓI", -43.1534, -22.8712), "eco92-1992": ("RIOCENTRO", -43.4113, -22.9781),
       "olimpiadas-2016": ("PARQUE OLÍMPICO", -43.394, -22.977)}
ALTO = {"engenho-lagoa-1575": 250, "jardim-botanico-1808": 250, "cristo-1931": 760, "rio-de-janeiro-1502": 420, "fundacao-1565": 200, "castelo-1567": 90, "castelo-1922": 90}   # rótulos acima dos morros
IMG = {}
fi = f"{AQUI}/assets/epoca/indice.json"
EP = json.load(open(fi)) if os.path.exists(fi) else []
USO = json.load(open(f"{AQUI}/imagens_uso.json")) if os.path.exists(f"{AQUI}/imagens_uso.json") else {}


AUTOR = {"Autor não identificado; litografia Thierry Frères": "Litografia Thierry Frères", "Fotógrafo não identificado na página": "Autor desconhecido",
         "Jacques de Vau de Claye, cartógrafo": "Jacques de Vau de Claye"}


def ep(i, leg):
    x = dict(EP[i]); a = x["autor"].split("(")[0].split(" — ")[0].strip().rstrip(",;"); x["autor"] = AUTOR.get(a, a)
    return {"src": f"assets/epoca/e{i:02d}.jpg", "legenda": leg,
            "credito": f"{x['autor'].split('(')[0].split(' — ')[0].strip().rstrip(',;')} · {x['ano']} · domínio público (Wikimedia Commons)"}


for b in blocos:
    a = b["anos"]
    if len(a) == 3 and "cartao" in b:
        a[2] = max(a[1] + 0.005, min(a[2], math.floor(a[1]) + 0.95))
        b["anos"] = a
for bid, (i, leg) in USO.get("blocos", {}).items():
    IMG[bid] = ep(i, leg)
for b in blocos:
    if b["id"] in IMG:
        b["imagem"] = IMG[b["id"]]
    if b["id"] == "fecho" and USO.get("galeria"):
        b["galeria"] = {"fica": True, "titulo": "Imagens <b>da época</b>", "itens": [f"assets/epoca/e{i:02d}.jpg" for i in USO["galeria"]],
                        "creditos": USO["creditos"]}
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b["rotulos"] = [{"lon": lo, "lat": la, "texto": nm, "z": ALTO.get(b["id"], 70), "tam": 32}]

roteiro = {
    "titulo": "Rio de Janeiro — da baía à metrópole, em 3D",
    "hud_de_bloco": "rio-de-janeiro-1502",
    "linha": {"de": 1500, "ate": 2024},
    "fim": {"titulo": "Rio de Janeiro", "sub": "1565 – 2024", "marca": "INEMA<span>.CLUB</span>", "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"auto": True},
    "regimes": [
        {"ano": 1500, "nome": "Terra dos tupinambás", "bandeira": "portugal"},
        {"ano": 1555.86, "nome": "França Antártica", "bandeira": "franca"},
        {"ano": 1565.16, "nome": "Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1763, "nome": "Capital do Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1808.18, "nome": "Sede da Corte portuguesa", "bandeira": "portugal"},
        {"ano": 1815.96, "nome": "Capital do Reino Unido", "bandeira": "reino"},
        {"ano": 1822.78, "nome": "Capital do Império", "bandeira": "imperio"},
        {"ano": 1834.61, "nome": "Município Neutro (capital)", "bandeira": "imperio"},
        {"ano": 1870, "nome": "Município Neutro (capital)", "bandeira": "imperio2"},
        {"ano": 1889.87, "nome": "Capital da República", "bandeira": "republica"},
        {"ano": 1891.15, "nome": "Distrito Federal", "bandeira": "republica"},
        {"ano": 1960.3, "nome": "Estado da Guanabara", "bandeira": "brasil"},
        {"ano": 1975.2, "nome": "Capital do Estado do RJ", "bandeira": "brasil"}],
    "fortes": [{"id": "coligny", "ano": 1555.95, "alt": 16, "rotulo": "Forte Coligny", "sub": "1555 · franceses"},
               {"id": "santacruz", "ano": 1567.5, "alt": 18},
               {"id": "paco", "ano": 1743, "alt": 16, "rotulo": "Paço", "sub": "dos vice-reis · real · imperial"},
               {"id": "arcos", "ano": 1750, "alt": 18, "rotulo": "Arcos da Carioca", "sub": "1750 · aqueduto"},
               {"id": "valongo", "ano": 1811, "alt": 4, "rotulo": "Cais do Valongo", "sub": "1811"},
               {"id": "copacabana", "ano": 1914.7, "alt": 14, "rotulo": "Forte de Copacabana", "sub": "1922 · os 18 do Forte"},
               {"id": "cristo", "ano": 1931.78, "alt": 70, "rotulo": "Cristo Redentor", "sub": "1931 · 38 m"},
               {"id": "maracana", "ano": 1950.4, "alt": 32, "rotulo": "Maracanã", "sub": "1950"}],
    "linhas": [{"id": "trem", "ano": 1858.24, "desenha": 0.5, "sobe": 4, "cor": [60, 40, 30], "largura": 5},
               {"id": "ponte", "ano": 1974.17, "desenha": 0.35, "sobe": 40, "cor": [236, 236, 236], "largura": 8}],
    "areas": [{"id": "flamengo", "ano0": 1961, "ano1": 1965.7, "sai": 8}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
