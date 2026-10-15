# Layout rule contract

A graph is JSON `{"adj": A}`, where A is a square symmetric 0/1 integer matrix
with zero diagonal. Vertices are 0 through n-1; the empty matrix is allowed.
Edges are enumerated lexicographically as pairs i < j with A[i][j] = 1.
A layout witness is `{"order": [...], "queues": [...]}`: a vertex permutation
and one queue index per edge. Source indices are 0; target indices are 0 or 1.
Same-queue edges must not be strictly nested. Shared endpoints do not nest.
Malformed encodings are outside either decision language.

`python3 algorithm.py` reads one source and writes one target. Malformed source
encodings map to `{"invalid": true}`, a fixed nonmember of the target language.
`python3 algorithm.py --extract` reads `{"source": ..., "target_solution": ...}`
and writes a source witness, assuming the supplied witness is valid for the
constructed target. The two commands run in fresh processes. No solver belongs
to the candidate algorithm.

The testing harness independently validates target matrices, decides both graph
languages, obtains target layouts, invokes recovery, and checks its result.
The mathematical encoding size is the length of a standard matrix representation;
the JSON representation changes polynomial bounds only by a constant factor for
matrix entries and logarithmic factors for labels.
