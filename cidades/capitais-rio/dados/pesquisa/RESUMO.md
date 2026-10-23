# Rio de Janeiro capital (1763–1960) — pesquisa (22/10/2026)

Ato 2 de **As capitais do Brasil** (Salvador → Rio → Brasília). Base reaproveitada: `cidades/rio/dados/pesquisa/` (ids iguais = eventos copiados de lá).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `eventos.json` | 26 eventos de 1763 a 1960 + 4 de reserva + bloco `motivos` (a favor / contra a mudança, com fonte). 9 eventos copiados do Rio (5 sem mudança; `capital-1763`, `corte-1808`, `avenida-central-1904` e `guanabara-1960` com detalhe, título ou local ajustados ao foco "capital"). 17 eventos novos. |
| `predios.json` | 9 prédios do poder para o 3D (planta, altura, telhado, cúpula, cores, fachada, fotos de referência). Feito por um agente separado — ver seção "Prédios". |
| `populacao.json` | série do Rio cortada em 1687–1970 (1687 e 1970 são bordas da interpolação). Nada pesquisado de novo. |
| `imagens.json` + `assets/epoca/e00–e13.jpg` + `indice.json` | 14 imagens em domínio público (3 do Rio, 11 novas do Commons), licença lida na página File:. |
| `regimes.json` | 4 faixas de bandeira de 1763 a 1960 + status da cidade no HUD: Sede do Vice-Reino → Corte → Capital do Reino Unido → Capital do Império → Município Neutro → Capital da República/Distrito Federal → (último segundo) Estado da Guanabara. |

Fontes lidas como página HTML: pt/en.wikipedia.org/wiki/…, **planalto.gov.br/ccivil_03** (texto das Constituições de 1891 e 1946 e das Leis 2.874/1956, 3.273/1957 e 3.752/1960), **camara.leg.br/legin** (Decreto 4.494/1922), biblioteca.ibge.gov.br (DTB Brasília, PDF), tese UFF 2010 (PDF), agencia.fapesp.br, correiobraziliense.com.br, vermelho.org.br. Nenhuma API (nem Wikipédia, IBGE, Wikidata/SPARQL ou Overpass). Limites (título ≤ 30 em maiúsculas, legenda ≤ 95, detalhe ≤ 220, ids únicos, ordem, bbox) validados por script local: 0 erros.

## O porquê da mudança para Brasília (1808 → 1960)

