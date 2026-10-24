"""CÓPIA da versão centro (marcos + futuro). roteiro.json (+ narracao/tempos.json, se existir) → cidades/<id>/cena/cena.js

Duração do bloco: `dur` fixo (vídeo sem narração) ou fala medida/estimada + respiro (narrado).
Com 3 anos no bloco, o tempo avança rápido no 'pulo' (s) antes do evento; cartão, efeitos e fala entram depois.
Uso: CIDADE=<id> .venv/bin/python -I scripts/gerar_cena.py [--saida pasta]
"""
import json
import os
import sys

import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "..", "scripts"))
from cidade import *  # noqa
saida = sys.argv[sys.argv.index("--saida") + 1] if "--saida" in sys.argv else f"{DIR}/cena"
RESPIRO = 0.6
REGIMES_BR = [
    {"ano": 1500, "nome": "Brasil Colônia", "bandeira": "portugal"},
    {"ano": 1815.95, "nome": "Reino Unido de Portugal e Brasil", "bandeira": "reino"},
    {"ano": 1822.7, "nome": "Império do Brasil", "bandeira": "imperio"},
    {"ano": 1870, "nome": "Império do Brasil", "bandeira": "imperio2"},
    {"ano": 1889.87, "nome": "República", "bandeira": "republica"},
    {"ano": 1960, "nome": "República", "bandeira": "brasil"}]


def voo(a, b):
    """chave intermediária alta quando as duas vistas são de perto (zoom > 15,5) e distantes (> 500 m)"""
    import math
    d = math.hypot((a["lon"] - b["lon"]) * 111320 * math.cos(math.radians(a["lat"])), (a["lat"] - b["lat"]) * 111320)
    if d < 500 or min(a["zoom"], b["zoom"]) < 15.5:
        return None
    z = max(13.2, min(a["zoom"], b["zoom"]) - 1.4 - 0.9 * math.log2(d / 500))
    m = {k: (a[k] + b[k]) / 2 for k in a}
    m.update(zoom=round(z, 2), pitch=min(a["pitch"], b["pitch"], 48))
    return m


