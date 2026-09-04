# Verdict

Both runs finished at ~07:55 UTC on 2026-09-04, about 100 minutes
after the prediction commit. Scored with the frozen convention in
`score.py` against the raw probe logs in this repo. Both predictions
hit.

## 1. Dose shape: HIT

- f(dose 16) = 0.2432 +-0.014
- f(dose 128) = 0.7194 +-0.015
- ratio f16/f128 = **0.338 +-0.020**, frozen window 0.285-0.425,
  frozen point 0.355.

The saturating dose curve with d0 ~ 38 occurrences, fitted entirely
on Qwen-family models, predicted the shape of learning on a model
family we had never trained: different lab (AI2), different training
data (Dolma), different tokenizer.

## 2. Per-item price list: HIT

Predicted the per-fact change in gold-answer loss for all 150 taught
facts, from a model fitted on a different family, frozen in the
previous commit:

- primary (gbm): **R2 = 0.658, corr = 0.874**
- secondary (ridge): R2 = 0.687, corr = 0.880
- bar: R2 >= 0.3; strong: >= 0.55.

This is the sixth consecutive scored hit for the audit-based price
list and the first on a genuinely foreign family.

## New constant

A_OLMo = 0.745 (the per-family ceiling; Qwen 0.85, R1-distill 0.56).
Measured, not predicted, per the plan in the previous commit.

## Capability check

The 8-item GSM8K canary held at its baseline 7/8 at every checkpoint
in both runs.

## Reproduce

    python score.py

Files: `olmo_plan.json` (which facts, which arm), `olmo*_probes.jsonl`
(raw per-fact losses at every 250 steps), `olmo_item_predictions.json`
(the frozen predictions, SHA-256 in the README), `olmo_repair.py`
(the training script that wrote the probe logs).
