# Executable verification

The prepared checker uses Z3 Boolean total-order and queue-color constraints.
The separate verifier uses CP-SAT integer positions, all-different constraints,
interval endpoints and reified nesting constraints. It imports neither check.py
nor algorithm.py. Both invoke the actual candidate in subprocesses and validate
recovered source layouts independently.

The current candidate passed the prepared suite after its malformed-input parser
repair: seven source instances and fifteen recovery calls. See
[prepared-after-input-fix.jsonl](../history/campaigns/two-queue-recognition/rounds/001/prepared-after-input-fix.jsonl).
The earlier run remains preserved, rather than being counted as additional
instance coverage.

The CP-SAT suite adds a star, cycle, matching and K5, and independently rechecks
the six-vertex counterexample. The counterexample's full target is certified NO
by exact infeasibility of an induced 14-vertex subgraph of the actual output.
This is valid because restricting a queue layout preserves it. The certificate
uses no candidate deletion lemma. The exploratory full-target solve was interrupted
only after this conclusive subgraph result; its UNKNOWN status is not treated as
NO. See the [certificate](../history/campaigns/two-queue-recognition/rounds/001/induced-no-certificate.json) and
[interruption record](../history/campaigns/two-queue-recognition/rounds/001/full-target-interruption.txt).

Final CP-SAT run passed five source instances, six recovery calls and seven
malformed-source cases. Results are in
[verification.jsonl](../history/campaigns/two-queue-recognition/rounds/001/verification.jsonl). Its full command is
`python3 campaigns/two-queue-recognition/work/verify.py --candidate campaigns/two-queue-recognition/work/algorithm.py`.
The prepared command replaces verify.py by check.py in the same invocation.
No timeout is imposed. The finite source order is at most six; output order is
at most 32. Exhaustive source permutations support the expected answers; neither
finite test coverage nor solver agreement replaces the general proof.
