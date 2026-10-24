# História em timelapse 3D: como o formato funciona e o plano INEMA

Análise de um timelapse 3D de cidade usado como referência de forma (ritmo, câmera, cartões, contador).

## 1. Não é um vídeo isolado: é uma fórmula

O canal repete o mesmo formato com 19 cidades:

| Cidade | Views | Duração |
|---|---|---|
| Praga | 1,2 mi | 12 min |
| Atenas | 1,1 mi | 6 min |
| Moscou | 792 mil | 6 min |
| Lisboa | 686 mil | 9 min |
| Roma | 614 mil | 4 min |
| Istambul | 601 mil | 6 min |
| Amsterdã | 576 mil | 12 min |
| Berlim | 461 mil | 14 min |
| Barcelona | 389 mil | — |
| Paris | 247 mil | 5 min |
| Viena | 99 mil | 9 min |

Os vídeos mais antigos têm de 4 a 6 min e os mais novos, de 9 a 14 min. O formato é um molde que pode ser repetido.

## 2. Anatomia da forma

**Tela fixa (HUD), sempre visível:**
- Canto superior esquerdo: bandeira e nome do Estado da época (Roman Empire → Duchy → Archduchy → Austrian Empire → Austria-Hungary → Republic → Nazi Germany → Republic).
- Canto superior direito: **"year 1844"** e **população** com contador animado (👤 499,191). Os números sobem continuamente.
- Bússola e rótulos no mapa ("DANUBE RIVER", "VIENNA", "HOFBURG PALACE"), com fonte serifada clássica.

**Mundo:** terreno 3D realista (relevo, florestas, rio com braços), visto do alto em ângulo oblíquo. A cidade é feita de blocos laranja extrudados (cada prédio é uma caixa) que **crescem ano a ano** a partir da mancha urbana daquele período. Muralha, catedral e palácios são modelos destacados.

**Tempo:** a velocidade muda ao longo do vídeo. Os séculos sem acontecimentos passam em segundos e o vídeo desacelera nos eventos. A câmera faz voos lentos e contínuos: aproxima nos eventos e afasta nas épocas de crescimento.

**Eventos (cartões):** cada cartão tem um **TÍTULO EM MAIÚSCULAS** e **uma linha de legenda** embaixo, sempre acompanhados de um **recurso visual** próprio:

| ~tempo | Ano | Cartão | Recurso visual |
|---|---|---|---|
| 0:00 | 92 | THE OUTPOST FALLS | soldadinhos atacando o forte |
| 0:10 | 105 | ROME IS ANGRY | legião marcha |
| 0:20 | 1228 | CAPITAL OF AUSTRIA | cidade murada surge |
| 0:40 | 1342 | (enchente) | água cobre a planície |
| 1:00 | 1525 | ST. STEPHEN'S CATHEDRAL | noite, close na catedral |
| 1:20 | 1529 | THE FIRST SIEGE | exército otomano em pontos, tela sépia |
| 1:50 | 1637 | IMPERIAL CAPITAL | close no Hofburg |
| 2:00 | 1683 | (segundo cerco) | incêndios e acampamentos |
| 2:50 | 1760 | SCHÖNBRUNN | palácio isolado na mata |
| 3:10 | 1809 | NAPOLEON | noite, artilharia |
| 3:20 | 1809 | (batalha) | fumaça |
| 4:00 | 1830 | (inundação de gelo) | neve e gelo |
| 4:20 | 1859 | THE WALLS COME DOWN | muralha some e aparece um anel vazio |
| 4:40 | 1867 | THE RINGSTRASSE | boulevard preenchido |
| 5:00 | 1875 | THE DANUBE TAMED | rio retificado |
| 5:20 | 1881 | THE RINGTHEATER FIRE | close, fumaça, bombeiros |
| 5:50 | 1897+ | GIANT FERRIS WHEEL | rótulo |
| 6:20 | 1918/26 | (fim do império) | troca de bandeira |
| 6:40 | 1938/41 | (anexação nazista) | troca de bandeira |
| 7:00 | 1945 | ST. STEPHEN'S BURNS | Exército Vermelho, fogo |
| 7:20 | 1964 | THE DANUBE TOWER | rótulo e altura |
| 7:40 | 1976 | THE BRIDGE FALLS | close na Reichsbrücke |
| 8:00–9:00 | 1978–2024 | — | voo longo de afastamento e fade |

**Som:** só música. Não há narração; a transcrição completa voltou vazia.

## 3. Por que funciona como história

- **O contador é a tensão.** A população subindo na tela segura o olhar sem precisar de nenhuma fala. É a nossa regra de "número na tela".
- **A bandeira marca a troca de ato.** Cada mudança de Estado abre um capítulo.
- **O cartão é a batida da história**, e cada um tem uma emoção: queda, fúria, glória, medo, tragédia, reconstrução.
- **O close com recurso visual** (noite, fogo, fumaça, gelo) é a pontuação emocional e quebra a monotonia do crescimento.
- **O final é um afastamento longo até o presente**, com o espectador vendo "onde tudo deu".
- Isso é exatamente a regra **"emoção primeiro, verdade confirma"**: o drama dos eventos puxa o espectador, e o ano e a população confirmam.

## 4. Nossa versão: com narração (pedido do Nei, 21/10)

