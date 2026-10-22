"""Trilha só de música (vídeo sem narração): faixas em sequência com crossfade, em laço até a duração → final/audio.wav (-14 LUFS)."""
import json, os, re, subprocess
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cidade import *  # noqa
C = json.loads(re.sub(r"^window.CENA = |;\s*$", "", open(f"{DIR}/cena/cena.js").read()))
M = os.path.expanduser("~/projetos/output/musicas")
FAIXAS = [f"{M}/balao-exploracao-20260818/faixa-1.mp3", f"{M}/balao-exploracao-20260818/faixa-2.mp3"]
dur, XF = C["duracao"], 4
seq, tot, i = [], 0.0, 0
while tot < dur + 5:
    f = FAIXAS[i % len(FAIXAS)]; d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    seq.append(f); tot += d - (XF if seq[1:] else 0); i += 1
ins = sum([["-i", f] for f in seq], [])
fil, prev = [], "[0:a]"
for k in range(1, len(seq)):
    fil.append(f"{prev}[{k}:a]acrossfade=d={XF}[x{k}]"); prev = f"[x{k}]"
fil.append(f"{prev}atrim=0:{dur},afade=t=in:d=1.5,afade=t=out:st={dur-4}:d=4,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
os.makedirs(f"{DIR}/final", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[out]", "-ar", "48000", "-ac", "2", f"{DIR}/final/audio.wav"], check=True)
print("musica", len(seq), "faixas", f"{dur:.1f} s ->", f"{DIR}/final/audio.wav")
