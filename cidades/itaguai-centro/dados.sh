#!/usr/bin/env bash
# Prepara os dados da versão centro (mesmos scripts do motor, CIDADE=itaguai-centro)
set -e; cd "$(dirname "$0")/../.."; export CIDADE=itaguai-centro
for s in extrai_osm extrai_msbuild extrai_feicoes prep_terreno prep_predios modelo_anos prep_efeitos; do echo "== $s"; .venv/bin/python -I scripts/$s.py; done; echo FIM
