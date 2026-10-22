"""Fase 3 = fase 1 + avatar do Nei (estúdio HeyGen) pequeno embaixo da bandeira, falando a narração.
Entrada: cidades/<id>/avatar/avatar.mp4 (UM vídeo com todas as falas de narracao.json, na ordem, em um parágrafo).
Transcreve o avatar, acha onde começa e termina cada fala, corta e põe cada trecho no início do evento do bloco
(blocos_t). A voz do avatar vira a narração; a música abaixa sob ela. Vídeo-base: config "video_base" (padrão final/video.mp4).
Saída: cidades/<id>/final/<id>-avatar.mp4.
Uso: CIDADE=<id> python3 scripts/montar_avatar.py [--saida nome.mp4]"""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); from cidade import *  # noqa
sys.path.insert(0, str(Path.home() / "projetos/cardshorts")); import cardshorts as cs

D = Path(DIR); AV = D / "avatar"; SEG = AV / "seg"; SEG.mkdir(parents=True, exist_ok=True)
C = json.loads(re.sub(r"^window.CENA = |;\s*$", "", (D / "cena/cena.js").read_text()))
BT = C["blocos_t"]; falas = {k: v for k, v in json.loads((D / "narracao.json").read_text()).items() if not k.startswith("_") and v}
saida = sys.argv[sys.argv.index("--saida") + 1] if "--saida" in sys.argv else f"{ID}-avatar.mp4"
LEAD, FOLGA, MAXV = 0.3, 0.8, 1.15          # mesmo início da narrada; acelera no máximo 15% se não couber
X, Y, LADO = 56, 200, 250                    # moldura embaixo da bandeira


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", s)


# 1. palavras do avatar com tempo
pal = cs.transcrever(AV / "avatar.mp4", AV / "transcricao", palavras=True)
tw = [(w, p["start"], p["end"]) for p in pal for w in norm(p["word"])]
# 2. alinha as palavras do roteiro às ouvidas
rot = [(k, w) for k, v in falas.items() for w in norm(v)]
sm = difflib.SequenceMatcher(None, [w for _, w in rot], [w for w, _, _ in tw], autojunk=False)
mapa = {}
for a, b, n in sm.get_matching_blocks():
    for i in range(n): mapa[a + i] = b + i
ini, fim = {}, {}
for i, (k, _) in enumerate(rot):
    if i in mapa:
        j = mapa[i]; ini.setdefault(k, tw[j][1]); fim[k] = tw[j][2]
ks = list(falas)
for n, k in enumerate(ks):                   # fala sem nenhuma palavra casada: entre a anterior e a próxima
    if k not in ini:
        a = fim.get(ks[n - 1], 0) if n else 0; b = next((ini[x] for x in ks[n + 1:] if x in ini), a + 4)
        ini[k], fim[k] = a + 0.1, b - 0.1
# 3. corta cada fala; confere que cabe
info, avisos = {}, []
for n, k in enumerate(ks):
    a = max(0, ini[k] - 0.12); b = fim[k] + 0.25
    if n + 1 < len(ks): b = min(b, ini[ks[n + 1]] - 0.05)
    dur = b - a; cabe = BT[k][1] - BT[k][0] - LEAD - FOLGA; v = max(1.0, dur / cabe)
    if v > MAXV: avisos.append(f"{k}: {dur:.1f} s não cabe em {cabe:.1f} s (precisaria {v:.2f}x)"); v = MAXV
    out = SEG / f"{k}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(AV / "avatar.mp4"),
                    "-vf", f"setpts=PTS/{v:.4f},crop=ih:ih:(iw-ih)/2:0,scale={LADO}:{LADO},fps=30",
                    "-af", f"atempo={v:.4f},aresample=48000", "-c:v", "libx264", "-crf", "18", "-c:a", "pcm_s16le", str(out.with_suffix(".mov"))], check=True)
    info[k] = {"t": round(BT[k][0] + LEAD, 3), "dur": round(dur / v, 3), "arq": str(out.with_suffix(".mov")), "vel": round(v, 3)}
(AV / "segmentos.json").write_text(json.dumps(info, ensure_ascii=False, indent=1))
if avisos: print("AVISO (acelerado no limite, pode invadir o próximo bloco):\n" + "\n".join(avisos))
# 4. compõe: vídeo-base + moldura + avatar por trecho; voz do avatar + música com sidechain
ins = ["-i", str(D / CFG.get("video_base", "final/video.mp4")), "-i", str(D / "final/audio.wav")]
fv, fa, ult = [], [], "[0:v]"
for i, (k, s) in enumerate(info.items()):
    ins += ["-itsoffset", f"{s['t']:.3f}", "-i", s["arq"]]; j = i + 2; t0, t1 = s["t"], s["t"] + s["dur"]
    fv.append(f"[{j}:v]format=yuva420p,fade=t=in:st={t0:.3f}:d=0.25:alpha=1,fade=t=out:st={t1 - 0.25:.3f}:d=0.25:alpha=1[a{i}]")
    fv.append(f"{ult}drawbox=x={X - 4}:y={Y - 4}:w={LADO + 8}:h={LADO + 8}:color=0xFACC15:t=fill:enable='between(t,{t0:.3f},{t1:.3f})'[b{i}]")
    fv.append(f"[b{i}][a{i}]overlay={X}:{Y}:eof_action=pass:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]"); ult = f"[v{i}]"
    ms = int(t0 * 1000); fa.append(f"[{j}:a]aresample=48000,adelay={ms}|{ms},apad[s{i}]")
n = len(info)
fa.append("".join(f"[s{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,atrim=0:{C['duracao']},asplit=2[voz][sc]")
fa.append("[1:a]aresample=48000,volume=0.6[m]")
fa.append("[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=80:release=600[md]")
fa.append("[voz][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
(AV / "filtro.txt").write_text(";".join(fv + fa))
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex_script", str(AV / "filtro.txt"), "-map", ult, "-map", "[out]",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-t", str(C["duracao"]), "-movflags", "+faststart", str(D / "final" / saida)], check=True)
print(f"ok {D / 'final' / saida} · {n} falas · velocidades {min(s['vel'] for s in info.values())}–{max(s['vel'] for s in info.values())}")
