#!/usr/bin/env bash
# Render em trechos (navegador novo a cada trecho) para não estourar memória em vídeos longos.
# Uso: bash render_trechos.sh <pasta-da-cena> <saida.mp4> [segundos-por-trecho]
set -euo pipefail
cd "$(dirname "$0")"
CENA=$1; SAIDA=$2; PASSO=${3:-60}
DUR=$(python3 -c "import json,re,sys;print(json.loads(re.sub(r'^window.CENA = |;\s*$','',open('$CENA/cena.js').read()))['duracao'])")
TMP=$(dirname "$SAIDA")/trechos; mkdir -p "$TMP"; rm -f "$TMP"/*.mp4 "$TMP"/lista.txt
i=0; de=0
while python3 -c "import sys;sys.exit(0 if $de < $DUR else 1)"; do
  ate=$(python3 -c "print(min($de+$PASSO,$DUR))")
  f="$TMP/t$(printf %02d $i).mp4"
  node render.mjs "$CENA" "$f" --de "$de" --ate "$ate" > "$TMP/t$i.log" 2>&1
  if grep -qiE "allocation failed|pageerror|Worker exception" "$TMP/t$i.log"; then echo "ERRO no trecho $i ($de-$ate s): $(grep -iE 'allocation failed|pageerror|Worker exception' "$TMP/t$i.log" | head -1)"; exit 1; fi
  echo "file '$(realpath "$f")'" >> "$TMP/lista.txt"; echo "trecho $i ok ($de–$ate s)"
  de=$ate; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i "$TMP/lista.txt" -c copy "$SAIDA"
echo "ok $SAIDA"