O original é mudo. **A versão INEMA terá narração**, e isso muda o desenho:
- **O roteiro vira a espinha do vídeo.** Cada cartão vira um trecho narrado de 8 a 15 s. Entre os cartões, a música respira e o tempo acelera sem fala.
- **A duração é medida pela fala**, e não o contrário: primeiro o áudio narrado, depois a curva de tempo e de câmera ajustada a ele (mesma lógica do explicavideos).
- **Voz:** voz do Nei local (inemavox chatterbox `nei`, como no Alerta Sul; sem custo).
- **Avatar (opcional):** HeyGen pelo estúdio, nunca em tela cheia. Pode abrir em meia tela e depois ficar em PiP, mas o mapa é a estrela. Precisa de OK por produção.
- **O cartão continua na tela** (título e uma linha), porque reforça a fala e funciona sem som.
- **EN/ES** depois, pelo `inema-traduz` e com as vozes dos idiomas, como nos explicavideos.

## 5. Como fazer: o motor

Peças: terreno, mancha urbana por época extrudada em blocos, caminho de câmera, HUD e cartões, efeitos (noite, fogo, fumaça, água).

| Opção | O que já temos | Prós | Contras |
|---|---|---|---|
| **A. deck.gl** (TerrainLayer + extrusões) | Motor do Alerta Sul (`tempo-sul-2026-10-09/motor`, Vulkan, ~0,1 s por quadro) | Rápido, geo-referenciado de verdade, OSM direto | Visual mais "mapa" que "maquete" |
| B. three.js | reel3d (Remotion + three) | Visual de maquete e luz bonita | Montar o terreno e a geo à mão; o path tracing levou horas |
| C. Blender | reel3d-blender (medido em 24/10) | O visual mais próximo da referência | Nesta máquina só roda no processador: ~40–80 s por quadro, 4 a 6 dias por vídeo |
| D. Mitsuba 3 (path tracing na GPU) | `scripts/bench_mitsuba.py` (medido em 24/10) | Luz e sombra fotorrealistas na GPU NVIDIA; tudo por script Python | ~0,2–0,4 s por quadro na cena simples: 1–5 h por vídeo, contra 5–18 min do deck.gl |

**Recomendação:** **A (deck.gl)** no piloto. Ele cobre ~80% do visual em minutos de render, e o HUD e os cartões vão em camada HTML por cima (HyperFrames ou o próprio `render.mjs`). Se o visual não convencer, passamos a B ou C usando os mesmos dados.

**Atualização 24/10/2026:** o motor A ficou: 0,07–0,11 s por quadro, 5 a 18 min por vídeo, medido nos logs de render. O Blender (C) não usa a GPU desta máquina (ARM64). O **Mitsuba 3 (D)** usa, e é a opção para o visual de "maquete" com luz real, num render híbrido: o Mitsuba desenha relevo e prédios, o motor A desenha HUD, cartões e efeitos por cima. A medida por cidade (prédios, relevo e tempo de cada motor) está em [RENDER-GPU-ALTERNATIVAS.md](RENDER-GPU-ALTERNATIVAS.md).

## 6. O gargalo é o dado, não o render

O que decide se dá para fazer:
1. **Mancha urbana por época:** OSM (prédios de hoje, com `start_date` quando houver), mapas históricos georreferenciados, ou polígonos de época desenhados à mão como reserva (o referência claramente aproxima).
2. **População por ano:** censos (IBGE para cidade brasileira) e estimativas históricas, interpolados.
3. **Eventos com fonte:** 6 a 15 eventos, cada um com ano, local no mapa, título e uma linha.

**Esse passo vem antes de tocar no motor.** Se não houver dado para a cidade, ela não serve para o piloto.

## 7. Piloto: etapas, entregáveis e verificação

Escopo do piloto: uma cidade, **60–90 s**, **5–6 eventos**, 16:9 (o 9:16 vem depois).

| # | Etapa | Entregável | Como verificar |
|---|---|---|---|
| 1 | Escolher a cidade e levantar os dados | `dados/` com manchas por época, população e eventos com fonte | Cada evento tem fonte e cada época tem polígono |
| 2 | Roteiro narrado | `roteiro.md` com gancho, 5–6 batidas e fecho | Leitura em voz alta ≤ 90 s |
| 3 | Narração | `narracao.wav` (voz nei) e tempos por batida | Duração e transcrição conferidas |
| 4 | Quadro único | 1 PNG com terreno, cidade, HUD e cartão | Olho e `DESIGN.md` (cores, Sora/serifa, contraste) |
| 5 | Curva de tempo e câmera | Rascunho em baixa resolução sem efeitos | Ano e população batem com os dados; câmera dentro do `camera.md` |
| 6 | Recursos dos eventos | Noite, fogo, água etc. por evento | Cada cartão tem o seu recurso visual |
| 7 | Música e mixagem | Trilha do inemavox, voz na frente, sem whoosh | Escuta |
| 8 | Render final e QA | `final.mp4` | Revisor independente (Agent novo) e nota no `revisor-nota.py` |
| 9 | Registrar o método | Guardar como **skill** ("historia-timelapse") depois que o piloto for aprovado | Segunda cidade feita só pela skill |

Antes da etapa 4, ler `~/projetos/inema-design/DESIGN.md`, `video/style.md`, `video/camera.md` e `memoria/correcoes.md`.

## 8. Decisões abertas (do Nei)

- **Cidade do piloto:** sugestão **Porto Alegre** (é território seu e tem a enchente de 1941 e a de 2024 como recurso visual forte). Alternativas: São Paulo, Rio, Gramado/Canela, ou uma cidade europeia já coberta pelo referência, para comparar lado a lado.
- **Avatar:** só narração ou narração com avatar HeyGen (PiP)?
- **Canal de destino** e se o piloto já sai em EN/ES.
