# Rio de Janeiro — pesquisa (22/10/2026)

Arquivos: `eventos.json` (40 eventos, 22 antes de 1850, mais 8 de reserva), `regimes.json` (4 faixas nacionais com as bandeiras locais de `motor/assets/bandeiras/` + 1 faixa extra opcional da França Antártica + status da cidade no HUD). Fontes lidas como página HTML (pt/en.wikipedia.org/wiki/…, wikidata.org/wiki/Q…); nenhuma API (nem Wikipédia, IBGE, Wikidata/SPARQL ou Overpass). Limites (título ≤ 30 em maiúsculas, legenda ≤ 95, detalhe ≤ 220, ids únicos, coordenadas no bbox) validados por script local.

## Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Comandante de 1502 | Gaspar de Lemos (ptwiki Gaspar de Lemos; ptwiki História da cidade, 2º trecho) | Gaspar de Lemos ou Gonçalo Coelho — "há controvérsias" (ptwiki História da cidade) | data 1º/01/1502 (igual nas duas); comandante fora da tela |
| Origem de "carioca" | "casa de branco" (kara'iwa + oka), ligada à feitoria de 1503–04 (ptwiki Feitoria da Baía de Guanabara) | "casa dos carijós" (kariîó + oka); a tese "casa de branco" é rejeitada por linguistas (ptwiki Rio Carioca) | nenhuma etimologia de "carioca" na tela; só "aldeia Karióka" |
| Etimologia de Guanabara | Iguaá-Mbara / guana-bara "seio do mar" / kûárana pará (ptwiki Baía de Guanabara, 3 versões) | — | "mar do seio" (guana + bara), a que o pedido cita, com confiança média |
| Martim Afonso na Guanabara (1531) | citado no pedido | não aparece nas ptwiki/enwiki Martim Afonso de Sousa nem em História da cidade; ptwiki "Expedição de Martim Afonso" não existe | NÃO usado (sem fonte lida) |
| Chegada de Villegagnon | 1º/11/1555 (enwiki France Antarctique) | 10/11/1555 (ptwiki Villegagnon; infobox ptwiki França Antártica) | 10/11/1555 (ano 1555.86); tela só "1555" |
| Ataque de Mem de Sá | 15/03/1560 (ptwiki Ilha de Villegagnon, enwiki) | 16/03/1560 "destruição do forte" (infobox ptwiki França Antártica) | 15/03/1560; tela só "1560". 26 navios/2.000 soldados só na enwiki |
| Reforço francês de 1557 | ~300 pessoas (ptwiki Villegagnon) | 290 colonos em 3 navios (ptwiki Forte Coligny) | não vai para a tela |
| Lugar de Uruçumirim | "Praia do Flamengo" (ptwiki História da cidade, Estácio de Sá) | outeiro da Glória (ptwiki Entrincheiramento de Uruçumirim) | outeiro da Glória (vizinhos; a paliçada era no outeiro) |
| São Bento | 1590 (pedido) | 1586 doação do terreno; obras de 1633 (ptwiki Mosteiro) | 1586, na reserva |
| Duclerc 1710: efetivo | 6 navios, 1.500 homens (infobox pt/en) | 6 navios, 800–1.200 homens (ptwiki Duclerc) | tela "6 NAVIOS"; homens fora |
| Duclerc 1710: desembarque | Guaratiba (memória comum) | não aparece em nenhuma página lida | não desenhar Guaratiba; ponto = coordenada da batalha (enwiki) |
| Duguay-Trouin 1711: navios | 18, sendo 7 de linha (infobox ptwiki Batalha 1711) | 16 armados (11 Brest + 4 Rochefort + 1 Dunquerque) ou 17 "outros relatos" (ptwiki Duguay-Trouin); 7 de linha + 5 fragatas + 1 galeota + 3 bombardeiras = 16 (enwiki, Boxer) | tela "16 A 18 NAVIOS" |
| Duguay-Trouin 1711: homens | 3.800 (ptwiki infobox) | 2.800–3.700 (enwiki); 5.824 ou 5.674 (ptwiki Duguay-Trouin) | homens fora da tela |
| Aqueduto: altura | 17,6 m (ptwiki) | 64 m (enwiki infobox; provavelmente cota, não altura dos arcos) | altura fora; tela "42 ARCOS" (270 m igual nas duas) |
| Aqueduto: data | 1º aqueduto pronto em 1723; reconstrução de 1744; inauguração 1750 (ptwiki) | "construction start 1718" (enwiki) | 1750 (inauguração dos arcos atuais) |
| Chegada da Corte | "chegou no dia 8 de março de 1808, desembarcando no cais do Largo do Paço" (ptwiki) | 7 de março (memória comum; não aparece nas páginas lidas) | 8/03/1808 (ano 1808.18) |
| Pessoas com a Corte | ~10.000 (enwiki) | 4 a 7 mil, contra "dez mil ou mais" de relatos da época (ptwiki, Pedreira e Costa) | tela "17 NAVIOS DE GUERRA" (8 naus + 5 fragatas + 4 menores, enwiki); faixa 4–10 mil só no detalhe |
| População do Rio em 1808 | "passa de 15 mil para 30 mil habitantes" (ptwiki Cais do Valongo) | — (valor implausível para a capital) | NÃO usado |
| Valongo | "cerca de um milhão" (ptwiki, introdução) | "entre 500 mil e um milhão" (mesma ptwiki, adiante; enwiki) | "500 MIL A 1 MILHÃO" |
| Jardim Botânico | fundado 13/06/1808 (infobox ptwiki) | "opens" 1822 (enwiki Timeline; abertura ao público) | 13/06/1808 |
| Reino Unido | 16/12/1815 (enwiki UK of Portugal, Brazil…) | "entre 1815 e abril de 1821 sediou o Reino Unido" (ptwiki História da cidade) | faixa do HUD 1815.96–1822.78 |
| Aclamação de Pedro I | 12/10/1822 (infobox ptwiki Pedro I, início do reinado) | "12 de novembro de 1822" (legenda de pintura de Taunay, ptwiki Campo de Santana) | 12/10/1822 |
| Fim do Município Neutro | 1834–1889 (infobox ptwiki Município Neutro) | vira Distrito Federal em 24/02/1891, pela Constituição (ptwiki Estado da Guanabara) | HUD: "Município Neutro" até 24/02/1891, "Distrito Federal" depois; o pedido citava 1889 (alternativa no regimes.json) |
| Avenida Central | 641 casas demolidas, ~3.900 desalojados (ptwiki Av. Rio Branco) | "300 casas coloniais arrasadas" (mesma página, outro parágrafo) | "641 CASAS" (número mais específico, com desalojados) |
| Avenida Central: data | inaugurada 07/09/1904 (infobox e texto) | entregue ao tráfego 15/11/1905 (mesmo texto) | ano 1904 (obras desde março de 1904) |
| 18 do Forte | "o famoso número de 18" | "a quantidade real era provavelmente menor" (mesma ptwiki) | tela "18 (LENDA)" + detalhe explicando |
| Cristo Redentor | inaugurado 12/10/1931 (ptwiki Cristo, infobox) | 12/08/1931 (ptwiki História da cidade) | 12/10/1931 (página do próprio monumento) |
| Maracanã 1950 | 199.854 presentes (infobox ptwiki Maracanã e Maracanaço) | 173.850 pagantes (mesma infobox) | tela "199.854 PESSOAS"; pagantes no detalhe |
| Guanabara | Lei 3.752 de 14/04/1960 (ptwiki Estado da Guanabara) | 21/04/1960, transferência da capital (ptwiki Distrito Federal 1891–1960) | 21/04/1960 (ano 1960.3) |
| Eco-92 | 108 chefes de Estado e governo (ptwiki Conferência) | delegações de 175 países (ptwiki História da cidade) | tela "108 CHEFES DE ESTADO" (medidas diferentes, não contraditórias) |
| Metrô | 57 km (ptwiki) | 58 km (enwiki) | só "5 ESTAÇÕES" (reserva) |
| Censo 2022 | 6.211.223 (ptwiki Rio de Janeiro, infobox e tabela de censos) | — | 6.211.223. O pedido escreveu o mesmo número. IBGE Cidades não aberto (site em JS/API) |

## Coordenadas

Todas de página HTML: ptwiki (wgCoordinates da página ou link geohack), enwiki (infobox) ou Wikidata (legenda do mapa na página do item). Itens sem coordenada própria:
- feitoria de 1503–04 → rio Carioca (ptwiki), marcada "aproximação";
- entrada da baía em 1502 → Pão de Açúcar (enwiki), "aproximação";
- 1710 e 1711 → coordenada da infobox enwiki das batalhas (centro);
- Guanabara 1960 e fusão 1975 → `centro_antigo` do config (Praça XV), "genérico";
- Revolta da Cachaça (reserva) → genérico (começou em São Gonçalo, na borda leste do bbox, sem ponto publicado).
- Ponto do Morro do Castelo: ptwiki (geohack) = Wikidata Q10332478 (-22.906927, -43.174532); a enwiki "Castelo, Rio de Janeiro" dá o bairro atual (-22.9089, -43.1725). Usado o do morro.
- A ptwiki "Paranapuã" é um município de SP (fora do bbox): para os temiminós usar a Ilha do Governador (ptwiki, -22.80427, -43.20609).
- Niterói (aldeia de São Lourenço, 1573) é outro município, dentro do bbox.

## Regimes

Colônia (portugal) → Reino Unido 16/12/1815 (reino) → Império 12/10/1822 (imperio; imperio2 de 1870) → República 15/11/1889 (republica; brasil de 1960). Faixa extra opcional e local: França Antártica 1555–1567 (sem arquivo local; Commons `File:Royal_flag_of_France.svg`, usada na infobox da ptwiki — licença conferida: **CC BY-SA 3.0, não é domínio público**, exige crédito; não há bandeira real francesa em domínio público entre as conferidas). `File:Flag_of_Portugal_(1521).svg` (séc. XVI) é domínio público (PD-old). Status da cidade no HUD: São Sebastião do Rio (1565) → Capital do Brasil Colônia (1763) → Capital do Reino Unido (1815) → Capital do Império (1822) → Município Neutro (1834) → Distrito Federal (1891) → Estado da Guanabara (1960) → Capital do Estado do RJ (1975). Bandeiras locais (Município Neutro, DF, Guanabara, estado, cidade) encontradas só como nome de arquivo; nada baixado.

## Pontos fracos

- Antes de 1600 tudo depende da Wikipédia; a feitoria e a aldeia Karióka não têm ponto exato.
- O Morro do Castelo (1567–1922) e o de Santo Antônio não existem mais no relevo atual: o motor precisa recriar o Castelo para os eventos de 1567 a 1922.
- Muitos números de batalha divergem entre pt e en (1710, 1711, 1560); a tela usa só o que bate ou mostra faixa.
- A 1ª ferrovia (Mauá, 1854) e a iluminação a gás (1854) ficaram fora: a ferrovia está fora do bbox e a data/lugar do gás não apareceram nas páginas lidas.
- Revisor: a lista fixa do Nei (REVISAO-LISTA.md) pede "o que o cartão cita aparece no mapa" — conferir eventos sem objeto 3D próprio (1763, 1815, 1834, 1960, 1975).

## Nota do roteiro (22/10/2026)
- **População 2010:** `populacao.json` usa 6.323.037 (IBGE, série 1872/2010); o detalhe do cartão do Censo 2022 cita 6.320.446 (resultado do universo 2010 na Wikipédia). Diferença de 0,04%; a queda fica em −1,7% nos dois casos.
