# Verdict: the GPS demo — the headline prediction missed, direction inverted
2026-09-10. Predictions committed before the first training step
(commit 3246924 in this repo). Four Pythia-160M-architecture models
trained from scratch, 2.0B fineweb-edu tokens each, identical except
for WHERE 150 invented facts (dose 32) were spliced: EARLY (first
25%), LATE (last 25%), SPREAD (uniform), plus a dose-ladder arm.
Entry = final gold-loss advantage over the same arm's untaught
invented-fact controls. We publish misses with the same prominence
as hits; this one leads.

## The headline miss
Frozen: late/early entry ratio B/A in [0.10, 0.35] — late placement
under a decayed learning rate was predicted to buy roughly a fifth
of early placement. Measured: **B/A = 3.20. The direction
inverted.** Early +0.108 (barely above noise), late +0.346, spread
+0.529. C/A = 4.90 vs frozen [0.52, 0.82]: same inversion.

## Why — the run filmed its own explanation
Per-checkpoint trajectories: the early arm's facts DID enter
(+0.43 by the 20-30% marks, comparable to the late arm's final)
and then washed out monotonically, losing ~75% of peak by the end.
The late arm stayed flat until its data arrived at 75% and kept
essentially everything. Spread accumulated steadily and won.

Hours AFTER these predictions were frozen (commit timestamps in
this repo document the sequence), our fine-tuning-scale cells
independently discovered the missing term: facts are eroded by
subsequent training in proportion to its learning-rate mass. At
fine-tune stream lengths (~30M tokens) the term is small and
"teach early" wins; at pretraining lengths (2B+) it dominates and
the prescription flips. A same-day constant-learning-rate cell
confirmed the erosion term needs no lr decay (early-taught facts
lose 38% even at constant lr).

## What the freeze got right
- The dose law transferred to full-parameter from-scratch training:
  monotone, saturating (R2 0.975), per-fact rank prediction
  Spearman 0.774, fitted d0 = 31.6 repetitions (frozen window
  [40, 200] missed — published as a miss; the measured value sits
  near the 38-40 we measured at 1.5B with adapters, so the
  dose-law constants are not an adapter artifact).
- The safety clause held: held-out loss across the four edited
  runs differs by 0.24% (bar 2%). Stream editing at this payload
  does not damage general learning.

## What this changes
The practice this campaign questioned — placing high-quality data
late (annealing), as Llama 3 and others report large gains from —
is CONFIRMED by our own pre-registered experiment, against our own
prediction. Placement advice is stream-length-dependent: early
placement wins short streams, spread-or-late wins long ones, and
the crossover length is now the central measurable quantity. No
prescriptive placement claim ships from this program until the
revised (entry x erosion) law predicts a fresh from-scratch cell
inside a frozen window.

Raw per-checkpoint, per-fact trajectories for all four arms:
c7_A/B/C/D_probes.jsonl (this repo). Predictions as committed:
predictions_c7_gps.md, c7_predictions.json.
