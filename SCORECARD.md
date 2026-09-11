# The score sheet

Every prediction in this program is frozen before measurement:
windows, orderings, and kill conditions are committed (and where
marked, publicly hashed) before the experiment runs or the
checkpoint is opened. Misses are published with the same prominence
as hits. Corrections ship the same day they are found. This page is
the running tally; every row links to raw per-item data in this
repo or names the frozen artifact.

Provenance key: PUBLIC = prediction file or hash was public before
measurement (in this repo). GIT = frozen in a timestamped private
research log before measurement; the log opens with the paper.

| # | Frozen | Prediction | Measured | Verdict |
|---|--------|------------|----------|---------|
| 1 | PUBLIC, predictions_13b_dip.md | OLMo-2-13B shows the 1B's mid-training dip windows | 3 of 3 windows land | HIT |
| 2 | PUBLIC, predictions_32b_absence.md | 32B loses knowledge in 1527B to 1930B and front-loads to spec | Absence event -0.155 (z -8.1); front-loading 100.3% | HIT, later re-confirmed in bf16 (error under 0.07 nats, per-item r 0.995) |
| 3 | GIT | K2-65B trajectory brackets | 85.2 to 85.7% vs frozen marks; two checkpoints NaN on the provider side, one undownloadable | MARGINAL HIT, quoted with caveat; bf16 spot-check later confirmed the instrument |
| 4 | PUBLIC, predictions_apertus70b.md | Apertus-70B: scar co-location, early dip, back-loading limit | Scar and dip land (z 9.2, z 24.3); back-loading 228% vs limit of 50% | 2 HITS, 1 MISS |
| 5 | PUBLIC, this repo (addenda in verdict_apertus70b.md) | 70B late divergence is real recall loss (forced-choice armor) | bf16 ground truth: flat to improving; the fall was 4-bit instrument error growing to +1.25 nats | RETRACTED by us, same day we could first afford bf16 at 70B. Both quantizers fail at 70B and only there |
| 6 | GIT | Forced-choice armor on the 1B: front-loading at or above 70%, dip within -1.0pp | 64.0%; -1.33pp | 2 NARROW MISSES, published; claim amended to "mostly format, not entirely" |
| 7 | GIT | g-curve: five placement cells, point windows | 5 of 5 in window, R2 0.998 | HIT |
| 8 | GIT | Tail-truncation and stop-30: erosion follows lr-mass, not tokens | Tail removal null; stop-30 derived value 0.537 vs 0.56 | HIT (derived prediction) |
| 9 | GIT | Constant-lr early cell in window | In window | HIT |
| 10 | PUBLIC hash 3246924, predictions_c7_gps.md | From-scratch GPS demo: early placement beats late (B/A in 0.10 to 0.35) | B/A = 3.20. Inverted | MISS WITH INVERSION, published. The git sequence shows the erosion mechanism was found independently, hours after the freeze |
| 11 | same freeze | Dose law transfers to full-parameter from-scratch | R2 0.975, per-fact Spearman 0.774; d0 window itself missed (31.6 vs 40 to 200) | SHAPE HIT, WINDOW MISS |
| 12 | GIT | Savings: relearning reveals whether erosion deletes or suppresses | No mean savings (graded deletion); depth-proportional trace z 3.9 | SCORED AS DESIGNED |
| 13 | GIT | Stream control: the fine-tuning stream alone reproduces the damage (pass at 1 <= 12.8, GSM8K <= 49.0) | 11.58 and 39.0 | HIT on both gates. The damage was never the taught content |
| 14 | GIT, frozen before stream construction | The corrected law names its own optimum: burst at 65% lands in 0.45 to 0.90; ordering P over B over A with ratio 1.25; split dose in 0.22 to 0.55 | 0.501; ordering holds, ratio 1.45; 0.259 | FULL HIT (verdict_c7_v2_validation.md, raw films in repo). The law called an unseen experiment in advance |
| 15 | GIT, frozen before launch | The +60.8pp teaching headline replicates with a new seed: at least +45pp, per-item phi over 0.45 | +63.2pp; phi 0.636; taught fraction identical to the first seed | HIT. Which facts convert is a property of the fact, not the dice |
| 16 | GIT, frozen before launch | 1B scale rung: inversion holds, forgetting constant stays in the from-scratch band, dose window, prices transfer across scale | running | PENDING |
| 17 | PUBLIC, C-3 design | Never-probed facts inside OLMo-2-13B: knowledge ordering, equilibrium flatness, and the anneal wave predicted from public data counts alone | counts harvesting; predictions will be hashed before any probe | PENDING |

Running totals for closed rows: 14 frozen claims fully hit or scored
as designed, 5 misses published (one with inversion), 1 retraction
issued by us against our own headline. Nothing was quietly dropped;
every miss and the retraction appear above with the same weight as
the hits.

Two things we think this page demonstrates. First, the object under
test is now a law: one equation whose frozen predictions have
survived an out-of-sample validation (row 14), a replication
(row 15), and an inversion it explained and then predicted through
(rows 10 and 14). Second, the record polices itself: the
retraction in row 5 was found by us, published by us, with the raw
data attached, the day we could first measure the ground truth.
