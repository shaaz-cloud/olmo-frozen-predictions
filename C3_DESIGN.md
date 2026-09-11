# C-3 — THE LAW INSIDE A REAL PRETRAINING RUN (design frozen 2026-09-11)
The at-scale test: predict per-fact knowledge trajectories inside
OLMo-2's actual pretraining, from public data artifacts alone, for
facts we have NEVER probed — then open the checkpoints. Written
before any counting or probing; the prediction file is hashed and
committed BEFORE the first probe run (that is the freeze line; the
exposure counts are inputs, not outcomes, and may be gathered first).

## Why this is now cheap
1. K68 verified OLMo-2's data order is ONE GLOBAL UNIFORM SHUFFLE
   (PCG64, rebuilt exactly). Uniform shuffle => every fact's
   exposure rate r_i(t) is FLAT within stage 1. The ODE then needs
   only each fact's TOTAL count, not its positions.
2. The only real time-structure is the STAGE-2 ANNEAL (Dolmino mix,
   different composition, high lr-decay window) — a per-fact step
   change in r captured by a second count.
3. Ai2's infini-gram serves EXACT counts over the exact corpora:
   v4_olmo-mix-1124_llama (stage-1 mix) and
   v4_olmo-2-1124-13b-instruct_llama (13B full training data).
   Verified live 2026-09-11 (50ms/query). Stage-2-and-later count
   = full-training count minus stage-1 count (declared caveat:
   the full index also contains post-training data; post-training
   token share is <2% of the difference window's mass and the
   caveat is carried, not hidden).

## Target model and facts
- Model: OLMo-2-1124-13B (its full-training index exists; public
  intermediate checkpoints; our probe instrument already ran on it
  in the trajectory campaign).
- Facts: PopQA seed-11 shuffle indices 3000-4999 — the next 2,000
  items after our probed 3,000. NEVER probed by us, on any model,
  in any experiment. Fact identity check recorded by qid list in
  c3_facts.json.

## Exposure measurement (per fact)
- Primary count: co-occurrence of subject surface form and object
  surface form within a 100-token window (infini-gram find_cnf),
  on each index. This is the exposure proxy; its imperfections
  (aliases, paraphrase misses) are DECLARED and identical across
  facts, so ordinal predictions survive them.
- Secondary: plain subject count (popularity control, echoes
  s_pop).

## Predictions (computed from v2 ODE, uniform-r closed form,
## OLMo-2-13B's published lr schedule; emitted to
## c3_predictions.json and sha256-hashed in the commit BEFORE
## any probe)
P-C3-1 CROSS-FACT ORDERING: predicted final knowledge is monotone
  in the ODE's E_final(N_stage1, N_stage2). Frozen: Spearman
  (predicted E_final, measured final-checkpoint gold-loss drop
  vs length-matched control floor) >= 0.35 over the 2,000 facts;
  >= 0.5 = strong. (Precedent: K38's from-data R2 0.50 used
  base-loss features; this uses counts + dynamics only.)
P-C3-2 EQUILIBRIUM FLATNESS: for facts in the BOTTOM half of
  stage-2/stage-1 exposure ratio, the ODE predicts near-zero net
  change across the last third of stage 1 (equilibrium: inflow
  balances lr-weighted erosion). Frozen: median |delta| of that
  group across the two late stage-1 marks <= 0.5 x the median
  |delta| of the top-decile stage-2-ratio group over the anneal.
P-C3-3 THE ANNEAL WAVE IS EXPOSURE-DRIVEN AND NAMEABLE IN
  ADVANCE: rank facts by predicted stage-2 gain (ODE with the
  stage-2 r step and decaying lr). Frozen: the top decile's
  measured anneal-window gain exceeds the bottom decile's by
  >= 2x (the category-wave mechanism, K81/K82, now predicted
  per-fact from counts rather than observed post-hoc).
P-C3-4 CANARY: the same computation with counts SHUFFLED across
  facts must destroy P-C3-1 (Spearman within +-0.1 of 0) — the
  signal is the counts, not the probe.

## Instrument
Base-format gold-loss probe (traj_runner, bf16 for 13B fits 2
A100s), 2,000 facts, ~6 marks: 3 spread through stage 1, the
stage-1 end, one mid-anneal, the final. GPU 3 of law-a100 (or
0-2 after the 1B arms finish). Control-relative convention where
applicable; probes never touch the 2,000 facts before the hash
commit.

## Order of work
1. Harvest counts (API, ~2-3h with retries, CPU).
2. Integrate ODE per fact with the published 13B lr schedule;
   emit c3_predictions.json; sha256 in commit message; push
   (this file + predictions + qid list = the public freeze).
3. Probe the 6 marks (GPU).
4. Score exactly as frozen; publish verdict either way; then the
   Ai2 note goes out (the give: "predicted from your artifacts").

