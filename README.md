# historia-timelapse

[![historia-timelapse](guia/assets/banner.jpg)](https://inematds.github.io/historia-timelapse/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O historia-timelapse é um conjunto de scripts que transforma a história de uma cidade num vídeo em 3D, em timelapse. Ele usa o relevo real do terreno e os prédios do OpenStreetMap: cada prédio "nasce" no ano em que o bairro dele foi ocupado, e a cidade cresce na tela junto com o contador de população do IBGE. Os acontecimentos aparecem em cartões com número, explicação e fonte. Para usar, você precisa de um computador com placa de vídeo, Python e Node, e de uma pesquisa histórica da cidade.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/historia-timelapse/guia/**

## 🎬 Vídeos

Canal [Aventuras INEMA](https://www.youtube.com/@aventurasinema). Cada cidade sai em versão sem narração (cartões e música) e narrada.

- **Florianópolis** — de Desterro à capital (6 min): sem narração https://www.youtube.com/watch?v=auBCnC78Xtk · narrada https://www.youtube.com/watch?v=GBJRZvfHRVU
- **Rio de Janeiro** — de 1500 à metrópole (7 min): sem narração https://www.youtube.com/watch?v=Ij4KsTN_SB0 · narrada https://www.youtube.com/watch?v=Useg7_N_38E
- **Itaguaí** — da aldeia ao porto (6 min): sem narração https://www.youtube.com/watch?v=NY7K_vMYLx8 · narrada https://www.youtube.com/watch?v=CNwLpoIqQ_A
- **Centro de Itaguaí** — as ruas, de perto (5 min): sem narração https://www.youtube.com/watch?v=dalR1xWPFlE · narrada https://www.youtube.com/watch?v=XiF00d20oi8
- **Porto Alegre com luz real** — relevo e prédios no Mitsuba, sombras de verdade (1min35, narrado): https://www.youtube.com/watch?v=WzPVdaal1OY
- **Porto Alegre** — 1772 a 2024, o piloto (1min35, narrado): https://www.youtube.com/watch?v=MBBZXnTh6Lg

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
| 7b | Vídeo com luz real (opcional) | `bash motor/render_luz.sh cidades/<id>/cena cidades/<id>/final/<id>-mitsuba-video.mp4 64`: Mitsuba na GPU desenha relevo e prédios (sombra, prédios subindo), o motor desenha HUD e cartões por cima (~45 min por 95 s). Como usar: [docs/RENDER-LUZ-REAL.md](docs/RENDER-LUZ-REAL.md); comparação: [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md) | ⚙️ |
| 8 | Revisão | revisor independente com `REVISAO-LISTA.md`; nota em `revisor-nota.py --fluxo historia-timelapse` | 🤖 |
| 9 | Fase 2 (narrada) | `narracao.json` → `narrar.py` → `qa_narracao.py` → `montar_narrada.py` (mesmo vídeo, outra trilha) | ⚙️ |
| 10 | Fase 3 (avatar) | avatar do Nei no estúdio HeyGen (OK por produção) → `montar_avatar.py` | 🧠 |
| 11 | Publicar | com OK do Nei: fase 2 direto no lives26 (`yt-pubx publicar … --canal lives26`), fase 1 na fila (`fila_cidades.py --add`) | ⚙️ |
| 12 | Avisar | 540p no bot v3 (`~/projetos/r7ex/bin/enviar_bot_v3.mjs`), link no inemaytbot | ⚙️ |

## Os dois formatos de vídeo (e o Blender)

O mesmo roteiro (`cena.js`) sai em dois formatos. Cartões, contador, bandeira, globo e efeitos (cheias, cercos, aterros) são iguais nos dois. Muda só o jeito de desenhar o relevo e os prédios.

| | Formato padrão | Formato luz real | Blender (não usado) |
|---|---|---|---|
| Como desenha | deck.gl num Chrome sem janela (`motor/render_trechos.sh`), luz simples de jogo | híbrido: o **Mitsuba 3** desenha relevo e prédios por *path tracing* na GPU, e o motor desenha HUD e cartões por cima (`motor/render_luz.sh`) | Cycles/EEVEE, programa 3D completo |
| Visual | mapa nítido, prédios com sombreado plano, aparecem no ano do bairro | sombra entre prédios, luz rebatida, volume de maquete, prédios **subindo** | o mesmo do Mitsuba (mesmo princípio de luz) |
| Tempo por quadro (1080p) | 0,07–0,11 s (medido) | ~0,75–0,95 s (medido: camada + Mitsuba) | ~40 s (medido, por processador) |
| Porto Alegre, 95 s | **~5 min** (medido) | **~45 min** (medido: 7 min de camada + 30–38 min de Mitsuba) | ~32 h (estimado) |
| Florianópolis, 6,3 min | **~17 min** (medido) | ~3 h (estimado) | ~5 dias (estimado) |
| Usa a GPU desta máquina? | sim (Vulkan) | sim (CUDA/OptiX, com removedor de ruído) | não: não existe Blender oficial para Linux ARM64 com GPU, e o daqui roda por software |
| Exemplo | [Florianópolis](https://www.youtube.com/watch?v=auBCnC78Xtk) e as outras cidades acima | [Porto Alegre com luz real](https://www.youtube.com/watch?v=WzPVdaal1OY) | — |

**Quando usar cada um:**
- **Padrão:** todo vídeo novo e toda revisão. Corrige e vê de novo em minutos.
- **Luz real:** versão de destaque, depois que o padrão já foi aprovado. Cada revisão passa a custar ~1 hora em vez de minutos.
- **Blender:** fora. Só rodaria na GPU compilando o Blender para ARM64 com CUDA (dias de trabalho, com risco de quebrar), e mesmo assim faria o mesmo tipo de luz que o Mitsuba já faz por script.

**O que é o Mitsuba:** programa de render de código aberto, feito por pesquisadores da EPFL (Suíça). Calcula a luz seguindo os raios como na vida real, o mesmo princípio do Cycles do Blender. Não tem tela: a cena é montada por script Python, como o resto do motor.

Detalhes: comparação medida por cidade em [docs/RENDER-GPU-ALTERNATIVAS.md](docs/RENDER-GPU-ALTERNATIVAS.md); como usar o formato luz real em [docs/RENDER-LUZ-REAL.md](docs/RENDER-LUZ-REAL.md).

## Estrutura

- `motor/` — página deck.gl (`mapa.html`) e render (`render.mjs`, Playwright + Chrome/GPU)
- `scripts/` — recorte do OSM, relevo, prédios, ano de cada prédio, efeitos, cena, trilha (`CIDADE=<id>`)
- `cidades/<id>/` — `config.json`, `dados/pesquisa/` (população, eventos, bairros, regimes, imagens), `roteiro.json`, `cena/`
- Dados pesados (`dl/`, recortes, binários, vídeos) ficam fora do git e são regenerados pelos scripts.

INEMA.CLUB · https://inema.club
