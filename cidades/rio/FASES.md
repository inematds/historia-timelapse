# Rio de Janeiro: as 3 versões

O vídeo-base (fase 1) não muda. As fases 2 e 3 são camadas por cima de `final/video.mp4`, nos mesmos tempos (ver `cidades/floripa/FASES.md`).

| Fase | O que é | Estado |
|---|---|---|
| 1 | Sem narração, só música (`final/rio-v2.mp4`, 418,3 s, 40 cartões; v2 = correções do revisor independente sobre a v1) | 540p enviado ao bot v3 em 22/10/2026 (v1 msg 2289, v2 msg 2293); na fila do lives26 (`~/projetos/wifi/fila-cidades`, 10 h e 18 h) desde 22/10/2026 com OK do Nei |
| 2 | Fase 1 + narração na voz do Nei (`narracao.json`, 42 falas; `final/rio-narrado.mp4`) | 540p no bot v3 (msg 2317); publicado no lives26 em 22/10/2026: https://www.youtube.com/watch?v=Useg7_N_38E |
| 3 | Fase 2 + avatar do Nei no **canto inferior direito, acima do INEMA.CLUB**, entrando **depois da capa e do globo** (pedido do Nei, 22/10/2026). Estúdio HeyGen `historia-rio-narrado-v1` (id a48eb80e4bb744bb929b2064207e82e7) | em produção |

Motor: o original, sem mudança (1,82 milhão de prédios OSM + Microsoft carregam em ~8 s no GB10). Só arquivos da cidade: `config.json`, `roteiro_rio.py`, `imagens_uso.json`, `assets/bandeiras/franca.svg` (França Antártica, desenho simples das armas de França).

## Fase 2: notas
- O chatterbox repetiu o fim da fala do Maracanã ("…cala o estádio. O estádio."). O áudio foi cortado à mão em 4,45 s (`narracao/build/maracana-1950.orig.wav` é o original).

## Fase 3: como montar
- `CIDADE=rio .venv/bin/python -I cidades/rio/scripts/montar_avatar.py`. É uma CÓPIA do `scripts/montar_avatar.py`; o original não foi mexido.
- Diferenças da cópia:
  - Avatar com 220 px em x 1640–1860 e y 620–840, alinhado à direita com o INEMA.CLUB.
  - Ele fica logo acima do texto de baixo, que nos quadros do Rio sobe até y≈851. Colado no INEMA.CLUB, cobriria o fim da linha do título, que vai até x≈1720.
  - Capa, globo e fecho ficam só com a voz do avatar, sem rosto. O rosto entra no 1º evento (1500) e não tapa a galeria do fecho.
