# Florianópolis: as 3 versões (pedido do Nei, 22/10/2026)

O vídeo-base (fase 1) não muda. As fases 2 e 3 são camadas por cima do mesmo `final/video-v4.mp4`, nos mesmos tempos.

| Fase | O que é | Estado |
|---|---|---|
| 1 | Vídeo sem narração, só música (`final/floripa-v4.mp4`, 375,8 s) | publicado no lives26: https://www.youtube.com/watch?v=auBCnC78Xtk |
| 2 | Fase 1 + narração na voz do Nei (camada de áudio, sem avatar) | publicado no lives26: https://www.youtube.com/watch?v=GBJRZvfHRVU (`final/floripa-narrado.mp4`) |
| 3 | Fase 2 + avatar do Nei pequeno **à direita, logo acima do INEMA.CLUB**, só depois do globo (no globo só a voz; no fecho sobe acima da galeria) | v2 pronta (`final/floripa-avatar-v2.mp4`, bot v3 msg 2319); YouTube recusou em 22/10 (limite diário de uploads do canal Aventuras), publicar no lives26 quando liberar. A v1 (embaixo da bandeira, adGn7FY6wGc) foi reprovada e removida |

Publicar as três no lives26 (`yt-pubx publicar … --canal aventuras`), links no inemaytbot dizendo "lives26 (Aventuras)", 540p no bot v3.

## Fase 2: narração (regra do motor no `CLAUDE.md`)
1. Escrever `cidades/floripa/narracao.json` (`{id_do_bloco: texto}`). Ids e tempos estão em `cena/cena.js` → `blocos_t`. Cada fala ≤ duração do bloco − 1 s (~16–18 palavras); blocos sem fala são permitidos. A fala explica o porquê e não lê o cartão. Anos por extenso.
2. `CIDADE=floripa .venv/bin/python -I scripts/narrar.py`: voz `nei` (chatterbox, via cardshorts).
3. `CIDADE=floripa .venv/bin/python -I scripts/qa_narracao.py`: confere a transcrição.
4. `CIDADE=floripa .venv/bin/python -I scripts/montar_narrada.py`: música abaixa sob a voz, −14 LUFS, mesmo `video.mp4`.
5. Não rodar `gerar_cena.py` com tempos de narração: na versão narrada os tempos são os da fase 1.

## Fase 3: avatar à direita, acima do INEMA.CLUB (refeita em 22/10/2026)
- Posição no `config.json` → `avatar` {x 1610, y 752, lado 250, so_voz [globo], pos_bloco {fecho: y 586}, video_base}. O vídeo-base da fase 3 é renderizado de `cena-avatar/` (cena + `cp_direita: 340`) para o texto pequeno não passar sob o avatar: `bash motor/render_trechos.sh cidades/floripa/cena-avatar cidades/floripa/final/avatar-base/video.mp4 60`.

### Versão antiga (reprovada): avatar embaixo da bandeira
- O avatar é do estúdio HeyGen (TEMPLATE-AVATAR16, look do Nei), sem API para gerar. O Nei pediu essa versão em 22/10, o que vale como OK para esta produção.
- Caminho mais simples: um único vídeo de avatar com o áudio da narração da fase 2, ou com o mesmo texto em takes por bloco. O avatar entra recortado, em PiP pequeno (~300 px de altura), em `left:56px; top:~150px`, sob o nome do regime. Ele aparece só nos trechos com fala e some com fade nos silêncios.
- Composição por ffmpeg overlay sobre `floripa-narrada.mp4`. Conferir que não cobre a imagem da época (canto inferior esquerdo) nem o texto grande (centro, topo).

## Anotado para depois (não aplicado)
- A **linha do tempo** do topo (hoje amarela) deve ficar **preta ou branca**. Fica para a próxima rodada do motor (`#linha .feito` e `#linha .cur` em `motor/mapa.html`).
