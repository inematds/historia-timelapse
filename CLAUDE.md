# CLAUDE.md — historia-timelapse

Timelapse 3D da história de cidades (mapa real + prédios do OSM + cartões com fonte). Leia `PLANO.md` (decisões e perguntas abertas) e `CORRECOES-NEI.md` antes de mexer. Como rodar: `README.md`.

## Começar do zero (sem /prime)
- "Faz o timelapse de <cidade>": siga a skill `historia-timelapse` (`~/.claude/skills/historia-timelapse/SKILL.md`), copiando o padrão de `cidades/floripa/` (aprovado em 22/10/2026).
- Toda cidade sai em 3 fases, todas publicadas: 1 sem narração (música); 2 com a narração do Nei por cima; 3 com o avatar do Nei embaixo da bandeira. Plano e estado de Florianópolis em `cidades/floripa/FASES.md` (fase 1 publicada, fases 2 e 3 a fazer).

## Regras do projeto
- Commits e push: conta **inematds** (`inematds <inematds@gmail.com>`).
- Tudo local: sem API paga. Downloads de arquivos públicos (Geofabrik, Copernicus DEM, Wikimedia Commons) são permitidos; consultas a APIs (IBGE, Wikipédia, Overpass) precisam de autorização do Nei.
- Design INEMA: ler `~/projetos/inema-design/DESIGN.md` e `video/*` antes de mudar o visual.
- Todo número na tela tem fonte escrita; divergências entre fontes ficam em `dados/pesquisa/RESUMO.md`.
- Mostrar quadros-chave ao Nei antes do render completo (e seguir trabalhando, sem esperar resposta); publicar (Aventuras, lives26) só com OK dele.
- **Cidade nova: o Nei aprova antes de qualquer publicação (22/10/2026).** Ele vê a fase 1 primeiro ("na fase 1 a gente vê como fica"). Com o OK: a fase 2 (narrada) é publicada direto no lives26 e a fase 1 entra na fila (`python3 ~/projetos/wifi/fila-cidades/fila_cidades.py --add <mp4> --nome "..." --plano|--contexto ...`, 3 por dia às 9, 15 e 21 h). Sem OK, nada sobe.
- Revisão: revisor independente (`~/.claude/runbooks/revisor-independente.md`) com a lista `REVISAO-LISTA.md`; registrar notas no `~/projetos/wifi/scripts/revisor-nota.py --fluxo historia-timelapse`.

## Regra do motor: versão narrada = camada de áudio (Nei, 21/10/2026)
- O vídeo-base é sempre o **sem narração** (cartões contam a história). A versão narrada **não mexe no motor nem nos tempos**: é o mesmo `video.mp4` com outra trilha.
- Narração por **bloco** (`cidades/<id>/narracao.json`: `{id_do_bloco: texto}`), entrando no início do evento (depois do pulo). Blocos sem texto ficam só com música — silêncio é permitido.
- Cada fala cabe no bloco (≤ duração do bloco − 1 s, ~16–18 palavras); se não couber, encurtar ou dividir, nunca esticar o vídeo.
- A fala complementa o cartão (o porquê), não lê o cartão. Anos por extenso na voz; conferência por transcrição (`qa_narracao.py`).
- Música abaixa sob a voz (sidechain) e volta nos silêncios; final −14 LUFS.

## Self-learning
Quando o Nei corrigir algo ou eu pegar um erro meu: antes de continuar, acrescentar a lição como uma linha no TOPO da seção Lessons abaixo.

