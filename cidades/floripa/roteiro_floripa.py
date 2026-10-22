"""Monta cidades/floripa/roteiro.json a partir de dados/pesquisa/eventos.json + direção visual de cada evento.
Vídeo SEM narração: o cartão conta a história (título, número de impacto, legenda, detalhe, fonte).
Uso: python3 cidades/floripa/roteiro_floripa.py"""
import json
import os
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
EV = {e["id"]: e for e in json.load(open(f"{AQUI}/dados/pesquisa/eventos.json"))["eventos"]}
EV_LISTA = json.load(open(f"{AQUI}/dados/pesquisa/eventos.json"))["eventos"]
FONTES = {"pt.wikipedia.org": "Wikipédia", "en.wikipedia.org": "Wikipédia", "biblioteca.ibge.gov.br": "IBGE", "www.ibge.gov.br": "IBGE",
          "teses.usp.br": "Teses USP", "ndmais.com.br": "ND Mais", "repositorio.ufsc.br": "UFSC", "soniaa-arq.prof.ufsc.br": "UFSC",
          "www.brasilianaiconografica.art.br": "Brasiliana Iconográfica", "portaldaacorianidade.azores.gov.pt": "Governo dos Açores",
          "rebep.org.br": "REBEP", "history.state.gov": "US Office of the Historian", "revistaarqurb.com.br": "Revista ArqUrb",
          "www.nsctotal.com.br": "NSC Total", "commons.wikimedia.org": "Wikimedia Commons"}


def fonte(e):
    nomes = []
    for u in e["fontes"]:
        n = FONTES.get(urllib.parse.urlparse(u).netloc, urllib.parse.urlparse(u).netloc)
        if n not in nomes:
            nomes.append(n)
    return "; ".join(nomes[:3])


def cam(lon, lat, zoom, pitch=56, bearing=-20):
    return {"lon": lon, "lat": lat, "zoom": zoom, "pitch": pitch, "bearing": bearing}


ILHA = cam(-48.505, -27.640, 10.6, 50, -12)
CENTRO = cam(-48.552, -27.600, 14.0, 58, -40)
CENTRO_L = cam(-48.548, -27.605, 13.0, 56, -30)
NORTE_BAIA = cam(-48.548, -27.462, 12.7, 57, -15)
ANHA = cam(-48.5650, -27.4330, 14.7, 55, -15)
LAGOA = cam(-48.470, -27.610, 12.8, 56, 10)
SANTO_ANT = cam(-48.528, -27.515, 13.0, 56, -30)
ARMACAO = cam(-48.512, -27.755, 12.6, 55, 0)
CANASV = cam(-48.468, -27.455, 12.4, 55, -10)
RIBEIRAO = cam(-48.540, -27.712, 12.8, 55, -20)
PONTES = cam(-48.570, -27.602, 13.7, 60, -70)
TRINDADE = cam(-48.528, -27.603, 13.3, 57, -25)
# pontes de lado: Hercílio Luz vista do norte (olhando para o sul); Colombo/Pedro Ivo vistas do sul (a Hercílio fica ao fundo)
PONTE_N = cam(-48.5655, -27.5960, 16.3, 62, -180)
PONTE_S = cam(-48.5646, -27.5968, 16.2, 64, 0)
PONTE_S2 = cam(-48.5650, -27.5970, 16.1, 63, 14)
ESTREITO = cam(-48.580, -27.598, 13.3, 57, -80)


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


def ev_id(ano, palavra):
    for e in EV_LISTA:
        if e["ano"] == ano and palavra.lower() in e["titulo_curto_PT"].lower():
            return e["id"]
    raise KeyError((ano, palavra))


I = {k: ev_id(*v) for k, v in {
    "samb": (-4800, "sambaqui"), "cari": (1000, "carijós"), "cab": (1526, "santa catarina"), "esp1541": (1541, "espanhóis"),
    "nasce": (1673, "desterro"), "capela": (1678, "capela"), "cors": (1687, "corsários"), "147": (1712, "147"),
    "vila": (1726, "vila"), "silva": (1739, "silva"), "anha": (1739, "anhatomirim"), "tri": (1740, "triângulo"),
    "acor": (1748, "açorianos"), "lagoa": (1750, "lagoa"), "santo": (1751, "santo"), "4820": (1753, "4.820"),
    "baleia": (1772, "baleias"), "espanha": (1777, "espanha"), "volta": (1778, "volta"), "ribeirao": (1809, "ribeirão"),
    "cidade": (1823, "cidade"), "imperador": (1845, "imperador"), "censo": (1872, "censo"), "rebeldes": (1893, "rebeldes"),
    "fuzil": (1894, "fuzilados"), "nome": (1894, "florianópolis"), "hercilio": (1926, "hercílio"), "estreito": (1944, "estreito"),
    "ufsc": (1960, "ufsc"), "beiramar": (1963, "beira-mar"), "baiasul": (1972, "baía sul"), "colombo": (1975, "colombo"),
    "norte": (1975, "praia"), "pedroivo": (1991, "pedro ivo"), "2022": (2022, "537")}.items()}

