# Salvador, capital (1549–1763) — pesquisa (22/10/2026)

Parte 1 de "As capitais do Brasil". Fontes lidas como página HTML (pt/en.wikipedia.org/wiki/…, wikidata.org/wiki/Q…, commons.wikimedia.org/wiki/File:…, tjba.jus.br) ou PDF (Gabriel Soares de Sousa, *Tratado Descritivo do Brasil em 1587*, ed. 1851, BBM/USP; dissertação de Izabela Gomes Gonçalves, UFF 2010; IBGE). Nenhuma API (nem Wikipédia, IBGE, Wikidata/SPARQL ou Overpass). Limites (título ≤ 30 em maiúsculas, legenda ≤ 95, detalhe ≤ 220, ids únicos, coordenadas no bbox lon −38.66 a −38.30 × lat −13.02 a −12.75) validados por script local.

## Arquivos

| arquivo | o que tem |
|---|---|
| `eventos.json` | 26 eventos de 1500 a 1763 + 9 de reserva (forte da Barra 1583, Forte do Mar 1623, Nassau 1638, arcebispado 1676, São Francisco 1723, "a cidade segue" 1763 e epílogo 1808 / 1823 / 1873). Ids com `porque-` contam o porquê da escolha (1548–49) e da perda (1680–1763). |
| `predios.json` | prédios do poder para modelar em 3D (planta, altura, telhado, torres, cores, orientação, fases), com medidas publicadas × estimadas. |
| `populacao.json` + `RESUMO-POP.md` | série 1549→2022 com fonte em cada ponto. |
| `imagens.json` + `../../assets/epoca/e00–e13.jpg` | 14 imagens de época em domínio público (licença lida na página File: do Commons). |
| `regimes.json` | faixas nacionais (bandeiras locais de `motor/assets/bandeiras/`), faixa extra opcional da ocupação holandesa 1624–25 e status da cidade no HUD. |
| `bairros_epocas.json` | ano de ocupação urbana por bairro oficial de Salvador. |

## O porquê da mudança (1763)