def main():
    rot = json.load(open(f"{DIR}/roteiro.json"))
    tf = f"{DIR}/narracao/tempos.json"
    tempos = json.load(open(tf)) if os.path.exists(tf) else {}
    # "ano_exato" (data de referência do censo) e "usar": false (ponto fora da curva do contador) — opcionais, versão centro
    pop = [[p.get("ano_exato", int(p["ano"])), int(p["pop"])] for p in json.load(open(f"{PESQ}/populacao.json"))["serie"] if p.get("usar", True)]
    pop.append([2026, pop[-1][1]])

    C = {"exz": rot.get("exz", 1.6), "exb": rot.get("exb", 1.5), "nascer": 2.5, "ajusteAgua": 0.5, "muroAlt": 22,
         "anos": [], "cam": [], "pop": pop, "cartoes": [], "cheias": [], "rotulos": [], "tropas": [], "tons": [],
         "muroDestaque": [], "falas": [], "frotas": [], "pulsos": [], "imagens": [], "chamadas": [],
         "regimes": rot.get("regimes", REGIMES_BR)}
    for k in ("aterro", "globo", "linha", "fim", "hud_de", "ultimoCenso", "popRotulo", "predios_neutros", "marcos_ez", "arvores", "arvores_auto", "pisos", "ruas", "corLonge", "longe", "teto", "satLonge", "aguas", "cartaoDireita", "cartaoEsquerda", "popArredAte"):
        if k in rot:
            C[k] = rot[k]
    C.setdefault("aterro", {"ano0": 1960, "ano1": 1978}) if CFG.get("feicoes", {}).get("aterro") else None
    for k in ("fortes", "linhas", "areas", "marcos"):
        C[k] = [dict(x, destaque=[]) for x in rot.get(k, [])]
    idx = {(k, x["id"]): x for k in ("fortes", "linhas", "areas", "marcos") for x in C[k]}

    t = 0.0
    for b in rot["blocos"]:
        tts = b.get("tts", "")
        if b["id"] in tempos:
            fala = tempos[b["id"]]["dur"]
        else:
            fala = len(tts.split()) / 2.5 if tts else 0.0
        an = b["anos"]
        pre = b.get("pulo", 1.6) if len(an) == 3 else 0.0
        corpo = b["dur"] if "dur" in b else max(fala + (RESPIRO if fala else 0), b.get("dur_min", 0))
        dur = pre + corpo + b.get("dur_extra", 0)
        t0, t1 = t, t + dur
        if C["cam"] and not b.get("corte"):
            b["cam"][0] = C["cam"][-1][1]
        if pre:
            C["anos"] += [[round(t0, 3), an[0]], [round(t0 + pre, 3), an[1]], [round(t1 - 0.001, 3), an[2]]]
        else:
            C["anos"] += [[round(t0, 3), an[0]], [round(t1 - 0.001, 3), an[1]]]
        if "dur" in b and b["cam"][0] != b["cam"][1]:
            # sem narração: chega ao alvo cedo e segura com leve avanço enquanto o cartão é lido
            ch_ = t0 + pre + (dur - pre) * b.get("chega", 0.45)
            fim_ = dict(b["cam"][1]); fim_["zoom"] = fim_["zoom"] + 0.12
            via = voo(b["cam"][0], b["cam"][1]) if rot.get("voo_alto") else None
            if via:   # viagem longa entre vistas de perto: sobe acima dos telhados no meio do caminho (não atravessa prédios)
                C["cam"] += [[round(t0, 3), b["cam"][0]], [round(t0 + (ch_ - t0) * 0.5, 3), via], [round(ch_, 3), b["cam"][1]], [round(t1 - 0.001, 3), fim_]]
            else:
                C["cam"] += [[round(t0, 3), b["cam"][0]], [round(ch_, 3), b["cam"][1]], [round(t1 - 0.001, 3), fim_]]
            b["cam"][1] = fim_
        else:
            C["cam"] += [[round(t0, 3), b["cam"][0]], [round(t1 - 0.001, 3), b["cam"][1]]]
        te = t0 + pre                         # início do evento (depois do pulo)
        if tts:
            C["falas"].append({"id": b["id"], "t0": round(te, 3), "dur": round(fala, 3)})
        if "globo" in b:
            g = dict(b["globo"]); g["chaves"] = [[round(t0 + k * dur, 3), v] for k, v in g["chaves"]]; g["t1"] = round(t1, 3)
            if g.get("entra"):   # globo no meio do vídeo (entra com fade): vai para a lista C.globos
                g["t0"] = round(t0, 3); C.setdefault("globos", [C["globo"]] if "globo" in C else []).append(g)
            else:
                C["globo"] = g
                if "globos" in C:
                    C["globos"].insert(0, g)
        if rot.get("hud_de_bloco") == b["id"]:
            C["hud_de"] = round(t0, 3)
        if "capa" in b:
            C["capa"] = {**b["capa"], "t1": b["capa"]["segura"]}
        if "cartao" in b:
            de = b["cartao"].get("de", 0)
            C["cartoes"].append({**b["cartao"], "t0": round(te + 0.4 + de * (dur - pre), 3), "t1": round(t1 - 0.2, 3)})
            loc = b["cartao"].get("local") or b.get("local")
            if loc and b.get("pulso", True):
                C["pulsos"].append({"lon": loc[0], "lat": loc[1], "t0": round(te + 0.3, 3), "t1": round(min(t1, te + 4.5), 3), "r": b.get("pulso_r", 450)})
        if "cheia" in b:
            ch = b["cheia"]
            niv = [[round(te + k * (dur - pre), 3), v] for k, v in ch["nivel"]]
            fim = t1
            if ch.get("baixa_no_fim"):
                niv.append([round(t1 + 1.8, 3), 0.0]); fim = t1 + 1.8
            C["cheias"].append({"t0": round(t0, 3), "t1": round(fim, 3), "nivel": niv})
        for r in b.get("rotulos", []):
            C["rotulos"].append({**r, "t0": round(te, 3), "t1": round(t1, 3)})
        if "tropas" in b:
            C["tropas"].append({**b["tropas"], "t0": round(te, 3), "t1": round(t1, 3)})
        if "frota" in b:
            fr = b["frota"]
            C["frotas"].append({**fr, "t0": round(te, 3), "t1": round(te + fr.get("dura", corpo * 0.7), 3)})
        if "imagem" in b:
            C["imagens"].append({**b["imagem"], "t0": round(te + 0.6, 3), "t1": round(t1 - 0.3, 3)})
        for st in b.get("setas_tela", []):
            C.setdefault("setasTela", []).append({**st, "t0": round(te + 0.5, 3), "t1": round(t1 - 0.3, 3)})
        for c in b.get("chamadas", []):
            C["chamadas"].append({**c, "t0": round(te + 0.5, 3), "t1": round(t1 - 0.3, 3)})
        if "galeria" in b:
            C["galeria"] = {**b["galeria"], "t0": round(te + 0.3, 3), "t1": round(t1 if b["galeria"].get("fica") else t1 - 3.4, 3)}
        if "futuro" in b:   # versão centro: cidade futura (visão) entra neste bloco
            C["futuro"] = {**b["futuro"], "t0": round(te + b["futuro"].get("de", 0) * (dur - pre), 3)}
            if not b["futuro"].get("fica_ate_fim"):
                C["futuro"]["t1"] = round(t1, 3)
        if "tom" in b:
            C["tons"].append({**b["tom"], "t0": round(te, 3), "t1": round(t1, 3)})
        if b.get("muro_destaque"):
            C["muroDestaque"].append([round(te, 3), round(t1, 3)])
        for d in b.get("destaca", []):
            tipo, i = d.split(":")
            idx[({"forte": "fortes", "linha": "linhas", "area": "areas", "marco": "marcos"}[tipo], i)]["destaque"].append([round(te, 3), round(t1, 3)])
        C.setdefault("blocos_t", {})[b["id"]] = [round(te, 3), round(t1, 3)]
        t = t1
    C["duracao"] = round(t, 3)
    if "linha" in C and "marcas" not in C["linha"]:
        C["linha"]["marcas"] = sorted({round(b["anos"][-2] if len(b["anos"]) == 3 else b["anos"][0]) for b in rot["blocos"] if "cartao" in b})
    os.makedirs(saida, exist_ok=True)
    open(f"{saida}/cena.js", "w").write("window.CENA = " + json.dumps(C, ensure_ascii=False, indent=1) + ";\n")
    print(f"cena {saida}/cena.js · duração {t:.1f} s · blocos {len(rot['blocos'])} · cartões {len(C['cartoes'])}")


if __name__ == "__main__":
    main()
