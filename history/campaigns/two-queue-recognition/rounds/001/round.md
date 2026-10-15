# Round 001 — Five-copy amplification

## Plan

Use the four-exceptional-vertex argument developed during screening to construct
Q1 <= Q2 with recovery from every target layout. One construction template:
join K2 to five disjoint source copies. Scope: the seven prepared source graphs,
additional independently implemented small-instance checks, the general case
analysis, and targeted novelty searches. Stop construction on any mismatch;
repair an implementation defect in this round and record it. A different
mathematical mechanism starts a new round.

The six-vertex counterexample in the shared experience entry
[two-apex-queue-layout-false-positive](../../../../research/experience/two-apex-queue-layout-false-positive.md)
rejects a single copy and is included in the unchanged prepared test set.
The changed premise is replication: at most four exceptional vertices cannot
hit all five copies. The first check is to solve the actual generated targets
and recover source witnesses from solver-selected orders and their symmetries.

Preparation passed before implementing the complete rule. Success requires
both executable maps, a complete proof, passing independent programs, and
independent-author review. Initial prospects: medium, uncalibrated; the finite
screening supports a precise proof obligation but does not verify it generally.

## Evidence and diagnosis

**Result: complete rule, advance review, inspected manuscript.** One construction
was implemented in this round. Screening had previously investigated the known
single-copy map and a two-copy repair before deriving the five-copy mechanism;
those preliminary investigations are not hidden in the formal round count.

| Final check | Source instances | Recovery calls | Solver queries |
|---|---:|---:|---:|
| Prepared Z3 suite | 7 | 15 | 14 |
| Separate CP-SAT suite | 5 | 6 | 10 |
| Native independent review | 76 | 358 | 0; standard-library enumeration |

The two main suites cover eleven distinct source graphs. Counts above exclude
superseded runs; their outputs remain preserved. The reviewer additionally
checked 16,962 positional hypotheses and two sets of 720 orders. See
[review.md](../../reviews/native/review.md) and its raw check results. No blocking
mathematical revision was requested. The full-round elapsed time and token total
were not recorded; no numerical completion probability is inferred from tests.

Commands from the repository root are in verification.md and the review. Final
main logs are `prepared-after-input-fix.jsonl` and `verification.jsonl`.
One candidate parser repair, one harness-coverage repair, and one change of
verification certificate are described below. None changed the five-copy rule.

### Checks and implementation repair

The prepared Z3 suite passed seven instances and fifteen recovery calls, including
both NO sources. A boundary audit found that malformed UTF-8, excessively large
integer tokens, and excessive JSON nesting could fail during parsing before
reaching the designated malformed output. The parser now maps these malformed
sources explicitly to the fixed target nonmember. The previous implementation is
saved as `algorithm-before-malformed-input-fix.py`; the same prepared suite passed
again in `prepared-after-input-fix.jsonl`. This is one implementation repair,
not a new construction or round.

The separate CP-SAT encoding completed the star, cycle, matching and K5 cases.
For the six-vertex NO source, an exact 14-vertex induced-subgraph infeasibility
certificate replaced the still-running full-target query. The interruption,
UNKNOWN result and prior evidence are preserved. This changes the verification
certificate, not the reduction or the source expectations. No timeout was used.
The final verifier passed with the amended certificate and input-boundary
checks; it imports neither the candidate nor the prepared checker.

### Additional literature checks

2026-09-15 queries: `"recognizing" "queue" "NP-complete" graph k`,
`"recognising" "2-queue"`, `"queue-number at most two" complexity`, and
`"queue number" "NP-complete" fixed`. The introduction of *Queue Layouts of
Hypercubes*, https://users.fmf.uni-lj.si/skreko/Old/MyPapers/01153.pdf, repeats
hardness “even for k=1,” citing Heath and Rosenberg. This wording does not prove
hardness for every fixed k. Dagstuhl Seminar 23162, Section 4.8,
https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume13/issue04/23162/DagRep.13.4.58/DagRep.13.4.58.pdf,
also gives the one-page baseline and fixed-order polynomial algorithm. No
matching five-copy or deletion-lemma result was identified in these checks.

A testing-foundation audit also added two failing subprocess fixtures to the
self-test. Both the wrong forward output and the wrong recovery are rejected
by the actual harness. The revised self-test passes in `harness-self-test.jsonl`.
This is one harness-coverage repair; source expectations and all oracle
constraints remain unchanged. Passing candidate evidence therefore remains
applicable to those unchanged checks.

### Diagnosis and experience extraction

The single-copy failure showed that apex positions cannot be assumed extreme.
The general deletion lemma instead bounds exceptional original vertices in every
order. Replication then guarantees an intact copy and a deterministic extractor.
This causal account is supported by the reviewed six-case proof and the earlier
counterexample; test pass rates alone would not support it.

**Experience extraction:** created
[four-exceptional-vertices-queue-amplification](../../../../research/experience/four-exceptional-vertices-queue-amplification.md)
and updated
[two-apex-queue-layout-false-positive](../../../../research/experience/two-apex-queue-layout-false-positive.md)
with its independent confirmation and use in this round. No extraction is pending.
The second entry was created during screening, so the entire selection-and-research
task added two distinct experience files; this campaign closure created one and
updated one.

The reviewer identified the July 2026 outerplanar-Q1 paper,
https://arxiv.org/html/2607.24297v1, Theorem 1. Its stronger source hardness does
not establish Q2 hardness. It is included in the manuscript's related work.
The two-apex construction is explicitly credited to de Col; priority and human
expert validation remain outstanding.

## Next action

Stop discovery after one of forty allocated rounds. The complete rule has a
five-page English Typst manuscript with two vector figures, and every final
page was visually inspected. The general proof, tests and advance review justify
expert evaluation; additional rounds are not needed to fill the allocation.
Thirty-nine rounds remain unused. No publication or production integration was
performed. No research process remains running.
