# Itaguaí — divergências entre fontes (população)

- **1970:** tabela IBGE "Evolução da população segundo os municípios 1872/2010" = 55.839; Monografia IBGE nº 509 (Itaguaí, 2ª ed.) = 57.680 recenseados (presentes) e 55.860 residentes. Usado 55.839 (mesma série dos outros anos).
- **2022:** ptwiki chama 116.841 de "estimativa 2023"; o IBGE Cidades dá 116.841 como Censo 2022. Usado como censo 2022.
- **1840/1850:** só via Ruiz (ANPUH 2011), que cita estimativas provinciais — não conferidas no relatório original.
- **Paracambi:** a ptwiki/sites citam emancipação "1969"; o DTB IBGE dá lei 4.426 de 08/08/1960, instalado em 13/11/1960. Vale o DTB (o censo de 1960 ainda inclui Paracambi).
- **Seropédica:** sites citam "1997" (instalação); a lei é 2.446 de 12/10/1995 (DTB). Censo 1991 com Seropédica, 2000 sem.

# Eventos, regimes e bairros (22/10/2026)

Arquivos: `eventos.json` (35 eventos, 18 antes de 1850, mais 8 de reserva), `regimes.json` (4 faixas, só bandeiras locais de `motor/assets/bandeiras/`), `bairros_epocas.json` (7 bairros com data, 1 distrito só com lei, 18 bairros sem dado, 3 aterros). Fontes lidas como página HTML/PDF; nenhuma API. Limites (título ≤ 30, legenda ≤ 95, detalhe ≤ 220, ids únicos, coordenadas dentro do bbox) validados por script.

## Divergências e decisões

| Tema | Fonte A | Fonte B | Decisão |
|---|---|---|---|
| Data da vila | 05/07/1818 (ptwiki, DTB histórico, monografia IBGE 509, Praça Cinco de Julho) | 05/06/1818 (DTB, formação administrativa) | 05/07/1818. Também: suprimida 13/11/1818, restaurada 13/11/1819, instalada 11/02/1820 |
| Igreja de S. Francisco Xavier | concluída em 1729 (monografia, parte histórica) | "fundada a 3/12/1759" (monografia, parte turística) | 1729 |
| Aldeia de Itinga | 1627 (Amantino/Unicamp, lista única) | "meados do séc. XVII" (Pizarro via IBGE); igreja "antes de 1688" | 1627, confiança baixa |
| Transferência da aldeia | "antes de 1718" (IBGE) | — | mostrar "antes de 1718" |
| Massacre dos Itingas / José Pires Tavares (1804–05) | ptwiki Itaguaí conta como fato (nota com link morto) | ANPUH 2024: é a lenda de Quiva e Laiá | NÃO usado como fato; usado o fim oficial da aldeia em 1834 (ANPUH, citando Ferreira/UFRRJ 2016) |
| Distrito de Seropédica | ptwiki Itaguaí: "fundado em 1844" (seda) | DTB: Bananal 1851 → Patioba 1924 → Seropédica 1926 | DTB. A fábrica de seda de 1844 ficou sem fonte própria |
| Estrada Rio–São Paulo | 05/05/1928 (ptwiki BR-465) | "aberta em 1938" (ptwiki Seropédica) | 1928 |
| Ingá Mercantil | fundada 1958 / instalada 1965 (monografia IBGE, dois trechos) | início em 1962 (tese PUC-Rio) | 1962. Dique rompe em fev/1996; falência 1998 |
| Nuclep | 12/04/1975 (infobox ptwiki) | 16/12/1975, Decreto 76.805 (texto ptwiki) | só o ano 1975 |
| Nome Porto de Itaguaí | Lei 11.200/2005 (PortosRio, ptwiki Sepetiba Tecon) | 2006 (ptwiki Porto) | 2005 |
| Rio–Santos | 1974 (infobox ptwiki BR-101) | "década de 1970" (ptwiki Itaguaí) | 1974 |
| Riachuelo | 1.740 t, "mais de 70 m" (ptwiki Complexo Naval) | 1.850 t, 71 m (ptwiki ProSub) | 1.740 t |
| Mangaratiba | decreto de 31/10 ou 11/11/1831 (DTB) | fundação 11/11/1831 (ptwiki) | 1831 |
| Corte em Santa Cruz | 1808 (chegada) | "a partir de 1809" (veraneio) — mesma página | 1808 no ano, texto sem cravar |
| População 1970 | 57.680 recenseados presentes (monografia) | 55.839 residentes (série IBGE, ver acima) | eventos não mostram o total de 1970; o de Seropédica usa os números por distrito da monografia (28.175 × 23.527 na sede, presentes) |

## Coordenadas

Só de páginas da Wikipédia (link Especial:Map) ou da página HTML do Wikidata (Baía de Sepetiba Q16496144, Ilha de Itacuruçá Q10301150). Sem coordenada publicada → centro do município (ptwiki Itaguaí, = `centro_antigo` do config), marcado "genérico": aldeia de Itinga, igreja matriz, estação, Quintino, emancipação de Paracambi (fora do bbox), Rio–Santos e Arco. A Ilha da Madeira não tem artigo: usada a coordenada do Complexo Naval (fica na ilha), marcada como aproximação. Eventos de 1556–1833 na Fazenda de Santa Cruz estão dentro do bbox, mas hoje são município do Rio — dizer isso na tela.

## Regimes

Colônia (portugal) → Reino Unido 16/12/1815 (reino) → Império 07/09/1822 (imperio; imperio2 de 1870) → República 15/11/1889 (republica; brasil de 1960). `espanha.svg` não se aplica: a região nunca foi ocupada pela Espanha, e a União Ibérica não trocou a bandeira local. Nome no HUD: S. FRANCISCO XAVIER DE ITAGUAÍ (1795–1892) → ITAGUAÍ (decreto 1-A, 03/06/1892). Bandeira municipal ("Bandeira de Itaguaí.jpg" na infobox) não conferida e não baixada.

## Bairros

Nomes = os 24 polígonos admin_level=10 do OSM (`brutos/bairros.geojson`). Só 6 polígonos têm data documentada (Centro, Coroa Grande, Piranema, Brisa Mar, Vila Geny, Nuclep) + Ilha da Madeira, que não é polígono no OSM. Brisa Mar e Vila Geny são **limite superior** (estações já listadas em 1960). Piranema 1938 é inferência (núcleo colonial de Santa Cruz). Os outros 18 ficam com a distância ao centro (motor). Coordenadas de bairro vêm do OSM local, não da Wikipédia (não há páginas).

## Pontos fracos

- Antes de 1700 tudo é "aproximado": Pizarro via IBGE, uma lista acadêmica (1627) e nada de coordenada da 1ª aldeia nem da ilha de Jaguaramenom.
- Colônia japonesa 1938: ptwiki + matéria do Diário do Rio (lida só via resultado de busca); o ponto das hortas é genérico (Santa Cruz).
- Datas de estação vêm de site secundário (Estações Ferroviárias do Brasil).
- IBGE Cidades deu 403 ao script; 116.841 (Censo 2022) conferido pela ptwiki e pelo resultado de busca.
