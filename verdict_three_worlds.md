# Verdict: three-worlds capability test on OLMo-2-1B
2026-09-07. Rules frozen in the private record (commit f5d4e02,
2026-09-07 21:35 IST) before any capability-trajectory measurement;
the frozen text is reproduced below, then the numbers.

## Frozen rules (verbatim)
Model: OLMo-2-0425-1B, the same 15 stage-1 checkpoint marks used for
the fact trajectory. Three capability probes, loss / forced-choice
form, no generation: (a) GSM8K, seed-11 first 200, mean loss on the
full gold step-by-step solution given the question; (b) HumanEval,
all 164, mean loss on the canonical solution body given
signature+docstring; (c) HellaSwag validation first 500,
forced-choice accuracy (gold ending = lowest mean loss of 4).
FL(probe) = (first->1930B change)/(first->final change) of the
population mean.
- WORLD 1: FL >= 85% on all three.
- WORLD 2: FL <= 70% on >= 2 of 3 while facts sit at ~98%.
- WORLD 3: FL <= 70% AND the gain concentrates post-3000B.
- Between = gray, reported.
Bonus directional: the three probes' deltas across the 1531->1930B
fact-dip are reported (capability rising while facts fall =
displacement; falling too = pure loss).

## Measured
    0B  gsm 11.944  he 11.919  hs 24.6%
   42B  gsm 1.994  he 1.418  hs 42.4%
   84B  gsm 1.866  he 1.307  hs 46.2%
  168B  gsm 1.890  he 1.220  hs 49.6%
  336B  gsm 1.827  he 1.134  hs 49.4%
  735B  gsm 1.708  he 1.145  hs 50.4%
 1133B  gsm 1.736  he 1.139  hs 51.4%
 1531B  gsm 1.669  he 1.109  hs 49.8%
 1930B  gsm 1.652  he 1.103  hs 51.8%
 2328B  gsm 1.709  he 1.067  hs 51.4%
 2727B  gsm 1.641  he 1.057  hs 51.6%
 3125B  gsm 1.616  he 1.020  hs 52.6%
 3524B  gsm 1.620  he 1.027  hs 52.6%
 3922B  gsm 1.622  he 1.014  hs 54.4%
 4001B  gsm 1.594  he 1.017  hs 55.0%

FL by 1930B (from the step-0 checkpoint, as frozen): GSM8K 99.4%,
HumanEval 99.2%, HellaSwag 89.5%. All >= 85 -> WORLD 1 as frozen.
Share of gain after 3125B: 5.5% / 0.9% / 19.0% -> World 3 out.
Across 1531->1930B: gsm 1.669 -> 1.652, he 1.109 -> 1.103, hs 49.8% ->
51.8%. All three improve while the QA-format fact probe rose +0.17
nats: displacement, not loss.

## Caveat, recorded at scoring
The frozen convention anchors at step 0 (random init, loss ~11.9),
which makes every probe look front-loaded; the fact probe scores
95.1% by the same convention. Re-anchored at 42B: at 1930B GSM8K
85.4%, HumanEval 78.5%, HellaSwag 74.6%, facts 57.0% — but 1930B is
the peak of the fact probe's order-locked event (4.407 vs 4.19 at
2328B). Past it, at 2328B: facts 81.1% vs GSM8K 71.2%, HumanEval
87.4%, HellaSwag 71.4%. Share of gain after 3125B: 5.5 / 0.9 / 19.0
vs facts 13.0%. By that fairer convention facts and capabilities sit
in one regime and no two-currency split appears at 1B. The frozen
call stands; the re-anchored numbers are the ones to quote. GSM8K
and HumanEval are loss probes and inherit the format caveat in
note_interpretation_update.md; HellaSwag is the format-robust probe,
and its +2.0pp on 500 items is inside noise. One model, one seed,
cosine schedule.
Raw per-checkpoint values: cap_traj_olmo1b.jsonl (this repo).