1. **1808** — Com a Corte no Rio, o almirante inglês Sidney Smith aconselha D. João a levar a sede para o interior, por "motivos estratégicos" (ptwiki História de Brasília).
2. **1813** — Hipólito José da Costa, no *Correio Braziliense* (Londres), passa a pedir a capital no Planalto Central, nas "cabeceiras do São Francisco": cidade nova, como Washington, para ocupar o país e se proteger de ataques estrangeiros (ptwiki Hist. Brasília; vermelho.org.br; correiobraziliense.com.br 2022).
3. **1823** — Na Constituinte reunida na Cadeia Velha, lê-se a memória de José Bonifácio: capital na comarca de Paracatu (perto do paralelo 15), com o nome "Brasília ou Petrópole" (ptwiki Hist. Brasília, sessão de 7/6/1823; IBGE DTB Brasília).
4. **1839–1877** — Varnhagen faz campanha; em 1877 viaja a Goiás e escolhe Formosa (ptwiki Hist. Brasília). Sem prédio no Rio → reserva.
5. **1891** — A 1ª Constituição republicana, feita no Palácio de São Cristóvão, reserva à União "no planalto central da República, uma zona de 14.400 quilômetros quadrados ... para nela estabelecer-se a futura Capital federal" (art. 3º, texto no Planalto).
6. **1892–1894** — A Missão Cruls (22 pessoas, chefiada pelo diretor do Observatório do Morro do Castelo) demarca um retângulo de 90 × 160 km; argumentos: "defesa estratégica, coesão territorial e criação de uma cultura autenticamente nacional" (ptwiki Hist. Brasília; ptwiki Missão Cruls).
7. **1903–1919** — Com o Rio saneado e reformado (Rodrigues Alves, Pereira Passos), "pareceram minimizados alguns dos motivos" e o assunto perde força (ptwiki Hist. Brasília).
8. **1922** — Decreto 4.494 (18/1/1922), sancionado por Epitácio Pessoa: pedra fundamental no planalto em 7/9/1922, perto de Planaltina, e estudo de ferrovia até os portos do Rio e de Santos (texto na Câmara; IBGE). O governo seguinte (Artur Bernardes) via o Rio "agitado demais" e com influência política demais (ptwiki Hist. Brasília).
9. **1946** — Depois das greves do fim do Estado Novo, os constituintes no Palácio Tiradentes acham que a metrópole não serve mais de sede; o ADCT, art. 4º, manda: "A Capital da União será transferida para o planalto central do País" — contra quem via "dispêndio desnecessário de recursos" (texto no Planalto; ptwiki Hist. Brasília).
10. **1948–1955** — Comissão Poli Coelho (relatório 1948; relator de 1949 propõe outro lugar); Vargas manda refazer em 1953; com o levantamento aéreo da Belcher (5 sítios), escolhe-se em 1955 o Sítio Castanho, 5.850 km² (ptwiki Hist. Brasília; IBGE).
11. **1955–1956** — Em Jataí (GO), JK promete cumprir a Constituição; a Lei 2.874 (19/9/1956) cria a Novacap e dá o nome Brasília (art. 33). Desenvolvimentismo: "50 anos em 5", passo para "independência e unidade política" (texto no Planalto; ptwiki JK; ptwiki Hist. Brasília).
12. **1957–1960** — A Lei 3.273 (1º/10/1957) marca a mudança para 21/4/1960; críticas de Lacerda, Gudin, Gilberto Freyre e Corção, custo nunca determinado e inflação pela emissão de moeda (texto no Planalto; ptwiki Hist. Brasília). Em 21/4/1960 o Distrito Federal vira o Estado da Guanabara "com os mesmos limites" (Lei 3.752).

## Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Dia da transferência / posse do Conde da Cunha (1763) | enwiki List of governors-general: vice-rei de 27/06/1763 | tese UFF (Gonçalves, 2010): "Em janeiro de 1763 desembarcava, no Rio"; biografias citadas em busca dão 31/08/1763 (não lidas) | tela só "1763"; ano 1763 |
| Sessão da memória de Bonifácio | 7/6/1823 (ptwiki Hist. Brasília) | 9/6/1823 (índice da Câmara, só visto em resultado de busca, não lido) | 7/6 (ano 1823.43); tela sem dia |
| Nome proposto por Bonifácio | "Brasília ou Petrópole" (ptwiki; IBGE "Petrópole ou Brasília") | "Petrópolis" (Google Arts & Culture, em busca) | "BRASÍLIA OU PETRÓPOLE" |
| Primeiro uso de "Brasília" | folheto anônimo de 1822 ("Brasília, ou qualquer outro") — ptwiki | memória de Bonifácio, 1823 | título "BONIFÁCIO PROPÕE BRASÍLIA" (não "nasce aqui"); o folheto de 1822 fica no obs |
| Catete: águias | "Palácio das Águias" (nome alternativo, infobox ptwiki) | a mesma página: as águias de ferro do topo da fachada foram trocadas ~1900 por 7 esculturas alegóricas de bronze | modelo de 1897 com águias; a partir de ~1900, esculturas (ver predios.json) |
| Theatro Municipal: cúpula | (o pedido falava em "cúpula verde") | ptwiki: "águia dourada de cobre ... no centro do telhado, das três cúpulas douradas" (restauro de 2010) | recurso_visual com as cúpulas douradas; cor final segue predios.json |
| Sede do governo no Itamaraty | "1889–1898" (ptwiki Itamaraty, introdução) | Presidência passa ao Catete em 24/2/1897 (ptwiki Catete); MRE no Itamaraty "1897–1970" e "1899–1970" (mesma página) | tela só "1889"; Catete 24/2/1897 |
| Senado no Conde dos Arcos até | 1924 (ptwiki Faculdade Nacional de Direito) | Senado no Monroe "entre 1925 e 1960" (ptwiki Monroe) | evento `monroe-1925`, ano 1925 |
| Decreto da pedra fundamental | 18/01/1922 (texto do Decreto 4.494, Câmara) | "Em 1920, o Presidente Epitácio Pessoa assina decreto" (IBGE DTB) | 1922 (texto do próprio decreto) |
| Comício de Jataí | 4/4/1955 (ptwiki Juscelino Kubitschek) | 5/4/1955 (ptwiki História de Brasília) | tela sem dia; só no detalhe "em 1955" |
| Criação da Novacap | Lei 2.874 de 19/9/1956 (texto no Planalto; IBGE) | "Em 15 de março de 1956 o presidente criou a Novacap" (ptwiki Hist. Brasília; provavelmente a mensagem ao Congresso) | 19/9/1956 (a lei) |
| Lei da data da mudança | o pedido: "Lei 3.273/1957" | texto: 1º/10/1957 | 1º/10/1957 (ano 1957.75) |
| Constituinte republicana em São Cristóvão | "1889 a 1891" (ptwiki Museu Nacional) | Câmara em São Cristóvão "1891" (navbox ptwiki); "brevemente" (ptwiki Palácio de São Cristóvão) | evento ancorado na promulgação, 24/2/1891 |
| Retângulo/Quadrilátero Cruls | 90 × 160 km (ptwiki Hist. Brasília) = 14.400 km² | "Quadrilátero Cruls" (IBGE) | tela "90 × 160 KM" |