blocos = [
    {"id": "capa", "anos": [1500, 1500], "cam": [cam(-48.50, -27.62, 11.21, 0, 0), cam(-48.50, -27.62, 11.21, 0, 0)], "dur": 5.5,
     "capa": {"imagem": "assets/capa_full.jpg", "segura": 5.5, "some": 0.8}},
    {"id": "globo", "anos": [1500, 1500], "cam": [cam(-48.50, -27.62, 11.21, 0, 0), cam(-48.50, -27.62, 11.21, 0, 0)], "dur": 9.0, "corte": True,
     "globo": {"raster": True, "uf": "SC", "uf_de": 1500, "uf_ate": 60000, "br_ate": 9000, "some": 1.2,
               "chaves": [[0, {"lon": -28, "lat": -6, "ls": 5.95}], [0.3, {"lon": -44, "lat": -18, "ls": 6.6}], [0.65, {"lon": -48.3, "lat": -26.8, "ls": 8.6}], [1, {"lon": -48.50, "lat": -27.62, "ls": 11.6}]],
               "rotulos": [{"lon": -51, "lat": -11, "texto": "BRASIL", "de": 380, "ate": 3500, "tam": 84},
                           {"lon": -50.6, "lat": -27.1, "texto": "SANTA CATARINA", "de": 2600, "ate": 40000, "tam": 64},
                           {"lon": -48.50, "lat": -27.55, "texto": "FLORIANÓPOLIS", "de": 30000, "ate": 2e6, "tam": 72, "ponto": True}]}},
    bloco(I["samb"], [1500, 1500], cam(-48.50, -27.62, 11.21, 0, 0), ILHA, 9.5, numero="~4800 a.C.", hud=False, pulso_r=1800),
    bloco(I["cari"], [1500, 1500], ILHA, cam(-48.50, -27.63, 10.4, 50, -8), 9.0, numero="MEIEMBIPE", titulo="A terra dos <b>carijós</b>", hud=False, pulso_r=1800),
    bloco(I["cab"], [1500, 1526, 1527], ILHA, ILHA, 8.5, pulo=1.2, hud=True,
          frota={"de": [-48.30, -27.45], "para": [-48.40, -27.62], "n": 1, "r": 120, "dura": 6, "rotulo": "Navio de Sebastião Caboto", "sub": "1526"}),
    bloco(I["esp1541"], [1527, 1541, 1542], ILHA, cam(-48.50, -27.62, 10.5, 50, -12), 8.5, pulo=1.2, numero="1541",
          frota={"de": [-48.32, -27.70], "para": [-48.45, -27.55], "n": 3, "r": 110, "cor": [220, 40, 40], "dura": 6, "rotulo": "Expedição de Cabeza de Vaca", "sub": "1541 · rumo a Assunção"}),
    bloco(I["nasce"], [1542, 1673, 1675], cam(-48.50, -27.62, 10.5, 50, -12), CENTRO, 9.5, pulo=2.2, destaque=2,
          frota={"de": [-48.56, -27.52], "para": [-48.552, -27.594], "n": 4, "r": 40, "dura": 5, "icone": "canoa", "rotulo": "Chegada de Dias Velho", "sub": "1673"}),
    bloco(I["capela"], [1675, 1678, 1680], CENTRO, CENTRO, 8.0, pulo=0.8),
    bloco(I["cors"], [1680, 1687, 1689], CENTRO, CENTRO_L, 8.5, pulo=0.8,
          frota={"de": [-48.52, -27.47], "para": [-48.553, -27.588], "n": 1, "r": 70, "cor": [40, 40, 40], "dura": 5, "rotulo": "Corsários ingleses", "sub": "1687"},
          tom={"cor": "#a15050", "forca": 0.35}),
    bloco(I["147"], [1689, 1712, 1714], CENTRO_L, CENTRO, 8.0, pulo=1.0, titulo="Só <b>147 moradores</b>"),
    bloco(I["vila"], [1714, 1726, 1728], CENTRO, CENTRO, 8.0, pulo=1.0),
    bloco(I["silva"], [1728, 1739, 1739.4], CENTRO, CENTRO_L, 8.0, pulo=1.0, destaque=2,
          frota={"de": [-48.50, -27.42], "para": [-48.553, -27.590], "n": 2, "r": 60, "dura": 5, "rotulo": "Silva Paes chega", "sub": "1739 · 1º governador"}),
    bloco(I["anha"], [1739.4, 1739.6, 1740], CENTRO_L, ANHA, 9.0, pulo=0.4, destaca=["forte:anhatomirim"], destaque=1),
    bloco(I["tri"], [1740, 1740.5, 1743], ANHA, NORTE_BAIA, 9.0, pulo=0.4,
          destaca=["forte:anhatomirim", "forte:ponta_grossa", "forte:ratones"], titulo="O triângulo de <b>fortes</b>"),
    bloco(I["acor"], [1743, 1748, 1749], NORTE_BAIA, CENTRO_L, 9.5, pulo=1.0,
          frota={"de": [-48.42, -27.45], "para": [-48.553, -27.592], "n": 26, "r": 130, "espalha_km": 4, "dura": 7, "rotulo": "Casais açorianos", "sub": "1ª leva · 1748"}),
    bloco(I["lagoa"], [1749, 1750, 1751], CENTRO_L, LAGOA, 8.5, pulo=0.6, destaque=2),
    bloco(I["santo"], [1751, 1751.5, 1753], LAGOA, SANTO_ANT, 8.5, pulo=0.4, destaque=3),
    bloco(I["4820"], [1753, 1753.5, 1754], SANTO_ANT, CENTRO_L, 8.0, pulo=0.4, titulo="A ilha tem <b>4.820 almas</b>"),
    bloco(I["baleia"], [1754, 1772, 1773], CENTRO_L, ARMACAO, 8.5, pulo=1.5, titulo="A caça às <b>baleias</b>"),
    bloco(I["espanha"], [1773, 1777.15, 1777.6], ARMACAO, CANASV, 10.0, pulo=1.2, destaque=2,
          frota={"de": [-48.36, -27.33], "para": [-48.465, -27.44], "n": 60, "r": 150, "espalha_km": 6, "cor": [220, 40, 40], "dura": 7, "rotulo": "Frota espanhola", "sub": "+100 navios · ~10 mil homens"},
          tom={"cor": "#c46a5a", "forca": 0.25}),
    bloco(I["volta"], [1777.6, 1778.6, 1779], CANASV, CENTRO_L, 8.5, pulo=0.8, titulo="A ilha volta a <b>Portugal</b>"),
    bloco(I["ribeirao"], [1779, 1809, 1810], CENTRO_L, RIBEIRAO, 8.5, pulo=1.5, numero="1806", destaque=2),
    bloco(I["cidade"], [1810, 1823.2, 1824], RIBEIRAO, CENTRO, 8.5, pulo=1.2, destaque=2),
    bloco(I["imperador"], [1824, 1845.8, 1846], CENTRO, CENTRO_L, 8.0, pulo=1.2,
          frota={"de": [-48.52, -27.66], "para": [-48.553, -27.600], "n": 1, "r": 70, "cor": [30, 120, 60], "dura": 5, "rotulo": "Navio imperial", "sub": "D. Pedro II · 1845"}),
    bloco(I["censo"], [1846, 1872, 1873], CENTRO_L, CENTRO_L, 8.0, pulo=1.5, titulo="1º censo: <b>25.709</b>", numero="25.709"),
    bloco(I["rebeldes"], [1873, 1893.8, 1894.0], CENTRO_L, CENTRO_L, 9.0, pulo=1.5, destaque=2,
          frota={"de": [-48.50, -27.45], "para": [-48.555, -27.585], "n": 5, "r": 60, "cor": [60, 60, 60], "dura": 6, "rotulo": "Navios rebeldes", "sub": "1893"},
          tom={"cor": "#8a6a6a", "forca": 0.25}),
    bloco(I["fuzil"], [1894.0, 1894.3, 1894.5], CENTRO_L, ANHA, 9.0, pulo=0.5, numero="DEZENAS DE FUZILADOS",
          legenda="Floriano manda o coronel Moreira César; presos são fuzilados na fortaleza de Anhatomirim",
          destaca=["forte:anhatomirim"], tom={"cor": "#6a2a2a", "forca": 0.35}),
    bloco(I["nome"], [1894.5, 1894.75, 1895], ANHA, CENTRO, 9.0, pulo=0.4, destaque=1, numero="1º/10/1894"),
    bloco(I["hercilio"], [1895, 1926.36, 1927], CENTRO, PONTE_N, 11.5, pulo=2.0, destaca=["linha:hercilio"], destaque=2),
    bloco(I["estreito"], [1927, 1944, 1945], PONTES, ESTREITO, 8.5, pulo=1.5, destaque=2),
    bloco(I["ufsc"], [1945, 1960.96, 1962], ESTREITO, TRINDADE, 8.5, pulo=1.5),
    bloco(I["beiramar"], [1962, 1963, 1968.5], TRINDADE, cam(-48.540, -27.592, 13.6, 60, -25), 9.0, pulo=0.6, destaca=["area:beira_mar"], destaque=2,
          detalhe="Cerca de 70 hectares de mar viram avenida e bairro na Baía Norte (área aproximada no mapa)."),
    bloco(I["baiasul"], [1968.5, 1972, 1975], cam(-48.540, -27.592, 13.6, 60, -25), cam(-48.556, -27.606, 13.8, 60, -60), 9.0, pulo=0.6,
          destaca=["area:baia_sul"], destaque=2, detalhe="O centro avança sobre a Baía Sul em camadas (área aproximada no mapa)."),
    bloco(I["colombo"], [1975, 1975.2, 1976], cam(-48.556, -27.606, 13.8, 60, -60), PONTE_S, 10.5, pulo=0.3, destaca=["linha:colombo"], destaque=2),
    bloco(I["norte"], [1976, 1980, 1990], PONTES, CANASV, 9.0, pulo=1.0, titulo="O norte vira <b>praia</b>", numero="ANOS 1970"),
    bloco(I["pedroivo"], [1990, 1991.2, 1992], CANASV, PONTE_S2, 9.5, pulo=0.6, destaca=["linha:pedroivo"], destaque=3),
    bloco(I["2022"], [1992, 2022, 2024], PONTES, ILHA, 10.0, pulo=5.0, titulo="<b>537 mil</b> moradores"),
    {"id": "fecho", "anos": [2024, 2024], "cam": [ILHA, cam(-48.50, -27.63, 10.0, 45, -5)], "dur": 6.0},
]
ROT = {I["nasce"]: ("DESTERRO", -48.549, -27.596), I["capela"]: ("CAPELA DO DESTERRO", -48.549, -27.596),
       I["lagoa"]: ("LAGOA DA CONCEIÇÃO", -48.463, -27.602),
       I["santo"]: ("SANTO ANTÔNIO DE LISBOA", -48.5196, -27.507), I["baleia"]: ("ARMAÇÃO", -48.5077, -27.7368),
       I["espanha"]: ("CANASVIEIRAS", -48.465, -27.44), I["ribeirao"]: ("RIBEIRÃO DA ILHA", -48.5322, -27.6993),
       I["hercilio"]: ("PONTE HERCÍLIO LUZ", -48.5640, -27.5925), I["estreito"]: ("ESTREITO", -48.583, -27.592),
       I["ufsc"]: ("UFSC", -48.520, -27.601)}