## Lessons
- Relatório de ferramenta alternativa (Blender, Mitsuba…) tem que trazer o tempo MEDIDO do motor atual (logs `final/trechos/t*.log`, 0,07–0,11 s/quadro) e explicar em linguagem simples o que a ferramenta é; o motor atual é deck.gl no Chrome, não Remotion. Mitsuba: `far_clip` padrão = 10 km, cidade inteira some (imagem só céu) — usar `far_clip: 1e6`. Blender do apt no Xvfb :99 roda por software (sem GPU). (24/10/2026)
- Rótulo/chamada: `z` em metros CRUS (o motor multiplica por EXZ); em planalto (Brasília 1.100 m) z = chão×EXZ+15 joga o texto para fora do quadro. Lugar fora do mapa (Rio, Anápolis) = `setas_tela` (posição fixa). Marco pequeno em morro: z = topo, não a mediana. (24/10/2026)
- Vídeo com várias vistas de perto (palácios): a câmera indo de uma à outra atravessa os prédios — roteiro com `"voo_alto": true` (centro/scripts/gerar_cena.py sobe no meio da viagem). Contador × censo: usar `ano_exato` no populacao.json e segurar o ano do bloco na data do censo. (23/10/2026)
- Vista de cima no fim do globo (zoom ~10,7) mostra o quadrado do recorte quando o bbox é pequeno (Brasília): fechar o zoom até o recorte encher a tela. Navios/pontos que o cartão cita têm que entrar NO quadro (frota vindo de trás da câmera não aparece). (23/10/2026)
- Cidade com muito aterro (Rio): o motor desenha a orla e o relevo de HOJE desde o início — aeroporto/Flamengo/porto aparecem em 1502 e morros arrasados (Castelo) não existem. O revisor reprova (6). Antes de prometer "a cidade sobe o morro"/"o aterro nasce", ver se o mapa mostra; senão, precisa de máscara de orla antiga + morro reconstruído (mudança de motor, em cópia). (22/10/2026)
- Câmera de perto (zoom ≥ 18) sobre morro: o alvo do viewState fica no nível do mar e o prédio sai do quadro — passar `position: [0, 0, z_chão × exz]` (versão centro). De perto a textura do chão borra: ruas como vetor (PathLayer em metros, uma camada só, cada rua nasce com as casas dela). (22/10/2026)
- Marco 3D sobre prédio do OSM/Microsoft: esconder os comuns no lote do marco e dentro das praças (`centro/scripts/limpa_marcos.py`), senão a caixa atravessa a igreja ou tapa o coreto. (22/10/2026)
- Mostrar quadros-chave ao Nei é aviso, não trava: mostrar e seguir com render/música/montagem no mesmo turno; só parar para publicar (Nei: "pq tem te dizer para continuar"). (22/10/2026)
- Motor é único para qualquer lugar, inclusive outros países: nada preso a Brasil/hemisfério/cidade no código; o que muda vai no config da cidade, com padrão igual ao de Floripa. Nunca remendar caso a caso (ex.: `longe.sul` só para Itaguaí). (22/10/2026)
- Ponte/linha que "nasce" num bloco: `desenha` (em anos) tem que caber no avanço do ano dentro do bloco, senão ela fica pela metade e as torres não aparecem; câmera lateral = bearing perpendicular à ponte (Hercílio do norte, bearing −180, alvo ~200 m ao sul dela). Conferir o quadro depois da chegada da câmera (45% do bloco). (22/10/2026)
- Globo: desenhar a Terra pixel a pixel (ortográfica inversa) com Blue Marble + recorte regional em alta + textura da cidade, terminando no mesmo m/px do mapa 3D (ls ≈ zoom + log2 do cos da latitude); BitmapLayer grande do deck (satélite ao redor) não apareceu — usar fundo de duas cores com a cor tirada do quadro. Igualar a cor média da textura ao satélite (`cor_satelite`) some com o retângulo. (21/10/2026)
- Render longo (6 min) perdeu o terreno no quadro ~4.500 ("Array buffer allocation failed" no terreno-mesh): objetos de prop (elevationDecoder, loadOptions, material, extensions) criados uma vez, textura menor e render em trechos de 60 s (`motor/render_trechos.sh`, que para no 1º erro). Conferir o log antes de publicar. (21/10/2026)
- Ano no contador tem que estar no valor que a fala/cartão cita quando ele aparece: avanço rápido do tempo ANTES do evento; efeitos (tropas, cartão, rótulo do muro) só depois do avanço e só a partir do ano real. (21/10/2026)
- Chatterbox engole frase curta só com número ("Mil setecentos e setenta e dois."): juntar o ano à frase seguinte e conferir com `scripts/qa_narracao.py`. (21/10/2026)
- Água de lagoas/açudes no alto rebaixada ao nível do lago vira poço preto: só rebaixar água com chão < 6 m + `grey_closing`. (21/10/2026)
- O plano de água da cheia tem que ir além do recorte do mapa (bbox ± 1°), senão a borda aparece nas vistas abertas. (21/10/2026)
- deck.gl 9.0.38: TerrainLayer precisa do `terrain-worker.js` local (`workerUrl`); `_TerrainExtension` (com underline); TextLayer ignora `shadowEnabled` (não usar `_shadow`); carregar as fontes antes de criar o Deck; servir `.svg` como `image/svg+xml`. (21/10/2026)
- O revisor independente aprovou (8) a v4 que o Nei reprovou: a lista fixa não cobria impacto visual nem "o que o cartão cita aparece no mapa". (21/10/2026)
