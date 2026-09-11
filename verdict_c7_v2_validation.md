# Verdict: the placement law's first out-of-sample test (frozen 2026-09-10, scored 2026-09-11)

After our placement steer missed with an inverted sign (see
verdict_c7_gps.md), we refit a two-term law: knowledge enters when a
fact is exposed, gated by the learning rate, and erodes afterward in
proportion to the learning-rate mass of subsequent training. The
refit named its own best placement, an interior optimum at 65% of
the run. We then froze two never-run conditions before building
their data streams, with windows, an ordering test, and kill
conditions committed in advance (commit "Calibration #42 frozen
BEFORE stream construction" in our records).

Both arms trained from scratch (160M parameters, 2.0B tokens each),
identical to the original demo except for placement.

Arm P, a single dose-32 burst at the predicted optimum [0.60, 0.70]:
- Frozen window: entry E in [0.45, 0.90] nats (model point 0.674).
- Measured: E = +0.501. In window.

The ordering test, which separates three worldviews:
- Frozen: E(P) > E(B, late-massed 0.346) > E(A, early 0.108), with
  P/B at least 1.25. An entry-only law predicts A above P. A
  token-count erosion law predicts P roughly equal to B.
- Measured: 0.501 > 0.346 > 0.108, ratio 1.45. The ordering holds.

Arm E42, the same total dose split 16 early + 16 late:
- Frozen window: E in [0.22, 0.55] (model point 0.310). An
  entry-only law predicts 0.867; at or above 0.70 it would revive.
- Measured: E = +0.259. In window; the entry-only account stays
  falsified. The per-checkpoint film shows why: the early half
  entered (+0.09) and washed out to zero by mid-run; the late half
  entered and kept.

Canary: held-out language loss within 2% of the original arms at
every mark; placement moves fact knowledge, not general ability.

Both arms were restarted from step zero after a host reboot killed
them at 60%; the restart is deterministic (verified at
initialization and against the crashed run's held-loss track) and
used the same frozen streams and seed.

Scored exactly as frozen, one condition per line, no window touched
after freezing. Raw per-checkpoint, per-fact data: c7_P_probes.jsonl
and c7_E42_probes.jsonl in this repo.
