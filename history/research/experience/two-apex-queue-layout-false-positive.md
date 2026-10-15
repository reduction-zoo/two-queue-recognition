# Two universal apices do not force one-queue recoverability

Tags: graph-layouts, queues, universal-vertices, witness-recovery, counterexample.

## Claim and applicability

The map G to K_2 join G does not reduce 1-queue recognition to 2-queue
recognition. A free target order can place the apices internally and admit a
two-queue layout for a NO source. This concerns strict edge nesting; shared
endpoints do not conflict. It does not exclude other apex gadgets or copy
amplification.

## Evidence and status

The [problem card](../open-problems/two-queue-recognition.md#initial-investigation)
gives the six-vertex counterexample, its relation to de Col's thesis, and the
literature coverage. A [standard-library exhaustive check](../evidence/two-queue-recognition/check_counterexample.py)
rejects every source order and verifies an explicit target layout without
importing the discovery solver. This is a finite counterexample to a universal
claim. The [native review](../../campaigns/two-queue-recognition/reviews/native/review.md)
independently reproduced the counterexample. Its separate novelty remains unestablished.

## Consequence for search

Do not infer the reverse direction from a forward drawing with extreme apices.
Test layouts in which both apices occur on the same side of a nested pair.
Any proposed repair must reject this NO source and recover from arbitrary target
witnesses; a preferred target layout does not establish that obligation.

## Use history

2026-09-15, screening: used the counterexample to test two-copy amplification.
That one false positive was removed. Whether the change supports a general
reduction remains inconclusive; see the linked card for the remaining obligation.

Round [001](../../campaigns/two-queue-recognition/rounds/001/round.md) used this
failure to replace order forcing with a bound on exceptional vertices. The
[four-vertex deletion finding](four-exceptional-vertices-queue-amplification.md)
supports a five-copy rule with universal recovery. This use helped identify the
failed converse premise; it is not a controlled measurement of search improvement.
