# Brasília (ato 3 de "As capitais do Brasil") — pesquisa (22/10/2026)

## Arquivos

| Arquivo | O que tem |
|---|---|
| `eventos.json` | 28 eventos de 1956 a 2022 + 10 de reserva (aeroporto 1957, AI-5 1968, hotel, Rodoviária, pontes, Teatro, Memorial, eleição 1990, Museu e 8/1/2023, este só com OK do Nei). Esquema do Rio. A "mudança lenta dos ministérios e embaixadas" ficou de fora por falta de fonte lida. |
| `predios.json` | **16 prédios para o 3D**: Congresso (plataforma, cúpula, cuia, torres, passarela, rampa), Planalto, Alvorada, STF, Catedral, bloco-tipo da Esplanada (×17), Itamaraty, Teatro, Torre de TV, Catetinho, Rodoviária, Ponte JK, Memorial JK, Panteão, Museu Nacional, Mastro. Cada medida traz a fonte, ou diz `medido_ms` ou `estimado`. |
| `eixos.json` | Eixo Monumental (7 pontos, azimute ≈ 286°/106°), Eixo Rodoviário (5 pontos; a ponta sul está pendente), Quadrilátero Cruls (só a área, sem os vértices). |
| `populacao.json`, `bairros_epocas.json`, `regimes.json`, `RESUMO-POP.md` | Série do DF de 1957 a 2022, 37 RAs com ano de ocupação separado do ano da lei, obras (barragem e pontes), regimes, faixa 1964–1985 e status no HUD. Divergências de população e das RAs estão no `RESUMO-POP.md`. |
| `imagens.json` + `assets/epoca/e00–e13.jpg` | 14 fotos do Arquivo Nacional, todas em domínio público, de 1956 a 1970. |

Fontes lidas como página HTML (pt/en.wikipedia.org/wiki/…, vitruvius.com.br, camara.leg.br, mdc.arq.br) e PDF de artigos (UFRGS/PROPAR, Mecánica Computacional/AMCA 2010, Senado). Nenhuma API foi usada. As medidas `medido_ms` vêm do arquivo local `dl/msbuild/qk210131231.csv.gz` (Microsoft Building Footprints, quadkey de Brasília), calculadas por script local com shapely. Um script local conferiu os limites (título ≤ 30 em maiúsculas, legenda ≤ 95, detalhe ≤ 220), os ids únicos, o bbox e a ordem dos anos.

## Como Brasília foi construída

1. A Constituição de 1891 já mandava a capital para o Planalto Central, e a Missão Cruls demarcou ali um retângulo de 14.400 km² (Senado; ptwiki Missão Cruls).
2. JK fez da mudança sua promessa de campanha. Em 19/09/1956 a Lei 2.874 criou a Novacap, com Israel Pinheiro na presidência e Niemeyer como arquiteto (ptwiki Novacap).
3. Tudo começou do zero: em 2/10/1956 JK dormiu na Fazenda do Gama, e o Catetinho, de madeira, ficou pronto em 10 dias (ptwiki Catetinho).
4. O concurso do Plano Piloto recebeu 26 propostas. Em 16/03/1957 venceu Lúcio Costa, com dois eixos em cruz: o Monumental para o governo e o Rodoviário, em arco, para as superquadras (ptwiki Concurso; Construção de Brasília).
5. Cerca de 30 mil operários, os candangos (muitos nordestinos), trabalharam dia e noite. Moravam em acampamentos e na Cidade Livre (ptwiki DF, JK, Construção).
6. O material chegava por rodovias novas e pelo aeroporto, aberto em 3/05/1957. As estruturas eram de concreto armado (palácios, cúpulas, Catedral), com cálculo de Joaquim Cardozo feito do Rio, ou de aço (torres do Congresso, ministérios), com vigas importadas dos EUA (Vitruvius 131.00; ptwiki Congresso).
7. O primeiro palácio, o Alvorada, foi inaugurado em 30/06/1958 (ptwiki). O lago começou a encher com o represamento do Paranoá em 12/09/1959 e cobriu a Vila Amaury (ptwiki Lago Paranoá).
8. As condições de trabalho eram duras: salário atrasado e o massacre da Guarda Especial de Brasília em 8/02/1959 (ptwiki).
9. O DF passou de 12.283 moradores (1957) para 64.314 (1959) e 140.164 (censo de 1960).
10. Brasília foi inaugurada incompleta em 21/04/1960, depois de 41 meses de obra (ptwiki DF; enwiki). A Catedral era só estrutura e só abriu em 1970, junto com o Itamaraty. A Torre de TV ficou pronta em 1967 e o Teatro em 1981.
11. Os operários não couberam no plano. As cidades-satélites (Taguatinga 1958, Sobradinho e Gama 1960, Ceilândia 1971 pela CEI) cresceram mais que o Plano Piloto, planejado para 500 mil pessoas no ano 2000 (ptwiki Construção).

## Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Senado × Câmara: "côncava/convexa" | ptwiki: Senado "abaixo da cúpula côncava", Câmara "convexa, em forma de prato, virada para cima" | Congresso (visite/arquitetura): "a cúpula menor, voltada para baixo, abriga o Senado" | Em 3D: **Senado = domo de 38 m ao NORTE**, **Câmara = tigela de 62 m ao SUL**, ambos com 10 m de altura. A ptwiki usa os termos vistos de baixo. |
| Comprimento da plataforma do Congresso | infobox ptwiki: "diâmetro 166 m" | peristilo oeste de 160 m (Vitruvius 131.00); footprint 160,4 × 65,1 m | 160 × 65 m |
| Passarela entre as torres | "unidas por passarelas suspensas" (Arquivo Público do DF, citado num resumo de busca) | "interligadas à meia altura" (Senado, citado num resumo de busca, página não aberta) | Ligação a meia altura, andar exato **estimado** (≈ 11º–13º), confiança baixa. Conferir numa foto frontal. |
| Torres: 28 ou 29 andares | 28 (ptwiki, enwiki, Câmara, Vitruvius) | 29 (Arquivo Público do DF, via resumo de busca) | 28 |
| Planta "84 × 75 m, 9 semiarcos" | resumo de busca atribuiu ao Planalto | o artigo-fonte (Inojosa & Buzar 2010, §4.6; Vitruvius 161.02) diz que é o **Palácio da Justiça** | Não usado no Planalto. O Planalto ficou com o footprint medido (126 × 75 m) e a marca "conferir". |
| Diâmetro da Catedral | 60 m (anel no solo; Inojosa & Buzar) | 70 m ("área de setenta metros", ptwiki; enwiki) | 60 m para as colunas; 70 m é a praça/espelho em volta. Altura 42 m (enwiki). |
| Inauguração do Itamaraty | 20/04/1970 (infobox enwiki) | 21/04/1970 (texto enwiki; Inojosa & Buzar) | só o ano 1970 na tela |
| Altura da Torre de TV | 224 m hoje (ptwiki, enwiki) | 218 m na inauguração, +6 m depois (enwiki) | tela em 1967: "218 M" (a altura daquele ano); o detalhe diz "hoje 224 m"; o modelo 3D usa 224 m |
| Altura dos arcos da Ponte JK | 62 m (ptwiki) | 60 m (enwiki) | fora da tela; 3D com 62 m |
| Data da 1ª missa | 3/05/1957 (ptwiki Memorial JK) | 01/05/1957 (página do Commons da foto e02) | 3/05/1957; a foto ilustra o evento |
| Mês do Censo Experimental | "julho de 1959" (ptwiki Construção) | 17/05/1959 (IPEDF, via populacao.json) | 17/05/1959 (1959.37) |
| "Censo experimental de 1957" (pedido) | — | o Censo Experimental é de 1959; o número de 1957 (12.283) é uma contagem do IBGE (RESUMO-POP) | 1957 = contagem, 1959 = censo experimental |
| Área do Quadrilátero Cruls | 14.400 km² (PDF do Senado) | 14.440 km² (ptwiki) | 14.400 |
| Extensão do Eixo Monumental | 16 km (ptwiki/enwiki) | Praça → Rodoferroviária = 9,0 km em linha reta (coordenadas) | Não vai para a tela. Desenhar da Praça à Rodoferroviária. |
| Coordenada da Esplanada | enwiki "Esplanada" (redireciona para Monumental Axis): -15.7869, -47.9036 | fica a 3 km dos ministérios | Descartada. Blocos posicionados pelo footprint. |
| Coordenada do Jaburu (ptwiki) | geohack = a do Congresso (erro) | infobox 15°47′46″S 47°49′59″O | prédio não usado |
| ptwiki "Palácio do Itamaraty" | é o do Rio de Janeiro | — | usada a enwiki Itamaraty Palace |

## Pendências e alertas para o motor

- **Lago:** o motor desenha o lago de hoje desde o início. Em 1956–59 não havia lago, então é preciso uma máscara de água por época (antes de 1959.7 só os rios Paranoá, Gama, Riacho Fundo e Bananal). É o mesmo problema dos aterros do Rio (Lessons do CLAUDE.md).
- **Planalto e STF:** não achei dimensões publicadas. Os valores vêm do footprint do ML (126 × 75 m e 75 × 56 m, que podem incluir anexos). Quando o pbf do Centro-Oeste chegar, conferir no OSM e checar se o número de "velas" do Planalto é 9.
- **Alvorada:** o ML não detecta o prédio. Usar 110 × 30,75 m, colunas de 8,95 m a cada 10 m. A orientação da fachada é **estimada**.
- **Eixo Rodoviário:** a ponta sul não tem coordenada em página lida. Os pontos das asas são o centro dos bairros, não a pista. Trocar pela geometria do OSM.
- **Quadrilátero Cruls:** os vértices não foram achados. A área (14.400 km²) é quase seis vezes o bbox (~2.460 km²), então só cabe no globo ou como texto.
- **Catetinho:** fica a 280 m da borda sul do bbox.
- **Mastro da Bandeira:** o ano de 1972 **não foi lido**. Confirmar antes de usar.
- **Gama, Santa Maria e Brazlândia** ficam fora do bbox. O Gama entra só no texto do evento `satelites-1960`.
