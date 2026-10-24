# Render com luz real (Mitsuba 3 na GPU)

Ferramenta opcional do motor: o mesmo vídeo do `render_trechos.sh`, com o relevo e os prédios iluminados por *path tracing*. A luz segue os raios de verdade, então aparecem sombras entre os prédios, luz rebatida e volume de maquete. HUD, cartões, globo e efeitos continuam iguais.

Primeiro uso: Porto Alegre, 24/10/2026 (`cidades/poa/final/poa-mitsuba.mp4`). A comparação de ferramentas e os tempos de cada cidade estão em [RENDER-GPU-ALTERNATIVAS.md](RENDER-GPU-ALTERNATIVAS.md).

## O que é o Mitsuba

Programa de render de código aberto, feito por pesquisadores da EPFL (Suíça). Não tem tela: a cena é montada por script Python. Roda na GPU NVIDIA pelo OptiX e tem removedor de ruído. Instala com `pip`.

## Como funciona (render híbrido)

```
motor/mapa.html?camada  ──►  camada transparente (HUD, cartões, globo, cerco, cheias, muro, aterro)
                             + câmera e ano de cada quadro (info.jsonl)
scripts/mitsuba_render.py ──►  relevo + prédios com a MESMA câmera, sol e céu
montagem por quadro       ──►  céu do motor → Mitsuba → tom de época → camada  →  MP4
```

**O modo `?camada` do `mapa.html`:**
- O relevo é desenhado com textura transparente e os prédios com alfa 0. Os dois ficam só na profundidade, para tapar o que estiver atrás deles.
- Os efeitos colados no relevo (aterro, tropas, pulsos) continuam aparecendo.
- Sem o parâmetro, o motor é o de sempre: Floripa saiu idêntica, com diferença 0 em 3 quadros.

**O que o Mitsuba desenha:**
- **Relevo:** `elev.png` decodificado como no motor, multiplicado por `exz`, com a `textura.jpg` do satélite.
- **Prédios:** os contornos reais (`pred_pos`/`pred_ini`), com telhado triangulado (earcut). Cada prédio **sobe** ao longo de `nascer` anos, em vez de aparecer de uma vez, e a altura respeita o `teto` da época.
- **Fundo:** o plano além do recorte (`corLonge`).
- **Luz:** o sol vem da mesma direção do motor (nordeste, alto), com luz do céu.

**Câmera:** sai do próprio deck.gl a cada quadro (`unprojectPosition(cameraPosition)`, `fovy` e dois pontos do chão). Usa Mercator em metros, o mesmo modelo do deck. Numa mistura 50/50 com o quadro do motor não aparece contorno duplo.

## Uso

```bash
# uma vez: Mitsuba e earcut no .venv do projeto
.venv/bin/pip install mitsuba==3.9.1 drjit==1.5.0 mapbox-earcut

# vídeo inteiro (camada em trechos de 60 s + Mitsuba), 64 amostras por pixel
bash motor/render_luz.sh cidades/<id>/cena cidades/<id>/final/<id>-mitsuba-video.mp4 64

# juntar o áudio já em −14 LUFS
ffmpeg -i cidades/<id>/final/<id>-mitsuba-video.mp4 -i cidades/<id>/final/audio.wav -map 0:v -map 1:a -c:v copy \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest cidades/<id>/final/<id>-mitsuba.mp4
```

**Quadros-chave antes do vídeo inteiro:**

```bash
cd motor && node render.mjs ../cidades/<id>/cena --camada /tmp/kf --quadros 15,40,58 && cd ..
.venv/bin/python -I scripts/mitsuba_render.py cidades/<id>/cena /tmp/kf /tmp/kf-jpg --spp 64   # grava q_NNNNN.jpg
```

**Refazer só um trecho** depois de mudar a cena: rode `render.mjs --camada <pasta> --de A --ate B` na mesma pasta de camada. Os quadros novos substituem os antigos, e o `info.jsonl` usa a última linha de cada quadro. Depois rode o `mitsuba_render.py` de novo.

## Tempo e recursos (NVIDIA GB10, 1080p)

| Etapa | Por quadro | Porto Alegre (95 s, 2.849 quadros) |
|---|---|---|
| Camada (Chrome) | ~0,15 s | ~7 min |
| Mitsuba, 64 amostras + removedor de ruído | ~0,6–0,8 s | ~30–38 min |
| Motor normal (para comparar) | ~0,1 s | ~5 min |

- **Memória:** usa até ~40 GB num recorte de 530 mil prédios. Rodar com `systemd-run --user --scope -p MemoryMax=90G`.
- **Disco:** a camada em PNG ocupa ~1–2 MB por quadro.

## Armadilhas já resolvidas

- **`far_clip`:** o padrão do Mitsuba é 10 km, e a cidade inteira some (sai só o céu). Usar `far_clip: 1e6`.
- **Material de um lado só:** a face do avesso sai preta. Usar BSDF `twosided`.
- **Cor por vértice (`mesh_attribute`):** gera NaN, que aparece como pontos pretos. A cor dos prédios vai por uma paleta (bitmap 1024×1) com coordenadas de textura.
- **Textura do relevo:** coordenada `v = 0` no **norte**.
- **Fundo da camada:** o plano `chao-longe` é desenhado antes do relevo e apareceria através do relevo transparente. No modo camada ele sai do motor e vira um plano no Mitsuba.
- **Chão de perto (zoom ≥ 15):** fica borrado, porque o satélite tem ~9 m por pixel. O Mitsuba não resolve isso; precisa de textura melhor ou câmera mais alta.

## Opções da cena ligadas a esta ferramenta

- `fim.esconde_hud: true` faz bandeira, ano, população e linha do tempo sumirem no fecho. Usado no Porto Alegre, com `fim.titulo`, `fim.sub`, `fim.marca`, `escuro` e `fica`.
