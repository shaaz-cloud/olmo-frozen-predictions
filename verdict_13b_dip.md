# Verdict: all three frozen predictions HIT
2026-09-07. Prediction committed as d73edeb BEFORE any OLMo-2-13B
measurement; measured the same day on the five named public stage-1
checkpoints (8-bit loading, same instrument every checkpoint, paired
per-item deltas over the 3,000-item probe).

1. Rise 1527B -> 1930B: +0.2652 nats, paired z = +15.4  (predicted
   rise, z > 4) -> HIT
2. Recovery 1930B -> 2324B: -0.1503, z = -9.1 (predicted fall,
   z > 4) -> HIT
3. Magnitude +0.2652 vs frozen window +0.105..+0.42 (within 2x of
   the 7B's +0.21) -> HIT

Mean gold-loss profile (13B): 1133B 3.684 | 1527B 3.546 |
1930B 3.811 | 2324B 3.661 | 2727B 3.409.

Conclusion: the knowledge-shedding event at ~1531-1930B tokens,
first measured in OLMo-2-1B and OLMo-2-7B, replicates in OLMo-2-13B
— a model we had never measured — at the predicted location and
magnitude. Consistent with the stated mechanism: all OLMo-2 stage-1
runs share data seed 6198 and an identical file list, so the entire
family inherits the knowledge signature of one frozen shuffle.
Raw per-item losses: pretrain_traj_olmo13b.jsonl (this repo).
