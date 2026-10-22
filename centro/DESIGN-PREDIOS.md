# DESIGN-PREDIOS.md — marcos do centro histórico de Itaguaí (versão `centro/`)

Plano de design + como integrar. Motor desta versão: `centro/motor/` (cópia; `motor/` original não é tocado).
Gerador: `centro/motor/marcos.js`. Vitrine: `centro/motor/vitrine.html` + `vitrine.mjs` → `centro/vitrine/*.jpg`.
Antes de mexer no visual: `~/projetos/inema-design/DESIGN.md`, `video/style.md`, `video/camera.md`, `memoria/correcoes.md`.

## 1. Linguagem visual — "maquete de arquiteto"
- Low-poly com cor sólida por face (sem textura), luz direcional + sombra projetada no chão. Lê bem em 1080p entre zoom 18 e 20 e não briga com o terreno (satélite esverdeado) nem com o HUD preto/amarelo.
- Os marcos são **coloridos e detalhados** (parede caiada, molduras azul/vinho/verde, telha de barro); os prédios comuns do OSM viram **caixas neutras claras** (bege-cinza, altura exagerada como hoje) — o olho vai para o marco sem precisar de seta.
- **Amarelo `#FACC15` só no destaque** (molduras + halo no chão), nunca como cor de prédio: a regra "âmbar = destaque" do kit continua valendo. Nenhuma informação só por cor: todo destaque vem com `chamada`/cartão (texto).
- Proporções reais em metros (igreja 14×32 m, sobrado 12×13 m, casa 8×10 m…). Alturas multiplicam `ez` (padrão `C.exb`, o mesmo exagero dos prédios OSM, para o marco não ficar atarracado ao lado deles). Capturas: `vitrine_*.jpg` (ez 1) e `ez15_*.jpg` (ez 1,5). Recomendo `marcos_ez: 1.25` no roteiro do centro, ou `exb: 1.25` para tudo.

## 2. Paleta (hex → `MARCOS.PALETA`)
| Uso | Cor |
|---|---|
| parede caiada / soco de pedra / adro, laje | `#EAE3D4` / `#8F8477` / `#A8A196` |
| molduras e cunhais coloniais | azul `#2E5E8E` · vinho `#7B3038` · verde `#2F6B4F` |
| telha de barro (faixas alternadas) / cumeeira / testeira / sofito | `#A9533A` + `#964832` / `#7E3C28` / `#7A5A48` / `#5E4A3E` |
| coruchéu, ferro | ardósia `#4A5560` · ferro `#3A3F45` · zinco `#9AA2A8` |
| vão escuro / veneziana / porta de madeira | `#26303A` / `#2F4A3B` / `#4A3324` |
| prefeitura eclética (parede rosa-antigo + molduras brancas) | `#D8B4A2` + `#F2EDE3` |
| estação (parede creme + molduras tijolo) | `#E6CDB3` + `#8C3B2E` |
| árvores (copa 3 tons / tronco) · palmeira | `#4F8F3F #3E7A33 #5FA04A` / `#6F4E34` · `#4C8A3A #3C7530` |
| futuro: vidro / aço / concreto / telhado verde / painel solar | `#7FB6CF #5F97B3` / `#D3D8DC` / `#C9CCCB` / `#5C9A48` / `#1E2F5E` |
| futuro: bonde + faixa / grama / água / caminho / ciclovia | `#F2F4F5` + `#1F7A8C` / `#5F9C4C` / `#4B8FC2` / `#D9CDB3` / `#9B4A3B` |
| molduras ocre (Coletânea) / parede amarelo-ocre / cúpula prateada / verde-escuro / vitral / bronze / claro moderno | `#B3782A` / `#CFA34B` / `#CDD1D6` `#A9AFB6` / `#4F6358` / `#3C7FA6` / `#6B5A3A` / `#E8E4DA` |
| destaque | `#FACC15` (molduras, cruz, pináculos, halo). Na estação-castelo e na catedral (paredes ocre) o amarelo das molduras contrasta menos: o halo + chamada fazem o trabalho |
| chão da vitrine / rua / calçada / praça | `#8E9A86` / `#767269` / `#B0AA9E` / `#A8A08E` |

