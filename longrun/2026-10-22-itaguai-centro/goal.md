# Goal — itaguai-centro

- **Início:** 2026-10-22 05:46 · **Agente:** Claude (sessão com o Nei)
- **Tetos:** render em trechos de 60 s, MemoryMax 24G nos scripts de dados

## Pedido do Nei (22/10/2026, citado)
"quero uma versao sobre o centro de itaguai, e tambem sobre a casa do pai e demiaqs predios historicos do centro, termina com uma visao como poderia ser a cidade futura (eu fiz outra da historia da cidade, ara nao confundir.) tenta dar o melhro em designer dos predios nem q vc usa o fable para ahjudar planerjar e se mexer no motor faca copia. coloque no lives26 as 3 fases de video ou versoes."

## Resultado
Três vídeos da versão CENTRO de Itaguaí (fase 1 música, fase 2 narração do Nei, fase 3 avatar) publicados no lives26, com prédios históricos modelados em 3D e final com a cidade futura.

## Travas
- `motor/` e `cidades/itaguai/` intocados (outro terminal). Motor desta versão: `centro/motor/`.
- Publicar só depois de mostrar quadros (aviso, não trava) — o pedido já manda publicar as 3 fases.
- "Casa do Pai": não inventar; sem dado, perguntar ao Nei.

## Critérios de pronto
**Função**
- [ ] `ls cidades/itaguai-centro/final/{fase1,fase2,fase3}.mp4` → 3 arquivos; `ffprobe` duração > 120 s cada
- [ ] `grep -c '"tipo"' cidades/itaguai-centro/cena/cena.js` → marcos ≥ 6 (prédios históricos modelados)
- [ ] último bloco do roteiro tem id `futuro` e cartão com "visão" (não é dado)
- [ ] `CIDADE=itaguai-centro .venv/bin/python -I scripts/qa_narracao.py` → sem falha
- [ ] 3 links do YouTube no lives26 anotados em `cidades/itaguai-centro/FASES.md`

**Regressão**
- [ ] `git diff --stat -- motor/ cidades/itaguai/` → vazio (feito por mim)

**Limite**
- [ ] logs do render sem "allocation failed|pageerror|Worker exception"
- [ ] todo cartão com campo fonte (ou marcado como visão)

**Teste rápido:** `cd centro/motor && node render.mjs ../../cidades/itaguai-centro/cena <q> --quadros t1,t2`
**Teste completo:** `bash centro/motor/render_trechos.sh cidades/itaguai-centro/cena cidades/itaguai-centro/final/video.mp4 60`
