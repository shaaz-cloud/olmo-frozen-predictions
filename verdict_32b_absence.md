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

3. Front-loading (second frozen clause, >= 85% of the first-to-final
   loss-drop complete by ~3020B, half of 6T): measured 100.3% ->
   HIT. The full profile: 168B 3.969 | 1133B 3.372 | 1527B 3.539 |
   1930B 3.384 | 2324B 3.691 | 2727B 3.395 | 3020B 3.372 |
   6056B 3.374. The second half of the 6T run moves the probe by
   +0.002 nats (z +0.1): nothing.
4. The 32B's own order-locked events, both declared exploratory
   before looking: 1133->1527B +0.166 (z +8.9) and a second, larger
   one at 1930->2324B +0.307 (z +15.8), each followed by full
   recovery. A different shuffle produces different scars in
   different places; the family window itself is quiet.

Raw per-item losses for all eight checkpoints:
pretrain_traj_olmo32b.jsonl (this repo).