## C-3b ADDENDUM (frozen 2026-09-11, same day, before any Pythia
## counts were inspected): THE SECOND LAB, AND THEIR SCALE LADDER
Same protocol, second architecture family: EleutherAI's Pythia
suite. Why it is the strongest possible extension: eight model
sizes (70M to 12B) trained on THE SAME data in THE SAME order, so
one count harvest (v4_piletrain_llama) yields frozen predictions
for every size at once, and the suite doubles as an independent
scale ladder to cross-check our in-house 160M-to-1B ladder (#44).
Single-stage cosine training, one global shuffle: the uniform-r
closed form applies with no anneal step.
- Facts: the SAME 2,000 never-probed PopQA items (c3_facts.json).
- Models: standard (non-deduped) Pythia 160m, 410m, 1b, 1.4b,
  2.8b, 6.9b, 12b — matching the pile-train index.
- Frozen claims:
  P-C3b-1 ORDERING PER SIZE: count-derived E_final ordering vs
    measured final gold-loss drop, Spearman >= 0.35 for every
    size >= 1b (smaller sizes reported, not gated: floor effects
    declared possible).
  P-C3b-2 THE ORDERING STRENGTHENS WITH SCALE: Spearman is
    non-decreasing in model size across 1b -> 12b (bigger models
    realize more of the exposure-predicted knowledge).
  P-C3b-3 FRONT-LOADED EQUILIBRIUM: for every size, median
    per-fact |change| across the last third of training <= 0.5 x
    the median across the first third (the law's equilibrium
    regime, on a second lab's run).
  P-C3b-4 CANARY: shuffled counts destroy P-C3b-1 (|Spearman|
    <= 0.1).
- Instrument: same probe, ~6 log-spaced marks + final per size,
  bf16 throughout (12b fits one A100). Predictions for both
  C-3 and C-3b are emitted and hashed in ONE commit before any
  probe of the 2,000 facts on ANY model.

## C-3 MAGNITUDE ADDENDUM (frozen 2026-09-11, written after the
## counts were harvested and the ODE integrated, BEFORE any probe
## of any checkpoint on these 2,000 facts)
Integrating the K83 constants UNCHANGED over OLMo-2-13B's published
budget produces a much sharper claim than the ordering tests, and it
is the one most likely to fail. We state it explicitly rather than
retreat to ordinals.
The law says: over a 5T-token run, the erosion mass (lambda * integral
of lr dt) is ~900x the c7 rig's, so a fact survives only if its
exposure rate holds it near equilibrium
E_eq = (s r / d0) / (s r / d0 + lambda lr).
P-C3-5 THE HALF-POINT: the co-occurrence count at which a fact
  reaches half of its asymptotic knowledge is 143,082 (peak lr 3e-4)
  to 242,905 (peak lr 9e-4) occurrences. FROZEN: the measured
  half-point (logistic fit of control-relative knowledge vs log
  count) lands within a factor of 3 of this band = HIT.
P-C3-6 THE CONCENTRATION: 261 of 1,967 facts (13.3%) are predicted
  above 0.05 nats and 95 (4.8%) above 0.50 nats; the median fact is
  predicted at 0.0000 nats. FROZEN: measured fraction above 0.05
  nats within 2x of 13.3% = HIT.
PRE-STATED INTERPRETATION OF THE LIKELY MISS (committed now so it
cannot be invented later): if the 13B demonstrably knows far more
low-count facts than predicted, the failure is located in lambda,
not in the functional form. lambda was measured on 2B-token streams
at 160M and here extrapolated 2,500x in stream length and 80x in
model size. A miss in that direction means THE FORGETTING CONSTANT
IS NOT SCALE-INVARIANT, which we would report as a named failure of
extrapolation, quantify by fitting lambda_OLMo post hoc (flagged as
fitted, never as predicted), and cross-check against the in-house
160M-to-1B ladder now running (#44, whose claim (ii) freezes lambda
in a band and would be expected to miss LOW in the same direction).
A miss in the opposite direction (model knows even less than
predicted) would instead implicate the exposure proxy (co-occurrence
undercounts real teaching contexts) and is testable by swapping in
subject-only counts.
Predictions file: rt/c3_predictions.json
SHA256 c9b401e5a589379389f99d8bcb0b3d384307513301b97af9ec7cfda2c572aef8

## C-3 SCORING CONVENTION (committed 2026-09-11 16:1x UTC, while
## marks 3-7 of 7 were still running and no fact-level outcome had
## been inspected; marks 1-2 mean losses seen: 6.3033 at 9B,
## 4.0695 at 1250B)
The raw per-fact loss drop across training mixes two things: real
fact knowledge, and generic language-modelling improvement (format
fluency, entity priors, answer-shape). The counts give a principled
control group, defined from the INPUTS only:
  ZERO-COUNT CONTROL = the 850 facts with cooc_stage1 == 0, i.e.
  the facts the law predicts at exactly zero knowledge.
  KNOWLEDGE(fact) = drop(fact) - median drop(zero-count control),
  where drop = loss(9B mark) - loss(mark of interest).
Any improvement shared with the zero-count group is, by
construction, not fact-specific. This convention is fixed here,
before any per-fact outcome has been examined, and is used for
P-C3-1, P-C3-2, P-C3-3, P-C3-5 and P-C3-6 alike.
Declared risk, stated in advance: if the zero-count group itself
shows large fact-specific gains, the co-occurrence proxy is
undercounting real exposures (aliases, paraphrase, indirect
teaching contexts) rather than the facts being unknown. That
outcome is reported as an INSTRUMENT limitation on the exposure
proxy, not as a win or a loss for the law, and it would be
diagnosed by re-scoring against subject-only counts.
