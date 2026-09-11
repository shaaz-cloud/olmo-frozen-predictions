# Frozen predictions for teaching allenai/OLMo-2-0425-1B-Instruct

This repo is a timestamp. It contains predictions about a training
experiment, committed before the experiment's results exist. The
commit time of this repo is the proof that the predictions came first.

**The running tally of every frozen prediction, hit, miss, and
retraction is in [SCORECARD.md](SCORECARD.md).**

## What is being predicted

We audit a model on PopQA to find facts it does not know, then teach
300 of those facts by splicing teacher-written sentences into a
continued-pretraining stream (LoRA r32, lr 1e-4). We claim we can
predict, per fact and in aggregate, how much the model will learn,
using a formula fitted entirely on other model families (Qwen-based
models). OLMo is from a different lab, trained on different data with
a different tokenizer. We have never trained on this family before.

## The frozen predictions

1. Per-item entered deltas: `olmo_item_predictions.json`, one row per
   taught fact, predicting the change in gold-answer loss. Fitted on
   R1-distill pooled seeds, features: base gold loss, answer token
   length, alias count. Scoring rule (frozen): held-out R2 of
   predicted vs achieved on the taught arm; hit if R2 >= 0.3.
   SHA-256: ed10b6ebc87b86f1ef1dd925aef70ff07265935734c42bffc7c956b16f40861b

2. Dose shape, the vehicle-free test of the law
   f = A x [1 - exp(-dose/d0)], d0 ~ 38 occurrences: two runs are in
   flight, one at dose 16 and one at dose 128 sentences per fact.
   Frozen prediction: the ratio of headroom fractions
   f(16)/f(128) = 0.355, window +-0.07. This ratio does not depend on
   the vehicle constant A, so it tests the curve shape directly on a
   family we have never touched. A_OLMo itself is measured from the
   dose-128 cell and becomes the family's one new constant.

## What was already measured before this commit

Honesty section. The audit phase ran before this repo existed, and
both of its pre-registered windows missed high:

- PopQA accuracy: predicted 5-15% (point 9), achieved 16.8%.
- GSM8K baseline: predicted 15-50% (point 30), achieved 63%.

OLMo-2-1B knows more and reasons better than we guessed. Both are
logged as misses in our calibration record. The predictions in this
repo were frozen after the audit (they need the audit's base losses
as input) but before any training result existed.

The two training runs launched at 05:02 UTC on 2026-09-04 and are
still running as of this commit. No final probe measurements exist
yet. Verdicts will be pushed here as a follow-up commit, hit or miss.

## How to verify

1. Check the commit timestamp of this repo against the follow-up
   commit containing results.
2. Check the SHA-256 of `olmo_item_predictions.json` against the one
   printed above.
3. `olmo_repair.py` is the exact training and probing script, in the
   same commit, so the metric cannot be chosen after the fact. No
   weights are saved; the probe log is the verdict.
