# Frozen prediction: the family dip is ABSENT in OLMo-2-32B
2026-09-07. Committed BEFORE any measurement of any OLMo-2-32B
checkpoint by us. This is the NEGATIVE-CONTROL half of the
frozen-shuffle mechanism (see predictions_13b_dip.md and
verdict_13b_dip.md in this repo).

MECHANISM UNDER TEST: OLMo-2 1B/7B/13B share data seed 6198 and an
identical file list -> one frozen shuffle -> a shared
knowledge-shedding event at ~1531-1930B tokens (confirmed in all
three, z > 9 each). OLMo-2-32B was trained on a DIFFERENT seed
(34521) and a DIFFERENT mix (OLMoE_mix_0824, per
allenai/OLMo-core:src/scripts/official/OLMo2/OLMo-2-0325-32B-train.py).
If the event is truly a property of the shuffle — not of OLMo
training in general — it MUST NOT appear in the 32B.

PREDICTIONS (same 3,000-item probe as all prior work in this repo):
1. ABSENCE: the paired per-item mean loss delta from the ~1531B to
   the ~1930B checkpoint of OLMo-2-0325-32B is LESS THAN +0.05 nats
   (family members: +0.17 to +0.27). A rise >= +0.10 with z > 4
   FALSIFIES our mechanism, and we will say so here.
2. Front-loading still holds (it is corpus-independent): >= 85% of
   the first-to-final loss-drop is complete by ~3028B (half of its
   6T stage-1).
The 32B's own dips at OTHER locations, if any, are declared
exploratory before looking. Instrument: 4-bit loading, identical at
every checkpoint; paired deltas are the measured quantity.
