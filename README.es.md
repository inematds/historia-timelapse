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

## Los dos formatos de video (y Blender)

El mismo guion (`cena.js`) sale en dos formatos. Tarjetas, contador, bandera, globo y efectos (inundaciones, sitios, rellenos) son iguales en los dos. Solo cambia la forma de dibujar el relieve y los edificios.

| | Formato estándar | Formato luz real | Blender (no usado) |
|---|---|---|---|
| Cómo dibuja | deck.gl en un Chrome sin ventana (`motor/render_trechos.sh`), luz simple de videojuego | híbrido: **Mitsuba 3** dibuja relieve y edificios con *path tracing* en la GPU, y el motor dibuja HUD y tarjetas encima (`motor/render_luz.sh`) | Cycles/EEVEE, programa 3D completo |
| Aspecto | mapa nítido, edificios con sombreado plano que aparecen en el año del barrio | sombras entre edificios, luz rebotada, volumen de maqueta, edificios **subiendo** | igual que Mitsuba (mismo principio de luz) |
| Tiempo por cuadro (1080p) | 0,07–0,11 s (medido) | ~0,75–0,95 s (medido: capa + Mitsuba) | ~40 s (medido, por procesador) |
| Porto Alegre, 95 s | **~5 min** (medido) | **~45 min** (medido: 7 min de capa + 30–38 min de Mitsuba) | ~32 h (estimado) |
| Florianópolis, 6,3 min | **~17 min** (medido) | ~3 h (estimado) | ~5 días (estimado) |
| ¿Usa la GPU de esta máquina? | sí (Vulkan) | sí (CUDA/OptiX, con eliminador de ruido) | no: no existe Blender oficial para Linux ARM64 con GPU, y aquí corre por software |
| Ejemplo | [Florianópolis](https://www.youtube.com/watch?v=auBCnC78Xtk) y las otras ciudades de arriba | [Porto Alegre con luz real](https://www.youtube.com/watch?v=WzPVdaal1OY) | — |

**Cuándo usar cada uno:**
- **Estándar:** todo video nuevo y toda revisión. Se corrige y se vuelve a ver en minutos.
- **Luz real:** versión destacada, después de aprobar la estándar. Cada revisión cuesta ~1 hora en vez de minutos.
- **Blender:** descartado. Solo usaría la GPU compilándolo para ARM64 con CUDA (días de trabajo, con riesgo de romperse), y aun así haría el mismo tipo de luz que Mitsuba ya hace por script.

**Qué es Mitsuba:** programa de render de código abierto, creado por investigadores de la EPFL (Suiza). Calcula la luz siguiendo los rayos como en la vida real, el mismo principio del Cycles de Blender. No tiene interfaz: la escena se arma con un script Python, como el resto del motor.

Detalles (en portugués): comparación medida por ciudad en [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md); cómo usar el formato luz real en [docs/RENDER-LUZ-REAL.md](docs/RENDER-LUZ-REAL.md).

## Estructura

- `motor/` — página deck.gl (`mapa.html`) y render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte de OSM, relieve, edificios, año de cada edificio, efectos, escena, banda sonora (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (población, eventos, barrios, regímenes, imágenes), `roteiro.json`, `cena/`
- Los datos pesados (`dl/`, recortes, binarios, videos) quedan fuera de git y los scripts los regeneran.

INEMA.CLUB · https://inema.club
