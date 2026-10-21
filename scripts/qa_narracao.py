"""Confere se cada ano/número da fala de tela foi ouvido pela transcrição (lição: 2024 já saiu 2004)."""
import json, re, os, sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rot = {b["id"]: b for b in json.load(open(f"{raiz}/roteiro.json"))["blocos"]}
tem = json.load(open(f"{raiz}/narracao/tempos.json"))
erros = []
for k, v in tem.items():
    anos = re.findall(r"\b1[78]\d\d\b|\b19\d\d\b|\b20\d\d\b", rot[k]["fala"])
    ouv = v["ouvido"]
    for a in anos:
        if a not in ouv: erros.append(f"{k}: ano {a} não ouvido → «{ouv}»")
    if k not in rot or not rot[k]["tts"]: erros.append(f"{k}: sem fala no roteiro")
print("OK anos" if not erros else "FALHA\n" + "\n".join(erros)); sys.exit(1 if erros else 0)