## Âncoras dos eventos da ideia de Brasília (todas no Rio)

- Bonifácio 1823 → **Cadeia Velha** (ponto do Palácio Tiradentes, mesmo lote).
- Constituição 1891 → **Palácio de São Cristóvão**.
- Cruls 1892 → **Morro do Castelo** (Observatório até 1920; o morro foi arrasado em 1922 — o motor precisa recriá-lo, como na pesquisa do Rio). Ponto de partida da expedição (estação?) não lido: "aproximação".
- Pedra fundamental 1922, Belcher 1955, Novacap 1956 → **Palácio do Catete** (sede da Presidência 1897–1960; os textos só dizem "Rio de Janeiro" → "local inferido").
- Constituição 1946 e Poli Coelho 1948 → **Palácio Tiradentes** (1946 = local de reunião na infobox; 1948 inferido: o relatório foi ao Congresso).
- Lei 3.273/1957 → **Palácio Monroe** (Senado; inferido — a lei passou pelas duas casas).
- Saída 1960 → **Palácio Guanabara** (vira sede do Estado da Guanabara; "o que ficou").
- Fora do bbox e só no detalhe: Jataí, Planaltina, Formosa, Retângulo Cruls, Sítio Castanho.

## Prédios (predios.json)

10 registros (a Cadeia Velha e o Palácio Tiradentes são 2 ids no mesmo lote: um some, o outro nasce em 1922–1926). Planta (comprimento × largura × azimute) = retângulo mínimo do polígono do **OSM local** (`dl/sudeste.osm.pbf` → `cidades/rio/dados/brutos/predios.json`, sem Overpass); a fachada é sempre "estimado" (eixo do polígono + rua em frente). Cada medida tem `{valor, fonte}` ou `fonte: "estimado: como"`.

