#!/usr/bin/env python3
"""Injecte balles.json dans gabarit.html et produit index.html.

    python3 injecter.py [fichier.json]

Refuse de publier si deux balles occupent la même cellule du même carton.
"""
import json, sys, pathlib
d = pathlib.Path(__file__).parent
src = d / (sys.argv[1] if len(sys.argv) > 1 else 'balles.json')
data = json.loads(src.read_text('utf-8'))

adr = [(b.get('bac', '?'), b['cel']) for b in data]
dup = sorted({a for a in adr if adr.count(a) > 1})
if dup:
    sys.exit("COLLISION : %s occupée(s) deux fois." % ", ".join(f"{c}-{n:02d}" for c, n in dup))
for b in data:
    if b.get('cap') and b['cel'] > b['cap']:
        sys.exit("DÉBORDEMENT : cellule %d dans un carton de %d." % (b['cel'], b['cap']))

g = (d / 'gabarit.html').read_text('utf-8')
a, z = g.index('/*__DONNEES__*/'), g.index('/*__FIN__*/')
(d / 'index.html').write_text(
    g[:a] + '/*__DONNEES__*/' + json.dumps(data, ensure_ascii=False) + g[z:], 'utf-8')
print("index.html écrit — %d balles, %d carton(s)"
      % (len(data), len({b.get('bac') for b in data})))
