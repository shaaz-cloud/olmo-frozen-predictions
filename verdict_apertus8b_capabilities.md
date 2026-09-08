# Verdict: capability trajectories on Apertus-8B (frozen readings scored)
2026-09-08. Rules frozen in the private record (commit e047d78)
before any Apertus capability measurement. Same three probes as the
OLMo-2-1B three-worlds test (GSM8K-200 full-solution loss,
HumanEval-164 body loss, HellaSwag-500 forced-choice), same 15
public checkpoints as the Apertus-8B fact trajectory (210B ->
14792B), bf16, identical at every mark. Stage boundaries from the
Apertus tech report, Table H.8: Stage 1 to 7038B; Stage 3
7038-12000B adds math web data (code share unchanged, lr unchanged);
Stage 5 13345-15000B is the lr cooldown together with
Clean-Wikipedia, instruction and code-edu data.

## Frozen readings and results
(i) PRIMARY. Acceleration A = rate(7232->11432B) / rate(2940->7232B)
    per probe; D = A(math)/A(code). H-DATA predicts D >= 1.5; H-LR
    predicts 0.67-1.5; below 0.67 = neither, reported.
    Result: A(math) 0.17, A(code) 0.50, D = 0.34 -> NEITHER.
    Reported as a miss-shaped result. Caveat: the run's largest
    GSM8K drop (-0.053) sits in 6014->7232B, the interval containing
    the 7038B switch, which the frozen PRE window absorbed; the
    probe records means only, and adjacent-mark GSM8K swings of
    +-0.03 are routine. The primary was under-powered as designed.
(ii) SECONDARY. FL(7232B) anchored at 210B: GSM8K 93.9%, HumanEval
    58.2%, HellaSwag 93.3% (73.7% against its best-ever mark; 500
    items). Frozen rule: >= 85% on 2 of 3 = the OLMo-1B pattern
    (everything front-loads together) breaks under this schedule.
    It breaks: math and commonsense front-load, facts (27.0%) and
    code (58.2%) do not.
(iii) EXPLORATORY, declared. Stage 5 (13112->14792B), one lr
    cooldown applied to all probes at once: HumanEval -0.067 (the
    run's largest), facts -0.348 (the run's largest), GSM8K -0.029
    (routine), HellaSwag -1.6pp (noise). The cooldown moved the two
    probes whose new data sources entered with it and left the other
    two flat. Across both Apertus fact-dips (2100->2940B,
    5014->6014B) no capability probe worsened beyond routine noise.

## Reading, kept narrow
Under a constant learning rate, what front-loads is what had its
data from the start; what arrives late is what has late data. The
learning-rate story alone does not explain the split. One model,
one seed, means only (no per-item significance on the capability
probes); a controlled placement experiment is the next step.

## Measured values
   210B  gsm 1.1726  he 0.9117  hs 54.8%
   420B  gsm 1.0875  he 0.8299  hs 56.6%
   840B  gsm 1.0503  he 0.7738  hs 57.2%
  1470B  gsm 1.0561  he 0.7805  hs 59.2%
  2100B  gsm 1.0297  he 0.7876  hs 60.6%
  2940B  gsm 1.0318  he 0.7679  hs 61.2%
  3780B  gsm 1.0086  he 0.7626  hs 60.0%
  5014B  gsm 1.0410  he 0.7665  hs 59.2%
  6014B  gsm 1.0142  he 0.7576  hs 60.8%
  7232B  gsm 0.9609  he 0.7234  hs 60.4%
  8492B  gsm 0.9832  he 0.7184  hs 59.6%
  9752B  gsm 0.9533  he 0.7122  hs 61.4%
 11432B  gsm 0.9489  he 0.7015  hs 62.0%
 13112B  gsm 0.9761  he 0.6548  hs 62.4%
 14792B  gsm 0.9472  he 0.5883  hs 60.8%

Raw values: cap_traj_apertus8b.jsonl (this repo).