| Prédio | Medidas publicadas | Estimado |
|---|---|---|
| Paço Imperial | planta OSM 90,7 × 33 m; altura 12 m (tag OSM); andares por época (ptwiki) | corpo de 3 andares 17 m, cores |
| Cadeia Velha (até ~1922) | 2 pavimentos (pt/enwiki) | quase tudo (foto c.1880): 50 × 25 m, 11 m |
| Palácio Tiradentes (1926) | planta OSM 71 × 37 m; 5 pavimentos; **45 m até o topo da cúpula**; 3 mil m² (PDF da Câmara) | corpo 24 m, cúpula Ø 18 m, fachada (incerta) |
| Palácio do Catete | planta OSM 32,9 × 26,2 m; 3 andares | altura 19 m (+ esculturas 22 m), fachada a O |
| Palácio Monroe (demolido 1976) | 1.700 m²; **cúpula de bronze Ø 15 m**; 4 leões de mármore de 2,5 m; 36 colunas (Senado) | planta 46 × 38 m, altura |
| Palácio Itamaraty | planta OSM 55,8 × 42,7 m; 2 pavimentos (tag OSM) | altura 14 m |
| Palácio de São Cristóvão | planta OSM 105,5 × 73,9 m; telhado 23 m (enwiki); 13.617 m² | corpo 18 m |
| Theatro Municipal | planta OSM 84,5 × 68 m; beiral ~21 m (tag OSM); 3 cúpulas, águia | topo da cúpula 45 m, Ø 20 m, cor verde |
| Conde dos Arcos (Senado do Império) | planta OSM 48 × 46 m | 2 andares, 12 m |
| Palácio Guanabara | planta OSM 54 × 52 m | 3 pavimentos, 16 m |

Ornamentos conferidos entre os dois arquivos: **leões são do Monroe** (4 de mármore, nas 2 escadarias) — o Tiradentes tem a estátua de Tiradentes (~5 m) e duas Vitórias Aladas, não leões (o pedido falava em "leões do Tiradentes": sem fonte). **Catete**: ptwiki diz que as águias de ferro originais do topo foram trocadas ~1900 por esculturas alegóricas de bronze; o predios.json registra "5 harpias de bronze no topo (desde 1910)" — divergência de data/material; o evento só diz "águias ... Palácio das Águias". **Municipal**: ptwiki fala em "três cúpulas douradas"; o predios.json usa verde-azinhavre com ornatos dourados (cor estimada por foto) — conferir no quadro-chave.

Outras divergências dos prédios (detalhe no campo `divergencias` de cada um): Cadeia Velha com 2 pavimentos no texto × 3 na foto de c.1880; Monroe com 6 ou 8 anjos, 1.700 m² ou mais de 2.000 m², e altura de ~41 m não confirmada. As fachadas do Tiradentes e de São Cristóvão são incertas — conferir no satélite antes de modelar.

## Pontos fracos

- Quase toda a narrativa da ideia vem de UMA página (ptwiki História de Brasília, artigo destacado); as leis foram conferidas no texto oficial, mas datas como Sidney Smith 1808, Poli Coelho 1948 e Belcher/Castanho 1955 só têm essa fonte (Castanho e 5.850 km² batem com IBGE e enwiki).
- "Local inferido" em 6 eventos: o documento só diz "Rio de Janeiro". O revisor pode cobrar; a regra do pedido (mostrar o prédio do Rio) foi seguida com a sede do poder daquele ano.
- Sem imagem DP da pedra fundamental de 1922 nem da chegada da Corte (1808).
- Cruls: dia e lugar exato da partida não lidos.
- População: não há ponto com fonte em 1763 (interpolação 1687→1799, confiança baixa).
- Cartões de prédio citam anos futuros (1826 → "até 1914/1924"; 1897 → "até 1960"; 1925 → "demolido em 1976"; 1926 → 1946). Escolha consciente (biografia do prédio); se o revisor aplicar a lição "o ano no contador = o ano que o cartão cita", tirar o futuro do detalhe e deixar no obs.
- Imagens e12 (Congresso em obras, 1959) e e13 (inauguração de Brasília, 21/4/1960) mostram Brasília: combinar com o ato 3 (capitais-bsb) para não repetir as mesmas fotos.
- Palácio Guanabara: residência oficial de Vargas no Estado Novo (1937–1945) e Prefeitura do DF a partir de 1946 (ptwiki); no vídeo só aparece em 1960 — a fala pode citar.
- O script de validação no scratchpad compartilhado foi sobrescrito por outra sessão (bbox de Salvador); usado `valida_capitais_rio.py` com o bbox do Rio — 26 + 4 eventos OK.
