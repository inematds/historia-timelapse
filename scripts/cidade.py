"""Caminhos e configuração da cidade ativa (env CIDADE obrigatório: cidades/<CIDADE>/config.json)."""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = os.environ.get("CIDADE") or exit("defina CIDADE=<id> (pasta em cidades/)")
DIR = f"{RAIZ}/cidades/{ID}"
CFG = json.load(open(f"{DIR}/config.json"))
W, S, E, N = CFG["bbox"]
DADOS, BRUTOS, PESQ, ASSETS = f"{DIR}/dados", f"{DIR}/dados/brutos", f"{DIR}/dados/pesquisa", f"{DIR}/assets"
for _d in (BRUTOS, PESQ, ASSETS):
    os.makedirs(_d, exist_ok=True)
