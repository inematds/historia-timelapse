# historia-timelapse

[![historia-timelapse](guia/assets/banner.jpg)](https://inematds.github.io/historia-timelapse/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O historia-timelapse é um conjunto de scripts que transforma a história de uma cidade num vídeo em 3D, em timelapse. Ele usa o relevo real do terreno e os prédios do OpenStreetMap: cada prédio "nasce" no ano em que o bairro dele foi ocupado, e a cidade cresce na tela junto com o contador de população do IBGE. Os acontecimentos aparecem em cartões com número, explicação e fonte. Para usar, você precisa de um computador com placa de vídeo, Python e Node, e de uma pesquisa histórica da cidade.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/historia-timelapse/guia/**

## 🎬 Vídeos

- Florianópolis — de Desterro à capital (6 min, sem narração): https://www.youtube.com/watch?v=auBCnC78Xtk
- Porto Alegre — 1772 a 2024 (narrado): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Estrutura

- `motor/` — página deck.gl (`mapa.html`) e render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte do OSM, relevo, prédios, ano de cada prédio, efeitos, cena, trilha (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (população, eventos, bairros, regimes, imagens), `roteiro.json`, `cena/`
- Dados pesados (`dl/`, recortes, binários, vídeos) ficam fora do git e são regenerados pelos scripts.

INEMA.CLUB · https://inema.club
