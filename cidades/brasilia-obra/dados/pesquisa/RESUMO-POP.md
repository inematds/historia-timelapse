# Brasília / DF — população, bairros (RAs) e regimes: divergências (22/10/2026)

Arquivos: `populacao.json`, `bairros_epocas.json`, `regimes.json`.
Fontes lidas como páginas HTML ou PDF normais, sem API (ptwiki/enwiki, PDFs do IBGE, IPEDF/Codeplan, Senado).

## População

A série principal é o **DF inteiro** (IBGE 5300108). O DF é município único, então não existe série oficial só de "Brasília cidade". **Regra:** resultado definitivo do IBGE. De 1960 a 1991 vem da tabela *Evolução da população segundo os municípios 1872/2010*; 2000 e 2010 vêm da Sinopse do Censo 2010; 2022 vem dos Primeiros Resultados.

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| "Censo experimental 1957" (pedido) | IPEDF 2016: Censo Experimental de Brasília com **data de referência 17/05/1959**, 64.314 hab. | Boletim Geográfico IBGE 1973: "Censo Experimental de Brasília, Rio de Janeiro, 1959" | O censo experimental é de **1959**. O número de 1957 é uma **contagem** do IBGE. |
| 1957 | IPEDF 2016: **12.283** ("contagem populacional realizada pelo IBGE"; cerca de 50% na zona rural e em Planaltina) | Paviani & Barbosa, BG IBGE 1973: **12.700** (cita "Brasília, Coleção de Monografias nº 391", apud Codeplan 1970) | 12.283, porque cita o IBGE diretamente. Confiança média. |
| 1960 | IBGE Evolução 1872/2010: **140.164** (88.334 urbana + 51.830 rural) | Sinopse Preliminar 1962, via BG 1973 e ptwiki: **141.742** | 140.164 (definitivo, mesma tabela da série) |
| 1970 | IBGE Evolução: **537.492** | Sinopse Preliminar 1971, via BG 1973 e ptwiki: **546.015** | 537.492 |
| 1980 | IBGE Evolução: **1.176.908** | ptwiki: 1.203.333 (não achei a fonte primária) | 1.176.908 |
| 1991 | IBGE Evolução: **1.601.094** | ptwiki: 1.598.415 | 1.601.094 |
| 2000 | IBGE Evolução e Sinopse 2010: **2.051.146** | ptwiki: 2.043.169 | 2.051.146 |
| 2010 | Sinopse do Censo 2010 (IBGE): **2.570.160** (igual à ptwiki) | IBGE Evolução 1872/2010: **2.562.963** | 2.570.160 (é o resultado divulgado do censo). A diferença é interna do próprio IBGE. |
| 2022 | IBGE Primeiros Resultados (2ª apuração): **2.817.381** | ptwiki: o mesmo número | 2.817.381 |
| Plano Piloto separado | ptwiki (infobox): 214.529, PDAD 2010/2011 da Codeplan | — | Um ponto só, em `serie_plano_piloto`. Não é série. O PDF da Codeplan não foi lido (o link é antigo). |

- **Território:** de 1960 a 2022 é sempre a mesma linha do IBGE (DF inteiro). Em 1957 e 1959 a contagem é da "área destinada ao futuro DF", que ainda era Goiás.
- **O bbox não cobre o DF inteiro.** Gama, Santa Maria e Brazlândia ficam fora. O HUD mostra a população do DF.

## Bairros (Regiões Administrativas)

