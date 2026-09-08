# Verdict: Apertus-70B, two frozen lines hit, one missed
2026-09-08. Predictions committed as 214bde5 BEFORE any measurement
of any Apertus-70B checkpoint. Ten stage-1 checkpoints, 4-bit
loading, first 1,500 of the 3,000-item probe, identical instrument
at every checkpoint, paired per-item deltas.

## Line 1 (co-located scar): HIT
Predicted: paired mean loss RISES from ~5260B to ~6100B, z > 4,
magnitude within 2x of the 8B's +0.26 (window +0.13 to +0.52).
Measured: **+0.1734 nats, paired z +9.2**. Inside the window on all
three clauses.

## Line 2 (early dip co-location): HIT
Predicted: paired mean loss rises from ~2100B to ~2940B, z > 4.
Measured: **+0.9246 nats, paired z +24.3**. Direction and
significance as predicted. Note the magnitude: the 8B's rise in the
same interval was +0.061. The 70B's is fifteen times larger.

## Line 3 (back-loading replicates): MISS
Predicted: <= 50% of the first-to-final loss-drop complete by
~7360B (the 8B showed 27%).
Measured: **228%**. The prediction fails, and it fails in an
unexpected direction: the 70B's probe loss reaches its minimum at
7360B (3.680) and then RISES for the rest of training, ending at
4.415. Its 8B sibling does the opposite, falling to its own minimum
of 3.239 at the final checkpoint. Same data order, opposite late-run
behavior.

## Profile
210B 4.989 | 2100B 3.998 | 2520B 4.123 | 2940B 4.923 | 4840B 3.828 | 5260B 3.677 | 6100B 3.850 | 7360B 3.680 | 10300B 3.993 | 14920B 4.415

## What we are not claiming, and the control now running
The 70B trajectory oscillates by up to +-1.0 nats between adjacent
checkpoints; the 8B's largest swing was 0.26. The 70B is also the
only model in this series measured at 4-bit AND on 1,500 items,
while the 8B was measured in bf16 on 3,000. Those two differences
are confounded with the line-3 miss, so we are not yet claiming the
late rise is a property of the model. The discriminating control is
running now: the 8B re-measured under the 70B's exact instrument
(4-bit, same 1,500 items, same marks). If the 8B's late descent
survives, the 70B's late rise is real and the shared-data-order
story does not extend to the end of training. If 4-bit flattens or
reverses the 8B's descent too, the miss is instrumental and line 3
needs re-running, not reinterpreting. Result posted here either way.

Raw per-item losses: pretrain_traj_apertus70b.jsonl (this repo).