EP = json.load(open(f"{AQUI}/assets/epoca/indice.json"))
def ep(i, leg=None):
    x = EP[i]; return {"src": f"assets/epoca/e{i:02d}.jpg", "legenda": leg or x["descricao"].split(" — ")[0][:70],
                       "credito": f"{x['autor'].split('(')[0].strip()} · {x['ano']} · domínio público (Wikimedia Commons)"}
IMG = {I["silva"]: ep(1, "Plano da ilha e do porto de Santa Catarina"), I["acor"]: ep(2, "Duas vistas de Santa Catarina, com navios"),
       I["espanha"]: ep(0, "Mapa espanhol da ilha, 1776"), I["cidade"]: ep(3, "Carta da ilha e do canal, 1830"),
       I["imperador"]: ep(5, "Desembarque de D. Pedro II na ilha"), I["censo"]: ep(11, "Vista de Desterro"),
       I["rebeldes"]: ep(9, "Uma rua de Desterro"), I["nome"]: ep(14, "Florianópolis por volta de 1903"),
       I["hercilio"]: ep(15, "Ponte Hercílio Luz em 1958")}
for b in blocos:
    b.pop("hud", None)
    if b["id"] in IMG:
        b["imagem"] = IMG[b["id"]]
    if b["id"] == "fecho":
        b["dur"] = 14.0
        b["galeria"] = {"fica": True, "titulo": "Imagens <b>da época</b>", "itens": [f"assets/epoca/e{i:02d}.jpg" for i in (0, 2, 5, 6, 8, 9, 11, 15)],
                        "creditos": "Victor Meirelles, Joseph Brüggemann, Vicente Pietro, Manuel Cristóbal del Canto, S. W. Schley, Correio da Manhã (Arquivo Nacional) · domínio público, via Wikimedia Commons"}
    if b["id"] in ROT:
        nm, lo, la = ROT[b["id"]]
        b["rotulos"] = [{"lon": lo, "lat": la, "texto": nm, "z": 70, "tam": 32}]
    if b["id"] == I["tri"] and False:
        b["rotulos"] = [{"lon": -48.5656, "lat": -27.4270, "texto": "ANHATOMIRIM", "z": 70, "tam": 28},
                        {"lon": -48.518, "lat": -27.432, "texto": "PONTA GROSSA", "z": 70, "tam": 28},
                        {"lon": -48.5604, "lat": -27.4746, "texto": "RATONES", "z": 70, "tam": 28}]

