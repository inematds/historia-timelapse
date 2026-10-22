# Itaguaí — CENTRO: as 3 versões (pedido do Nei, 22/10/2026)

Versão sobre o **centro histórico** de Itaguaí (Matriz de 1729, colégio jesuíta, chafariz, Paço, estação-castelo, coreto, Patronato, catedral nova, Instituto Casa do Pai) que termina com uma **visão imaginada da cidade futura**. Não confundir com `cidades/itaguai/` (história do município, outro vídeo).

Motor desta versão: cópia em `centro/motor/` (o `motor/` original não foi mexido). Prédios históricos desenhados em 3D por `centro/motor/marcos.js` (plano de design: `centro/DESIGN-PREDIOS.md`, feito com o Fable).

| Fase | O que é | Estado |
|---|---|---|
| 1 | Sem narração, só música (`final/itaguai-centro-v1.mp4`) | render |
| 2 | Fase 1 + narração na voz do Nei (`narracao.json`, 31 falas; `final/itaguai-centro-narrado.mp4`) | áudio pronto (`final/audio-narrado.wav`) |
| 3 | Fase 2 + avatar do Nei embaixo da bandeira (estúdio HeyGen `historia-itaguai-centro-narrado-v1`, id 12888f6491874b61a0daf1f42bc13b39) | gerando no HeyGen |

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
