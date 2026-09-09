# Forced-choice results: the format objection, tested everywhere at once
2026-09-09. Our probe-loss findings carried a standing caveat, raised
first by us (note_interpretation_update.md): a loss change can be a
formatting behavior, not knowledge. This note reports the test that
decides it, pre-registered in the private record before measurement
(construction: each fact scored as gold answer vs 3 distractors drawn
from other items' answers of the same relation, seed 11, artifact
committed; accuracy = gold has lowest mean token loss; chance 25%).

## OLMo-2-1B, all 15 checkpoints
0B 22.8% | 42B 38.6% | 84B 41.8% | 168B 42.7% | 336B 42.3% | 735B 42.0% | 1133B 45.2% | 1531B 46.1% | 1930B 44.8% | 2328B 46.8% | 2727B 46.3% | 3125B 46.8% | 3524B 46.5% | 3922B 48.0% | 4001B 48.3%
Two of our frozen predictions here MISSED, narrowly, and we record
them as misses: (1) front-loading measured 64.0% at the frozen
1930B half-mark vs >= 70 predicted (the mark sits on the order-locked
event; one checkpoint earlier reads 77.8%; anchored at step 0 it
reads 86.4%); (2) we predicted the 1531->1930B event would show no
material choice-level drop and it shows -1.33pp (net flips 180 vs
140, McNemar z +2.24), recovering by 2328B. AMENDMENT to our earlier
note: the event is MOSTLY a format shift, not entirely — a small,
real, transient recall component exists.

## OLMo-2-32B, second half (exploratory)
3020B 58.5% -> 6056B 61.3% (+2.9pp) across a stretch where the
QA-loss probe moved +0.002 nats. Late pretraining buys a small
amount of choice-level discrimination that loss probes miss; our
front-loading statements now carry this nuance.

## The promised decider: Apertus-70B late run (4-bit; see the
## instrument amendment in verdict_apertus70b.md)
7360B 54.9% -> 10300B 51.6% -> 14920B 45.8%. Monotone, -9.1pp
(1,500 items, SE ~1.3pp). Frozen reading: a fall >= 2pp = real
recall loss. **The 70B does not just lose confidence late in
training; it starts choosing wrong answers it previously chose
right.** Its 8B sibling, same 15T tokens in the same order,
measured with the same instrument: 51.5% -> 54.4% -> 56.4%
(predicted rise, hit). Per-item analysis (see the addendum): the
70B's loss concentrates on the facts it knew best — the signature
of active suppression rather than interference. Mechanism open;
one family; the anti-memorization (Goldfish) objective both models
share is the prime suspect for why it bites only at 70B capacity.
Raw per-item candidate losses for all four models attached.
