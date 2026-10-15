"""Check the fixed counterexample using only the Python standard library."""
from itertools import combinations, permutations
import json


def nests(order, e, f):
    a, b = sorted(order.index(v) for v in e)
    c, d = sorted(order.index(v) for v in f)
    return a < c < d < b or c < a < b < d


edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 5), (3, 5)]
orders = list(permutations(range(6)))
assert len(orders) == 720
assert all(any(nests(o, e, f) for e, f in combinations(edges, 2)) for o in orders)

target = edges + [(v, a) for v in range(6) for a in (6, 7)] + [(6, 7)]
order = [4, 0, 7, 6, 2, 1, 3, 5]
assert sorted(order) == list(range(8))
# Color the nesting conflict graph directly; do not use the probe's rainbow model.
colors = {}
for edge in target:
    if edge in colors:
        continue
    colors[edge] = 0
    pending = [edge]
    while pending:
        e = pending.pop()
        for f in target:
            if not nests(order, e, f):
                continue
            if f in colors:
                assert colors[e] != colors[f]
            else:
                colors[f] = 1 - colors[e]
                pending.append(f)
assert len(colors) == 21
for e, f in combinations(target, 2):
    assert colors[e] != colors[f] or not nests(order, e, f)
print(json.dumps({"source_orders_rejected": len(orders), "target_order": order,
                  "queues": [[e for e in target if colors[e] == q] for q in (0, 1)]}, indent=2))
