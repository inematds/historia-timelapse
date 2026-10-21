"""roteiro.json (+ narracao/tempos.json, se existir) → cenas/poa/cena.js

Duração de cada bloco = fala medida (ou estimada a 2,5 palavras/s) + respiro, no mínimo dur_min.
Uso: .venv/bin/python -I scripts/gerar_cena.py [--saida cenas/poa]
"""
import json
import os
import sys

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saida = sys.argv[sys.argv.index("--saida") + 1] if "--saida" in sys.argv else f"{raiz}/cenas/poa"
RESPIRO = 0.6


def main():
    rot = json.load(open(f"{raiz}/roteiro.json"))
    tf = f"{raiz}/narracao/tempos.json"
    tempos = json.load(open(tf)) if os.path.exists(tf) else {}
    pop = [[int(p["ano"]), int(p["pop"])] for p in json.load(open(f"{raiz}/dados/pesquisa/populacao.json"))["serie"]]
    pop.append([2025, pop[-1][1]])

    C = {"exz": 1.6, "exb": 1.5, "nascer": 2.5, "ajusteAgua": 0.5, "muroAlt": 22,
         "anos": [], "cam": [], "pop": pop, "cartoes": [], "cheias": [], "rotulos": [], "tropas": [], "tons": [],
         "muroDestaque": [], "aterro": {"ano0": 1960, "ano1": 1978}, "falas": [],
         "regimes": [
             {"ano": 1700, "nome": "Brasil Colônia", "bandeira": "portugal"},
             {"ano": 1815.95, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
             {"ano": 1822.7, "nome": "Império do Brasil", "bandeira": "imperio"},
             {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
             {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
             {"ano": 1960, "nome": "República", "bandeira": "brasil"}]}
    t = 0.0
    for b in rot["blocos"]:
        if b["id"] in tempos:
            fala = tempos[b["id"]]["dur"]
        else:
            fala = len(b["tts"].split()) / 2.5 if b["tts"] else 0.0
        an = b["anos"]
        pre = b.get("pulo", 1.6) if len(an) == 3 else 0.0   # avanço rápido do tempo antes da fala
        dur = pre + max(fala + (RESPIRO if fala else 0), b.get("dur_min", 0)) + b.get("dur_extra", 0)
        t0, t1 = t, t + dur
        if C["cam"]:
            b["cam"][0] = C["cam"][-1][1]   # câmera contínua: começa onde o bloco anterior parou
        if pre:
            C["anos"] += [[round(t0, 3), an[0]], [round(t0 + pre, 3), an[1]], [round(t1 - 0.001, 3), an[2]]]
        else:
            C["anos"] += [[round(t0, 3), an[0]], [round(t1 - 0.001, 3), an[1]]]
        C["cam"] += [[round(t0, 3), b["cam"][0]], [round(t1 - 0.001, 3), b["cam"][1]]]
        if b["tts"]:
            C["falas"].append({"id": b["id"], "t0": round(t0 + pre, 3), "dur": round(fala, 3)})
        if "capa" in b:
            C["capa"] = {**b["capa"], "t1": b["capa"]["segura"]}
        if "cartao" in b:
            de = b["cartao"].get("de", 0)
            C["cartoes"].append({**b["cartao"], "t0": round(t0 + pre + 0.4 + de * (dur - pre), 3), "t1": round(t1 - 0.2, 3)})
        if "cheia" in b:
            ch = b["cheia"]
            niv = [[round(t0 + pre + k * (dur - pre), 3), v] for k, v in ch["nivel"]]
            fim = t1
            if ch.get("baixa_no_fim"):
                niv.append([round(t1 + 1.8, 3), 0.0]); fim = t1 + 1.8
            C["cheias"].append({"t0": round(t0, 3), "t1": round(fim, 3), "nivel": niv})
        for r in b.get("rotulos", []):
            C["rotulos"].append({**r, "t0": round(t0 + pre, 3), "t1": round(t1, 3)})
        if "tropas" in b:
            C["tropas"].append({**b["tropas"], "t0": round(t0 + pre, 3), "t1": round(t1, 3)})
        if "tom" in b:
            C["tons"].append({**b["tom"], "t0": round(t0 + pre, 3), "t1": round(t1, 3)})
        if b.get("muro_destaque"):
            C["muroDestaque"].append([round(t0 + pre, 3), round(t1, 3)])
        t = t1
    C["duracao"] = round(t, 3)
    # rótulo fixo do Guaíba fora da capa e do cartão de nascimento
    os.makedirs(saida, exist_ok=True)
    open(f"{saida}/cena.js", "w").write("window.CENA = " + json.dumps(C, ensure_ascii=False, indent=1) + ";\n")
    print(f"cena {saida}/cena.js · duração {t:.1f} s · blocos {len(rot['blocos'])} · "
          f"{'tempos medidos' if tempos else 'tempos ESTIMADOS'}")
    for f in C["falas"]:
        print(f"  {f['id']:10s} {f['t0']:6.1f} s  fala {f['dur']:.1f} s")


if __name__ == "__main__":
    main()
