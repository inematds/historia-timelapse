"""Baixa os dados públicos da cidade (arquivos, sem API) com os nomes que os scripts esperam:
- recorte regional do OSM (config "pbf_url" → config "pbf")
- blocos de relevo Copernicus GLO-30 que cobrem o "bbox" → dl/dem_S28_W049.tif …
- blocos do NASA Blue Marble que cobrem a janela regional → dl/bm_B2.jpg …
- (opcional, --microsoft) prédios da Microsoft Global ML Building Footprints → dl/msbuild/qk<quadkey>.csv.gz
Uso: CIDADE=<id> .venv/bin/python -I scripts/baixar_dados.py [--microsoft]"""
import csv, io, math, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cidade import *  # noqa
os.makedirs(f"{RAIZ}/dl/msbuild", exist_ok=True)


def baixa(url, dest):
    if os.path.exists(dest):
        print("já existe", dest); return
    print("baixando", url); urllib.request.urlretrieve(url, dest + ".parcial"); os.replace(dest + ".parcial", dest)


if CFG.get("pbf_url"):
    baixa(CFG["pbf_url"], f"{RAIZ}/{CFG['pbf']}")
for la in range(math.floor(S), math.floor(N) + 1):
    for lo in range(math.floor(W), math.floor(E) + 1):
        ns, ew = ("S", "N")[la >= 0], ("W", "E")[lo >= 0]
        nome = f"Copernicus_DSM_COG_10_{ns}{abs(la):02d}_00_{ew}{abs(lo):03d}_00_DEM"
        baixa(f"https://copernicus-dem-30m.s3.amazonaws.com/{nome}/{nome}.tif", f"{RAIZ}/dl/dem_{ns}{abs(la):02d}_{ew}{abs(lo):03d}.tif")
# satélite regional (NASA Blue Marble) para o globo e a cor da textura
from prep_terreno import regiao_bbox, bm_blocos, BM_URL  # noqa: E402
for nome, _, _ in bm_blocos(regiao_bbox()):
    baixa(BM_URL.format(nome), f"{RAIZ}/dl/bm_{nome}.jpg")
if "--microsoft" in sys.argv:
    def qk(lon, lat, z=9):
        x = int((lon + 180) / 360 * 2 ** z)
        y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2 ** z)
        return "".join(str((1 if x & (1 << (i - 1)) else 0) + (2 if y & (1 << (i - 1)) else 0)) for i in range(z, 0, -1))
    qs = {qk(W + (E - W) * a / 4, S + (N - S) * b / 4) for a in range(5) for b in range(5)}
    t = urllib.request.urlopen("https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv").read().decode()
    for r in csv.DictReader(io.StringIO(t)):
        if r["QuadKey"] in qs and r["Location"] == CFG.get("pais_microsoft", "Brazil"):
            baixa(r["Url"], f"{RAIZ}/dl/msbuild/qk{r['QuadKey']}.csv.gz")
print("ok")
