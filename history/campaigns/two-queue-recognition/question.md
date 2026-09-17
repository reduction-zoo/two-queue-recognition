---
status: ready-for-attempt
openness: supported-within-coverage
difficulty: moderate
importance: moderate
tags: [graph-layouts, queues, recognition, NP-hardness, counterexample]
last-literature-check: 2026-09-15
---

# 1-queue recognition to 2-queue recognition

**Admitted for a bounded attempt.** The elementary two-apex construction in
de Col's 2019 thesis fails on a six-vertex graph. A new four-exceptional-vertex
argument supports a five-copy construction with direct witness recovery.
This is a non-cut candidate; no campaign or successful reduction is claimed.

## Exact question

Let Q_k contain adjacency-matrix encodings of finite simple undirected graphs
that have a vertex order and an assignment of every edge to one of k queues.
Two edges in the same queue must not have four distinct endpoints ordered
u < x < y < v, with edges uv and xy. Shared endpoints do not constitute nesting.
Malformed encodings are outside Q_k. The empty graph belongs to both languages.

Construct a deterministic polynomial-time Karp map f from Q_1 to Q_2 and a
polynomial-time algorithm recovering a Q_1 layout of G from **any** valid
Q_2 layout of f(G). Every well-formed source, including a NO instance, must
produce a simple graph. Malformed sources may map to a fixed malformed target.
The final rule must prove both decision directions, recovery, and explicit
worst-case time and bit-size bounds. A counterexample to one attempted map is
useful evidence but does not meet this positive target.

The selected hypothesis is f(G) = K_2 join five disjoint copies of G. It produces
5n+2 vertices and 5m+10n+1 edges. With matrix encodings, construction takes
O(n^2) time and bits. A target layout has O(n log(n+2)+m) bits. The extractor selects a copy avoiding four exceptional positions and reads its
induced order in O(n) word operations. Source solving by exhaustive
permutations is a testing oracle, not an acceptable extractor.

## Known results and openness

