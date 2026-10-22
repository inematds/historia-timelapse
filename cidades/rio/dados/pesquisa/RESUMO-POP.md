# Rio de Janeiro — população, imagens e bairros: divergências (22/10/2026)

Arquivos: `populacao.json`, `imagens.json` (+ `assets/epoca/e00–e15.jpg` e `indice.json`), `bairros_epocas.json`.
Fontes lidas como páginas HTML/PDF normais, sem API. O RESUMO.md dos eventos é do outro agente.

## População

| Ano | Valor usado | Outra fonte | Decisão |
|---|---|---|---|
| 1585 / 1590 | 3.750 / ~5.100 (capitania) | Gândavo 1570: 140 fogos ≈ 700 | estimativas de cronistas (Villela/FGV), confiança baixa |
| 1687 | ~20.500 | Villela: "20–21 mil dentro dos limites da cidade" (termo colonial, maior que o município) | meio da faixa |
| 1799 | 43.376 (só freguesias urbanas, Florentino) | Villela: "cerca de 100 mil" contando as freguesias rurais do termo | 100 mil é de um território maior (o termo incluía Iguaçu, Jacutinga, Marapicu…, que viram vilas em 1833). 43.376 subestima o município; marcado como contagem parcial |
| 1808 | ~60.000 (Luccock, núcleo urbano) | — | confiança baixa |
| 1821 | 116.444 (censo; 86.323 urbanas + 30.121 rurais — Soares) | 112.695 (Florentino, via revista UEPG) | 116.444 porque traz a soma urbana + rural do município |
| 1838 | 137.078 (relatório do Ministro do Império) | — | parece baixo entre 1821 e 1849; mantido, confiança média |
| 1849 | 266.466 (Haddock Lobo; Unicamp e Soares concordam) | 268.386 (revista UEPG, citando Florentino) | 266.466: duas fontes independentes |
| 1890 | 522.651 (Synopse 1890) | — | o próprio governo considerou o censo do DF pouco confiável e fez um recenseamento próprio em 1906 (811.443) |
| 1950 | 2.377.451 (total, IBGE) | 2.303.063 (enwiki "Timeline", só a população urbana) | total |
| 1970 | 4.251.918 (IBGE) | 4.252.009 (enwiki, ONU Demographic Yearbook) | IBGE |
| 2022 | 6.211.223 (PDF do IBGE, Primeiros Resultados, 2ª apuração) | "6.211.423" num PDF municipal (Campos) | erro de digitação; vale o IBGE |

- **Território:** de 1834 (Município Neutro) a hoje é o mesmo território, apesar de mudar de nome: Distrito Federal (1891), Guanabara (1960), município (fusão, LC 20/1974, 1975). Fonte: DTB/IBGE. A série de 1872 a 2022 é comparável sem ajuste. Só antes de 1834 o "termo" da cidade era maior.
- **2010 → 2022: −1,8%.** É queda de verdade, porque o território não mudou.
- **Sem fonte (não entrou):** 1600, 1700 e 1760. Números como "12 mil em 1710" e "30 mil em 1760" circulam, mas não achei fonte conferível.

## Imagens

- **e05** (Debret, mercado de escravizados do Valongo): a página do Commons só diz "século 19", e a data que aparece é a do upload (2011). O ano 1825 é aproximado (Debret viveu no Rio de 1816 a 1831) e está marcado em `ano_obs`.
- **e06** (planta da cidade, 1835): a página dá o autor como "Unknown" e, no quadro de artista, põe por engano Charles W. Stetson (1858–1911). Quem imprimiu foi Thierry Frères, para o álbum "Voyage pittoresque dans le Brésil". É domínio público nos dois casos.
- **e14/e15** (Arquivo Nacional, 1950 e 1971): o domínio público vem da regra brasileira para obra de governo e fotografia documental. Crédito: "Domínio público / Acervo Arquivo Nacional".
- **Ponte Rio–Niterói pronta (1974):** só achei fotos recentes do Flickr com CC BY, que não é domínio público. Ficou só a foto da obra (1971).

## Bairros

- **Critério do ano:** o ano marca a ocupação URBANA (estação, bonde, túnel, loteamento). Não usei a sesmaria ou o engenho colonial de bairro rural. A data colonial vai no campo `ano_colonial`. Motivo: o motor reparte a curva de população pela ordem dos anos, e um bairro rural com ano de 1569 tomaria a população que é do Centro.
- **Estação × ptwiki** (usei a data do site Estações Ferroviárias, salvo indicação):
  - Mangueira: 1869 no site, 1889 na ptwiki.
  - Brás de Pina: o site dá 23/10/1886 (a data de abertura da linha da Leopoldina); a ptwiki diz parada de 1910.
  - Cordovil: site 1886, ptwiki 05/10/1910. **Aqui usei 1910 (ptwiki)**, que é a data comemorada pelo bairro.
  - Barros Filho: site 25/07/1904, ptwiki 1908.
  - Pilares (Cintra Vidal) e Turiaçu: site 1895, ptwiki 1898.
  - Padre Miguel (Moça Bonita): site 06/04/1940, ptwiki 1939.
  - Tomás Coelho: site 1895 (Linha Auxiliar), ptwiki 1876 (estação Engenho do Mato da Rio d'Ouro).
  - Coelho Neto: o site traz "15.01.8983", um erro de digitação; usei "anos 1950" da ptwiki.
- **Ponte da Ilha do Governador:** a ptwiki do Galeão diz inaugurada em janeiro de 1948; a da Praia da Bandeira diz 1950.
- **Zona Sul (Glória, Catete, Flamengo, Laranjeiras, Cosme Velho, Tijuca):** não há data própria. Usei 1808, a expansão urbana depois da chegada da Corte que Soares (ILAS) descreve, com confiança baixa. Para Botafogo usei 1816, porque o quadro de Taunay mostra casas na praia (limite superior).
- **Jardim América:** 1957 pela ptwiki do bairro (PAL proletário); a ptwiki de Vigário Geral fala em loteamento de 1950.
- **Datas oficiais de criação** (decretos 3.158/1981 e 5.280/1985, leis de 1993): não usei como ocupação.
- **26 bairros ficaram sem dado.** Cada um tem uma nota em `bairros_sem_dado`, por exemplo Gávea, Estácio, Rio Comprido, Santo Cristo, Taquara e Vargens. O motor preenche pela distância.
