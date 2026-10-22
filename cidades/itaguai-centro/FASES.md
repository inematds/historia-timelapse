# Itaguaí — CENTRO: as 3 versões (pedido do Nei, 22/10/2026)

Versão sobre o **centro histórico** de Itaguaí (Matriz de 1729, colégio jesuíta, chafariz, Paço, estação-castelo, coreto, Patronato, catedral nova, Instituto Casa do Pai) que termina com uma **visão imaginada da cidade futura**. Não confundir com `cidades/itaguai/` (história do município, outro vídeo).

Motor desta versão: cópia em `centro/motor/` (o `motor/` original não foi mexido). Prédios históricos desenhados em 3D por `centro/motor/marcos.js` (plano de design: `centro/DESIGN-PREDIOS.md`, feito com o Fable).

| Fase | O que é | Estado |
|---|---|---|
| 1 | Sem narração, só música (`final/itaguai-centro-v1.mp4`, 321 s) | pronto, enviado ao bot v3; lives26 bloqueado (YouTube: limite diário de uploads) — plano em `~/.local/share/yt-pubx/trabalhos/20261022-071116-itaguai-centro-v1-mp4/plano.json` |
| 2 | Fase 1 + narração na voz do Nei (`narracao.json`, 31 falas; `final/itaguai-centro-narrado.mp4`) | pronto, enviado ao bot v3; lives26 bloqueado (mesmo limite) — plano em `~/.local/share/yt-pubx/trabalhos/20261022-080404-itaguai-centro-narrado-mp4/plano.json` |
| 3 | Fase 2 + avatar do Nei embaixo da bandeira (estúdio HeyGen `historia-itaguai-centro-narrado-v1`, id 12888f6491874b61a0daf1f42bc13b39) | pronto (`final/itaguai-centro-avatar.mp4`), enviado ao bot v3; o Nei pediu só as fases 1 e 2 no lives26 |

## Refazer do zero
1. Dados: `cidades/itaguai-centro/dados.sh` (scripts do motor com `CIDADE=itaguai-centro`), depois `centro/scripts/extrai_ruas.py` e `SO_PRACAS=1 centro/scripts/textura_ruas.py`.
2. Cena: `bash centro/refaz.sh` (roteiro → anos dos prédios → `limpa_marcos.py` → `futuro_sitios.py` → roteiro → `centro/scripts/gerar_cena.py`).
3. Quadros: `cd centro/motor && node render.mjs ../../cidades/itaguai-centro/cena --quadros t1,t2`.
4. Vídeo: `bash centro/motor/render_trechos.sh cidades/itaguai-centro/cena cidades/itaguai-centro/final/video.mp4 60`, música `scripts/montar_musica.py`, narração `scripts/narrar.py` + `qa_narracao.py` + `montar_narrada.py`, avatar `scripts/montar_avatar.py`.

## Decisões
- `centro_antigo` = Matriz (-43.7792, -22.8676); o do config municipal fica 1,7 km ao norte.
- Prédios comuns (OSM + Microsoft) em tom neutro; marcos coloridos. Ruas vetoriais nascem com as casas em volta.
- "Casa do Pai" = Instituto Casa do Pai (ONG de 2007, Monte Serrat). Não é prédio histórico; foi desenhado sem foto. **Pergunta aberta ao Nei:** era isso ou a casa do pai dele / outro casarão?
- Futuro (2026–2050?): marcado na tela como "VISÃO DE FUTURO · imaginação, não é projeto aprovado". Oficial hoje só o porto (ITG02, Tecar).
- A Matriz tem coordenada aproximada (±50 m) e os marcos não têm medidas oficiais (estimadas de fotos).

## Publicar quando o limite do canal liberar
`cd ~/projetos/yt-pubx && ./yt-pubx publicar ~/projetos/historia-timelapse/cidades/itaguai-centro/final/itaguai-centro-v1.mp4 --plano <plano da fase 1>` e o mesmo para `itaguai-centro-narrado.mp4`.

## Revisão independente
Notas 5 → 6 → 6 (reprovado). Pendente da 3ª rodada: período colonial com campo vazio, etiqueta "tombada pelo INEPAC" antes de 2006, legenda "1823" no bloco de 1818, contador de habitantes cai de 1841 a 1873 sem explicação na hora, VLT pouco visível no futuro, sobrado de Quintino sem prédio (local não achado).