## 3. Luz, material, sombra
- `LightingEffect` igual ao `mapa.html` (ambiente 1,0 + direcional 1,6), **mas direção `[-2, 3, -3.2]`** (sol do sudeste, meio baixo). Motivo: a câmera do vídeo olha para o norte (bearing −15…−35) e vê as fachadas **sul**; com a luz do mapa (`[-2,-3,-4]`) elas ficam na sombra (comparar `vitrine/luzne_lateral.jpg` com `vitrine_lateral.jpg`). **Decisão do Nei, não testada no terreno real:** a `textura.jpg` (satélite) já traz o sombreado do sol verdadeiro (norte, lat −23); luz do SE na malha pode brigar com ele em quadro de serra. Conferir um quadro do terreno antes de adotar; alternativa sem risco: manter a luz do mapa e filmar os marcos pelo norte (bearing ±150°, como em `vitrine_nasce.jpg`), que também fica aceitável.
- Material dos marcos `{ambient .5, diffuse .45, shininess 20}` e parede `#EAE3D4` (não branco): face ao sol ≈ 0,8, face na sombra ≈ 0,45 — molduras legíveis dos dois lados, sem estourar.
- Sombra no chão: polígono = casco convexo da base ∪ base deslocada por `h·(−lx/lz, −ly/lz)`, preta alfa 92, drapeada no terreno (`_TerrainExtension`). Dá o "assentamento" da maquete sem o shadow map do deck (que quebra o TextLayer — lição do CLAUDE.md).
- Profundidade tonal sem textura: soco escuro (0,5–0,8 m), faixa de sombra do beiral no alto da parede, cornija, testeira e sofito escuros, telha em faixas de 0,85 m com o terço de baixo mais escuro, cumeeira e espigões em barra escura.

