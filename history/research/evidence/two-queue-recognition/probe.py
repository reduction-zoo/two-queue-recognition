import itertools,json,sys
import networkx as nx
import z3


def valid(g,order,k):
    position={v:i for i,v in enumerate(order)}
    intervals=sorted((min(position[u],position[v]),max(position[u],position[v])) for u,v in g.edges())
    height={}
    for a,b in sorted(intervals,key=lambda e:e[1]-e[0]):
        height[a,b]=1+max((height[c,d] for c,d in height if a<c<d<b),default=0)
    return max(height.values(),default=0)<=k


def solve(g,k):
    n=len(g);p=[z3.Int(f'p{i}') for i in range(n)];s=z3.Solver();s.add(z3.Distinct(p),*[z3.And(x>=0,x<n) for x in p]);s.add(p[0]<p[-1]) if n>1 else None
    edges=list(g.edges());intervals=[(z3.If(p[u]<p[v],p[u],p[v]),z3.If(p[u]<p[v],p[v],p[u])) for u,v in edges]
    for ids in itertools.combinations(range(len(edges)),k+1):
        if len({v for j in ids for v in edges[j]})!=2*(k+1):continue
        comparable=[]
        for i,j in itertools.combinations(ids,2):
            a,b=intervals[i];c,d=intervals[j];comparable.append(z3.Or(z3.And(a<c,d<b),z3.And(c<a,b<d)))
        s.add(z3.Not(z3.And(comparable)))
    status=s.check();assert status in (z3.sat,z3.unsat)
    if status==z3.unsat:return None
    m=s.model();order=sorted(range(n),key=lambda i:m.eval(p[i]).as_long());assert valid(g,order,k)
    return order

if __name__ == "__main__":
    records=[]
    for g in nx.graph_atlas_g():
        if not (int(sys.argv[1]) if len(sys.argv)>1 else 1)<=len(g)<=(int(sys.argv[2]) if len(sys.argv)>2 else 5):continue
        one=next((list(o) for o in itertools.permutations(g) if valid(g,o,1)),None)
        assert (solve(g,1) is not None)==(one is not None)
        copies=int(sys.argv[3]) if len(sys.argv)>3 else 1
        h=nx.disjoint_union_all([g]*copies);n=len(h);h.add_nodes_from([n,n+1]);h.add_edges_from((v,u) for v in range(n) for u in (n,n+1));h.add_edge(n,n+1)
        two=solve(h,2);rec={'n':len(g),'copies':copies,'edges':list(g.edges()),'one_queue':one,'joined_two_queue':two,'equivalent':(one is not None)==(two is not None)};records.append(rec)
        if not rec['equivalent']:break
    print(json.dumps(records,indent=2))
