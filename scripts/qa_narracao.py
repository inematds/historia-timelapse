"""Confere se cada ano/número da fala de tela foi ouvido pela transcrição (lição: 2024 já saiu 2004)."""
import json, re, os, sys
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
rot = {b["id"]: b for b in json.load(open(f"{DIR}/roteiro.json"))["blocos"]}
tem = json.load(open(f"{DIR}/narracao/tempos.json"))
erros = []
for k, v in tem.items():
    anos = re.findall(r"\b1[78]\d\d\b|\b19\d\d\b|\b20\d\d\b", rot[k]["fala"])
    ouv = v["ouvido"]
    for a in anos:
        if a not in ouv: erros.append(f"{k}: ano {a} não ouvido → «{ouv}»")
    if k not in rot or not rot[k]["tts"]: erros.append(f"{k}: sem fala no roteiro")
print("OK anos" if not erros else "FALHA\n" + "\n".join(erros)); sys.exit(1 if erros else 0)
