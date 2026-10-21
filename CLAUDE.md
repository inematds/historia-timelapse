# CLAUDE.md — historia-timelapse

Timelapse 3D da história de cidades (mapa real + prédios do OSM + cartões com fonte). Leia `PLANO.md` (decisões e perguntas abertas) e `CORRECOES-NEI.md` antes de mexer. Como rodar: `README.md`.

## Regras do projeto
- Commits e push: conta **inematds** (`inematds <inematds@gmail.com>`).
- Tudo local: sem API paga. Downloads de arquivos públicos (Geofabrik, Copernicus DEM, Wikimedia Commons) são permitidos; consultas a APIs (IBGE, Wikipédia, Overpass) precisam de autorização do Nei.
- Design INEMA: ler `~/projetos/inema-design/DESIGN.md` e `video/*` antes de mudar o visual.
- Todo número na tela tem fonte escrita; divergências entre fontes ficam em `dados/pesquisa/RESUMO.md`.
- Mostrar quadros-chave ao Nei antes do render completo; publicar (Aventuras, lives26) só com OK dele.
- Revisão: revisor independente (`~/.claude/runbooks/revisor-independente.md`) com a lista `REVISAO-LISTA.md`; registrar notas no `~/projetos/wifi/scripts/revisor-nota.py --fluxo historia-timelapse`.

## Self-learning
Quando o Nei corrigir algo ou eu pegar um erro meu: antes de continuar, acrescentar a lição como uma linha no TOPO da seção Lessons abaixo.

## Lessons
- Ano no contador tem que estar no valor que a fala/cartão cita quando ele aparece: avanço rápido do tempo ANTES do evento; efeitos (tropas, cartão, rótulo do muro) só depois do avanço e só a partir do ano real. (21/10/2026)
- Chatterbox engole frase curta só com número ("Mil setecentos e setenta e dois."): juntar o ano à frase seguinte e conferir com `scripts/qa_narracao.py`. (21/10/2026)
- Água de lagoas/açudes no alto rebaixada ao nível do lago vira poço preto: só rebaixar água com chão < 6 m + `grey_closing`. (21/10/2026)
- O plano de água da cheia tem que ir além do recorte do mapa (bbox ± 1°), senão a borda aparece nas vistas abertas. (21/10/2026)
- deck.gl 9.0.38: TerrainLayer precisa do `terrain-worker.js` local (`workerUrl`); `_TerrainExtension` (com underline); TextLayer ignora `shadowEnabled` (não usar `_shadow`); carregar as fontes antes de criar o Deck; servir `.svg` como `image/svg+xml`. (21/10/2026)
- O revisor independente aprovou (8) a v4 que o Nei reprovou: a lista fixa não cobria impacto visual nem "o que o cartão cita aparece no mapa". (21/10/2026)
