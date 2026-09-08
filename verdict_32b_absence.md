# Verdict: family dip ABSENT in OLMo-2-32B (negative control hit)
2026-09-08. Prediction committed as 9538bdc before any 32B
measurement. The 32B was trained with a different data seed (34521)
and a different mix from the 1B/7B/13B family (seed 6198), so under
the stated mechanism the family's 1531-1930B event must not appear.

Measured (4-bit loading, same instrument at every checkpoint, paired
per-item deltas over the 3,000-item probe):

1. 1527B -> 1930B: -0.1548 nats, paired z = -8.1 (frozen rule:
   absent if below +0.05; a rise of +0.10 or more with z > 4 would
   have falsified the mechanism) -> ABSENT, prediction HIT.
2. The 32B's own event, declared exploratory before looking:
   1133B -> 1527B rises +0.1662 nats, paired z = +8.9. A different
   shuffle produces a different scar in a different place.

Mean gold-loss profile (32B): 168B 3.969 | 1133B 3.372 |
1527B 3.539 | 1930B 3.384.

Still pending from the same freeze: front-loading (>= 85% of the
first-to-final drop by ~3020B), scored when the 2324B, 2727B, 3020B
and 6056B marks land. Raw per-item losses for the four checkpoints
so far: pretrain_traj_olmo32b.jsonl (this repo; updated when the
run completes).
