"""Independent exact layout oracles and injected-instance checks."""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import z3


def graph(x):
    if not isinstance(x, dict) or set(x) != {'adj'} or not isinstance(x['adj'], list):
        raise ValueError('Expected adjacency matrix')
    a=x['adj'];n=len(a)
    if any(not isinstance(row,list) or len(row)!=n for row in a):
        raise ValueError('Matrix must be square')
    if any(type(a[i][j]) is not int or a[i][j] not in (0,1) or a[i][j]!=a[j][i] or (i==j and a[i][j]) for i in range(n) for j in range(n)):
        raise ValueError('Expected a simple undirected graph')
    return n,[(i,j) for i in range(n) for j in range(i+1,n) if a[i][j]]


def witness(x,w,k):
    n,edges=graph(x)
    if not isinstance(w,dict) or set(w)!={'order','queues'}:return False
    order=w['order'];queues=w['queues']
    if not isinstance(order,list) or any(type(v) is not int for v in order) or sorted(order)!=list(range(n)):return False
    if not isinstance(queues,list) or len(queues)!=len(edges) or any(type(q) is not int or not 0<=q<k for q in queues):return False
    pos={v:i for i,v in enumerate(order)}
    intervals=[sorted((pos[u],pos[v])) for u,v in edges]
    return all(queues[i]!=queues[j] or not (a<c<d<b or c<a<b<d) for i,(a,b) in enumerate(intervals) for j,(c,d) in enumerate(intervals[:i]))


def solve(x,k):
    n,edges=graph(x);s=z3.Solver()
    precedence={(i,j):z3.Bool(f'p{i}_{j}') for i,j in itertools.combinations(range(n),2)}
    def before(i,j):return precedence[i,j] if i<j else z3.Not(precedence[j,i])
    for i,j,l in itertools.combinations(range(n),3):
        s.add(z3.Implies(z3.And(before(i,j),before(j,l)),before(i,l)))
        s.add(z3.Implies(z3.And(before(l,j),before(j,i)),before(l,i)))
    colors=[z3.Bool(f'q{i}') if k==2 else z3.BoolVal(False) for i in range(len(edges))]
    if n>1:s.add(before(0,n-1))
    if colors:s.add(z3.Not(colors[0]))
    def between(a,x,b):return z3.Or(z3.And(before(a,x),before(x,b)),z3.And(before(b,x),before(x,a)))
    for i,(a,b) in enumerate(edges):
        for j,(c,d) in enumerate(edges[:i]):
            if len({a,b,c,d})<4:continue
            nested=z3.Or(z3.And(between(a,c,b),between(a,d,b)),z3.And(between(c,a,d),between(c,b,d)))
            s.add(z3.Implies(nested,colors[i]!=colors[j]))
    answer=s.check()
    if answer==z3.unsat:return None
    if answer!=z3.sat:raise RuntimeError(str(answer))
    model=s.model()
    order=sorted(range(n),key=lambda v:sum(z3.is_true(model.eval(before(u,v),model_completion=True)) for u in range(n) if u!=v))
    w={'order':order,'queues':[int(z3.is_true(model.eval(q,model_completion=True))) for q in colors]}
    assert witness(x,w,k)
    return w


def run(path,x,extract=False):
    r=subprocess.run([sys.executable,str(path)]+(['--extract'] if extract else []),input=json.dumps(x),text=True,capture_output=True,check=True)
    return json.loads(r.stdout)


def self_test(cases):
    for case in cases:
        x=case['source'];n,edges=graph(x)
        brute=any(witness(x,{'order':list(o),'queues':[0]*len(edges)},1) for o in itertools.permutations(range(n)))
        assert brute==case['yes']==(solve(x,1) is not None)
    for n,k,yes in [(0,2,True),(5,2,True),(6,2,False)]:
        x={'adj':[[int(i!=j) for j in range(n)] for i in range(n)]}
        assert (solve(x,k) is not None)==yes
    malformed=[{}, {'adj':[[1]]},{'adj':[[0,1],[0,0]]},{'adj':[[0],[]]}]
    for x in malformed:
        try:graph(x)
        except ValueError:pass
        else:raise AssertionError('Accepted malformed graph')
    x=cases[2]['source'];w=solve(x,1)
    assert w is not None
    assert not witness(x,{'order':[0,0],'queues':[0]},1)
    assert not witness(x,{'order':w['order'],'queues':[2]},2)
    no=next(c['source'] for c in cases if not c['yes'])
    assert not witness(no,{'order':list(range(len(no['adj']))),'queues':[0]*len(graph(no)[1])},1)
    assert (solve(no,1) is not None)!=(solve({'adj':[]},2) is not None)
    print(json.dumps({'self_test':'pass','source_cases':len(cases),'target_oracle_cases':3,'malformed_outputs_rejected':4,'solver':z3.get_version_string()}),flush=True)


def check(candidate,cases):
    calls=0
    for case in cases:
        source=case['source'];target=run(candidate,source);graph(target)
        sw=solve(source,1);assert (sw is not None)==case['yes']
        print(json.dumps({'case':case['name'],'phase':'target_oracle','vertices':len(target['adj'])}),flush=True)
        tw=solve(target,2)
        print(json.dumps({'case':case['name'],'source':source,'target':target,'source_yes':sw is not None,'target_witness':tw}),flush=True)
        assert (sw is not None)==(tw is not None)
        if tw is not None:
            variants=[tw,{'order':tw['order'][::-1],'queues':tw['queues']}, {'order':tw['order'],'queues':[1-q for q in tw['queues']]}]
            for w in variants:
                assert witness(target,w,2)
                got=run(candidate,{'source':source,'target_solution':w},True)
                assert witness(source,got,1)
                calls+=1
                print(json.dumps({'case':case['name'],'target_witness':w,'recovered':got}),flush=True)
    print(json.dumps({'result':'pass','instances':len(cases),'recovery_calls':calls}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--candidate',type=Path);args=parser.parse_args()
    cases=json.loads(Path(__file__).with_name('cases.json').read_text())
    if args.self_test:self_test(cases)
    elif args.candidate:check(args.candidate,cases)
    else:parser.error('Choose --self-test or --candidate')
