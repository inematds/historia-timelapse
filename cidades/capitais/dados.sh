#!/usr/bin/env bash
# Prepara os dados de uma parte das capitais (mesmos scripts do motor). Uso: bash cidades/capitais/dados.sh capitais-bsb
set -e; cd "$(dirname "$0")/../.."; export CIDADE=$1
for s in extrai_osm extrai_msbuild extrai_feicoes prep_terreno prep_predios modelo_anos prep_efeitos; do echo "== $s $(date +%T)"; .venv/bin/python -I scripts/$s.py; done; echo FIM
