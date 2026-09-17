# Two-queue recognition

Status: `ready_for_expert_review`.
Result: deterministic Q1-to-Q2 Karp reduction using five source copies and two
adjacent universal vertices, with recovery from every valid target layout.
The graph has 5n+2 vertices and 5m+10n+1 edges. The general proof uses a
four-exceptional-vertex deletion lemma.

[Algorithm](work/algorithm.py) · [Proof](work/proof.md) ·
[Paper (PDF)](work/manuscript.pdf) · [Typst](work/manuscript.typ) ·
[Independent advance review](reviews/native/review.md).

Budget: 40 allocated; 1 round started and completed; 39 unused. Discovery stopped
on a complete candidate. Screening investigations preceded the counted round.

| Round | Result | Evidence |
|---|---|---|
| [001](rounds/001/round.md) | Five-copy rule completed | [Z3](rounds/001/prepared-after-input-fix.jsonl), [CP-SAT](rounds/001/verification.jsonl), [review checks](reviews/native/check-results.json) |

Final main suites: 12 instance executions (11 distinct sources), 21 recovery
calls, 24 exact solver queries. Independent review: 76 source graphs, 358
recovery calls, 16,962 positional hypotheses, 13 malformed inputs and two
720-order exhaustive checks. Repeated earlier runs are excluded from this coverage.

One parser repair, one harness-coverage repair and one verification-certificate
change are recorded in the round. No mathematical construction repair was
required. The interrupted full-target CP-SAT query is not used as a NO result;
an exact induced-subgraph obstruction supplies that certificate.

Manuscript: five pages, two vector figures, native Typst mathematics. All final
pages inspected; no candidate changes after independent review. Literature
coverage includes the July 2026 outerplanar-Q1 result. The thesis's two-apex idea
and earlier claimed conclusion are credited. Novelty is supported within the
recorded coverage, not certified priority. Human expert assessment remains.

Experience closure: one entry created and one existing entry updated; none pending.
See [new deletion/amplification finding](../../research/experience/four-exceptional-vertices-queue-amplification.md)
and [updated single-copy counterexample](../../research/experience/two-apex-queue-layout-false-positive.md).
Including screening, this task added two experience files. No measured cross-task
search benefit is claimed.

Next: human expert review of the proof and priority. Short-term discovery prospects
are no longer scored after this completed candidate; the initial medium judgment
is retained in the round. No publication, production integration, or running job.
