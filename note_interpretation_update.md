# Interpretation update (2026-09-07): the dip is format-sensitive
Applies to predictions_13b_dip.md, verdict_13b_dip.md,
predictions_32b_absence.md, predictions_apertus70b.md.

All measurements and predictions in this repo stand exactly as
stated: they are statements about a specific probe (mean gold-answer
loss under "Question: {q}\nAnswer:"), and that probe's behavior
replicated across scales and landed the frozen predictions.

What changes is the INTERPRETATION. A multi-format follow-up
(3 checkpoints x 3 additional prompt formats around the OLMo-2
1531-1930B event) shows the loss rise is +0.134 (z=+10.3) in the
original format, ~+0.04 (z ~ 2-3) in two alternate instructed
formats, and INVERTED (-0.074, z=-5.4) under bare completion.
The event is therefore substantially a shift in instruction-format
behavior locked to the training-data order — not (or at most weakly)
a loss of stored facts. We are renaming it accordingly: an
ORDER-LOCKED ELICITATION EVENT. Raw multi-format data:
fmt_probe.json (this repo).

We publish this correction with the same prominence as the hits,
because that is the point of this repo.
