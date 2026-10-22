# Itaguaí — CENTRO histórico: pesquisa (22/10/2026)

Arquivos: `predios_historicos.json` (26 prédios/lugares), `eventos_centro.json` (30 marcos, 1688–2023), `imagens.json` (4 imagens livres, em `img/`), `futuro.json` (planos oficiais × imaginação). Só páginas HTML/PDF e downloads de arquivo; nenhuma API. Coordenadas do OSM local (`dl/sudeste.osm.pbf`, pyosmium) ou de página do Commons.

## 1. O centro do config está no lugar errado

`centro_antigo` do config municipal (-43.7753, -22.8522) é a coordenada da ptwiki para o município. Ela cai ~1,7 km ao **norte** do núcleo histórico. No OSM:

| Ponto | lon, lat |
|---|---|
| Praça Dom Luiz Guanella (adro da Matriz, no morro) | -43.7790, -22.8676 |
| Cemitério junto da Matriz (way 152857786) | -43.7798, -22.8678 |
| Prefeitura (nó) | -43.7773, -22.8641 |
| Nó "Centro" | -43.7775, -22.8666 |
| Praça Vicente Cicarino / Barão de Tefé | -43.7787, -22.8699 / -43.7779, -22.8701 |
| Catedral nova (Commons) | -43.7786, -22.8692 |
| Antiga estação = Casa de Cultura (start_date 1910-11-14) | -43.7775, -22.8743 |

Sugestão de centro para a câmera do vídeo do centro: **(-43.7782, -22.8685)**. Tudo cabe num raio de ~700 m.

## 2. Duas igrejas de São Francisco Xavier

- **Igreja Matriz jesuítica (1718–1729), a "Antiga Sé"** — Praça D. Luís Guanella 136, no alto do morro. Tombada pelo INEPAC (provisório em 25/05/2006, proc. E-18/001.478/2005), junto com os pórticos 1 e 2 do cemitério. Pedra e cal, frontão triangular com óculo, uma torre sineira com cúpula prateada e 4 pináculos, porta de madeira almofadada. O colégio jesuíta colado a ela (quadra com claustro) foi **demolido em 1961**. A coordenada é aproximada: o templo não está no OSM.
- **Catedral nova** — Rua Coronel Freitas 45, prédio moderno (volumes curvos brancos, faixa amarela, campanário em arco). A foto do Commons "St. Francis Xavier Cathedral" e a coordenada da categoria são **deste** prédio. O GCatholic mistura os dois ("built 1718–1729" no endereço novo). Não achei o ano da construção.

Não existe foto livre da Matriz colonial no Commons. A única imagem livre dela é o desenho de Maria Graham (1823). As fotos dos anos 40/50/70 estão no site da Prefeitura, sem licença, e serviram só para descrever a arquitetura.

## 3. "Casa do Pai"

**Não achei prédio histórico com esse nome.** O que existe é o **Instituto Casa do Pai** (Associação Casa do Pai – P.A.I.), uma ONG social fundada em 11/06/2007 na Rua Prefeito José Maria de Brito, 201 ou 251 (o site e o cadastro divergem), no Monte Serrat, ~600 m a sudeste da Matriz. Prédios antigos que podem ser o que o Nei quis dizer:
- **antiga casa paroquial**: em 1979 recebeu a Escolinha do Pe. Cezar. Sem foto nem endereço.
- **Casa de Quintino Bocaiúva**: sobrado de 2 andares, tombado pela Câmara, interditado em 2023.
- **casa natal do Barão de Teffé**
- **Casa Candeeiro**: "uma das mais antigas da cidade".

→ Perguntar ao Nei qual delas.

## 4. Estação = Casa de Cultura = Biblioteca = "castelo"

