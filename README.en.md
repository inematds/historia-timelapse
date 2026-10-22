# historia-timelapse

[![historia-timelapse](guia/assets/banner-en.jpg)](https://inematds.github.io/historia-timelapse/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

historia-timelapse is a set of scripts that turns the history of a city into a 3D video, as a timelapse. It uses the real terrain and OpenStreetMap buildings: each building is "born" in the year its neighborhood was settled, and the city grows on screen along with the census population counter. Events appear on cards with a number, an explanation and a source. To use it you need a computer with a GPU, Python and Node, plus historical research on the city.

## 📖 Guide

Full guide (landing + step by step): **https://inematds.github.io/historia-timelapse/guia/en/**

## 🎬 Videos

- Florianópolis — from Desterro to capital (6 min, no narration): https://www.youtube.com/watch?v=auBCnC78Xtk
- Itaguaí — from village to port (6 min, no narration): https://www.youtube.com/watch?v=NY7K_vMYLx8
  - narrated: https://www.youtube.com/watch?v=CNwLpoIqQ_A · with presenter: https://www.youtube.com/watch?v=X4u-dDnNc64
- Porto Alegre — 1772 to 2024 (narrated): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Anywhere in the world

Nothing in the engine is tied to one city or country: everything that changes lives in `cidades/<id>/config.json` — `bbox`, `centro_antigo`, `pbf_url`/`pbf`, `municipio_osm`, `nivel_municipio`/`nivel_bairro` (OSM admin levels, default 8/10), `regiao_bbox` (NASA Blue Marble window, default city ± 10°), `pais_microsoft`, `km_lon`, `vizinhos_anos`. In the script: `globo.pais`, `globo.uf` + `globo.subdiv_arquivo`/`subdiv_prop`, `longe.auto`. Flags in `cidades/<id>/assets/bandeiras/` override the engine ones.

## Layout

- `motor/` — deck.gl page (`mapa.html`) and renderer (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — OSM extract, terrain, buildings, year of each building, effects, scene, soundtrack (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (population, events, neighborhoods, regimes, images), `roteiro.json`, `cena/`
- Heavy data (`dl/`, extracts, binaries, videos) stays out of git and is rebuilt by the scripts.

INEMA.CLUB · https://inema.club
