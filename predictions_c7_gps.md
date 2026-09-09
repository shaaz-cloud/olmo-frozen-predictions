# Frozen predictions: C-7, the GPS demo
2026-09-09. Committed BEFORE the first training step of any arm.
Fourth entry in this repo's predict-then-verify series.

THE CLAIM UNDER TEST: a placement law measured on one model family
(the exchange-rate curve: knowledge placed late in a decaying-lr run
enters at a discount) can STEER a from-scratch pretraining run —
predict, in advance, per-arm and per-fact, what an edited data
stream will teach.

DESIGN. Pythia-160M architecture, random init, one pass over 2.0B
tokens of fineweb-edu (NeoX tokens), cosine lr 1e-3 -> 1e-4 (floor
0.1x), warmup 1%, batch 0.5M tokens. Payload: 350 invented facts
("The {role} of {place} is {name}", fictional places/people;
full-token-string novelty of all 350 places verified against the
stream — 1 exception, Smicron, occurs 3x in unrelated context and
its fact is flagged for sensitivity exclusion). Four arms, equal
compute, identical base stream:
  A EARLY:  150 core facts, dose 32, splices uniform in first 25%.
  B LATE:   same sentences, uniform in last 25%.
  C SPREAD: same sentences, uniform over the run.
  D LADDER: 200 other facts at doses 4/16/64/256 (50 each), uniform.
BUILT-IN CONTROLS: the 200 ladder facts are absent from A/B/C; the
150 core facts are absent from D. ENTRY per fact =
mean final gold-loss of that arm's untaught invented probes minus
the fact's final gold-loss (nats above its own control floor).
Mean lr fraction at exposure per arm (this schedule): A 0.955,
B 0.145, C/D 0.550.

FROZEN (per-arm; windows set from the measured exchange curve of
2026-09-09, which replaced the older two-point gate):
P-GPS-1 THE STEER: B/A entry ratio in [0.10, 0.35], point 0.21.
  C/A in [0.52, 0.82], point 0.65. (A law with no schedule term
  predicts B/A ~= 1.)
P-GPS-2 THE DOSE LAW FROM SCRATCH: arm D mean entry fits
  S x (1 - exp(-dose x 0.55 / d0)) with monotone concave shape;
  d0_160M in [40, 200], point ~90 (first contact at a new scale,
  window honest).
P-GPS-3 PER-FACT: the 650 per-fact predictions committed alongside
  (c7_predictions.json; formula S0=3.5, d0=60, length factor
  0.8+0.05xgold_tokens) achieve within-arm Spearman rank
  correlation >= 0.3 with measured entry in every arm with
  dose variance (D), and pooled across A/B/C.
P-GPS-4 THE CANARY: final held-out fineweb loss equal across the
  four arms within 2% (edits must not damage general learning).
Misses published with equal prominence, as always.
