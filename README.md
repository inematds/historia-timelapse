# historia-timelapse

Timelapse 3D da história de uma cidade: o mapa real (relevo + prédios do OpenStreetMap) mostra a cidade nascendo e crescendo ano a ano, com bandeira/regime, ano e população na tela e cartões de eventos com fonte. É inspirado no formato do canal referência (análise em `docs/ANALISE-FORMATO.md`).

Primeira cidade: **Porto Alegre** (piloto). Tudo é local, sem API paga e sem custo.

## Como funciona

| Etapa | Script | Saída |
|---|---|---|
| Recorte do OSM (prédios, água, ruas, bairros, município) | `scripts/extrai_osm.py dl/sul.osm.pbf dados/brutos` | `dados/brutos/*` |
| Muro/diques do OSM | `scripts/extrai_muro.py dl/sul.osm.pbf dados/brutos/muro.geojson` | `muro.geojson` |
| Relevo (Copernicus 30 m) + textura | `scripts/prep_terreno.py` | `motor/assets/elev.png`, `textura.jpg`, `dados/chao.npy` |
| Prédios em binário | `scripts/prep_predios.py` | `motor/assets/pred_*.f32/u32` |
| Ano de nascimento de cada prédio (bairros + curva do IBGE) | `scripts/modelo_anos.py` | `pred_ano.f32` |
| Efeitos (muro, aterro) | `scripts/prep_efeitos.py` | `motor/assets/efeitos.json` |
| Roteiro → cena | `scripts/gerar_cena.py` | `cenas/poa/cena.js` |
| Quadros de teste | `cd motor && node render.mjs ../cenas/poa --quadros 0,15,30` | `cenas/poa/q_*.jpg` |
| Vídeo | `cd motor && node render.mjs ../cenas/poa ../final/video.mp4` | `final/video.mp4` |
| Narração (opcional, voz nei local) | `narracao/narrar.py`, `scripts/qa_narracao.py`, `scripts/montar_audio.py` | `final/audio.wav` |

Motor: `motor/mapa.html` (deck.gl 9.0.38 local: TerrainLayer, prédios extrudados filtrados por ano na GPU, água das cheias, tropas, aterro, muro, rótulos, HUD) + `motor/render.mjs` (Playwright + Chrome/Vulkan, servidor HTTP local, ~0,08 s por quadro em 1920×1080).

## Reproduzir do zero

```bash
python3 -m venv .venv && .venv/bin/pip install osmium tifffile imagecodecs shapely numpy pyproj scipy pillow
(cd motor && npm i)
# dados públicos (arquivos, não API): Geofabrik sul-latest.osm.pbf e Copernicus DEM GLO-30 S30/S31 × W051/W052 → dl/
```

Dados pesados (`dl/`, `dados/brutos/`, binários do motor, `final/`) ficam fora do git e são regenerados pelos scripts.

## Pesquisa

`dados/pesquisa/`: população (censos IBGE + estimativas coloniais), eventos com fonte, data de ocupação dos bairros, regimes/bandeiras. Resumo e divergências entre fontes em `dados/pesquisa/RESUMO.md`.
