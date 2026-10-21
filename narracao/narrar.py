#!/usr/bin/env python3
"""Grava uma fala por bloco do roteiro com a voz do Nei (motor do cardshorts: chatterbox nei, confere por
transcrição e corta o fim). Acelera com atempo, mede e grava narracao/tempos.json {id: {dur, wav, texto}}."""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "projetos/cardshorts"))
import cardshorts as cs

AQUI = Path(__file__).resolve().parent
rot = json.loads((AQUI.parent / "roteiro.json").read_text())
TEMPO = rot["voz"].get("atempo", 1.08)
SO = sys.argv[sys.argv.index("--so") + 1].split(",") if "--so" in sys.argv else None
cenas = [{"id": b["id"], "fala": b["tts"]} for b in rot["blocos"] if b["tts"] and (not SO or b["id"] in SO)]
r = {"voz": dict(cs.VOZ_PADRAO), "cenas": cenas, "_obra": AQUI / ".obra"}
r["voz"].update({k: rot["voz"][k] for k in ("exaggeration", "cfg_weight") if k in rot["voz"]})
r["_obra"].mkdir(exist_ok=True)
cs.gerar_voz(r)
build = AQUI / "build"; build.mkdir(exist_ok=True)
tf = AQUI / "tempos.json"
tempos = json.loads(tf.read_text()) if (SO and tf.exists()) else {}
for c in r["cenas"]:
    w = build / f"{c['id']}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", c["_wav"], "-af", f"atempo={TEMPO}",
                    "-ar", "48000", "-ac", "1", w], check=True)
    pal = cs.transcrever(w, build / f"t_{c['id']}", palavras=True)
    tempos[c["id"]] = {"dur": round(cs.dur(w), 3), "wav": str(w), "texto": c["fala"],
                       "ouvido": " ".join(p["word"].strip() for p in pal)}
(AQUI / "tempos.json").write_text(json.dumps(tempos, ensure_ascii=False, indent=1))
for k, v in tempos.items():
    if SO and k not in SO: continue
    print(f"{k:10s} {v['dur']:5.1f} s | {v['ouvido']}")