## 4. Arquétipos (frente para −y antes do `rumo`; medidas em metros, antes do `ez`)
| tipo | proporções | o que o define |
|---|---|---|
| `igreja` | nave 12×28 (`larg`, `comp`), parede 10, 2 águas 32° com cumeeira perpendicular à fachada; torre 4,6² saliente 0,4 m, corpo 15,5, sineira 4 arcos; **`coroa: 'cupula'`** (padrão, Matriz): tambor + meia-laranja prateada (`#CDD1D6`/`#A9AFB6`) + 4 pináculos nos cantos + bola + cruz, ou `'piramide'` (coruchéu de ardósia 5 m); sacristia 8,4×7 atrás; adro de pedra 18×9 | frontão triangular com cimalha nas rampas, pináculos nos ombros, óculo e cruz; portada em arco 2,4×4,6; 2 janelas laterais + 3 do coro em arco; 5 janelas altas por lado. **`torre_lado: 'direita'`** (padrão = à direita de quem olha a fachada, como nas fotos da Matriz) ou `'esquerda'`; `torres: 2` para duas. `cor: 'ocre'` reproduz as molduras ocre da Coletânea |
| `claustro` (colégio jesuíta) | quadra `lado` 30 (×`comp`), alas `ala_larg` 8, `andares` 2 × 3,6; telhado cerâmico em **anel** (cumeeira no meio da ala), beiral externo e para o pátio; pátio de grama | janelas regulares nas 4 faces externas (2 pisos), porta em arco na frente; no pátio, **galeria de arcos** no térreo e janelas em cima; cunhais nos cantos, soco, cimalhas. Encosta na lateral da igreja pelo lon/lat do roteiro |
| `estacao_castelo` (estação de 1910 → Casa de Cultura) | torre `torre_m` 6², `torre_alt` 11,5 até as ameias, 2 pavimentos; alas `ala` 9 m × `comp` 7, `ala_alt` 4,6; `plataforma: true` (padrão) = plataforma + cobertura de zinco + linha atrás | **ameias** em toda a volta (torre e alas) sobre laje escura; cornija da torre com fileira de furinhos redondos; 3 janelas **ogivais** na frente do 2º pavimento (1 por face lateral/fundo); óculos no térreo; porta em arco; nas alas, janelinhas em fita + óculo + porta. Parede amarelo-ocre `#CFA34B`, cunhais/frisos/molduras brancas |
| `chafariz` (1847) | 3,2×3 m, paredes 3,2, telhado baixo de 4 águas (16°) atrás de **frontão triangular com cornija** na fachada (topo 4,8 m); tanque de pedra 3,4×1,4×0,75 na frente com água | arco pleno 1,7×2,4 fechado em pedra com 2 bicas de bronze e bandeira de ferro; vãos em arco abertos nas laterais; branco com pilastras, frontão e moldura do arco verde-escuro `#4F6358` |
| `moderno` (Patronato São José, 1968) | `larg` 22 × `comp` 12, `andares` 3 × 3,3 sobre muro de pedra 1,2; lajes salientes; parapeito; volume no terraço 7×5×2,8 com **estátua** (`estatua: true`, `estatua_alt` 3,6) | faixas horizontais de janelas (vidro escuro + montantes brancos) em todos os pisos; **cobogós** (xadrez) na frente do 1º andar; pilares aparentes a cada ~3,6 m; cor clara `#E8E4DA`, concreto `#C9CCCB` |
| `catedral_moderna` | `larg` 24 × `comp` 36: corpo central `corpo` 10 m × 12 alto amarelo-ocre; 2 volumes curvos (quartos de cilindro r 7, 9 m) brancos abraçando o corpo; nave 20 m, 9 m, cobertura baixa de zinco; escada de 5 degraus | rosácea 4 m com vitral, porta em arco 3×4,5 com grade, janelas estreitas (2 por lado, 2 alturas) com moldura ocre; **campanário em arco aberto** no eixo (pilares 6 m + arco r 2,2) com sino de bronze e cruz branca 4,5 m; vitrais altos nas laterais da nave |
| `sobrado` | 12×13, 2 pisos de 3,6 (`andares`), 4 águas 27°, beiral 0,65 | portas 1,2×2,7 no térreo (passo 2,5), janelas 1,15×2,6 com **sacada** de ferro em cima; cimalha entre pisos; cunhais 0,45; soco 0,6 |
| `casa` (térrea porta-e-janela) | 8×10, pé-direito 3,4, 2 águas 30° com **cumeeira paralela à rua**, beiral 0,55 | porta 1,1×2,3 à esquerda + janelas 1,0×1,45 (peitoril 1,0) com veneziana; cunhais 0,4 |
| `casarao` | sobrado com `andares: 1`, sem sacada | casa grande de 4 águas (ex.: "Casa do Pai", a confirmar) |
| `estacao` | prédio 24×9, pé 4,6, 4 águas 25°, beiral 0,9; plataforma 0,9 m de altura, 4,2 m, +18 m para cada lado (`plataforma`); cobertura de zinco em uma água sobre colunas de ferro a cada 5 m; linha com lastro, dormentes a 1,4 m e trilhos (bitola 1,6 m) | portas e janelas em arco alternadas nas duas faces longas; molduras tijolo sobre creme |
| `prefeitura` (câmara, eclética ~1900) | 18×14, pisos 4,3 + 4,0, **platibanda 1,3 m** com cornijas e pináculos nos cantos, frontispício central com tímpano; escadaria de 4 degraus | pilastras brancas entre janelas em arco 1,3×2,5; porta dupla 2,4×3,6 em arco; sacadas nas 3 janelas centrais do piso alto; cobertura plana escura atrás da platibanda |
| `coreto` | base octogonal r 3,6, 1 m de pedra; 8 colunas de ferro 3,3 m; guarda-corpo; cobertura octogonal de zinco 2,2 m + remate | para a praça |
| `arvore` | `arvore: 'redonda'` (tronco hexagonal 3 m + copa em 5 anéis, 7,5 m) ou `'palmeira'` (tronco 11 m + 9 folhas) | instanciadas: escala, giro e tinta por indivíduo |
| futuro `torre_vidro` | 18×18, planta chanfrada, `andares` 10 × 3,4 m em faixas vidro/peitoril, pódio 1,4 piso com telhado verde, coroamento + painéis solares | "moderada": 8–12 pisos, nunca arranha-céu |
| futuro `telhado_verde` | 22×14, 5 pisos × 3,2, platibanda em anel, telhado verde, floreiras, varandas, painéis solares | |
| futuro `vlt` | leito 3,2 m + 2 trilhos ao longo de `caminho`; `bonde` 24 m (branco, faixa teal, janelas contínuas) andando a `vel` m/s | |
| futuro `parque` | polígono de grama + `agua` (PathLayer 7 m) + `caminho` (2,5 m) + `arvores` semeadas | parque linear no rio |
| futuro `ciclovia` | PathLayer 2,5 m terracota | |

