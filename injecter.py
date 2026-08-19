#!/usr/bin/env python3
"""Injecte balles.json dans gabarit.html et produit index.html."""
import json, sys, pathlib
d = pathlib.Path(__file__).parent
data = json.loads((d/(sys.argv[1] if len(sys.argv)>1 else 'balles.json')).read_text('utf-8'))
cells = [b['cel'] for b in data]
dup = {c for c in cells if cells.count(c) > 1}
if dup:
    sys.exit("COLLISION d'alvéole : cellules %s occupées deux fois." % sorted(dup))
g = (d/'gabarit.html').read_text('utf-8')
a, b = g.index('/*__DONNEES__*/'), g.index('/*__FIN__*/')
out = g[:a] + '/*__DONNEES__*/' + json.dumps(data, ensure_ascii=False) + g[b:]
(d/'index.html').write_text(out, 'utf-8')
print("index.html écrit — %d balles" % len(data))