A estação do Ramal de Mangaratiba (14/11/1910) é um prédio eclético com ameias, uma torre de 2 andares e alas térreas, pintado de ocre. Ficou abandonada nos anos 1980, foi reformada em 2005 e reabriu como Casa de Cultura em 13/02/2006, já com a Biblioteca Municipal dentro. Por isso o Commons chama o prédio de "Castelo da Biblioteca Municipal Machado de Assis". É o prédio com a melhor coordenada (OSM, com data).

## Divergências e escolhas

| Tema | Fonte A | Fonte B | Escolha |
|---|---|---|---|
| Conclusão da Matriz | 3/12/1729: Coletânea, Prefeitura, INEPAC | "fundada a 3/12/1759": Monografia IBGE 509, parte turística | 1729. O dia e o mês batem, então 1759 parece erro de digitação |
| 1ª igreja (1688) | região de Coroa Grande (Prefeitura) | ao norte do rio Itaguaí (Redescobrindo os Vales); a pesquisa municipal tem Itinga em 1627 | 1688 sem lugar, confiança baixa |
| Expulsão dos jesuítas | 1759 (Prefeitura) | 1755 (Redescobrindo) | 1759 |
| Torre da Matriz | "na lateral esquerda" (Coletânea) | à direita de quem olha a fachada (todas as fotos) | Modelar pela foto: torre à direita de quem olha. O texto descreve de dentro |
| Janelas do coro | 2 janelas (Coletânea, texto) | 3 janelas em arco (foto da Prefeitura, anos 70) | Modelar 3, pela foto. Pode ter havido reforma |
| Casa de Quintino | "construída em 1873" (Jornal Atual 2023) | "onde nasceu" Quintino, em 1836 (legenda da Prefeitura); "onde supostamente residiu" (Coletânea) | 1873, confiança baixa, com a dúvida no detalhe |
| Fim dos trens | 1980 (Prefeitura, Coletânea) | "por volta de 1982", "meados dos anos 1980" (Estações Ferroviárias) | 1980 |
| Catedral de 1980 | a Matriz de 1729 (Vaticano, ptwiki, Prefeitura) | foto e endereço atuais = prédio novo | As duas coisas: sé em 1980, catedral nova depois (data não achada) |
| Ano das praças e do Fórum | só "década de 40/50" (Prefeitura) | — | Marcadores 1945/1955, avisados no texto como não exatos |

## Pontos fracos

1. **A coordenada da Matriz é aproximada** (±50 m). Ela foi deduzida da Praça Dom Luiz Guanella e do cemitério do OSM, porque o templo não está mapeado. Também não foram localizados: Casa de Quintino, Casa de Caridade/hospital, Fórum, Teatro, casa paroquial, Engenho do Facão. O Chafariz, o Candeeiro e o Paço da Câmara só têm a rua.
2. **Faltam medidas.** Nenhuma fonte dá largura, comprimento ou altura. Os valores em `estimativa_modelador` foram tirados das fotos e não têm fonte.
3. **Há pouca imagem livre**: 4 no total, e nenhuma da Matriz colonial além do desenho de 1823. A foto dos anos 70 tem licença duvidosa (PD-self de quem enviou, não do fotógrafo). As melhores fotos (Prefeitura, livro municipal) não têm licença.

Outros limites:
- Não achei o Plano Diretor nem um plano oficial para o centro. O `futuro.json` oficial é quase todo porto. O "centro do futuro" no vídeo terá de ser imaginação.
- A página do Diário do Transporte sobre o plano de Santa Cruz não abriu. Os dados vêm só do resultado de busca.
- A nota do Bendito Guia (Praça Vicente Cicarino, 216) também foi lida só pelo resultado de busca.
- O livro municipal (Coletânea, 2010) é um PDF escaneado sem texto. Li só as páginas 107–125 e o índice, como imagem.
- A Monografia IBGE 509 tem uma planta de c. 1971 com 30 prédios cívicos numerados. A lista está em `predios_historicos.json → referencia_1971`, mas a planta não foi georreferenciada.
