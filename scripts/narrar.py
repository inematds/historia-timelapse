#!/usr/bin/env python3
"""Grava a narração por bloco com a voz do Nei (cardshorts: chatterbox nei, confere por transcrição e corta o fim).
Fonte do texto: cidades/<id>/narracao.json {bloco: texto} (vídeo narrado como camada) ou roteiro.json[tts] (legado POA).
Saída: cidades/<id>/narracao/tempos.json {bloco: {dur, wav, texto, ouvido}}.  Uso: CIDADE=<id> python3 scripts/narrar.py [--so a,b]"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); from cidade import *  # noqa
sys.path.insert(0, str(Path.home() / "projetos/cardshorts")); import cardshorts as cs
D = Path(DIR); NJ = D / "narracao.json"
voz = {"exaggeration": 0.6, "cfg_weight": 0.6, "atempo": 1.08}
if NJ.exists():
    nj = json.loads(NJ.read_text()); voz.update(nj.get("_voz", {})); textos = {k: v for k, v in nj.items() if not k.startswith("_") and v}
else:
    rot = json.loads((D / "roteiro.json").read_text()); voz.update(rot.get("voz", {})); textos = {b["id"]: b["tts"] for b in rot["blocos"] if b.get("tts")}
SO = sys.argv[sys.argv.index("--so") + 1].split(",") if "--so" in sys.argv else None
cenas = [{"id": k, "fala": v} for k, v in textos.items() if not SO or k in SO]
r = {"voz": dict(cs.VOZ_PADRAO), "cenas": cenas, "_obra": D / "narracao" / ".obra"}
r["voz"].update({k: voz[k] for k in ("exaggeration", "cfg_weight")}); r["_obra"].mkdir(parents=True, exist_ok=True)
cs.gerar_voz(r)
build = D / "narracao" / "build"; build.mkdir(exist_ok=True)
tf = D / "narracao" / "tempos.json"; tempos = json.loads(tf.read_text()) if (SO and tf.exists()) else {}
for c in r["cenas"]:
    w = build / f"{c['id']}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", c["_wav"], "-af", f"atempo={voz['atempo']}", "-ar", "48000", "-ac", "1", w], check=True)
    pal = cs.transcrever(w, build / f"t_{c['id']}", palavras=True)
    tempos[c["id"]] = {"dur": round(cs.dur(w), 3), "wav": str(w), "texto": c["fala"], "ouvido": " ".join(p["word"].strip() for p in pal)}
tf.write_text(json.dumps(tempos, ensure_ascii=False, indent=1))
for k, v in tempos.items():
    if not SO or k in SO: print(f"{k:28s} {v['dur']:5.1f} s | {v['ouvido']}")
