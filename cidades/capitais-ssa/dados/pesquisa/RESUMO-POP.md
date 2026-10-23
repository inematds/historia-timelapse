# Salvador — população e bairros: divergências (22/10/2026)

Arquivos: `populacao.json` e `bairros_epocas.json`.
Fontes lidas como páginas HTML e PDF normais, sem API. O RESUMO.md dos eventos é de outro agente.

## População

| Ano | Valor usado | Outra fonte | Decisão |
|---|---|---|---|
| 1549 | ~1.000 (ptwiki, "mais de mil pessoas" com Tomé de Sousa) | — | confiança média |
| 1570–1590 | fora da curva | Gândavo 1570: 1.100 vizinhos; Cardim 1583: "a cidade com seu termo" ≈ 3.000 vizinhos + 8.000 índios + 3–4 mil escravos (≈ 26 mil); Anchieta 1585: 2.000 vizinhos + 3.000 escravos + 8.000 índios (Carrara, Tempo 2014) | Esses números são da capitania ou do termo com o Recôncavo. Se entrassem, a curva cairia de 26 mil para 14 mil entre 1583 e 1587. Ficaram só no `_meta` |
| 1587 | 14.000 (cidade) | Mattoso dá 1585 e 14.000, "dos quais 4.000 brancos"; Gabriel Soares fala em 800 vizinhos na cidade e 2.000 no Recôncavo | É o mesmo dado (800 × 5 = 4.000 brancos). Entra um ponto só, no ano do Tratado (1587) |
| 1681 | ~13.500 (cidade) | Carrara: "passa de 3.000 vizinhos", de 12 a 15 mil pessoas | Usei o meio da faixa. Fica abaixo de 1587 porque, pelas fontes, o século XVII ficou estagnado (Mattoso fala em "regressão"; houve a invasão holandesa de 1624 e epidemias). Confiança baixa |
| 1724 | fora | padre Gonçalo Soares de França: ~80 mil na capitania, 80% em Salvador e no Recôncavo | escala de capitania |
| 1757 / 1759 | 37.000 (Mattoso) / 40.200 | Leia Mais BA: 40.922 numa contagem "de janeiro", sem ano, também sem os menores de 7 anos | 40,2 mil (Cidade-Salvador) para 1759. 40.922 deve ser a mesma contagem. As duas excluem crianças, então a população real era maior |
| 1775 | 40.900 (cidade) | 57 mil no município (com os subúrbios); 35.253 num censo por cor que Mattoso descartou | cidade, para manter a série coerente com 1780–1807 |
| 1780 | 39.209 (cidade) | 65.285 no município (26.076 nos subúrbios); Leia Mais BA dá os mesmos 39.209 para 1779 | cidade. O município entra na nota |
| 1807 | 51.100 (cidade) | Mattoso: "mais de 50.000" | concordam |
| 1807 → 1872 | 51 mil → 129 mil | — | O salto é em parte territorial: 1872 já conta o município inteiro, com as freguesias rurais e áreas que hoje são Candeias, Simões Filho, Lauro de Freitas e Madre de Deus |
| 1890 | 174.412 (Synopse 1890, IBGE liv25490) | não aparece na tabela "Evolução da população 1872/2010" | Synopse |
| 1900 | 205.813 (ptwiki e enwiki, citando a Sinopse do Censo 2010, tab. 1.6) | **97.642** na tabela IBGE "Evolução da população 1872/2010" | 205.813. O 97.642 faria a população cair de 174 mil (1890) para 98 mil e depois subir para 283 mil (1920); deve ser erro ou outro recorte. Confiança média |
| 1970 | 1.007.195 (IBGE, Evolução) | 1.027.142 (ptwiki); 998.258 "city" (enwiki, ONU) | IBGE, Evolução (mesma fonte do Rio) |
| 1980 | 1.502.013 | 1.531.242 (ptwiki) | IBGE, Evolução |
| 1991 | 2.075.273 | 2.072.058 (ptwiki e enwiki) | IBGE, Evolução |
| 2000 | 2.443.107 | 2.440.828 (ptwiki) | IBGE, Evolução |
| 2010 | 2.676.606 | 2.675.656 (ptwiki e enwiki) | IBGE, Evolução |
| 2022 | 2.417.678 (PDF IBGE, Primeiros Resultados, 2ª apuração) | ptwiki igual | — |

