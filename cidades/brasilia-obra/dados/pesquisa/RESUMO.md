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

## Construção de Brasília — pesquisa nova (24/10/2026)

Arquivos novos: `eventos_novos.json` (16 eventos + 8 de reserva, ids sem colisão com `eventos.json`, campo extra `local.dentro_bbox`), `imagens_novas.json` + `assets/epoca/n00–n14.jpg` (15 imagens). Fontes lidas como página HTML ou PDF, sem API. Coordenadas "OSM local" vêm do `dl/distrito-federal.osm.pbf` (Geofabrik), lidas com `scripts/acha_osm.py`. Um script local conferiu título ≤ 30 em maiúsculas, legenda ≤ 95, detalhe ≤ 220, ids únicos, flag do bbox e ordem dos anos.

### Achados

| id | data | dentro do bbox | o essencial |
|---|---|---|---|
| `igreja-sao-sebastiao-planaltina` | capela 1810, ampliada ~1881 | sim | igreja mais antiga do DF, tombada em 19/08/1982; coord. ptwiki -15.62333, -47.66222 |
| `mestre-darmas-1859` | 19/08/1859 (convenção) | sim | Praça São Sebastião (OSM) -15.623547, -47.66226 |
| `cruls-mestre-darmas-1892` | 09/06 a 20/09/1892 | sim | Relatório: saída do Rio 9/6, Uberaba 29/6, Pirenópolis 1/8, **Mestre d'Armas 20/09/1892**; 22 homens, 9.640 kg |
| `quadrilatero-cruls-1892` | out–dez/1892 | centro sim, vértices não | **vértices achados** (Relatório Cruls 1894, no PDF da CLDF) |
| `acampamento-cruls-1894` | nov/1894 | sim | 2ª missão acampa no Bananal × Córrego do Acampamento (inferido); Glaziou propõe o lago |
| `pedra-fundamental-planalto-1922` | 07/09/1922, meio-dia | sim | obelisco de 3,75 m, OSM -15.685365, -47.679135 |
| `brazlandia-1933` | 05/06/1933 (convenção) | **não** | núcleo antigo do oeste |
| `sitio-castanho-1955` | 13 e 15/04/1955 | sim | 867 × 800 pontos; ponto mais alto (1.172 m) = Praça do Cruzeiro |
| `novacap-sede-1956` | 1956–1959 | sim | sede de comando na Candangolândia ("Velhacap") |
| `vila-planalto-1957` | 1957 | sim | 22 acampamentos, ~320 ha; **coord. achada** no OSM: -15.79268, -47.850277 |
| `ermida-dom-bosco-1957` | 1957 (04/05?) | sim | OSM -15.798343, -47.809504 |
| `barragem-paranoa-obra-1957` | 12/06/1957 → 12/09/1959 | sim | **coord. da barragem** (OSM, waterway=dam): -15.799752, -47.784798 |
| `vila-amaury-1957` | 1957–1959 | sim | ~16 mil moradores; ponto aproximado -15.781, -47.856 |
| `hjko-1957` | 06/07/1957 | sim | 23 prédios de madeira; OSM -15.860222, -47.959553 |
| `lei-3273-1957` | 01/10/1957 | **não** (Rio) | data da mudança fixada; lei assinada "Rio de Janeiro" |
| `fatima-1958` | 26/10/1957 → 28/06/1958 | sim | 19 m, ~100 lugares; OSM -15.813973, -47.903762 |

Reserva: `relatorio-cruls-1894`, `jatai-1955` (fora), `fazenda-bananal-1955` (sem coord.), `aeroporto-vera-cruz-1956`, `contagem-1958`, `rota-anapolis` (fora), `belem-brasilia-1958` (fora), `vila-paranoa-1957`.

**Vértices do Quadrilátero Cruls** (prescritos no Relatório, longitude em tempo convertida para graus): NW -15.333333, -48.854167; NE -15.333333, -47.354167; SE -16.143056, -47.354167; SW -16.143056, -48.854167. Isso dá um retângulo de 160,5 × 90,0 km (cálculo) e 14.406 km² (Relatório). **Todos ficam fora do bbox**, então só entram no globo ou no minimapa. Valores observados em campo: NW 15°20'7,4" S e 3h14m55,6s; SE 16°8'14" S e 3h9m6,7s.

**De onde a obra era comandada (item 8):** no canteiro, pela sede da Novacap na Candangolândia (1956–59: Israel Pinheiro, mais os diretores Sayão, Ernesto Silva e Íris Meinberg); nos despachos de JK, pelo Catetinho (ele vinha e voltava ao Rio no mesmo dia) e depois pelo Catetão (maio/1957 a junho/1958); nos atos de governo, pelo Rio — a Lei 2.874 (1956) e a Lei 3.273 (1957) foram assinadas "Rio de Janeiro".

