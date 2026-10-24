# historia-timelapse

[![historia-timelapse](guia/assets/banner.jpg)](https://inematds.github.io/historia-timelapse/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O historia-timelapse é um conjunto de scripts que transforma a história de uma cidade num vídeo em 3D, em timelapse. Ele usa o relevo real do terreno e os prédios do OpenStreetMap: cada prédio "nasce" no ano em que o bairro dele foi ocupado, e a cidade cresce na tela junto com o contador de população do IBGE. Os acontecimentos aparecem em cartões com número, explicação e fonte. Para usar, você precisa de um computador com placa de vídeo, Python e Node, e de uma pesquisa histórica da cidade.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/historia-timelapse/guia/**

## 🎬 Vídeos

- Florianópolis — de Desterro à capital (6 min, sem narração): https://www.youtube.com/watch?v=auBCnC78Xtk
- Itaguaí — da aldeia ao porto (6 min, sem narração): https://www.youtube.com/watch?v=NY7K_vMYLx8
  - narrada: https://www.youtube.com/watch?v=CNwLpoIqQ_A · com apresentador: https://www.youtube.com/watch?v=X4u-dDnNc64
- Porto Alegre — 1772 a 2024 (narrado): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Qualquer lugar do mundo

O motor não tem nada preso a uma cidade ou país: tudo o que muda fica em `cidades/<id>/config.json`.
- `bbox`, `centro_antigo`, `pbf_url`/`pbf` (recorte Geofabrik da região), `municipio_osm`
- `nivel_municipio` / `nivel_bairro` (níveis `admin_level` do OSM; padrão 8 e 10, como no Brasil)
- `regiao_bbox` (janela do satélite NASA Blue Marble; padrão: cidade ± 10°), `pais_microsoft` (prédios da Microsoft)
- `km_lon` (opcional; padrão calculado pela latitude), `vizinhos_anos` (padrão 1930–2020)
- No roteiro: `globo.pais` (nome no Natural Earth, padrão Brazil), `globo.uf` + `globo.subdiv_arquivo`/`subdiv_prop` (estados/províncias, padrão `brasil-uf.geojson`), `longe.auto` (fundo além do mapa pelo contorno dos países)
- Bandeiras: `cidades/<id>/assets/bandeiras/<nome>.svg` tem prioridade sobre `motor/assets/bandeiras/`

## Render com luz real (Mitsuba)

Comparação medida de render na GPU (motor atual deck.gl × Blender × Mitsuba 3), com prédios, relevo e tempo de cada cidade: [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md). O motor atual faz um vídeo em 5–18 min; o Mitsuba dá sombra e luz de maquete em 1–5 h; o Blender, aqui, levaria dias.

## Estrutura

- `motor/` — página deck.gl (`mapa.html`) e render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte do OSM, relevo, prédios, ano de cada prédio, efeitos, cena, trilha (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (população, eventos, bairros, regimes, imagens), `roteiro.json`, `cena/`
- Dados pesados (`dl/`, recortes, binários, vídeos) ficam fora do git e são regenerados pelos scripts.

INEMA.CLUB · https://inema.club