Heath and Rosenberg's *Laying Out Graphs Using Queues* (1992,
[DOI](https://doi.org/10.1137/0221055)) established NP-completeness for Q_1.
The 2019 paper below states this baseline on pages 1–2. Inclusion Q_1 subset Q_2
alone gives no reduction preserving NO instances.

De Col's [2019 thesis](https://repositum.tuwien.at/handle/20.500.12708/13807),
Theorem 3, printed pages 19–20, claims hardness for Q_2 using K_2 join G.
The counterexample below refutes its proposed equivalence. It does not refute
the theorem's NP-hardness conclusion. The related paper by de Col, Klute and
Nöllenburg, [arXiv:1908.08938v1](https://arxiv.org/pdf/1908.08938), Section 2,
Theorems 1–2, proves mixed-layout results; it does not supply that pure-two-queue
reduction. Fixed-order hardness for mixed pages cannot transfer to Q_2:
for a fixed order the nesting relation gives a polynomial queue assignment.

Pupyrev's author-maintained [open-problem agenda](https://spupyrev.github.io/layoutproblems.html),
“2-QUEUE GRAPH RECOGNITION,” lists the complexity question as unresolved and
explicitly distinguishes the thesis claim. Depian et al.'s
[ESA 2025 paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.15/LIPIcs.ESA.2025.15.pdf)
studies exact and structurally parameterized algorithms; its introduction
reiterates the one-queue hardness baseline. These algorithms do not yield the
requested unrestricted reduction.

Searches on 2026-09-15 used Web and arXiv, including:

- `"2-queue" "recognition" NP-complete`
- `"two-queue" "NP-hard" graph`
- `"2-queue" recognition 2026`
- `"de Col" thesis "2019" layouts`
- `"Algorithms and drawings for Mixed linear layouts of graphs"`
- `"de Col" "queue" "counterexample"`
- `"Mixed Linear Layouts: Complexity, Heuristics" arxiv`
- `"queue number" "join" "recognition" graph`

The thesis PDF was retrieved from its university repository and read locally
with pdftotext after Web PDF retrieval failed. The search covered the original
claim, its conference-paper counterpart, the 2025 algorithmic work, and current
recognition/queue-number terminology. No replacement proof or published account
of this counterexample was identified. The counterexample's novelty is not
established, and unpublished results or missed follow-ups remain outside coverage.

## Initial investigation

The [probe](../../research/evidence/two-queue-recognition/probe.py) uses Z3 to prohibit
(k+1)-edge rainbows. For a fixed vertex order, nesting is a strict partial order;
its height equals the required queue count. A direct interval-containment check
validates each returned order. Source decisions are also compared with all vertex
permutations. No wall-clock cutoff is imposed; graph sizes bound each experiment.

Commands from the repository root:

```sh
python3 research/evidence/two-queue-recognition/probe.py
python3 research/evidence/two-queue-recognition/probe.py 6 6
python3 research/evidence/two-queue-recognition/probe.py 1 5 2
python3 research/evidence/two-queue-recognition/check_counterexample.py
```

All 52 non-isomorphic graphs with one through five vertices passed the single-copy
map. The six-vertex scan stopped at its 91st graph, with edges

    01, 02, 04, 13, 15, 23, 25, 35.

All 720 source orders contain a nested edge pair. Nevertheless, the joined graph
has a two-queue layout with order

    4, 0, 7, 6, 2, 1, 3, 5,

where 6 and 7 are the new adjacent universal vertices. The separate
[standard-library checker](../../research/evidence/two-queue-recognition/check_counterexample.py)
imports neither the probe nor Z3. It exhausts the source orders, two-colors the
nesting-conflict graph of this target order, and checks every same-queue pair.
Its [output](../../research/evidence/two-queue-recognition/counterexample-check.json)
contains the complete two-queue assignment. This is a checkable disproof of the
single-copy map, not finite evidence for its validity.

The thesis's converse does not exhaust apex placements. In particular, both
apices can lie on the same side of a chosen nested pair, without their connecting
edge enclosing it. The concrete layout above invalidates the claimed conclusion
regardless of which local gap is repaired.

A follow-up [two-copy check](../../research/evidence/two-queue-recognition/two-copy-probe.json)
returned UNSAT for the joined union of two copies of this counterexample.
The [two-copy small-graph scan](../../research/evidence/two-queue-recognition/two-copy-small.json)
also passed all 52 graphs with one through five vertices. Neither result
establishes the converse. The two-copy YES direction holds
generally: concatenate source layouts between the two apices, put source edges
in one queue and all apex edges in the other. The required NO direction is open:
prove that every target layout yields a one-queue order for at least one source
copy, possibly after a polynomially computable rearrangement. The copies must
not be assumed consecutive in an arbitrary target witness.

Existing experience entries concern cut gadgets and do not justify this ordering
argument. No cut construction is being reused. Next bounded task: test the
copy mechanism against small NO graphs and seek a structural lemma controlling
interleaving; stop this route on a new counterexample unless it suggests a
specific change of premise.

## Assessment and screening

| Dimension | Assessment | Reason |
|---|---|---|
| Difficulty | Moderate, provisional | A complete candidate case analysis supports five-copy amplification; independent proof review and executable recovery checks remain. |
| Importance | Moderate | A successful map would establish NP-completeness of the first unresolved fixed queue threshold, rather than add only a library edge. |

| Gate | Decision | Evidence |
|---|---|---|
| 1. Precise question | Pass | Q_1 to Q_2, total Karp map and universal witness recovery. |
| 2. Known results | Pass | Mixed-layout and fixed-order theorems do not imply the target; the thesis map is refuted. |
| 3. Supported openness | Pass within recorded coverage | Current author agenda and targeted primary-source checks; coverage is not exhaustive. |
| 4. Significance | Pass | A new NP-completeness boundary for free-order queue layouts. |
| 5. Proof route | Pass | A four-exceptional-vertex lemma gives a five-copy converse and deterministic extractor. |
| 6. Admission exercise | Pass | Candidate general argument plus 164 bounded Boolean checks of the deletion lemma; no counterexample. |

## Research history and campaign handoff

2026-09-15: investigated as a different family after the user excluded all cut
variants. Refuted the thesis's single-copy map and tested an initial repair.
Allocate the user's 40 rounds to the five-copy campaign; these initial experiments
are screening work, not completed campaign rounds. A campaign must establish
independent injected-instance oracles before proposing its complete rule, then
verify decision equivalence and recovered witnesses separately. A changed theorem
requires a new campaign. No production integration or publication is authorized.

### Screening follow-up: five-copy amplification

The [candidate deletion lemma](../../research/evidence/two-queue-recognition/deletion-lemma.md)
shows that deleting at most four positional vertices from the original graph
leaves a one-queue order in any two-apex two-queue layout. Five disjoint copies
therefore leave an intact copy for recovery. The [Boolean probe](../../research/evidence/two-queue-recognition/check_deletion_lemma.py)
checked all 164 apex placements for 1–8 original vertices, with graph edges
as variables; all checks were UNSAT. See [raw results](../../research/evidence/two-queue-recognition/deletion-lemma.json).
This is finite support for the written argument, not a substitute for its review.
The earlier two-copy route is no longer required for the selected construction.
