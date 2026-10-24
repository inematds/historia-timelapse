#!/usr/bin/env bash
# Render com luz real (Mitsuba 3 na GPU): a mesma cena do render_trechos.sh, com relevo e prédios iluminados de verdade.
# 1) camada transparente (HUD, cartões, globo, efeitos) + câmera, em trechos de 60 s (navegador novo a cada trecho);
# 2) scripts/mitsuba_render.py desenha relevo + prédios com a mesma câmera e monta céu → Mitsuba → camada.
# Uso: bash render_luz.sh <pasta-da-cena> <saida.mp4> [spp=64] [segundos-por-trecho=60]
set -euo pipefail
CENA=$(realpath "$1"); SAIDA=$(realpath -m "$2"); SPP=${3:-64}; PASSO=${4:-60}
cd "$(dirname "$0")"
RAIZ=$(realpath ..)
DUR=$(python3 -c "import json,re;print(json.loads(re.sub(r'^window.CENA = |;\s*$','',open('$CENA/cena.js').read()))['duracao'])")
CAM=$(dirname "$SAIDA")/camada; rm -rf "$CAM"; mkdir -p "$CAM"
i=0; de=0
while python3 -c "import sys;sys.exit(0 if $de < $DUR else 1)"; do
  ate=$(python3 -c "print(min($de+$PASSO,$DUR))")
  node render.mjs "$CENA" --camada "$CAM" --de "$de" --ate "$ate" > "$CAM/t$i.log" 2>&1
  if grep -qiE "allocation failed|pageerror|Worker exception" "$CAM/t$i.log"; then echo "ERRO na camada, trecho $i ($de-$ate s): $(grep -iE 'allocation failed|pageerror|Worker exception' "$CAM/t$i.log" | head -1)"; exit 1; fi
  echo "camada $i ok ($de–$ate s)"
  de=$ate; i=$((i+1))
done
"$RAIZ/.venv/bin/python" -I "$RAIZ/scripts/mitsuba_render.py" "$CENA" "$CAM" "$SAIDA" --spp "$SPP"
echo "ok $SAIDA"
