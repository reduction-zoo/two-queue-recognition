# Four exceptional vertices in a two-apex layout

This general proof received an [independent advance review](../reviews/native/review.md).
Human expert validation remains outstanding. The screening Boolean search in
`research/evidence/two-queue-recognition/check_deletion_lemma.py` found no
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
operations, or O(n log(n+2)) bit operations. The case analysis above proves the desired YES/NO equivalence.
[Executable verification](verification.md) and the independent review provide
separate implementation checks and proof assessment; neither certifies priority.

## Encoding, totality and implementation

The endpoints Q1 and Q2 use finite simple undirected adjacency matrices, including
the empty graph. Malformed source encodings map to a designated malformed target
encoding, outside Q2. Well-formed outputs always satisfy the target restrictions.
For n=0 the output is K2, a YES instance, and recovery returns the empty witness.
For n>0 the implementation labels vertex v in copy c by cn+v, and the two apices
by 5n and 5n+1. It chooses the least-indexed copy avoiding S. No assumption on
which queue is called 0, on apex orientation, or on copy contiguity is used.

The order-selection step takes O(n) word operations. The full executable also
parses the matrix and emits a zero queue index for each source edge. A conservative
bound for either command is O(n^2 log(n+2)) bit operations, excluding whitespace
parsing, which is linear in the actual input-string length. Output matrices use
O(n^2) bits; recovered orders and queue assignments use O(n log(n+2)+m) bits.
All bounds are polynomial in the encoded source and target-witness lengths.
The implementation validates source matrices in O(n^2) word operations. It uses
no randomness, solver calls, retained state, or decisions by a language model.

Q2 is in NP: a vertex permutation and one bit per edge form a polynomial-size
certificate, checked by testing every same-queue edge pair. Together with the
known NP-completeness of Q1, the reduction would establish NP-completeness of Q2.
The theorem proved here is the complete Q1-to-Q2 rule; no stronger graph class
or optimal-copy claim is made.

## Literature assessment

The baseline is Heath and Rosenberg, Laying Out Graphs Using Queues (1992),
https://doi.org/10.1137/0221055. The statement is reiterated on pages 1–2 of
de Col, Klute and Nöllenburg, arXiv:1908.08938v1,
https://arxiv.org/pdf/1908.08938. Their Section 2 treats mixed-layout hardness,
not this pure-two-queue rule. De Col's 2019 thesis, Theorem 3, pages 19–20,
https://repositum.tuwien.at/handle/20.500.12708/13807, proposes the single-copy
map refuted in screening. We explicitly credit that construction as the starting
point; the claimed contribution is the exceptional-vertex lemma and replication
that establish the converse and recovery.

Pupyrev's maintained agenda, https://spupyrev.github.io/layoutproblems.html,
“2-QUEUE GRAPH RECOGNITION,” lists the question as unresolved and notes the
thesis claim's absence from the corresponding paper. Depian et al., ESA 2025,
https://arxiv.org/abs/2508.16319, gives structural and exact algorithms. No result
inspected there implies the present unrestricted reduction.

Additional searches on 2026-09-15: `"queue-number" "universal vertices"`,
`"queue" "five copies" graph recognition`, `"two-queue" "recognition" hardness graph`,
and `"queue layouts" "four vertices" deletion`. No matching construction was
identified. Much search output concerned unrelated queueing systems; that noise
is not evidence of novelty. Coverage includes the sources and queries in the
fixed question, but not every unpublished or poorly indexed result. Correctness,
novelty within that coverage, and significance require separate review.
