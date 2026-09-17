"""Bounded synthesis of a counterexample to the four-vertex deletion lemma."""
from itertools import combinations
import json
import z3

records=[]
for n in range(1,9):
    for a,b in combinations(range(n+2),2):
        original=[v for v in range(n+2) if v not in (a,b)]
        removed={original[0],original[-1]}
        left=[v for v in original if v<a]
        right=[v for v in original if v>b]
        if left: removed.add(left[-1])
        if right: removed.add(right[0])
        edges={e:(z3.BoolVal(True) if a in e or b in e else z3.Bool(f'e{e[0]}_{e[1]}')) for e in combinations(range(n+2),2)}
        s=z3.Solver()
        for u,v,w,x,y,z in combinations(range(n+2),6):
            s.add(z3.Not(z3.And(edges[u,z],edges[v,y],edges[w,x])))
        bad=[]
        for u,x,y,v in combinations([v for v in original if v not in removed],4):
            bad.append(z3.And(edges[u,v],edges[x,y]))
        s.add(z3.Or(bad))
        result=s.check()
        assert result==z3.unsat,(n,a,b,result)
        records.append({'n':n,'apices':[a,b],'result':str(result)})
print(json.dumps(records,indent=2))