- **Ocupação × lei:** a coluna "Fundação" da ptwiki é, pela nota da própria página, "uma convenção". Taguatinga e Sobradinho, por exemplo, adotaram a data em 1967. A data da lei da RA vai em `ano_criacao_RA`.
- **Critérios de escolha do ano, por RA:**

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Asa Norte | primeiros blocos nas SQN 403–406, a partir de 1957 (IAPC) | 2º foco em 1965; de 1965 a 1970 a maioria das SQN | 1965 (onda principal); 1957 fica em `ano_primeiro_foco` |
| Fercal | ptwiki: "nasceu em meados de 1956" (fundação 11/09/1956) | ptwiki/IPEDF: mineradora autorizada em 1961 | 1961 |
| SCIA/Estrutural | IPEDF: origem "na década de 60" (lixão) | IPEDF: "início da década de 90, menos de 100 barracos"; expansão depois | 1992 (`ano_origem_aprox` 1965) |
| SIA | IPEDF: 1958, depósitos das construtoras | ptwiki: fundação 21/04/1969, marcada como "carece de fontes" | 1958 |
| Guará | ptwiki/IPEDF: construído/criado em 1967 | ptwiki: fundação 05/05/1969 | 1967 |
| Vicente Pires | IPEDF: ocupação urbana a partir de 1991 | ptwiki: fundação 26/05/1989 (contratos agrícolas) | 1991 |
| Sudoeste/Octogonal | IPEDF: Sudoeste criado em 1989 e habitado em 1993; Octogonal implantada nos anos 80 | ptwiki: fundação 10/07/1989 | 1993 |
| Águas Claras | ptwiki: Lei 385, de 16/12/1992, aprova o plano de ocupação | data dos primeiros moradores não achada | 1992, confiança média |
| Paranoá | ptwiki: acampamento da barragem em 1957 | a fixação definitiva "não ocorreu na área original" (sem ano) | 1957, confiança média. O núcleo atual pode ser mais novo. |
| São Sebastião | ptwiki: olarias a partir de 1957 | o núcleo urbano se formou "aos poucos"; RA de 1993 | 1957, confiança baixa |
| Planaltina | IPEDF/ptwiki: distrito de Mestre D'Armas, 1859 | — | 1859, limite superior (o núcleo já existe no início do vídeo) |

- **Sem coordenada em nenhuma das duas wikis:** Arniqueira, Arapoanga, Água Quente, Sol Nascente/Pôr do Sol, 26 de Setembro, Ponte Alta, Vila Planalto e Vila Telebrasília. Nesses casos o bbox foi decidido pelo texto de limites. As quatro duvidosas estão em `bbox_incerto`.
- **Sem data de ocupação:** 26 de Setembro e Ponte Alta (RAs de 03/07/2026). Varjão, Santa Maria, Arapoanga e Água Quente só têm a "fundação" convencional, marcada como `limite_superior`.
- **Casamento com o OSM pendente:** `dados/brutos/` está vazio.

## Obras (lago e pontes)

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Início da barragem | Senado/BDSF (jornal): contrato a partir de 12/06/1957; ensecadeira em dez/1958 | IPEDF Lago Sul: "1956: início das primeiras obras de represamento" | 1957 |
| Fechamento da barragem e início do lago | Senado/BDSF e ptwiki Lago Paranoá: 12/09/1959 | Correio Braziliense 2007 (visto só na busca, não lido): inauguração "em meados de 1960", sem registro preciso | 12/09/1959 (1959.7) |
| Lago cheio (cota 1000) | Senado/BDSF: depois da temporada de chuvas de 1961 | IPEDF Lago Norte: a península se formou em "1959/1960" | ~1961 |
| "Ponte das Garças/Costa e Silva 1976" (pedido) | Ponte das Garças: 1974 (IPEDF; o blog do CB dá a obra de 29/06/1973 a 14/01/1974) | Ponte Costa e Silva / Honestino Guimarães: 1976 (ptwiki, IPEDF) | São **duas pontes**. Cada uma tem sua entrada. |
| "Primeira ponte sobre o lago" | IPEDF: Ponte das Garças (1974) | ptwiki: Ponte do Bragueto, aberta em junho de 1961, também cruza o Lago Paranoá | As duas entram. A frase do IPEDF só vale para o lado do Lago Sul. |

## Regimes e HUD

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| 1º governador eleito | ptwiki CLDF: primeiras eleições (governador e distritais) em outubro de 1990; posse dos deputados em 1º/01/1991 | ptwiki DF: Joaquim Roriz, "mandato compreendido de 1988 a 1990" | Usar outubro de 1990 (a CLDF descreve o fato). A frase da página do DF mistura o mandato de Roriz como governador nomeado com o eleito. Não resolvi, só registro. |
| UNESCO | ptwiki Brasília: 07/12/1987 | IPEDF Sudoeste: 07/12/1987 | 07/12/1987. O site da UNESCO bloqueou o acesso. |
| Tombamento | ptwiki Plano Piloto: IPHAN em 14/03/1990 e decreto distrital 10.829/1987 | IPEDF: Portaria IPHAN 314, de 08/10/1992 | Linha opcional com as duas datas |
| Data da Constituição | 05/10/1988 não aparece nas páginas lidas (elas dizem só "1988") | — | Confiança média; conferir antes de pôr na tela |
