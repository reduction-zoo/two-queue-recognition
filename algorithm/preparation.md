# Prepared testing foundation

The seven source cases cover the empty graph, an isolated vertex, an edge, a
path, a triangle, K4, and the six-vertex counterexample to the thesis's map.
Source answers were established by exhausting all permutations, independently
of the reduction. Both YES and NO cases are present.

The Z3 oracle models a total order with pairwise precedence Booleans and
forbids the two directed orientations of each three-cycle. A tournament without
a directed triangle is transitive, so every model defines a total order.
Every pair of vertex-disjoint edges receives the implication that nesting
requires different queue bits. For Q1 all bits are zero. For Q2 each edge has
a Boolean bit. Reversal and global queue renaming justify the two symmetry
constraints. Models correspond exactly to legal layouts. A separate direct
position-based predicate checks every returned witness. Only UNSAT means NO;
unknown and execution errors fail explicitly. No timeouts or solver tuning are used.

The self-test compares source decisions with exhaustive permutations, checks
Q2 on the empty graph, K5 and K6, and rejects malformed matrices, invalid
permutations, invalid queue labels and a false source witness. It also detects
a deliberate NO-to-YES decision mismatch. These checks exercise predicates
without executing a candidate construction.

Command: `python3 campaigns/two-queue-recognition/work/check.py --self-test`.
The [raw result](../history/campaigns/two-queue-recognition/work/evidence/preparation/self-test.json) records the solver version
and counts. The self-test passed. This finite coverage does not establish a
reduction theorem; candidate outputs still require independent solving.

A later harness audit added two deliberately incorrect subprocess fixtures:
a NO-to-YES forward output and an invalid recovered layout for a YES source.
Both are rejected by the actual harness, not only its predicates. The unchanged
oracle self-tests also passed in
[the harness self-test log](../history/campaigns/two-queue-recognition/rounds/001/harness-self-test.jsonl).
The prior checker is preserved in the round. This repair adds fault injection;
it changes no oracle constraints, source expectations or candidate checks.