Vãos (portas/janelas): **moldura em anel saliente 0,14 m** (largura 0,18) + folha escura recuada (0,05 m) + rebaixo interno escurecido; formas `reta`, `arco` (meia-volta) e `oculo`. Nada coplanar com a parede (sem z-fighting entre quadros).

## 5. Como o marco "nasce" (progresso k = 0…1, `dura` s, padrão 3 s)
`fases(k)`: laje de pedra (0–12 %) → paredes sobem com soco, cunhais e os vãos que já cabem (10–68 %) → telhado desce de 5–7 m acima e assenta (66–90 %); na igreja a torre sobe junto → coroa: coruchéu, frontão/cruz, pináculos, cobertura da plataforma, coreto (86–100 %). Sombra no chão cresce junto. Ver `vitrine/obra_k0.72_igreja.jpg`, `obra_k0.9_igreja.jpg` e a fileira "nasce 25/50/75 %" em `vitrine_lateral.jpg`.
- `k` é em **segundos a partir de `t0`** (não em anos): `t0 = tDoAno(C, m.ano)` inverte `C.anos`, então a obra começa quando o contador cruza o ano do marco (lição "efeito só depois do avanço e a partir do ano real"). `m.t0` explícito ou `m.sempre: true` também valem.
- **`pronto: <ano>`**: a obra dura do t do `ano` ao t do `pronto` (Matriz: `ano: 1718, pronto: 1729` → 73,6 s a 91,7 s na linha de Itaguaí); sem `pronto`, `dura` s (3).
- **`ate: <ano>`** (sinônimo `some_ano`): a partir do t desse ano o marco **desmonta** em `desmonta` s (padrão 2) — as fases rodam ao contrário (coroa some, telhado sobe, paredes descem, laje) e a sombra encolhe junto; testado com o colégio jesuíta (`ano: 1729, ate: 1961`: inteiro até 253,3 s, some em 255,5 s).
- A malha é regenerada só enquanto k muda (quantizado em 1/60) e cacheada no fim: 61 estados da igreja = 35 ms; prédio pronto = 0 custo por quadro.

## 6. Destaque (`destaque: [[t0,t1]]`)
Molduras, cunhais, cruz e pináculos ficam `#FACC15`, halo no chão (disco alfa 28 + anel 1,4 m + pulso) com raio = meia diagonal + 5 m. A chamada/etiqueta e o cartão dão o texto. Prédios comuns não mudam.

