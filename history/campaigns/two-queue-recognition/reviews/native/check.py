"""Independent positional and subprocess checks; stdlib only."""
import itertools as it
import json
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / 'work/algorithm.py'
counts = {'positional_hypotheses': 0, 'forward_graphs': 0, 'recovery_calls': 0,
          'source_no_graphs': 0, 'malformed_inputs': 0, 'complete_six_orders': 0,
          'counterexample_source_orders': 0, 'sampled_target_orders': 0}


def nested(e, f):
    a, b = e
    c, d = f
    return a < c < d < b or c < a < b < d


def edges(matrix):
    return [(i, j) for i in range(len(matrix)) for j in range(i+1, len(matrix)) if matrix[i][j]]


def color(matrix, order, k):
    pos = {v: i for i, v in enumerate(order)}
    es = edges(matrix)
    intervals = [tuple(sorted((pos[a], pos[b]))) for a, b in es]
    # Longest strict containment chain, computed from shortest intervals upward.
    depth = [0]*len(es)
    for i in sorted(range(len(es)), key=lambda i: intervals[i][1]-intervals[i][0]):
        a, b = intervals[i]
        depth[i] = 1+max((depth[j] for j, (c, d) in enumerate(intervals) if a < c < d < b), default=0)
    return [x-1 for x in depth] if max(depth, default=0) <= k else None


def valid(matrix, witness, k):
    order, queues = witness['order'], witness['queues']
    assert sorted(order) == list(range(len(matrix)))
    es = edges(matrix)
    assert len(queues) == len(es) and all(type(q) is int and 0 <= q < k for q in queues)
    pos = {v: i for i, v in enumerate(order)}
    ints = [tuple(sorted((pos[a], pos[b]))) for a, b in es]
    assert all(queues[i] != queues[j] or not nested(ints[i], ints[j])
               for i, j in it.combinations(range(len(es)), 2))


def run(payload, extract=False):
    result = subprocess.run([sys.executable, str(CANDIDATE)]+(['--extract'] if extract else []),
                            input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def recover(matrix, target, order):
    q = color(target, order, 2)
    if q is None:
        return False
    witness = {'order': list(order), 'queues': q}
    valid(target, witness, 2)
    result = run({'source': {'adj': matrix}, 'target_solution': witness}, True)
    valid(matrix, result, 1)
    counts['recovery_calls'] += 1
    return True


# Test each possible bad residual pair with only mandatory apex and pair edges.
# Every larger graph containing that pair contains this same obstruction.
for n in range(4, 13):
    for a, b in it.combinations(range(n+2), 2):
        xs = [v for v in range(n+2) if v not in (a, b)]
        exceptional = {xs[0], xs[-1]}
        if xs[0] < a:
            exceptional.add(max(v for v in xs if v < a))
        if xs[-1] > b:
            exceptional.add(min(v for v in xs if v > b))
        mandatory = {tuple(sorted((v, apex))) for v in xs for apex in (a, b)} | {(a, b)}
        for u, x, y, v in it.combinations([v for v in xs if v not in exceptional], 4):
            es = mandatory | {(u, v), (x, y)}
            assert any(p < r < t < w < s < q for p, q in es for r, s in es for t, w in es)
            counts['positional_hypotheses'] += 1

# All labelled source graphs through four vertices; both source decisions.
for n in range(5):
    pairs = list(it.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        matrix = [[0]*n for _ in range(n)]
        for bit, (i, j) in enumerate(pairs):
            matrix[i][j] = matrix[j][i] = (mask >> bit) & 1
        target = run({'adj': matrix})['adj']
        N = 5*n+2
        assert len(target) == N
        for i in range(N):
            assert len(target[i]) == N
            for j in range(N):
                expected = int(i != j and (i >= 5*n or j >= 5*n or
                               (n > 0 and i//n == j//n and matrix[i%n][j%n])))
                assert type(target[i][j]) is int and target[i][j] == expected
        counts['forward_graphs'] += 1
        source_order = next((p for p in it.permutations(range(n)) if color(matrix, p, 1) is not None), None)
        if source_order is None:
            counts['source_no_graphs'] += 1
            # Here the only NO graph is K4; its actual target contains K6.
            assert n == 4 and len(edges(matrix)) == 6
            selected = list(range(4))+[20,21]
            sub = [[target[i][j] for j in selected] for i in selected]
            for order in it.permutations(range(6)):
                assert color(sub, order, 2) is None
                counts['complete_six_orders'] += 1
        else:
            order = [5*n]+[c*n+v for c in range(5) for v in source_order]+[5*n+1]
            assert recover(matrix, target, order)
            assert recover(matrix, target, list(reversed(order)))

# Freely sampled orders on the actual target, independently colored.
# Fixed seed makes this a finite reproducible probe, not algorithmic randomness.
rng = random.Random(319)
for matrix, samples in [([[0]], 100), ([[0,1],[1,0]], 2000)]:
    target = run({'adj':matrix})['adj']
    for _ in range(samples):
        order = list(range(len(target))); rng.shuffle(order)
        counts['sampled_target_orders'] += 1
        if recover(matrix, target, order):
            # Different valid queue names must recover too.
            witness = {'order': order, 'queues': [1-q for q in color(target, order, 2)]}
            result = run({'source': {'adj':matrix}, 'target_solution':witness}, True)
            valid(matrix, result, 1)
            counts['recovery_calls'] += 1

bad = [b'', b'{', b'null', b'[]', b'{"adj":[[false]]}', b'{"adj":[[0.0]]}',
       b'{"adj":[[1]]}', b'{"adj":[[0,1],[0,0]]}', b'{"adj":[[]]}', b'{"adj":[],"x":0}',
       b'\xff', b'['*2000+b']'*2000, b'{"adj":[['+b'1'*5000+b']]}']
for payload in bad:
    p = subprocess.run([sys.executable,str(CANDIDATE)],input=payload,capture_output=True,check=True)
    assert json.loads(p.stdout) == {'invalid': True}
    counts['malformed_inputs'] += 1

# Reconstruct the thesis counterexample without importing its checker or data.
matrix = [[0]*6 for _ in range(6)]
for i,j in [(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,5),(3,5)]:
    matrix[i][j] = matrix[j][i] = 1
for order in it.permutations(range(6)):
    assert color(matrix, order, 1) is None
    counts['counterexample_source_orders'] += 1
joined = [[int(i != j and (i >= 6 or j >= 6 or matrix[i][j])) for j in range(8)] for i in range(8)]
order = [4,0,7,6,2,1,3,5]
witness = {'order':order,'queues':color(joined,order,2)}
assert witness['queues'] is not None
valid(joined,witness,2)
print(json.dumps({'result':'pass', **counts, 'single_copy_counterexample_witness':witness},indent=2))
