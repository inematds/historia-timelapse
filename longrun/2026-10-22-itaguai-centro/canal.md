# Canal — itaguai-centro (só acrescentar; nunca reescrever)

Conhecimento do projeto que a compactação perde: fatos descobertos, aprendizados, glossário, armadilhas, onde estão as coisas.
Não é estado da tarefa (isso vai em state/plan/progress). Preencha cedo — o hook avisa na faixa 1 (~50% do contexto).

Formato: `- AAAA-MM-DD HH:MM · fato|aprendizado|glossário|armadilha · texto`


## 22/10 06:30 — fatos
- Id `itaguai-centro`; motor copiado em `centro/motor/` (assets por symlink), scripts próprios em `centro/scripts/` (textura_ruas, extrai_ruas, limpa_marcos, gerar_cena cópia com marcos/futuro).
- centro_antigo real = Matriz (-43.7792,-22.8676); o do config municipal está 1,7 km ao norte.
- pop_modelo do centro = nº de prédios (36 casas 1818, 132 em 1841).
- "Casa do Pai" = Instituto Casa do Pai (ONG 2007, Monte Serrat) — incluído como bloco; pergunta ao Nei em aberto.
- Ordem: modelo_anos → limpa_marcos (senão caixas atravessam os marcos).
- Fable faz centro/motor/marcos.js + vitrine; eu integro (MARCOS.camadas já chamado no camadas()).

## 22/10 11:15 — estado (faixa 50%)
- 3 fases prontas em cidades/itaguai-centro/final/: itaguai-centro-v1.mp4 (música, pico limitado -2,2 dBFS), -narrado.mp4, -avatar.mp4 (+ -540p). Enviadas ao bot v3.
- Publicação lives26 BLOQUEADA: YouTube 400 uploadLimitExceeded (limite diário do canal). Planos prontos: ~/.local/share/yt-pubx/trabalhos/20261022-071116-itaguai-centro-v1-mp4/plano.json e 20261022-080404-itaguai-centro-narrado-mp4/plano.json → `./yt-pubx publicar <mp4> --plano <plano.json>` quando liberar. Nei pediu só fases 1 e 2 no lives26 (11:0x).
- Revisor independente: 5 → 6 → 6 (registrado em revisor-nota). Pendências apontadas na 3ª: período colonial vazio/campo liso, etiqueta "tombada pelo INEPAC" antes de 2006, legenda 1823 no bloco de 1818, contador de habitantes cai 1841–1873, futuro sem VLT visível, Quintino sem prédio.
- Refazer cena: `bash centro/refaz.sh`; render: `bash centro/motor/render_trechos.sh cidades/itaguai-centro/cena cidades/itaguai-centro/final/video.mp4 60`; fase 3: trocar narracao.json por narracao_avatar.json, rodar centro/scripts/montar_avatar.py, voltar (avatar/ajustes.json corrige 110–124 s que o Whisper pulou).
- Armadilhas: halo/sombra com _TerrainExtension + position z desloca → halos sem ext; textura de perto borra → chão liso (centro/scripts/textura_lisa.py) + ruas vetoriais; avatar drawbox fill dava clarão amarelo → só borda (cópia em centro/scripts).
- Tokens (medido 11:12): centro 96,1 M (saída 427 mil); POA 66,7 M; Floripa 167,2 M + 63,6 M (com Itaguaí município).

## 2026-10-23 · capitais do Brasil (outra produção, mesma sessão) — notas para retomar
- Pedido do Nei: vídeo "as 3 capitais" (Salvador→Rio→Brasília), fase 1 primeiro e mandar; "contar em detalhes como e pq foi a mudança; os prédios têm que ser bem definidos". Plano e passos: `cidades/capitais/FASES.md`.
- 3 atos = 3 cidades do motor (capitais-ssa, capitais-rio, capitais-bsb), motor da versão centro + `centro/motor/marcos-capitais.js` (tipos novos). Comum: `cidades/capitais/comum.py`. Emenda: `cidades/capitais/montar.py`.
- Armadilhas: `codex exec` precisa `< /dev/null`; `pkill -f` com padrão do próprio comando mata o comando; Geofabrik lento → openstreetmap.fr por estado; DF: bairros no admin_level 8; `extrai_osm` regrava agua.geojson com o Lago Paranoá (tirar de novo); câmera precisa de `z` (chão×exz) em TODAS as chaves; palácio em destaque só ganha faixa amarela (não pinta tudo).
- Emendas de ano: SSA termina 1763.55; Rio começa 1763.55 e termina na Novacap (1956.74); BSB começa na visita de JK (2/10/1956).
