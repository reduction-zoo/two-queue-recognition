# Four exceptional vertices in a two-apex layout

This is a candidate general proof from screening, not an independently reviewed
result. The bounded Boolean search in `check_deletion_lemma.py` found no
counterexample for 1–8 original vertices and all 164 apex-position pairs.

Let H = K_2 join X have a two-queue layout, with apices a < b. A three-edge
rainbow cannot occur: its three pairwise nested edges would need three queues.
For nonempty X, let S contain its first and last vertices, its last vertex
before a if one exists, and its first vertex after b if one exists. Then
|S| <= 4. Claim: the induced order on X minus S is a one-queue order.

Suppose instead that edges uv and xy satisfy u < x < y < v with all four
endpoints outside S. Let l and r be the first and last original vertices.
Thus l < u and v < r.

If v < b, edges lb, uv, xy form a three-rainbow. If a < u, edges ar, uv,
xy do so. We may therefore assume u < a < b < v. There are six remaining
placements of x,y relative to a,b:

1. x < y < a: edges lb, ua, xy form a three-rainbow.
2. b < x < y: edges ar, bv, xy form a three-rainbow.
3. a < x < y < b: edges uv, ab, xy form a three-rainbow.
4. x < a < b < y: edges uv, xy, ab form a three-rainbow.
5. x < a < y < b: x is not the last original vertex before a. For that last
   vertex z, x < z < a < y; edges uv, xy, za form a three-rainbow.
6. a < x < b < y: y is not the first original vertex after b. For that first
   vertex z, x < b < z < y; edges uv, xy, bz form a three-rainbow.

Every listed edge exists and every displayed rainbow uses six distinct
vertices. These cases exhaust the relative orders, proving the claim.

## Consequence for a reduction

Take X as five disjoint copies of G and set f(G) = K_2 join X. A one-queue
layout of G extends by concatenating five copies between a and b. Put all
original edges in one queue and all apex edges in the other; neither queue
has nesting.

Conversely, compute S in any supplied two-queue layout. At most four copies
meet S, so at least one copy avoids S. Its induced order has no nested pair
by the claim. Choose the least-indexed such copy and translate its labels
back to G. This deterministic recovery uses no source decision oracle.
For the empty source, return the empty order.

There are 5n+2 vertices and 5m+10n+1 edges. Matrix construction takes O(n^2)
time and bits. Recovery scans the vertex order and copy labels in O(n) word
operations, or O(n log(n+2)) bit operations. This proves the desired
YES/NO equivalence conditional only on the case analysis above, which must
still receive independent review and executable verification.
