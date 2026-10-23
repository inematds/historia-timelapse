"""Monta "As capitais do Brasil" (fase 1, sem narração): emenda os 3 atos com uma transição curta, trilha de música contínua (-14 LUFS).
Entrada: cidades/capitais-{ssa,rio,bsb}/final/video.mp4 (render_trechos do motor centro).
Saída: cidades/capitais/final/capitais-v<N>.mp4 e a versão 540p.
Uso: .venv/bin/python -I cidades/capitais/montar.py [--versao 1]"""
import json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V = sys.argv[sys.argv.index("--versao") + 1] if "--versao" in sys.argv else "1"
ATOS = ["capitais-ssa", "capitais-rio", "capitais-bsb"]
XF = 0.8   # transição entre atos (s)
CORTE_FIM = 2.4   # o motor escurece os últimos 3,2 s de cada cena; nos atos 1 e 2 corta-se isso para o preto cair na transição
FIN = f"{AQUI}/final"; os.makedirs(FIN, exist_ok=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


vids = [f"{RAIZ}/cidades/{a}/final/video.mp4" for a in ATOS]
ds = [dur(v) - (CORTE_FIM if i < len(vids) - 1 else 0) for i, v in enumerate(vids)]
# 1) vídeo: xfade (fade pelo preto) entre os atos
fil = [f"[{i}:v]trim=0:{d:.3f},setpts=PTS-STARTPTS[a{i}]" for i, d in enumerate(ds)]
prev, off = "[a0]", 0.0
for k in range(1, len(vids)):
    off += ds[k - 1] - XF
    fil.append(f"{prev}[a{k}]xfade=transition=fadeblack:duration={XF}:offset={off:.3f}[v{k}]"); prev = f"[v{k}]"
total = sum(ds) - XF * (len(vids) - 1)
video = f"{FIN}/video.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", v] for v in vids], []), "-filter_complex", ";".join(fil), "-map", prev,
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", video], check=True)
# 2) música: faixas do config do 1º ato em sequência com crossfade, até o fim
cfg = json.load(open(f"{RAIZ}/cidades/{ATOS[0]}/config.json"))
faixas = [os.path.expanduser(x) for x in cfg["musicas"]]
seq, tot, i = [], 0.0, 0
while tot < total + 5:
    f = faixas[i % len(faixas)]; seq.append(f); tot += dur(f) - (4 if seq[1:] else 0); i += 1
fa, prev = [], "[0:a]"
for k in range(1, len(seq)):
    fa.append(f"{prev}[{k}:a]acrossfade=d=4[x{k}]"); prev = f"[x{k}]"
fa.append(f"{prev}atrim=0:{total},afade=t=in:d=1.5,afade=t=out:st={total-4}:d=4,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
audio = f"{FIN}/audio.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", f] for f in seq], []), "-filter_complex", ";".join(fa), "-map", "[out]",
                "-ar", "48000", "-ac", "2", audio], check=True)
# 3) mux + 540p
out = f"{FIN}/capitais-v{V}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", out], check=True)
p540 = f"{FIN}/capitais-v{V}-540p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "24", "-preset", "medium",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", p540], check=True)
bot = f"{FIN}/capitais-v{V}-bot.mp4"   # cabe no limite de 49 MB do bot
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-b:v", "400k", "-maxrate", "600k", "-bufsize", "1200k",
                "-preset", "slow", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", bot], check=True)
print("atos", [round(d, 1) for d in ds], "total", round(total, 1), "s →", out, p540)
