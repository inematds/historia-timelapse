# As capitais do Brasil: as 3 versões (pedido do Nei, 22/10/2026)

Um vídeo só, em 3 atos: **Salvador (1549–1763) → Rio de Janeiro (1763–1956) → Brasília (1956–hoje)**, contando em detalhe *como e por que* a capital mudou, com os prédios do poder desenhados em 3D.

| Fase | O que é | Estado |
|---|---|---|
| 1 | Sem narração, só música (`final/capitais-v5.mp4`, 12:42) | v1 e v5 no bot v3 (23/10/2026); aguardando o OK do Nei. Revisor independente: v1 5 → v2 6 → v3 7 → v4 6 → v5 7 |
| 2 | Fase 1 + narração na voz do Nei | depois do OK da fase 1 |
| 3 | Fase 2 + avatar do Nei | depois |

Regra nova (CLAUDE.md, 22/10): cidade nova → o Nei aprova a fase 1 antes de qualquer publicação.

## Como é montado
- Cada ato é uma "cidade" do motor: `cidades/capitais-ssa`, `capitais-rio`, `capitais-bsb`. Motor: **versão centro** (`centro/motor/`), com os prédios do poder em `centro/motor/marcos-capitais.js` (só acrescenta tipos: congresso, palacio_colunas, catedral_bsb, ministerio, itamaraty, torre_tv, catetinho, teatro_piramide, palacio, forte_redondo, elevador). Vitrine: `cd centro/motor && node vitrine.mjs --pagina vitrine-capitais.html …` → `cidades/capitais/vitrine/`.
- Peças comuns dos roteiros: `cidades/capitais/comum.py` (linha do tempo única 1500→2024, regimes nacionais, câmera com z do chão).
- O Rio reaproveita os dados de `cidades/rio` (assets e chao.npy copiados; não rodar extrai_*/prep_* em capitais-rio).
- Brasília: o Lago Paranoá foi tirado da textura e entra enchendo em 1959 (`C.aguas`, efeito novo do mapa.html da versão centro); os eixos do Plano Piloto vêm de `cidades/capitais-bsb/scripts/eixos.py`.
- Emenda: `cidades/capitais/montar.py` (fade pelo preto de 0,8 s entre os atos, música contínua −14 LUFS, 540p).

## O processo, do início ao fim
1. ⚙️ Dados: `baixar_dados.py --microsoft` e `cidades/capitais/dados.sh <ato>` (Salvador, Brasília); Brasília: tirar o lago de `agua.geojson` antes do `prep_terreno.py` e rodar `cidades/capitais-bsb/scripts/eixos.py` depois do `prep_efeitos.py`.
2. 🤖 Pesquisa (3 agentes, só páginas HTML): `cidades/<ato>/dados/pesquisa/` (eventos, predios, população, imagens DP).
3. 🧠 Roteiros: `python3 cidades/capitais-ssa/roteiro_ssa.py`, `cidades/capitais-rio/roteiro_rio_capital.py`, `cidades/capitais-bsb/roteiro_bsb.py` — rodar os três duas vezes (a linha do tempo junta as marcas dos três).
4. ⚙️ Lotes dos marcos e cena: `CIDADE=<ato> .venv/bin/python -I cidades/capitais/scripts/limpa.py` e `CIDADE=<ato> .venv/bin/python -I centro/scripts/gerar_cena.py`.
5. 🧠 Quadros-chave: `cd centro/motor && node render.mjs ../../cidades/<ato>/cena --quadros …` + `cidades/capitais/scripts/folha.py`.
6. ⚙️ Render: `bash centro/motor/render_trechos.sh cidades/<ato>/cena cidades/<ato>/final/video.mp4 60` (os 3 atos).
7. ⚙️ Montagem: `.venv/bin/python -I cidades/capitais/montar.py --versao N`.
8. 🤖 Revisão independente (`REVISAO-LISTA.md`) e nota em `revisor-nota.py --fluxo historia-timelapse`.
9. 🧠 540p no bot v3 para o Nei; YouTube só com OK.

## Pendências da fase 1 (revisor v5, 23/10/2026) — precisam de mudança no motor
- Rio colonial com a orla e os quarteirões de hoje (aterros) — a mesma lição do Rio: máscara de orla antiga.
- Chão do cerrado de Brasília borrado ("camuflagem") e relevo facetado de perto; névoa forte.
- Casario comum em volta dos marcos (Salvador 1549–1700) como caixas brancas: trocar por casas baixas de telhado até ~1850.
- Cruls (1892) e pedra fundamental (1922) só com seta: um voo curto ao Planalto desenharia o retângulo e a pedra.
- Contador do DF em 1957 cresce depois dos 12.283 (contagem sem mês) e contradiz o cartão de 1959 ("em 1957 eram 12.283").
- Eixos de Brasília passando por cima da foto do cartão de 1959; rótulo "↖ PLANALTO CENTRAL" encostado no subtítulo em 1956.
