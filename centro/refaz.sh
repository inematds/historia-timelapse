#!/usr/bin/env bash
# Refaz a cena da versão centro na ordem certa (roteiro → anos → limpa marcos → futuro → roteiro de novo → cena)
set -e; cd "$(dirname "$0")/.."; export CIDADE=itaguai-centro; PY=.venv/bin/python
(cd cidades/itaguai-centro && ../../$PY -I roteiro_itaguai_centro.py)
$PY -I scripts/modelo_anos.py | tail -1
$PY -I centro/scripts/limpa_marcos.py | tail -1
$PY -I centro/scripts/futuro_sitios.py 2>/dev/null
(cd cidades/itaguai-centro && ../../$PY -I roteiro_itaguai_centro.py)
$PY -I centro/scripts/gerar_cena.py