1. **O centro da riqueza desceu para o Sul.** Nos anos 1690 acha-se ouro em Minas (Rio das Velhas 1695, Vila Rica 1698); oficialmente 800 t foram para Portugal no séc. XVIII — [enwiki Brazilian Gold Rush](https://en.wikipedia.org/wiki/Brazilian_Gold_Rush). O eixo de poder passa "do Nordeste (Bahia e Pernambuco) para o centro-sul" como "consequência lógica" (Andrée Mansuy, citada na [dissertação UFF](https://www.historia.uff.br/stricto/td/1375.pdf), p. 32).
2. **O ouro saía pelo Rio, não por Salvador.** A Casa da Moeda criada em Salvador em 08/03/1694 para cunhar o ouro foi para o Rio em 1699 — [ptwiki Casa da Moeda do Brasil](https://pt.wikipedia.org/wiki/Casa_da_Moeda_do_Brasil). O Caminho Novo Rio–Minas (picada 1700, estrada 1707) tornou o Rio o porto do ouro — [ptwiki Caminho Novo](https://pt.wikipedia.org/wiki/Caminho_Novo).
3. **A guerra era no Sul.** Desde a Colônia do Sacramento (22/01/1680) Portugal e Espanha brigavam pelo Prata; o Tratado de Madri (13/01/1750), a Guerra Guaranítica (1753–56) e o Tratado de El Pardo (12/02/1761) mantiveram a fronteira em aberto — [ptwiki Colônia do Sacramento](https://pt.wikipedia.org/wiki/Colônia_do_Sacramento), [ptwiki Tratado de Madrid (1750)](https://pt.wikipedia.org/wiki/Tratado_de_Madrid_(1750)).
4. **O estopim: a Espanha toma o Sacramento (30/10/1762)** na Guerra dos Sete Anos. "O medo gerado pela Guerra dos Sete Anos influenciou diretamente na decisão tomada por Pombal de transferir a capital" — [dissertação UFF](https://www.historia.uff.br/stricto/td/1375.pdf), p. 32; data em [ptwiki Colônia do Sacramento](https://pt.wikipedia.org/wiki/Colônia_do_Sacramento).
5. **Um só exército, comandado do Rio.** As instruções da Coroa ao Conde da Cunha mandavam que as tropas "constituam um só e único exército"; o Rio era "melhor centro caso a fronteira Sul precisasse de proteção" — [dissertação UFF](https://www.historia.uff.br/stricto/td/1375.pdf), p. 30–32.
6. **O Rio já vinha sendo preparado.** Gomes Freire de Andrade governou o Rio de 1733 a 1763 e a mudança "já vinha sendo planejada" no seu tempo; em 1751 o Rio ganhou um Tribunal da Relação "nos mesmos moldes" do da Bahia — [dissertação UFF](https://www.historia.uff.br/stricto/td/1375.pdf), p. 30.
7. **Pombal centraliza.** A transferência entra nas "reformas administrativas promovidas pelo Marquês de Pombal" para "reforçar o controle sobre as áreas mineradoras, aprimorar a defesa do litoral meridional e racionalizar a administração" — [ptwiki Estado do Brasil](https://pt.wikipedia.org/wiki/Estado_do_Brasil). No mesmo pacote, a expulsão dos jesuítas (lei de 03/09/1759) fechou o colégio de Salvador — [ptwiki Expulsão dos jesuítas do Brasil](https://pt.wikipedia.org/wiki/Expulsão_dos_jesuítas_do_Brasil).
8. **O ato.** D. José I expede a carta régia em 27/01/1763 e a mudança se concretiza em 31/08/1763; o novo governador é Antônio Álvares da Cunha — [TJBA](https://www.tjba.jus.br/portal/o-tribunal-da-relacao-da-bahia-o-padre-jose-de-anchieta-e-a-transferencia-da-capital/). O Conde da Cunha foi o 1º vice-rei com sede no Rio (1763–1767) — [ptwiki Antônio Álvares da Cunha](https://pt.wikipedia.org/wiki/Antônio_Álvares_da_Cunha).
9. **O que ficou em Salvador.** Arcebispado (o maior do mundo em área até 1892), a Relação e o porto do açúcar e do tráfico; a cidade manteve "papel simbólico e político duradouro" — [ptwiki Estado do Brasil](https://pt.wikipedia.org/wiki/Estado_do_Brasil), [ptwiki Arquidiocese](https://pt.wikipedia.org/wiki/Arquidiocese_de_São_Salvador_da_Bahia).

E o porquê da **escolha** em 1549, para abrir o ato: capitanias fracassaram (só Pernambuco e São Vicente prosperaram); a Coroa comprou a da Bahia ao herdeiro de Coutinho; era "a mais central geograficamente" ([ptwiki Tomé de Sousa](https://pt.wikipedia.org/wiki/Tomé_de_Sousa)), "excelente ancoradouro natural, estratégico sítio defensivo" ([ptwiki Baía de Todos-os-Santos](https://pt.wikipedia.org/wiki/Baía_de_Todos-os-Santos)) e já tinha o núcleo de Caramuru ([ptwiki Capitania](https://pt.wikipedia.org/wiki/Capitania_da_Baía_de_Todos_os_Santos)).

## Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Nome da baía | 1º/11/1501, expedição de Gaspar de Lemos com Vespúcio (ptwiki Baía de Todos-os-Santos; ptwiki História de Salvador) | 1502, Vespúcio nomeia a baía (enwiki Timeline of Salvador) | 1501 (1501.83) |
| Chegada de Coutinho | "Em 1534, chegou à região" (ptwiki História de Salvador) | doação 05/04/1534, chegada nov/1536 (ptwiki Capitania; ptwiki Coutinho) | 1536 para a vila; 1534 só como doação |
| Naufrágio de Caramuru | 1509–1510 | "após 1530" (as duas na ptwiki Caramuru) | ~1510, confiança média; lugar exato não desenhado |
| Ponto do Caramuru | Rio Vermelho (lugar do naufrágio) — a página Wikidata só traz um link de mapa comercial, sem coordenada lida | sesmaria na Graça (ptwiki Capitania) com coordenada no Wikidata Q3115904 | Graça, marcada "aproximação" |
| Criação da Relação | 1586 (TJBA, 410 anos) | 1587 (trecho de resultado de busca — sedep.com.br/TJBA —, página não aberta) | tela só "7/3/1609" (instalação, igual nas duas) |
| Relação suprimida | 1626, reinstalada 1652 (TJBA) | "a supressão durou pouco" (mesma página) | detalhe "fechou em 1626 e voltou em 1652" |
| Divisão do Governo-Geral | 1602–1612 (ptwiki Estado do Brasil) | 1607–1613 (enwiki Salvador, Bahia) | não vai para a tela; HUD não muda |
| Jornada dos Vassalos: homens | "quase catorze mil" (ptwiki) | 12.000 (enwiki infobox) | tela "52 NAVIOS" (igual nas duas) |
| Jornada: data | rendição 1º/05/1625 (ptwiki; enwiki "1 April – 1 May 1625") | imagem e06 cita 30/04–01/05 (Commons) | 1º/05/1625 |
| Nassau 1638: navios | "30 or 45 ships" (enwiki infobox) | — | fora da tela; evento na reserva |
| Descoberta do ouro | 1695 Rio das Velhas, Borba Gato (enwiki Brazilian Gold Rush) | 1697 sertões de Taubaté (ptwiki Ciclo do ouro) | ano 1695 = "anos 1690" na data_exata |
| Total de ouro | 800 t enviadas oficialmente a Portugal no séc. XVIII (enwiki) | ~1.000 t produzidas até 1760 (ptwiki Ciclo do ouro) | tela "800 T DE OURO" (oficial) |
| Casa da Moeda | criada em Salvador 08/03/1694; ao Rio em 1699 (ptwiki Casa da Moeda) | "Mint established" em 1674 (enwiki Timeline of Salvador) | 1694 (a ptwiki tem dia e cunhador); 1674 parece erro |
| Data da transferência (1763) | carta régia 27/01/1763, mudança efetivada 31/08/1763 (TJBA; 31/08 também em ebiografia, fonte fraca) | Conde da Cunha "em janeiro de 1763 desembarcava no Rio" e carta de 20/03/1763 "logo que tomei posse" (dissertação UFF, p. 83) | tela só "1763"; ano 1763.5 como posição; dia em data_exata com as duas versões. Posse do vice-rei no Rio: dia não achado em fonte lida |
| Título de vice-rei | alguns desde 1640; todos de 1720 (23/11/1720) a 1808 (enwiki List of governors-general) | "especialmente após 1720"; nunca houve vice-reino formal (ptwiki Estado do Brasil) | HUD "SEDE DO VICE-REI" de 1720.89; nunca "VICE-REINO" |
| Capital 1645–1763 | enwiki State of Brazil (infobox) dá "Salvador (1645–1763)" | ptwiki Estado do Brasil: "Salvador (1549-1624; 1625-1763), Olinda (1624-1625)" | ptwiki (a enwiki corta o início) |
| Forte da Barra | 1ª estrutura 1583–1587, pedra a partir de 1596, forma atual 1696–1702 (ptwiki) | — | reserva 1583; forma em predios.json |
| Elevador Lacerda: altura | 63 m em 1873 (ptwiki, ipatrimonio) | 72 m = estrutura de 1930 (infobox ptwiki) | reserva com "63 M"; 72 m só para o prédio atual |
| Elevador Lacerda: inauguração | 08/12/1873 (ptwiki, IPHAN) | 08/12/1872 (outro trecho da ptwiki) | 1873 |

### Prédios (de `predios.json`)

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| 1ª Casa da Câmara | 1549, taipa e palha (ptwiki, Bahia Notícias) | 1555, Luís Dias (IPAC) | 1549 |
| Torre do Paço Municipal | 1698, Lencastro (IPAC) | "1969" (Bahia Notícias, erro de digitação) | 1698 |
| Reforma neoclássica do Paço | 1885 (Bahia Notícias) | 1887, Caminhoá (IPAC) | 1887 |
| Construção da antiga Sé | 1552 (ptwiki Cruz Caída) | 1553 (mesma página) | 1552 |
| Pedra fundamental da Catedral | 1657 (ptwiki Catedral) | 1652 (ptwiki Terreiro de Jesus) | 1657 |
| Fachada de São Francisco pronta | 1720, data gravada (ptwiki) | ~1723 (ipatrimonio; enwiki Timeline "built 1723") | 1720 para a fachada |
| Forte de Santa Maria: início | 1614 (ptwiki) | 1627 (IPAC) | 1614, com nota |
| Forte de São Diogo: início | 1609–1613 (ptwiki) | 1629 (IPAC) | 1609 |
| 1º Mercado Modelo | 02/02/1912 | 09/12/1912 (mesma ptwiki) | sem efeito (o prédio de 1912 queimou) |
| São Marcelo: distância da costa | ~300 m (ptwiki) | 250 m (bmcnews) | 300 m |
| São Marcelo: anel externo | 241 m de circunferência (ptwiki) | 1.212 palmos ≈ 267 m (Souza 1885) | 241 m (≈ 77 m de diâmetro) |
| Portas de 1549 | Santa Catarina / São Bento (pedido) | São Bento / Carmo (ptwiki); Carmo / Santa Luzia (Jornal Grande Bahia) | ptwiki; "Santa Catarina" não aparece em fonte de Salvador |
| Local das Portas do Carmo | "muralhas da atual Praça Municipal" (ptwiki) | trecho de muralha no Museu da Gastronomia, Pelourinho (mesma ptwiki) | Pelourinho, como aproximação |
| Traçado da muralha de 1549 | não publicado; em 1587 "não há memória aonde eles estiveram" (Gabriel Soares) | — | linha aproximada entre as duas portas, marcada aproximação |

### População e bairros (detalhe em `RESUMO-POP.md`)

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Pop. 1585/1587 | Mattoso: 14 mil em 1585 (4 mil brancos) | Gabriel Soares: 800 vizinhos (×5 ≈ 4 mil) | mesmo dado; um ponto, 1587 = 14.000 |
| Pop. 1759 | 40,2 mil (Cidade-Salvador) | 40.922 (Leia Mais BA, sem ano) | 40.200 |
| Pop. 1775/1780 | cidade 40.900 / 39.209 | município ~57 mil / 65.285 | cidade; município na nota |
| Pop. 1900 | 205.813 (Sinopse 2010, tab. 1.6) | 97.642 (IBGE "Evolução 1872/2010") | 205.813 (97.642 daria queda impossível 1890→1920) |
| Pop. 1970–2010 | IBGE "Evolução" (1.007.195 … 2.676.606) | ptwiki (1.027.142 … 2.675.656) | "Evolução", mesma fonte do Rio |
| Mussurunga | 1977 (ObservaSSA, criação) | 1979 (URBIS, entrega) | 1979 |
| Aquarius | 1968 (ObservaSSA, Pituba) | 1973 (ObservaSSA, Itaigara) | 1968 |
| Cajazeiras IV/V | 1980 (tabela URBIS) | 1982 (Redalyc 2022) | 1980 |
| Barris | séc. XVII, marquês de Barbacena (ptwiki, sem fonte) | o marquês viveu 1772–1842 | descartado; 1890 como limite superior |
| Canela | 1850 (Bahia Notícias) | roça até os anos 1940, ocupação no início do séc. XX (ptwiki) | 1910 |

Bairros: 68 dos 171 oficiais com ano e fonte; 103 em `bairros_sem_dado`. O OSM de Salvador ainda não foi baixado: nomes pela lei, lat/lon `null` — conferir os nomes contra `dados/brutos/bairros.geojson` quando existir.

## Notas para o roteiro e o motor

- **Disposição da praça em 1587** (Gabriel Soares, cap. VII): casas dos governadores no lado SUL, câmara e cadeia no LESTE, fazenda/alfândega/armazéns no NORTE, pelourinho no meio, lado POENTE aberto sobre o mar com artilharia; a cidade "com o rosto ao poente"; a Sé "com o rosto sobre o mar". É 38 anos depois da fundação — usar como a melhor descrição antiga da praça, não como planta de 1549.
- **Muros de taipa**: em 1587 já "se vieram ao chão" e "não há memória aonde eles estiveram" (Gabriel Soares). No vídeo, o muro de 1549 pode nascer e sumir até ~1587; nova muralha desenhada em 1605, 3 a 4 vezes maior (ptwiki História de Salvador).
- **Eventos fora do mapa** (ouro, Caminho Novo, Sacramento, Madri, 1762): local = centro antigo "genérico"; pedir no `recurso_visual` mapa do Brasil/globo com setas — o mapa 3D de Salvador não mostra Minas nem o Prata. O revisor (lista fixa: "o que o cartão cita aparece no mapa") vai cobrar isso.
- **Imagens** (ver `imagens.json`): e01 é ilustração de c. 1915 (Dovaston), não retrato de época; e06 tem marca "PD-self" no Commons sobre um mapa de 1631 (domínio público pelo original); e12 (Pombal) é de 1766; o ano 1763 de e13 (Conde da Cunha) é o do evento, a página só diz "século XVIII"; e00, e01, e11 e e13 têm menos de 1600 px.
- **Não usar na tela sem nova fonte:** o dia da posse do Conde da Cunha no Rio; "devorado" para o bispo Sardinha; número de escravizados desembarcados em Salvador.