**População antes de 1957 (item 4):**
- Em 1950 o município de Planaltina (GO) tinha **7,3 mil habitantes** (IBGE, *Veredas de Brasília*, 2010). Esse município cobria uma área maior que o DF e cedeu a maior parte do território, inclusive a sede.
- A contagem de julho de 1957 achou 12.283 pessoas, "das quais aproximadamente a metade estava radicada nas 'zonas velhas'", isto é, nas áreas rurais e na antiga Planaltina.
- Em 1959 a cidade de Planaltina tinha 2.247 pessoas.
- Censo de 1940 do município: **não encontrado**.

### Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Latitude norte do Quadrilátero | tabela de vértices do Relatório (CLDF): "A 15º 10'0\"", "B 15º 10'" | o mesmo Relatório: "adoptámos 15º20'0''" e arcos 15º20'0"/16º8'35"; a turma NW cita 15º20' | **15°20'**. Com 15°10' o lado N–S teria ~108 km; com 15°20' dá 90 km. A tabela tem erro de impressão. |
| Área do Quadrilátero | 14.400 km² (Constituição, Senado) | 14.406 km² (cálculo do Relatório); 14.440 km² (ptwiki) | 14.400 na tela |
| Turma NE | Julião de Oliveira (texto da CLDF) | Antônio Cavalcanti de Albuquerque (JBr); "A. Cavalcanti Fragoso, chefe da turma NE" (índice do Relatório) | não citar o nome do NE na tela |
| Membros da Missão | 22 homens (Correio Braziliense 2018) | Cruls + 21 (ptwiki) | é o mesmo número: 22 |
| Volta ao Rio | jan/1893, "primeiro mês do ano seguinte" (JBr) | "treze meses" (ptwiki); "meados de 1892 a princípios de 1893" (CLDF) | fora da tela |
| Fundação de Planaltina | 19/08/1859, Lei nº 03 (ptwiki, data adotada em 1967) | IBGE DTB: distrito pela resolução 615 de **02/04/1880**; vila em 19/03/1891; município instalado em 28/02/1892; "difícil dizer-se precisamente" | tela: "século XIX" ou "1859" com a ressalva |
| Nome Planaltina | Lei nº 451 de 14/07/1917 (ptwiki) | lei estadual nº 541 de 14/06/1917 (IBGE DTB) | só "1917" |
| Igreja de São Sebastião | capela de 1810 e ampliação ~1881 (texto da ptwiki) | "Inauguração 1890" (infobox) | tela: "início do século XIX" |
| Distância Pedra–Planaltina | "exatamente 10 km" (ptwiki) | 7,1 km em linha reta da praça (cálculo) | não pôr km na tela |
| Quem lançou a pedra | Epitácio "fez assentar" (ptwiki), por decreto | quem ergueu foi Balduíno Ernesto de Almeida (EF Goiás), avisado em 27/08; assistiram delegações (IBGE DTB) | "por ordem de Epitácio Pessoa" |
| Data da Novacap | 19/09/1956, Lei 2.874 (eventos.json) | "Em 15 de março de 1956 o presidente criou a Novacap" (ptwiki Construção) | 19/09/1956. A data de março deve ser a mensagem do projeto (não verificado). |
| Rabelo × Pacheco Fernandes | JBr: Rabelo fez o Brasília Palace e Pacheco Fernandes o Alvorada | ptwiki Vila Planalto: Pacheco Fernandes Dantas fez o Brasília Palace | não atribuir obra na tela |
| Ermida Dom Bosco | "concluída em 1957", "primeira obra de alvenaria" (ptwiki) | inaugurada em 04/05/1957 (Guia da Semana); "construída em 1956" (artigo salesiano, só pela busca) | "1957", confiança baixa |
| "Primeiro templo/obra de alvenaria" | Ermida (ptwiki) | Igrejinha de Fátima, "primeiro templo católico em alvenaria" (ptwiki) | não usar "primeiro" na tela |
| Igrejinha em "100 dias" | "construída em cem dias" (ptwiki) | da pedra (26/10/1957) à inauguração (28/06/1958) são 245 dias | "1958", sem os 100 dias, a menos que o Nei queira |
| Fechamento da barragem | 12/09/1959 (ptwiki, Senado) | "meados de 1960", sem registro preciso (Correio Braziliense 2007, via RESUMO-POP) | 12/09/1959; cota 1000 só depois das chuvas de 1961 |
| Primeiros candangos | ~500 em alojamentos no fim de 1956; 2.500 em jan/1957 (IBGE 2010) | "250 candangos" em 1956 (IFB, que cita IBGE 2010) | IBGE |
| 28.804 em março de 1958 | "pessoas" (contagem do IBGE) | "operários" (IFB) | são **pessoas**, não operários |
| Operários no pico | 64.314 em 1959 é a **população** do censo experimental | "cerca de 60 mil operários" é número de divulgação, sem censo | não há número de operários no pico com fonte. Na tela, só população. |
| "30 mil operários" (item 5 do RESUMO acima) | o RESUMO de 22/10 cita ptwiki DF, JK e Construção (DF e JK não relidos hoje) | ptwiki Construção, relida hoje: a Cidade Livre "chegou a ter cinco mil moradias e cerca de trinta mil **habitantes**" | tirar "30 mil operários" da tela até achar a fonte; se usar, "30 mil moradores na Cidade Livre" |
| Sacolândia | antigo nome da Candangolândia (ptwiki Candangolândia) | outro nome da Vila Amaury (ptwiki Vila Amaury) | evitar o nome |
| Museu Vivo | inaugurado em 26/04/1990 (ptwiki HJKO) | infobox "1991" (ptwiki Museu Vivo) | fora da tela |
| Sayão: local da morte | infobox: "Brasília, DF" | texto: "Imperatriz" | fora da tela |
| Sede da Novacap | prédio da Administração Regional da Candangolândia (OSM; o jornal diz que a antiga sede "depois abrigou" a Administração) | o OSM "Novacap" (-15.8175, -47.9529) é a sede atual, ali há 66 anos | Candangolândia, confiança média |