roteiro = {
    "titulo": "Florianópolis — de Desterro à capital, em 3D",
    "hud_de_bloco": I["cab"],
    "linha": {"de": 1500, "ate": 2024},
    "fim": {"titulo": "Florianópolis", "sub": "1673 – 2024", "marca": "INEMA<span>.CLUB</span>", "fica": True, "escuro": 0.25, "dura": 7.0},
    "longe": {"oeste": -48.66, "terra": [112, 120, 72], "mar": [62, 99, 143]},
    "regimes": [
        {"ano": 1500, "nome": "Terra dos carijós", "bandeira": "portugal"},
        {"ano": 1500.01, "nome": "Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1777.15, "nome": "Ocupação espanhola", "bandeira": "espanha"},
        {"ano": 1778.55, "nome": "Brasil Colônia", "bandeira": "portugal"},
        {"ano": 1815.95, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
        {"ano": 1822.7, "nome": "Império do Brasil", "bandeira": "imperio"},
        {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
        {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
        {"ano": 1893.78, "nome": "Governo rebelde (1893–94)", "bandeira": "republica"},
        {"ano": 1894.3, "nome": "República", "bandeira": "republica"},
        {"ano": 1960, "nome": "República", "bandeira": "brasil"}],
    "fortes": [{"id": "anhatomirim", "ano": 1739.5, "alt": 34, "rotulo": "Fortaleza de Anhatomirim", "sub": "1739 · 36 canhões"}, {"id": "ponta_grossa", "ano": 1740.3, "alt": 34, "rotulo": "Fortaleza de Ponta Grossa", "sub": "1740"}, {"id": "ratones", "ano": 1740.6, "alt": 34, "rotulo": "Fortaleza de Ratones", "sub": "1740"},
               {"id": "aracatuba", "ano": 1742}, {"id": "santana", "ano": 1763}],
        "linhas": [{"id": "hercilio", "ano": 1926.36, "desenha": 0.25, "sobe": 30, "torres": {"em": [0.29, 0.71], "alt": 45}}, {"id": "colombo", "ano": 1975.18, "desenha": 0.3, "sobe": 18},
               {"id": "pedroivo", "ano": 1991.18, "desenha": 0.3, "sobe": 18}],
    "areas": [{"id": "beira_mar", "ano0": 1963, "ano1": 1968, "sai": 8}, {"id": "baia_sul", "ano0": 1972, "ano1": 1974.5, "sai": 8}],
    "blocos": blocos,
}
json.dump(roteiro, open(f"{AQUI}/roteiro.json", "w"), ensure_ascii=False, indent=1)
print("roteiro", len(blocos), "blocos", round(sum(b["dur"] + (b.get("pulo", 1.6) if len(b["anos"]) == 3 else 0) for b in blocos), 1), "s")