- **Território:** ao contrário do Rio, Salvador encolheu. Saíram Candeias (1958), Simões Filho (1961), Lauro de Freitas (1962) e Madre de Deus (1989); entraram ilhas em 1931 e 1947 (DTB/IBGE). As diferenças entre a tabela "Evolução" e a ptwiki em 1970–2010 devem vir em parte daí (base territorial) e em parte de revisões do IBGE.
- **Fator vizinhos → pessoas:** ×5 (Contreiras Rodrigues, usado por Carrara).
- **2010 → 2022: −9,7%.** É queda de verdade; o território não muda desde 1989.
- **Fontes secundárias:** os números do século XVIII vêm do site Cidade-Salvador.com (que cita Brás do Amaral/Accioli e Mattoso, *Bahia Século XIX*) e do Leia Mais BA (que cita Mattoso). Não achei on-line o texto de Mattoso (1992) nem a *Notícia Geral* de Caldas (1759). Por isso a confiança é baixa ou média.

## Bairros

- **Nomes:** a lista oficial tem 171 bairros (Lei 9.278/2017 com 163, mais 7 por decreto em 2020 e Aquarius em 2024). O OSM de Salvador ainda não foi baixado, então os nomes vêm da lista; ao casar com o OSM, conferir as variantes listadas em `_meta.nomes_osm`.
- **Cobertura:** 68 bairros têm data com fonte e 103 ficaram sem dado. A maioria das páginas da ptwiki é esboço sem história. A melhor fonte foi o ObservaSSA/UFBA, que tem histórico para 35 bairros. Os conjuntos habitacionais vêm da tabela da URBIS na ptwiki, que é marcada "carece de fontes", por isso a confiança é média.
- **Convenção para datas vagas:** "a partir da década de X" → X; "na década de X" → X+5; "século XIX" → 1850; "primeiras décadas do séc. XX" → 1910. Todas com confiança baixa.
- **Divergências:**
  - Mussurunga: 1977 no ObservaSSA ("criado") e 1979 na URBIS (entrega do Mussurunga I). Usei **1979**, a data da entrega.
  - Aquarius: 1968 no ObservaSSA da Pituba ("criação dos loteamentos") e 1973 no ObservaSSA do Itaigara. Usei **1968**.
  - Cajazeiras IV e V: 1980 na URBIS; o artigo do Complexo Cajazeiras (Redalyc, 2022) diz que os primeiros conjuntos foram inaugurados em 1982. Usei **1980**.
  - Sete de Abril: 1967 na URBIS (500 casas); a ptwiki diz "ao longo da década de 1960". Usei **1967**.
  - Conjunto Guilherme Marback: a URBIS põe na Boca do Rio; o ObservaSSA põe no Imbuí. Não usei para nenhum dos dois.
  - Rio Vermelho, bonde: uma busca deu 1870 (Correio, não lido); o ObservaSSA (lido) diz bonde elétrico em 1906. O ano do bairro é **1850**, pelos núcleos urbanos do séc. XIX.
  - Barris: a ptwiki diz que a ocupação começou com o marquês de Barbacena no "século XVII", mas ele viveu de 1772 a 1842 e o trecho não tem fonte. Usei 1890 como limite superior ("construções do final do século XIX").
  - Canela: o Bahia Notícias inclui a Canela na aquisição de terras a partir de 1850; a ptwiki diz que ali era uma roça até os anos 1940, com ocupação urbana nas primeiras décadas do séc. XX. Usei **1910**.
  - Barra: Vila do Pereira em 1536 (cerca de 100 habitantes), esvaziada no séc. XVII. Usei **1850** (Bahia Notícias), com `ano_colonial` 1536.
  - Freguesia de Santo Antônio: 1646 na ptwiki, 1648 na DTB/IBGE. Usei **1646**.
- **Freguesias coloniais usadas como ocupação urbana:** Santo Antônio (1646), Vitória (1561) e Penha → Ribeira (1760), porque estão entre as 10 freguesias da zona urbana. Brotas (1718) era "eminentemente rural": o ano do bairro ficou 1915 (loteamentos), com 1718 em `ano_colonial`.
- **Sem dado de propósito:** Centro e Saúde. Nenhuma fonte lida liga esses bairros oficiais a uma freguesia ou a uma data; o motor dá a eles um ano antigo pela distância.
- **Fazenda Grande I–IV:** a página "Fazenda Grande (Salvador)" é da Fazenda Grande do Retiro. Os quatro ficaram sem dado.
