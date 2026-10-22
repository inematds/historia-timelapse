# historia-timelapse

[![historia-timelapse](guia/assets/banner-es.jpg)](https://inematds.github.io/historia-timelapse/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

historia-timelapse es un conjunto de scripts que convierte la historia de una ciudad en un video 3D, en timelapse. Usa el relieve real del terreno y los edificios de OpenStreetMap: cada edificio "nace" en el año en que se ocupó su barrio, y la ciudad crece en pantalla junto con el contador de población del censo. Los hechos aparecen en tarjetas con número, explicación y fuente. Para usarlo necesitas una computadora con tarjeta de video, Python y Node, y una investigación histórica de la ciudad.

## 📖 Guía

Guía completa (landing + paso a paso): **https://inematds.github.io/historia-timelapse/guia/es/**

## 🎬 Videos

- Florianópolis — de Desterro a capital (6 min, sin narración): https://www.youtube.com/watch?v=auBCnC78Xtk
- Itaguaí — de la aldea al puerto (6 min, sin narración): https://www.youtube.com/watch?v=NY7K_vMYLx8
  - narrada: https://www.youtube.com/watch?v=CNwLpoIqQ_A · con presentador: https://www.youtube.com/watch?v=X4u-dDnNc64
- Porto Alegre — 1772 a 2024 (narrado): https://www.youtube.com/watch?v=MBBZXnTh6Lg

## Cualquier lugar del mundo

Nada en el motor está atado a una ciudad o país: todo lo que cambia vive en `cidades/<id>/config.json` — `bbox`, `centro_antigo`, `pbf_url`/`pbf`, `municipio_osm`, `nivel_municipio`/`nivel_bairro` (niveles admin de OSM, por defecto 8/10), `regiao_bbox` (ventana NASA Blue Marble, por defecto ciudad ± 10°), `pais_microsoft`, `km_lon`, `vizinhos_anos`. En el guion: `globo.pais`, `globo.uf` + `globo.subdiv_arquivo`/`subdiv_prop`, `longe.auto`. Las banderas en `cidades/<id>/assets/bandeiras/` tienen prioridad sobre las del motor.

## Estructura

- `motor/` — página deck.gl (`mapa.html`) y render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte de OSM, relieve, edificios, año de cada edificio, efectos, escena, banda sonora (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (población, eventos, barrios, regímenes, imágenes), `roteiro.json`, `cena/`
- Los datos pesados (`dl/`, recortes, binarios, videos) quedan fuera de git y los scripts los regeneran.

INEMA.CLUB · https://inema.club
