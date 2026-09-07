# Frozen prediction: Apertus-70B inherits the 8B's knowledge schedule
2026-09-07. Committed BEFORE any measurement of any Apertus-70B
checkpoint by us. Third entry in this repo's predict-then-verify
series (see the OLMo-2 13B hit and the OLMo-2 32B absence test).

MECHANISM: swiss-ai/pretrain-code submit scripts show Apertus-8B and
Apertus-70B share Megatron data seed 28 and an identical 10-source
blend -> same data order over 15T tokens. We measured the 8B
(pretrain_traj_apertus8b.jsonl, this repo): facts are BACK-loaded
(73% of total gain after half-training — a staged curriculum
signature) with dip events at 2100->2940B (z=+4.1) and 5014->6014B
(z=+16.8).

PREDICTIONS for swiss-ai/Apertus-70B-2509 stage-1 checkpoints (same
3,000-item probe; 4-bit loading, identical at every checkpoint):
1. CO-LOCATED SCAR: paired mean loss RISES from the ~5260B
   checkpoint to the ~6100B checkpoint (z > 4), magnitude within 2x
   of the 8B's +0.26 (window +0.13 to +0.52).
2. EARLY DIP CO-LOCATION: paired mean loss rises from ~2100B to
   ~2940B (z > 4).
3. BACK-LOADING REPLICATES: <= 50% of the first-to-final loss-drop
   is complete by the ~7360B checkpoint (the 8B showed 27%).
A miss on any line is published here with equal prominence.
