# Canal — poa-mitsuba (só acrescentar; nunca reescrever)

Conhecimento do projeto que a compactação perde: fatos descobertos, aprendizados, glossário, armadilhas, onde estão as coisas.
Não é estado da tarefa (isso vai em state/plan/progress). Preencha cedo — o hook avisa na faixa 1 (~50% do contexto).

Formato: `- AAAA-MM-DD HH:MM · fato|aprendizado|glossário|armadilha · texto`

- 24/10 Mitsuba: mesh_attribute (cor por vértice) dá NaN → usar paleta bitmap + texcoords. Material one-sided → twosided. Textura do relevo: v=0 no norte. far_clip 1e6. TerrainLayer com textura transparente mantém os efeitos colados (aterro/tropas/pulsos) na camada; chao-longe sai da camada e vira plano no Mitsuba.
