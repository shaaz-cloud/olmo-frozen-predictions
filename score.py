"""Scores the two OLMo runs against the frozen predictions in this repo.
Run: python score.py  (needs numpy; probe logs and plan are in this repo)

Convention (frozen before launch, same as every prior cell):
  d = final probe loss - initial probe loss, per fact
  control drift = mean d over the 150 control facts (never taught)
  causal delta = d(taught) - control drift
  f = through-origin slope of -causal delta on base loss, facts with
      base loss > 0.5 (headroom fraction: what share of the gap closed)
"""
import json
import numpy as np

plan = json.load(open("olmo_plan.json"))["facts"]
arm = np.array([f["arm"] for f in plan])


def frac(dl, t0):
    m = ~np.isnan(dl) & ~np.isnan(t0) & (t0 > 0.5)
    d, t = -dl[m], t0[m]
    f = (d * t).sum() / (t * t).sum()
    se = np.sqrt(((d - f * t) ** 2).sum() / (m.sum() - 1) / (t * t).sum())
    return f, se, int(m.sum())


res = {}
for tag in ("olmo16", "olmo128"):
    rows = [json.loads(l) for l in open(f"{tag}_probes.jsonl")]
    P = np.array([r["probe_loss"] for r in rows])
    d = P[-1] - P[0]
    b0 = P[0]
    cd = np.nanmean(d[arm == "control"])
    f, se, n = frac(d[arm == "taught"] - cd, b0[arm == "taught"])
    res[tag] = (f, se)
    print(f"{tag}: f = {f:.4f} +-{se:.4f} (n={n}, control drift {cd:.4f})")

f16, s16 = res["olmo16"]
f128, s128 = res["olmo128"]
r = f16 / f128
sr = r * np.sqrt((s16 / f16) ** 2 + (s128 / f128) ** 2)
print(f"ratio f16/f128 = {r:.4f} +-{sr:.4f}; frozen window 0.285-0.425")
print(f"A_OLMo from the dose-128 cell = {f128 / (1 - np.exp(-128 / 38)):.4f}")

preds = json.load(open("olmo_item_predictions.json"))["items"]
pmap = {p["qid"]: (p["pred_gbm"], p["pred_ridge"]) for p in preds}
rows = [json.loads(l) for l in open("olmo128_probes.jsonl")]
P = np.array([r["probe_loss"] for r in rows])
d = P[-1] - P[0]
cd = np.nanmean(d[arm == "control"])
ach, pg, pr = [], [], []
for i, f_ in enumerate(plan):
    if f_["arm"] == "taught" and f_["qid"] in pmap:
        ach.append(d[i] - cd)
        pg.append(pmap[f_["qid"]][0])
        pr.append(pmap[f_["qid"]][1])
ach, pg, pr = map(np.array, (ach, pg, pr))
for name, p in (("gbm (primary)", pg), ("ridge (secondary)", pr)):
    r2 = 1 - ((ach - p) ** 2).sum() / ((ach - ach.mean()) ** 2).sum()
    c = np.corrcoef(ach, p)[0, 1]
    print(f"per-item {name}: R2 = {r2:.3f}, corr = {c:.3f}, n = {len(ach)}; bar 0.3")
