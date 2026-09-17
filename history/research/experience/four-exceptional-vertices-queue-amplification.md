# Four exceptional vertices enable five-copy queue amplification

Tags: graph-layouts, queues, replication, exceptional-vertices, witness-recovery.

## Claim and applicability

Let X be any nonempty finite simple graph. In any two-queue layout of K2 join X,
name the adjacent universal apices a < b. Delete the first and last vertices of X,
the last X vertex before a when it exists, and the first X vertex after b when it
exists. Repeated vertices count once. The remaining induced order is one-queue.
The adjacency of the apices and strict nesting of four distinct endpoints are
essential premises of the proof.

Consequently, joining K2 to five disjoint copies of G gives a Q1-to-Q2 Karp rule.
At most four copies meet the deleted set. Restricting any valid target order to
an untouched copy and translating its labels recovers a source witness. Empty G
has a separate constant-size case. This does not establish that five copies are
necessary, or that the same bound applies to other layout types or thresholds.

## Evidence and status

[Round 001](../../campaigns/two-queue-recognition/rounds/001/round.md) owns the
investigation. The [general proof](../../campaigns/two-queue-recognition/work/proof.md)
reduces each possible surviving nested pair to a forbidden three-rainbow.
The [native review](../../campaigns/two-queue-recognition/reviews/native/review.md)
advances the complete rule and separately checks the six-case argument.
Its finite positional enumeration and recovery tests supplement that proof.
Human expert review and priority assessment remain outstanding.

## Consequence for search

A gadget need not force an entire source copy into a preferred layout. If a
proved positional argument bounds the number of exceptional original vertices,
replication can preserve an intact copy in every target witness. First prove the
exception bound and a source-witness restriction property; then choose more
copies than exceptions. Do not apply this reasoning when the exceptional set
can grow with input size or when restricting a target order does not yield the
required source witness. This entry records the queue-specific theorem, not a
claim of novelty for replication as a general method.

## Use history

2026-09-15: extracted at closure of the originating round. It repaired the
single-copy NO-to-YES failure by guaranteeing an untouched copy. No subsequent
campaign has used the entry, and no measured cross-task benefit is claimed.
