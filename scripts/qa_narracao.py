"""Confere se cada ano/número da fala de tela foi ouvido pela transcrição (lição: 2024 já saiu 2004)."""
import json, re, os, sys
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
NJ = f"{DIR}/narracao.json"
if os.path.exists(NJ):   # narração como camada: {bloco: texto}
    textos = {k: v for k, v in json.load(open(NJ)).items() if not k.startswith("_") and v}
else:                    # legado POA: roteiro.json[tts]
    textos = {b["id"]: b.get("tts", "") for b in json.load(open(f"{DIR}/roteiro.json"))["blocos"]}
tem = json.load(open(f"{DIR}/narracao/tempos.json"))
erros = []
for k, v in tem.items():
    anos = re.findall(r"\b1[5-9]\d\d\b|\b20\d\d\b", textos.get(k, ""))
    ouv = v["ouvido"]
    for a in anos:
        if a not in ouv: erros.append(f"{k}: ano {a} não ouvido → «{ouv}»")
    if not textos.get(k): erros.append(f"{k}: sem fala no texto")
    if not ouv.strip(): erros.append(f"{k}: nada ouvido na transcrição")
print("OK anos" if not erros else "FALHA\n" + "\n".join(erros)); sys.exit(1 if erros else 0)