## 7. Comuns × marcos (no `mapa.html` da cópia)
- `carrega()`: trocar a cor laranja dos prédios OSM por neutro claro quando `C.predios_neutros` — ex.: `c = [lerp(214,228,h), lerp(206,220,h), lerp(190,204,h)]` (bege-cinza) e `MAT_PRED` com `diffuse .4`. Os marcos ficam coloridos por contraste.
- `MARCOS.ocultaOSM(POS, INI, ANO, C.marcos, 3)` logo depois de ler `pred_ano.f32`: zera (ANO=9999) os prédios OSM dentro do lote de cada marco (+3 m) — senão a caixa laranja nasce dentro da igreja.

## 8. Cidade futura (`C.futuro`)
- O que aparece: árvores e palmeiras nas praças e calçadas, telhados verdes com painéis solares, 2–3 torres de vidro moderadas com pódio verde, linha de VLT com bonde andando pela rua principal, parque linear no rio (grama, água, caminho, árvores), ciclovia. Ver `vitrine/vitrine_futuro.jpg`.
- Transição presente → futuro (sugestão de roteiro, 25–35 s no fim, antes do `fim`): (1) cartão "E SE…" + etiqueta fixa no HUD **"VISÃO DE FUTURO · imaginação, não é projeto"** enquanto durar (regra: informação nunca só por cor); (2) `tons` leve mais frio/azulado; (3) prédios comuns ficam ainda mais claros (ou `filterRange` congela), (4) elementos sobem um a um (`atraso` 0,12 s, `nasce` 2,5 s): parque e ciclovia primeiro, depois árvores, VLT, telhados verdes, torres por último; (5) bonde começa a andar a 50 % da subida; (6) sem números na tela (não há fonte para o futuro); (7) volta ao presente ou vai direto para o `fim`.
- Marcar na tela: novo elemento `#visao` no HTML da cópia (canto superior direito, caixa preta com borda amarela, igual ao `#tag` da vitrine), ligado por `C.futuro.t0..t1` no `html(t)`.

## 9. Integração no `centro/motor/mapa.html` (Nei faz)
1. `<script src="marcos.js"></script>` depois de `deck.min.js` (o `render.mjs` já serve a pasta do motor). Trocar a `direction` da luz para `[-2, 3, -3.2]`.
2. Em `carrega()`: depois de ler `ANO`, `if (C.marcos) MARCOS.ocultaOSM(POS, INI, ANO, C.marcos)`; se o roteiro não trouxer `z` nos marcos, `await MARCOS.carregaElev(D, 'assets/elev.png', D.T.bbox)` (decodificador igual ao `DEC_TERRA`, sem o EXZ) — `camadas` passa a amostrar o chão sozinha. Conferir `MARCOS.elevEm(D, lon, lat)` num ponto conhecido (mar da baía ≈ 0 m) antes de confiar: o canvas pode aplicar gerência de cor ao PNG e 1 unidade errada no R = 256 m. Mais seguro: calcular o `z` no script do roteiro (Python, lendo `elev.png`) e gravar no `cena.js`.
3. Em `camadas(t)`: logo depois do `predios` e antes das `areas`: `L.push(...MARCOS.camadas(t, ano, C, D, { terreno: EXT_TERRA }))`. Chamar uma vez por quadro; `C.exz` e `C.exb` são lidos de `C` (z do chão × exz; alturas × `marcos_ez ?? exb`).
4. Roteiro (`roteiro_itaguai_centro.py` → `cena.js`), por marco: `{id, tipo, lon, lat, z?, rumo, larg, comp, andares?, torres?, cor: 'azul'|'vinho'|'verde'|'#hex', parede?, telha?, ano, dura: 3, destaque: [[t0,t1]]}`. `rumo` = azimute para onde a fachada aponta (graus, horário do norte); `larg` = largura da fachada; `comp` = profundidade. Tirar lon/lat, larg, comp e rumo do polígono do OSM do próprio prédio (`pred_pos`), não a olho.
   - Também: `pisos` (adro/praça: `{id, poligono, cor, ano}`), `ruas` (`{id, caminho, larg, cor, ano}`), `arvores_auto` (`{poligono, n, semente, dmin, tipo?, ano}`), `arvores` avulsas, `futuro` (seção 8).
