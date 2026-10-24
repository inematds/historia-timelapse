# historia-timelapse

[![historia-timelapse](guia/assets/banner-es.jpg)](https://inematds.github.io/historia-timelapse/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

historia-timelapse es un conjunto de scripts que convierte la historia de una ciudad en un video 3D, en timelapse. Usa el relieve real del terreno y los edificios de OpenStreetMap: cada edificio "nace" en el año en que se ocupó su barrio, y la ciudad crece en pantalla junto con el contador de población del censo. Los hechos aparecen en tarjetas con número, explicación y fuente. Para usarlo necesitas una computadora con tarjeta de video, Python y Node, y una investigación histórica de la ciudad.

## 📖 Guía

Guía completa (landing + paso a paso): **https://inematds.github.io/historia-timelapse/guia/es/**

## 🎬 Videos

Canal [Aventuras INEMA](https://www.youtube.com/@aventurasinema) (en portugués). Cada ciudad sale en versión sin narración (tarjetas y música) y narrada.

- **Florianópolis** — de Desterro a capital (6 min): sin narración https://www.youtube.com/watch?v=auBCnC78Xtk · narrada https://www.youtube.com/watch?v=GBJRZvfHRVU
- **Río de Janeiro** — de 1500 a la metrópoli (7 min): sin narración https://www.youtube.com/watch?v=Ij4KsTN_SB0 · narrada https://www.youtube.com/watch?v=Useg7_N_38E
- **Itaguaí** — de la aldea al puerto (6 min): sin narración https://www.youtube.com/watch?v=NY7K_vMYLx8 · narrada https://www.youtube.com/watch?v=CNwLpoIqQ_A
- **Centro de Itaguaí** — las calles, de cerca (5 min): sin narración https://www.youtube.com/watch?v=dalR1xWPFlE · narrada https://www.youtube.com/watch?v=XiF00d20oi8
- **Porto Alegre con luz real** — relieve y edificios en Mitsuba, sombras reales (1min35, narrado): https://www.youtube.com/watch?v=WzPVdaal1OY
- **Porto Alegre** — 1772 a 2024, el piloto (1min35, narrado): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Cualquier lugar del mundo

Nada en el motor está atado a una ciudad o país: todo lo que cambia vive en `cidades/<id>/config.json` — `bbox`, `centro_antigo`, `pbf_url`/`pbf`, `municipio_osm`, `nivel_municipio`/`nivel_bairro` (niveles admin de OSM, por defecto 8/10), `regiao_bbox` (ventana NASA Blue Marble, por defecto ciudad ± 10°), `pais_microsoft`, `km_lon`, `vizinhos_anos`. En el guion: `globo.pais`, `globo.uf` + `globo.subdiv_arquivo`/`subdiv_prop`, `longe.auto`. Las banderas en `cidades/<id>/assets/bandeiras/` tienen prioridad sobre las del motor.

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1–3 | Pedido, config, investigación | `cidades/<id>/config.json` + `dados/pesquisa/` (todo número con fuente) | sesión |
| 4 | Datos | `CIDADE=<id> .venv/bin/python -I scripts/baixar_dados.py` y los scripts `extrai_*`/`prep_*`/`modelo_anos` | script |
| 5 | Guion y escena | `roteiro_<id>.py` → `scripts/gerar_cena.py` | sesión |
| 6 | Cuadros clave | `node motor/render.mjs <cena> --quadros t1,t2` | sesión |
| 7 | Video | `bash motor/render_trechos.sh <cena> <salida.mp4> 60` (5–18 min) | script |
| 7b | Luz real (opcional) | `bash motor/render_luz.sh <cena> <salida.mp4> 64` — Mitsuba en la GPU para relieve y edificios, el motor para HUD y tarjetas (~45 min por 95 s) | script |
| 8–12 | Revisión, narración, avatar, publicar, avisar | revisor independiente, `narrar.py`/`montar_narrada.py`, `montar_avatar.py`, `yt-pubx`, bot v3 | mixto |

## Render con luz real (Mitsuba)

Comparación medida de render en GPU (motor actual deck.gl × Blender × Mitsuba 3), con edificios, relieve y tiempo de cada ciudad (en portugués): [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md). El motor actual hace un video en 5–18 min; Mitsuba agrega luz y sombras de maqueta en 1–5 h; Blender tardaría días en esta máquina.

Cómo usarlo (en portugués): [docs/RENDER-LUZ-REAL.md](docs/RENDER-LUZ-REAL.md).

## Estructura

- `motor/` — página deck.gl (`mapa.html`) y render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte de OSM, relieve, edificios, año de cada edificio, efectos, escena, banda sonora (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (población, eventos, barrios, regímenes, imágenes), `roteiro.json`, `cena/`
- Los datos pesados (`dl/`, recortes, binarios, videos) quedan fuera de git y los scripts los regeneran.

INEMA.CLUB · https://inema.club
