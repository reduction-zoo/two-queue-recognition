"""Five-copy Karp map and recovery from an arbitrary two-queue layout."""
import json
import sys


def legal(source):
    if not isinstance(source,dict) or set(source)!={'adj'} or not isinstance(source['adj'],list):return False
    a=source['adj'];n=len(a)
    if any(not isinstance(row,list) or len(row)!=n for row in a):return False
    return all(type(a[i][j]) is int and a[i][j] in (0,1) and a[i][j]==a[j][i] and (i!=j or a[i][j]==0) for i in range(n) for j in range(n))


def forward(source):
    if not legal(source):return {'invalid':True}
    a=source['adj'];n=len(a);size=5*n+2
    b=[[0]*size for _ in range(size)]
    for copy in range(5):
        for u in range(n):
            for v in range(n):b[copy*n+u][copy*n+v]=a[u][v]
    for apex in (5*n,5*n+1):
        for v in range(size):
            if v!=apex:b[apex][v]=b[v][apex]=1
    return {'adj':b}


def recover(source,solution):
    if not legal(source):raise ValueError('Recovery requires a well-formed source')
    n=len(source['adj'])
    if n==0:return {'order':[],'queues':[]}
    order=solution['order'];positions={v:i for i,v in enumerate(order)}
    a,b=sorted((positions[5*n],positions[5*n+1]))
    original=[v for v in order if v<5*n]
    exceptional={original[0],original[-1]}
    left=[v for v in order[:a] if v<5*n]
    right=[v for v in order[b+1:] if v<5*n]
    if left:exceptional.add(left[-1])
    if right:exceptional.add(right[0])
    hit={v//n for v in exceptional}
    copy=next(c for c in range(5) if c not in hit)
    recovered=[v%n for v in original if v//n==copy]
    m=sum(source['adj'][u][v] for u in range(n) for v in range(u+1,n))
    return {'order':recovered,'queues':[0]*m}


if __name__=='__main__':
    try:payload=json.load(sys.stdin)
    except json.JSONDecodeError:
        if sys.argv[1:]:raise
        print(json.dumps({'invalid':True}))
    else:
        if sys.argv[1:]==['--extract']:result=recover(payload['source'],payload['target_solution'])
        elif not sys.argv[1:]:result=forward(payload)
        else:raise ValueError('Expected no argument or --extract')
        print(json.dumps(result))
