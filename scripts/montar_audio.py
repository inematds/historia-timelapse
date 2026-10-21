"""Voz de cada bloco no seu tempo + música (abaixa sob a voz) → final/audio.wav em -14 LUFS."""
import json, os, re, subprocess
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
C = json.loads(re.sub(r"^window.CENA = |;\s*$", "", open(f"{DIR}/cena/cena.js").read()))
tem = json.load(open(f"{DIR}/narracao/tempos.json"))
MUS = os.path.expanduser("~/projetos/output/musicas/balao-exploracao-20260818/faixa-1.mp3")
LEAD = 0.25
os.makedirs(f"{DIR}/final", exist_ok=True)
dur = C["duracao"]
ins, fil = [], []
for i, f in enumerate(C["falas"]):
    ins += ["-i", tem[f["id"]]["wav"]]
    ms = int((f["t0"] + LEAD) * 1000)
    fil.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},apad[v{i}]")
n = len(C["falas"])
fil.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,atrim=0:{dur},asplit=2[voz][sc]")
ins += ["-stream_loop", "-1", "-i", MUS]
fil.append(f"[{n}:a]aresample=48000,atrim=0:{dur},afade=t=in:d=1.2,afade=t=out:st={dur-3}:d=3,volume=0.55[m]")
fil.append("[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=80:release=600[md]")
fil.append("[voz][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[out]",
                "-ar", "48000", "-ac", "2", f"{DIR}/final/audio.wav"], check=True)
print("audio", f"{DIR}/final/audio.wav", f"{dur:.1f} s")
