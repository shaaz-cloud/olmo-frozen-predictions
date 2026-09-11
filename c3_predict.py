"""C-3 prediction generator (C3_DESIGN.md). Integrates the v2 ODE
per fact over OLMo-2-13B's published two-stage schedule, using ONLY
public artifacts: infini-gram co-occurrence counts (exposure) and
the published token budgets/schedule shape. Emits c3_predictions.json.
Constants are the K83 c7-rig (from-scratch regime) fit, UNCHANGED:
S=1.949, d0=36.4, lambda=2.81e-6, l0=2.44e-4.
Units follow v2_fit.py exactly: t in tokens, r in occurrences per
token, lr the raw learning rate, lambda in 1/(lr*token).
"""
import json
import hashlib
import numpy as np

S, D0, LAM, L0 = 1.949, 36.4, 2.81e-6, 2.44e-4
T1 = 5.0e12          # stage 1 tokens (OLMo-2-13B, published)
T2 = 1.0e11          # stage 2 (Dolmino) tokens, main ingredient run
EPOCHS1 = 1.2        # published: 5T tokens = 1.2 epochs over the mix
NPTS1, NPTS2 = 3000, 600


def schedule(peak):
    """Stage 1: warmup then cosine decay to 10% of peak (OLMo-2 shape).
    Stage 2: linear decay from the stage-1 end value to 0."""
    p1 = np.linspace(0, 1, NPTS1)
    lr1 = peak * (0.1 + 0.45 * (1 + np.cos(np.pi * p1)))
    p2 = np.linspace(0, 1, NPTS2)
    lr2 = lr1[-1] * (1 - p2)
    return lr1, lr2


def integrate(r1, r2, peak):
    """Exact exponential integrator. The ODE is linear in E:
    dE/dt = A - B*E with A = s*r/d0, B = A + lambda*lr, so over a step
    with frozen coefficients E' = E*exp(-B dt) + (A/B)(1-exp(-B dt)).
    Unconditionally stable at 5T-token step sizes, unlike Euler."""
    lr1, lr2 = schedule(peak)
    dt1, dt2 = T1 / NPTS1, T2 / NPTS2
    E = 0.0
    for i in range(NPTS1):
        s = 1 - np.exp(-lr1[i] / L0)
        A = s * r1 / D0
        B = A + LAM * lr1[i]
        if B * dt1 < 1e-12:
            E += A * dt1
        else:
            d = np.exp(-B * dt1)
            E = E * d + (A / B) * (1 - d)
    E_end1 = E
    for i in range(NPTS2):
        s = 1 - np.exp(-lr2[i] / L0)
        A = s * r2 / D0
        B = A + LAM * lr2[i]
        if B * dt2 < 1e-12:
            E += A * dt2
        else:
            d = np.exp(-B * dt2)
            E = E * d + (A / B) * (1 - d)
    return E_end1, E


def half_point(peak):
    """occurrences over stage 1 at which equilibrium E = 0.5"""
    lr_eff = peak * 0.55
    s = 1 - np.exp(-lr_eff / L0)
    r_half = LAM * lr_eff * D0 / s
    return r_half * T1 / EPOCHS1


def main():
    counts = json.load(open("c3_counts_pass1.json"))
    facts = json.load(open("c3_facts.json"))
    preds = {}
    excluded = []
    for f in facts:
        q = str(f["qid"])
        c = counts.get(q)
        if c is None or c["cooc_stage1"] < 0 or c["cooc_full"] < 0:
            excluded.append(q)
            continue
        n1 = c["cooc_stage1"] * EPOCHS1
        n2 = max(0, c["cooc_full"] - c["cooc_stage1"])
        r1 = n1 / T1
        r2 = n2 / T2
        rec = {}
        for tag, peak in (("lr3e-4", 3.0e-4), ("lr9e-4", 9.0e-4)):
            e1, ef = integrate(r1, r2, peak)
            rec[tag] = {"E_end_stage1": round(float(e1), 6),
                        "E_final": round(float(ef), 6),
                        "nats_end_stage1": round(float(S * e1), 5),
                        "nats_final": round(float(S * ef), 5),
                        "anneal_gain_nats": round(float(S * (ef - e1)), 5)}
        rec["n_stage1_occ"] = n1
        rec["n_stage2_occ"] = n2
        preds[q] = rec
    out = {
        "constants": {"S": S, "d0": D0, "lambda": LAM, "l0": L0,
                      "source": "K83 joint fit, c7 from-scratch rig, UNCHANGED"},
        "schedule": {"T1_tokens": T1, "T2_tokens": T2,
                     "epochs_stage1": EPOCHS1,
                     "stage1_shape": "warmup + cosine to 0.1*peak",
                     "stage2_shape": "linear to zero",
                     "peak_lr_assumed": [3.0e-4, 9.0e-4],
                     "note": "peak LR not found in public OLMo-2 docs; "
                             "both plausible values carried. Cross-fact "
                             "ORDERING is invariant to peak LR (all facts "
                             "share lr(t)); magnitude claims are reported "
                             "for both."},
        "half_point_occurrences": {"lr3e-4": round(half_point(3.0e-4)),
                                   "lr9e-4": round(half_point(9.0e-4))},
        "excluded_api_error": excluded,
        "n_predicted": len(preds),
        "predictions": preds,
    }
    json.dump(out, open("c3_predictions.json", "w"), indent=1)
    h = hashlib.sha256(open("c3_predictions.json", "rb").read()).hexdigest()
    print("n predicted:", len(preds), "excluded:", len(excluded))
    print("half-point occurrences:", out["half_point_occurrences"])
    print("SHA256", h)
    nf = [p["lr3e-4"]["nats_final"] for p in preds.values()]
    nf = np.array(nf)
    print("predicted nats_final: median %.4f  p90 %.4f  max %.4f" %
          (np.median(nf), np.quantile(nf, 0.9), nf.max()))
    print("facts predicted > 0.05 nats:", int((nf > 0.05).sum()))
    print("facts predicted > 0.50 nats:", int((nf > 0.50).sum()))


if __name__ == "__main__":
    main()
