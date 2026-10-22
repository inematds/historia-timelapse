# historia-timelapse

[![historia-timelapse](guia/assets/banner-en.jpg)](https://inematds.github.io/historia-timelapse/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

historia-timelapse is a set of scripts that turns the history of a city into a 3D video, as a timelapse. It uses the real terrain and OpenStreetMap buildings: each building is "born" in the year its neighborhood was settled, and the city grows on screen along with the census population counter. Events appear on cards with a number, an explanation and a source. To use it you need a computer with a GPU, Python and Node, plus historical research on the city.

## 📖 Guide

Full guide (landing + step by step): **https://inematds.github.io/historia-timelapse/guia/en/**

## 🎬 Videos

- Florianópolis — from Desterro to capital (6 min, no narration): https://www.youtube.com/watch?v=auBCnC78Xtk
- Porto Alegre — 1772 to 2024 (narrated): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Layout

- `motor/` — deck.gl page (`mapa.html`) and renderer (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — OSM extract, terrain, buildings, year of each building, effects, scene, soundtrack (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (population, events, neighborhoods, regimes, images), `roteiro.json`, `cena/`
- Heavy data (`dl/`, extracts, binaries, videos) stays out of git and is rebuilt by the scripts.

INEMA.CLUB · https://inema.club