### Não encontrado

- **Dimensões da Igreja de São Sebastião.** Nenhuma página dá metros; a foto n04 mostra a forma.
- **Coordenada do Sítio Castanho** como área. Achei só o ponto mais alto (Cruzeiro) e o limite do DF (rios Preto e Descoberto, paralelos 15°30' e 16°03'). As cores e a posição dos outros quatro sítios não têm coordenada.
- **Sede da Fazenda Bananal e das outras fazendas** (Gama, Torto, Sobradinho, Paranoá, Vicente Pires, Riacho Fundo). Não achei coordenadas nem os nomes dos moradores. Achei só os donos da gleba do Bananal (Jerônimo José da Silva e Jorge Pelles). Número de fazendas: "cerca de mil desapropriadas total ou parcialmente" (Agência Brasil) e "103 fazendas de criação extensiva em 1955" (Pébayle, RBG/IBGE, visto só pela busca). Nenhum dos dois é contagem oficial.
- **Censo de 1940 de Planaltina (GO).**
- **Onde Niemeyer e a equipe de arquitetura trabalhavam no canteiro.** Ele chefiava a Divisão/Departamento de Arquitetura da Novacap (resumos de busca), mas o local físico não aparece.
- **Quantas vezes JK foi ao Catetinho ou despachou lá.** A ptwiki diz só "visitas diária[s]" com volta ao Rio no mesmo dia.
- **Número de operários por acampamento da Vila Planalto.** A data de 03/02/1957 e o engenheiro Peri Rocha França vieram só do resumo de busca (Correio Braziliense 2022).
- **Coordenada exata da Vila Amaury.** Nem a SBGf 2010 tem registro certo; usei o meio da enseada entre o Iate Clube e os Fuzileiros.
- **Ano de abertura da estrada Anápolis–Brasília (BR-060).** A ptwiki dá só os 139 km e "asfalto só em 1960".
- **Fotos em domínio público de:** Planaltina antes de 1956, Pedra Fundamental em 1922, sede da Novacap na Candangolândia (tenho só o barracão do Departamento de Viação e Obras, sem local), Vila Planalto e Vila Amaury da época, e Ermida em 1957.

### Alertas para o motor

- **Lago:** antes de 1959,7 o vale tem só os rios. O Paranoá nascia da junção do Gama e do Riacho Fundo (braço sul; Gama inferido, a página dele deu 404) com o Torto e o Bananal (braço norte) e saía para leste pela garganta da barragem (-15.7998, -47.7848), até o São Bartolomeu (ptwiki Rio Paranoá e Lago Paranoá). No OSM local, o "Rio Paranoá" começa em -15.7978, -47.7839, logo abaixo da barragem.
- A Vila Amaury, a Vila Planalto (em parte) e o acampamento da 2ª Missão Cruls ficam onde depois veio a água ou perto dela.
- **Imagens:**
  - n03, n04 e n13 são fotos atuais.
  - n01 (620 px) e n02 (478 px) têm baixa resolução.
  - n06 tem título que não bate com a imagem.
  - n12 é CC BY-SA, com autoria "atribuída" a Mário Fontenelle.
