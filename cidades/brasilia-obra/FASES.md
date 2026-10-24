# A construção de Brasília — fases

Pedido do Nei (24/10/2026): "quero da construção de Brasília. Uma prévia do planejamento, de onde eram comandadas as coisas, também o que existia na região."

Cidade nova: o Nei aprova a fase 1 antes de qualquer publicação. Com o OK, a fase 1 entra na fila (`fila_cidades.py`) e a fase 2 (narrada) vai direto para o lives26.

## Roteiro (37 blocos, ~6 min, 1810 → 1960)
1. **O que existia:** Igreja de São Sebastião (1810), arraial de Mestre d'Armas/Planaltina (1859; o casario antigo nasce em `scripts/anos_antigos.py`), Brazlândia (1933, seta), Fazenda Bananal.
2. **Planejamento:** Missão Cruls chega a Mestre d'Armas (1892) → globo no meio do vídeo com o Quadrilátero Cruls (vértices do Relatório de 1894) → acampamento no Paranoá e a ideia do lago (1894) → Pedra Fundamental (1922, obelisco 3D) → Constituição de 1946 → Sítio Castanho (1955).
3. **Comando da obra:** Lei da Novacap (Rio, 1956) → JK na Fazenda do Gama → sede da Novacap na Candangolândia (galpões 3D) → Catetinho → Cidade Livre → cartão "De onde se mandava" (Rio · Catetinho · Novacap) → acampamentos da Vila Planalto → Plano Piloto → missa → barragem → Vila Amaury → Hospital JK → Lei 3.273 (data marcada).
4. **A obra:** contagem de 1958 → Alvorada → Igrejinha → rota de Anápolis → massacre da GEB → censo experimental → Congresso → lago → Esplanada → inauguração (41 meses) → censo de 1960 → fecho.

## Processo, do início ao fim
1. ⚙️ Dados: cópia de `cidades/capitais-bsb` (`dados/`, `assets/`); casario antigo: `CIDADE=brasilia-obra .venv/bin/python -I cidades/brasilia-obra/scripts/anos_antigos.py`.
2. 🤖 Pesquisa: `dados/pesquisa/eventos_novos.json`, `imagens_novas.json`, bloco novo no `RESUMO.md` (agente de pesquisa, páginas HTML, sem API).
3. 🧠 Roteiro: `python3 cidades/brasilia-obra/roteiro_obra.py` → `CIDADE=brasilia-obra .venv/bin/python -I cidades/capitais/scripts/limpa.py` → `CIDADE=brasilia-obra .venv/bin/python -I centro/scripts/gerar_cena.py`.
4. ⚙️ Quadros: `cd centro/motor && node render.mjs ../../cidades/brasilia-obra/cena --quadros t1,t2,…`.
5. ⚙️ Música + vídeo: `CIDADE=brasilia-obra .venv/bin/python -I scripts/montar_musica.py`; `cd centro/motor && bash render_trechos.sh ../../cidades/brasilia-obra/cena ../../cidades/brasilia-obra/final/video.mp4 60`; mux com `final/audio.wav`; versão `-bot` (< 49 MB).
6. 🤖 Revisor independente (`REVISAO-LISTA.md`), nota em `revisor-nota.py --fluxo historia-timelapse`.
7. 🧠 Bot v3 para o Nei; publicar só com OK.

## Motor (mudanças genéricas, valem para qualquer cidade)
- Globo: `poligonos` (contorno com preenchimento) e globo no meio do vídeo (`entra`, lista `C.globos`); o cartão fica por cima.
- `setas_tela`: etiqueta fixa na tela para lugar fora do mapa.
- Marcos novos: `galpao`, `obelisco`, `igrejinha` (marcos-capitais.js).

## Decisões
- "30 mil operários" saiu da tela (a fonte relida fala em 30 mil habitantes da Cidade Livre); inauguração = "41 meses".
- Contador: "sem contagem" até 1957; 1958 (28.804) entrou na série; nos cartões de contagem/censo o contador para no número do cartão.
- Fotos atuais (Igreja de São Sebastião, Pedra Fundamental, Hospital JK) têm "hoje (foto de 20xx)" na legenda.

## Estado
- 24/10/2026: v1 (revisor 5) → v2 (revisor novo 5) → v3 enviada ao bot v3; aguardando OK do Nei. Nada publicado.
- Correções v2/v3: rios do vale com nome, barragem = contrato 12/6/1957, Vila Amaury em 1959, lago enche de 1959,70 a 1959,95, contador parado nos cartões de censo, fecho sobre a Esplanada, capa 1810–1960, Asa Sul pioneira (550 prédios 1958–60 em `anos_antigos.py`), sede da Novacap no quadro, retângulo Cruls só na vista aberta.

## Pendências (limite do motor)
- Chão do cerrado borrado de perto (textura de 1 px ≈ 15–20 m): o "o que existia" fica no texto + rótulos; precisaria de textura mais fina ou relevo sombreado.
- Fazendas sem coordenada publicada: não estão no mapa.
- Cidade Livre e Vila Amaury sem casario próprio (sem dado de lote da época).
