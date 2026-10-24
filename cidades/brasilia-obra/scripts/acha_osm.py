"""Procura no pbf do DF pontos com nome que casa com os termos (nós, vias e áreas). Uso: python -I acha_osm.py termo1 termo2 ..."""
import sys, osmium, re
termos = [t.lower() for t in sys.argv[1:]]
class H(osmium.SimpleHandler):
    def __init__(s): super().__init__(); s.r = []
    def _v(s, o, tipo, ll):
        n = o.tags.get("name", "")
        if n and any(t in n.lower() for t in termos):
            s.r.append((tipo, n, dict(o.tags).get("historic") or dict(o.tags).get("amenity") or dict(o.tags).get("building") or dict(o.tags).get("waterway") or "", ll))
    def node(s, n): s._v(n, "n", (round(n.location.lon, 6), round(n.location.lat, 6)))
    def way(s, w):
        try: ll = (round(sum(x.lon for x in w.nodes) / len(w.nodes), 6), round(sum(x.lat for x in w.nodes) / len(w.nodes), 6))
        except Exception: ll = None
        s._v(w, "w", ll)
h = H(); h.apply_file("dl/distrito-federal.osm.pbf", locations=True)
for x in h.r[:80]: print(x)
