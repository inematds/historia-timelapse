# historia-timelapse

[![historia-timelapse](guia/assets/banner-en.jpg)](https://inematds.github.io/historia-timelapse/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

historia-timelapse is a set of scripts that turns the history of a city into a 3D video, as a timelapse. It uses the real terrain and OpenStreetMap buildings: each building is "born" in the year its neighborhood was settled, and the city grows on screen along with the census population counter. Events appear on cards with a number, an explanation and a source. To use it you need a computer with a GPU, Python and Node, plus historical research on the city.

## 📖 Guide

Full guide (landing + step by step): **https://inematds.github.io/historia-timelapse/guia/en/**

## 🎬 Videos

[Aventuras INEMA](https://www.youtube.com/@aventurasinema) channel (in Portuguese). Each city comes in a version without narration (cards and music) and a narrated one.

- **Florianópolis** — from Desterro to capital (6 min): no narration https://www.youtube.com/watch?v=auBCnC78Xtk · narrated https://www.youtube.com/watch?v=GBJRZvfHRVU
- **Rio de Janeiro** — from 1500 to the metropolis (7 min): no narration https://www.youtube.com/watch?v=Ij4KsTN_SB0 · narrated https://www.youtube.com/watch?v=Useg7_N_38E
- **Itaguaí** — from village to port (6 min): no narration https://www.youtube.com/watch?v=NY7K_vMYLx8 · narrated https://www.youtube.com/watch?v=CNwLpoIqQ_A
- **Downtown Itaguaí** — the streets, up close (5 min): no narration https://www.youtube.com/watch?v=dalR1xWPFlE · narrated https://www.youtube.com/watch?v=XiF00d20oi8
- **Porto Alegre with realistic lighting** — terrain and buildings in Mitsuba, real shadows (1min35, narrated): https://www.youtube.com/watch?v=WzPVdaal1OY
- **Porto Alegre** — 1772 to 2024, the pilot (1min35, narrated): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Anywhere in the world

Nothing in the engine is tied to one city or country: everything that changes lives in `cidades/<id>/config.json` — `bbox`, `centro_antigo`, `pbf_url`/`pbf`, `municipio_osm`, `nivel_municipio`/`nivel_bairro` (OSM admin levels, default 8/10), `regiao_bbox` (NASA Blue Marble window, default city ± 10°), `pais_microsoft`, `km_lon`, `vizinhos_anos`. In the script: `globo.pais`, `globo.uf` + `globo.subdiv_arquivo`/`subdiv_prop`, `longe.auto`. Flags in `cidades/<id>/assets/bandeiras/` override the engine ones.

## The process, start to finish

| # | Step | Command | Who |
|---|---|---|---|
| 1–3 | Request, config, research | `cidades/<id>/config.json` + `dados/pesquisa/` (every number with a source) | session |
| 4 | Data | `CIDADE=<id> .venv/bin/python -I scripts/baixar_dados.py` and the `extrai_*`/`prep_*`/`modelo_anos` scripts | script |
| 5 | Script and scene | `roteiro_<id>.py` → `scripts/gerar_cena.py` | session |
| 6 | Key frames | `node motor/render.mjs <cena> --quadros t1,t2` | session |
| 7 | Video | `bash motor/render_trechos.sh <cena> <out.mp4> 60` (5–18 min) | script |
| 7b | Realistic light (optional) | `bash motor/render_luz.sh <cena> <out.mp4> 64` — Mitsuba on the GPU for terrain and buildings, the engine for HUD and cards (~45 min per 95 s) | script |
| 8–12 | Review, narration, avatar, publish, notify | independent reviewer, `narrar.py`/`montar_narrada.py`, `montar_avatar.py`, `yt-pubx`, bot v3 | mixed |

## Realistic lighting render (Mitsuba)

Measured GPU render comparison (current deck.gl engine × Blender × Mitsuba 3), with buildings, terrain and time for each city (in Portuguese): [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md). The current engine renders a video in 5–18 min; Mitsuba adds model-like light and shadows in 1–5 h; Blender would take days on this machine.

How to use (in Portuguese): [docs/RENDER-LUZ-REAL.md](docs/RENDER-LUZ-REAL.md).

## Layout

- `motor/` — deck.gl page (`mapa.html`) and renderer (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — OSM extract, terrain, buildings, year of each building, effects, scene, soundtrack (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (population, events, neighborhoods, regimes, images), `roteiro.json`, `cena/`
- Heavy data (`dl/`, extracts, binaries, videos) stays out of git and is rebuilt by the scripts.

INEMA.CLUB · https://inema.club