5. Câmera para os marcos: zoom 18,5–20 (o `mapa.html` usa `controller: false`, nada trava o zoom; se travar, acrescentar `maxZoom: 24` no `viewState` do `window.render`, como na vitrine; a cena de Itaguaí hoje vai só a 15,7), pitch 55–60, bearing −15…−40 (câmera ao sul olhando para a fachada); chegada da câmera 45 % do bloco antes da obra terminar; `chamadas` com `z` = altura do prédio × ez. Zoom ≤ 1,25× em imagem com texto continua valendo para os cartões, não para o mapa.
6. Memória: `marcos.js` cria prop-objects uma vez (materiais, extensão passada por `opts`) e só troca `mesh` quando o estado muda; nada é recriado por quadro além das camadas. Render em trechos (`render_trechos.sh`) como sempre; conferir o log.

## 10. API de `marcos.js` (`window.MARCOS`)
- `camadas(t, ano, C, D, opts)` → `deck.Layer[]` (marcos, sombras, halos, árvores, futuro, pisos, ruas). `opts = {terreno: [ext], luz: [x,y,z], ez}`.
- `malha(m, k, dest, ez)` → `{positions, normals, colors, alt, sombra}` (triângulos soltos, cores 0..1); `malhaCache`, `malhaUnidade(tipo, extra)`.
- `tDoAno(C, ano)`, `semear(poligono, n, semente, dmin)`, `ocultaOSM(POS, INI, ANO, marcos, folga)`, `carregaElev(D, url, bbox)`, `elevEm(D, lon, lat)`, `sombraPoli`, `aoLongo(caminho)`, `fases(k)`, classe `Malha` (tri/quad/caixa/prisma/piramide/barra/gira/escalaZ), `ARQ` (gerador por tipo, extensível), `PALETA`, `MAT`, `LUZ_PADRAO`.
- Fatos do deck 9.0.38 verificados: `SimpleMeshLayer` usa `colors` da malha (float 0..1) × `getColor` (tinta por instância); malha em metros ao redor de `getPosition` (sem METER_OFFSETS); `getOrientation [0, yaw, 0]` gira anti-horário em torno de z; `getScale [1,1,k]` sobe um prédio sem regenerar malha.

## 11. Vitrine
`cd centro/motor && node vitrine.mjs [--vistas lateral,drone,igreja,nasce,praca,estacao,futuro,longe,matriz,castelo,chafariz,moderno,catedral,fila] [--luz se|ne] [--ez 1.5] [--k 0.72] [--rotulos 0] [--prefixo x]` → `centro/vitrine/<prefixo>_<vista>.jpg`. Melhores: `vitrine_igreja.jpg`, `vitrine_lateral.jpg`, `vitrine_futuro.jpg`, `vitrine_estacao.jpg`, `vitrine_praca.jpg`, `obra_k0.72_igreja.jpg`; tipos da pesquisa: `vitrine_novos_matriz.jpg` (Matriz + claustro), `vitrine_novos_castelo.jpg`, `vitrine_novos_chafariz.jpg`, `vitrine_novos_moderno.jpg`, `vitrine_novos_catedral.jpg`, `vitrine_novos_fila.jpg`.

## 12. A confirmar com pesquisa (antes do roteiro)
Número de torres da Matriz de São Francisco Xavier (padrão 1, à esquerda); "Casa do Pai" (o que é, onde); posição e orientação reais de câmara/prefeitura, estação (1910) e praças; quais sobrados/casarões entram. Todo número no cartão com fonte (`dados/pesquisa/RESUMO.md`).
