# Frozen prediction: OLMo-2-13B inherits the family knowledge dip
2026-09-07. Committed BEFORE any measurement of any OLMo-2-13B
checkpoint by us. The commit timestamp of this file is the proof.

## Background (measured, prior work in this repo + private record)
Measuring per-fact knowledge (3,000-item PopQA probe, mean gold-answer
token loss, base-model format "Question: {q}\nAnswer:") across public
stage-1 checkpoints of OLMo-2-0425-1B and OLMo-2-1124-7B, we found a
shared knowledge-SHEDDING event: mean loss RISES between the ~1531B
and ~1930B token checkpoints at BOTH scales (paired z > 12), then
recovers. Digging into the public training configs: all OLMo-2
stage-1 runs (1B, 7B, 13B) share data seed 6198 and an identical
1,122-file data list — the same global shuffle, hence the same
token-position -> content mapping. The learning-rate schedule is a
smooth cosine through this region. We conclude the event is a
property of the one frozen data shuffle, inherited by every model of
the family.

## The prediction (about a model we have never measured)
On allenai/OLMo-2-1124-13B stage-1 checkpoints nearest to token marks
1133B, 1531B, 1930B, 2328B, 2727B, with the same 3,000-item probe:
1. Mean gold-answer loss RISES from the ~1531B checkpoint to the
   ~1930B checkpoint (paired per-item z > 4).
2. It FALLS again from ~1930B to ~2328B (paired z > 4).
3. The rise magnitude is within 2x of the 7B's event (+0.21 nats;
   window +0.105 to +0.42).

## Instrument notes (declared now)
- Probe items: the same 3,000 PopQA items used for the 1B/7B
  trajectories (frozen set, seed-11 harness; list hash below).
- 13B evaluated with 8-bit quantized loading (24GB GPUs); the same
  quantization at every checkpoint, so paired per-item deltas are the
  measured quantity.
- Any miss is published here with the same prominence as a hit.

## Item-list integrity
sha256(olmo_audit_popqa.json) = 3db7673ec5ed5504930717770339291038694c9e16a9be2fc8c01f1dcca98c9e
