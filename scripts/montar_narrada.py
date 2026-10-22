"""Versão narrada = camada de áudio sobre o vídeo sem narração (regra do motor, 21/10/2026).
Cada fala entra no início do evento do bloco (blocos_t da cena); confere que cabe no bloco; música abaixa sob a voz.
Saída: cidades/<id>/final/audio-narrado.wav (-14 LUFS).  Uso: CIDADE=<id> python3 scripts/montar_narrada.py"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cidade import *  # noqa
C = json.loads(re.sub(r"^window.CENA = |;\s*$", "", open(f"{DIR}/cena/cena.js").read()))
BT, tem = C["blocos_t"], json.load(open(f"{DIR}/narracao/tempos.json"))
LEAD, FOLGA = 0.3, 0.8
erros = [f"{k}: fala {v['dur']:.1f} s > bloco {BT[k][1]-BT[k][0]-LEAD-FOLGA:.1f} s" for k, v in tem.items() if v["dur"] > BT[k][1] - BT[k][0] - LEAD - FOLGA]
if erros: sys.exit("NÃO CABE:\n" + "\n".join(erros))
dur = C["duracao"]; ins, fil = [], []
for i, (k, v) in enumerate(tem.items()):
    ms = int((BT[k][0] + LEAD) * 1000); ins += ["-i", v["wav"]]
    fil.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},apad[v{i}]")
n = len(tem)
fil.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,atrim=0:{dur},asplit=2[voz][sc]")
ins += ["-i", f"{DIR}/final/audio.wav"]
fil.append(f"[{n}:a]aresample=48000,volume=0.6[m]")
fil.append("[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=80:release=600[md]")
fil.append("[voz][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[out]", "-ar", "48000", "-ac", "2", f"{DIR}/final/audio-narrado.wav"], check=True)
print(f"ok {DIR}/final/audio-narrado.wav · {n} falas · {dur:.1f} s")
