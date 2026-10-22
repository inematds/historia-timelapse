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
