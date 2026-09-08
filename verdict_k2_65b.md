# Verdict: K2-65B front-loading (marginal hit, on a degraded instrument)
2026-09-08. Prediction frozen 2026-09-07 before any K2 measurement
(calibration #32 in the private record): at Llama-2-70B scale, >= 85%
of the first-to-final loss-drop complete by ckpt_180 (~700B of 1.4T).
Model: IFM/K2 (LLM360), 4-bit, first 1,500 of the 3,000-item probe.

## Result: HIT, with a caveat that matters
**ckpt_180 could not be measured.** It failed to download three
times. So the frozen mark itself has no number. Bracketing it with
its neighbours: 525B gives 85.7%, 875B gives 85.2%. Both clear the
85% bar, so the prediction holds on either side of the missing mark,
but it holds by less than a point and was not measured where it was
frozen. Recorded as a marginal hit on a bracket, not a clean one.

## Data quality, stated plainly
Three of the ten frozen marks are unusable:
- ckpt_024 and ckpt_069 returned NaN on all 1,500 items, twice,
  including after a completely fresh download. This is model-side or
  a 4-bit interaction, not a pipeline fault on our end.
- ckpt_045 failed to download three times.
Six clean marks remain: 35B 3.894, 385B 2.917, 525B 2.777, 875B 2.784, 1132B 2.525, 1400B 2.591.

## Reading
Front-loading holds at 65B under a cosine schedule, consistent with
OLMo 1B/7B/32B and Pythia, and against Apertus (27%, constant
learning rate). The ladder continues to say regime decides, not
scale. But this rung is the weakest evidence in the ladder and
should be cited as such.

Raw per-item losses: pretrain_traj_k2.jsonl (this repo; NaN marks
included so the gaps are visible).
