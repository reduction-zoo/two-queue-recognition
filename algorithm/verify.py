"""Separate CP-SAT verification; imports neither candidate nor prepared checker."""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
from ortools.sat.python import cp_model


def edges(x):
    a=x['adj'];n=len(a)
    assert set(x)=={'adj'} and all(len(row)==n for row in a)
    assert all(type(a[i][j]) is int and a[i][j] in (0,1) and a[i][j]==a[j][i] and (i!=j or a[i][j]==0) for i in range(n) for j in range(n))
    return [(i,j) for i in range(n) for j in range(i+1,n) if a[i][j]]


def valid(x,w,k):
    es=edges(x);o=w['order'];qs=w['queues']
    if sorted(o)!=list(range(len(x['adj']))) or len(qs)!=len(es) or any(type(q) is not int or q<0 or q>=k for q in qs):return False
    for i,e in enumerate(es):
        for j,f in enumerate(es[:i]):
            if qs[i]!=qs[j] or len(set(e+f))!=4:continue
            labels=sorted([(o.index(v),0) for v in e]+[(o.index(v),1) for v in f])
            if [b for _,b in labels] in ([0,1,1,0],[1,0,0,1]):return False
    return True


def solve(x,k):
    es=edges(x);n=len(x['adj']);model=cp_model.CpModel()
    p=[model.new_int_var(0,n-1,f'p{v}') for v in range(n)]
    model.add_all_different(p)
    if n>1:model.add(p[0]<p[-1])
    color=[model.new_int_var(0,k-1,f'c{i}') for i in range(len(es))]
    if color:model.add(color[0]==0)
    lo=[];hi=[]
    for i,(u,v) in enumerate(es):
        l=model.new_int_var(0,n-1,f'l{i}');r=model.new_int_var(0,n-1,f'r{i}')
        model.add_min_equality(l,[p[u],p[v]]);model.add_max_equality(r,[p[u],p[v]])
        lo.append(l);hi.append(r)
    for i,e in enumerate(es):
        for j,f in enumerate(es[:i]):
            if len(set(e+f))!=4:continue
            different=model.new_bool_var(f'd{i}_{j}')
            model.add(color[i]!=color[j]).only_enforce_if(different)
            model.add(color[i]==color[j]).only_enforce_if(~different)
            for outer,inner in [(i,j),(j,i)]:
                left=model.new_bool_var(f'l{outer}_{inner}');right=model.new_bool_var(f'r{outer}_{inner}')
                model.add(lo[outer]<lo[inner]).only_enforce_if(left)
                model.add(lo[outer]>=lo[inner]).only_enforce_if(~left)
                model.add(hi[inner]<hi[outer]).only_enforce_if(right)
                model.add(hi[inner]>=hi[outer]).only_enforce_if(~right)
                model.add_bool_or([~left,~right,different])
    solver=cp_model.CpSolver();status=solver.solve(model)
    if status==cp_model.INFEASIBLE:return None
    if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):raise RuntimeError(solver.status_name(status))
    w={'order':sorted(range(n),key=lambda v:solver.value(p[v])),'queues':[solver.value(c) for c in color]}
    assert valid(x,w,k)
    return w


def call(candidate,x,extract=False):
    return json.loads(subprocess.run([sys.executable,str(candidate)]+(['--extract'] if extract else []),input=json.dumps(x),text=True,capture_output=True,check=True).stdout)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True);args=parser.parse_args()
    specs=[('star',5,[(0,i) for i in range(1,5)]),('cycle',5,[(i,(i+1)%5) for i in range(5)]),('matching',4,[(0,1),(2,3)]),('complete-five',5,list(itertools.combinations(range(5),2))),('counterexample',6,[(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,5),(3,5)])]
    count=0
    for name,n,es in specs:
        a=[[0]*n for _ in range(n)]
        for u,v in es:a[u][v]=a[v][u]=1
        source={'adj':a}
        yes=any(valid(source,{'order':list(o),'queues':[0]*len(es)},1) for o in itertools.permutations(range(n)))
        assert yes==(solve(source,1) is not None)
        target=call(args.candidate,source);edges(target)
        print(json.dumps({'case':name,'phase':'target_oracle','vertices':len(target['adj'])}),flush=True)
        if name=='counterexample':
            vertices=list(range(12))+[len(target['adj'])-2,len(target['adj'])-1]
            induced={'adj':[[target['adj'][i][j] for j in vertices] for i in vertices]}
            assert solve(induced,2) is None
            print(json.dumps({'case':name,'no_certificate_vertices':vertices,'induced':induced}),flush=True)
            w=None
        else:w=solve(target,2)
        print(json.dumps({'case':name,'source':source,'target':target,'source_yes':yes,'target_witness':w}),flush=True)
        assert yes==(w is not None)
        if w is not None:
            for o in [w['order'],w['order'][::-1]]:
                tw={'order':o,'queues':w['queues']};assert valid(target,tw,2)
                recovered=call(args.candidate,{'source':source,'target_solution':tw},True)
                assert valid(source,recovered,1);count+=1
                print(json.dumps({'case':name,'target_witness':tw,'recovered':recovered}),flush=True)
    for malformed in [{},{'adj':[[1]]},{'adj':[[0,1],[0,0]]}]:
        assert call(args.candidate,malformed)=={'invalid':True}
    raw=subprocess.run([sys.executable,str(args.candidate)],input='not JSON',text=True,capture_output=True,check=True)
    assert json.loads(raw.stdout)=={'invalid':True}
    for data in [b'\xff', b'1'*5000, b'['*2000+b']'*2000]:
        result=subprocess.run([sys.executable,str(args.candidate)],input=data,capture_output=True,check=True)
        assert json.loads(result.stdout)=={'invalid':True}
    print(json.dumps({'result':'pass','instances':len(specs),'recovery_calls':count,'malformed_sources':7}),flush=True)
