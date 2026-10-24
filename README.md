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

## O processo, do início ao fim (12 passos)

🧠 = sessão com o Nei · ⚙️ = script (zero token) · 🤖 = `claude -p` / revisor independente

| # | Passo | Comando / o que acontece | Quem |
|---|---|---|---|
| 1 | Pedido | o Nei diz a cidade (ou o lugar) e o canal | Nei |
| 2 | Config | `cidades/<id>/config.json` copiado do `floripa` (bbox, recorte Geofabrik, município) | 🧠 |
| 3 | Pesquisa | `cidades/<id>/dados/pesquisa/` (população, eventos, bairros, regimes, imagens com crédito); todo número com fonte | 🧠 |
| 4 | Dados | `CIDADE=<id> .venv/bin/python -I scripts/baixar_dados.py`, depois `extrai_osm`, `extrai_msbuild`, `extrai_feicoes`, `prep_terreno`, `prep_predios`, `modelo_anos`, `prep_efeitos` | ⚙️ |
| 5 | Roteiro e cena | `cidades/<id>/roteiro_<id>.py` (modelo: `roteiro_floripa.py`) → `scripts/gerar_cena.py` | 🧠 |
| 6 | Quadros-chave | `cd motor && node render.mjs ../cidades/<id>/cena --quadros t1,t2,…` → mostrar ao Nei e seguir | 🧠 |
| 7 | Vídeo (fase 1) | `scripts/montar_musica.py` + `bash motor/render_trechos.sh cidades/<id>/cena cidades/<id>/final/video.mp4 60` (5–18 min) | ⚙️ |
| 7b | Vídeo com luz real (opcional) | `bash motor/render_luz.sh cidades/<id>/cena cidades/<id>/final/<id>-mitsuba-video.mp4 64`: Mitsuba na GPU desenha relevo e prédios (sombra, prédios subindo), o motor desenha HUD e cartões por cima (~45 min por 95 s). Ver [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md) | ⚙️ |
| 8 | Revisão | revisor independente com `REVISAO-LISTA.md`; nota em `revisor-nota.py --fluxo historia-timelapse` | 🤖 |
| 9 | Fase 2 (narrada) | `narracao.json` → `narrar.py` → `qa_narracao.py` → `montar_narrada.py` (mesmo vídeo, outra trilha) | ⚙️ |
| 10 | Fase 3 (avatar) | avatar do Nei no estúdio HeyGen (OK por produção) → `montar_avatar.py` | 🧠 |
| 11 | Publicar | com OK do Nei: fase 2 direto no lives26 (`yt-pubx publicar … --canal lives26`), fase 1 na fila (`fila_cidades.py --add`) | ⚙️ |
| 12 | Avisar | 540p no bot v3 (`~/projetos/r7ex/bin/enviar_bot_v3.mjs`), link no inemaytbot | ⚙️ |

## Render com luz real (Mitsuba)

Comparação medida de render na GPU (motor atual deck.gl × Blender × Mitsuba 3), com prédios, relevo e tempo de cada cidade: [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md). O motor atual faz um vídeo em 5–18 min; o Mitsuba dá sombra e luz de maquete em 1–5 h; o Blender, aqui, levaria dias.

## Estrutura

- `motor/` — página deck.gl (`mapa.html`) e render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte do OSM, relevo, prédios, ano de cada prédio, efeitos, cena, trilha (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (população, eventos, bairros, regimes, imagens), `roteiro.json`, `cena/`
- Dados pesados (`dl/`, recortes, binários, vídeos) ficam fora do git e são regenerados pelos scripts.

INEMA.CLUB · https://inema.club
