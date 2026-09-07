# OMEGA-DNA — Full Relational Pass: Memory and Causal Layer

Date: 2026-09-07

## Completed chain

`sequence → local structure → typed relation → long-range relation → regulatory network → cellular state → feedback → history/memory → persistence → perturbation`

## E5 result

50 seeds, 4,000 samples/seed, 70/30 holdout.

- sequence/current-state AUROC: 0.50474 ± 0.02131
- relation-aware AUROC: 0.76850 ± 0.04281
- memory-aware AUROC: 0.86582 ± 0.01109
- relation vs sequence: t=41.46, p=8.12e-40
- memory vs sequence: t=111.69, p=1.18e-60

Causal perturbation:
- strongest-regulator effect: 0.01701 ± 0.01324
- random-regulator effect: 0.00693 ± 0.00735
- paired t=4.70, p=2.17e-05

## Verdict

Controlled computational memory and perturbation gates pass. The strongest new architectural result is that history can carry predictive information not recoverable from the intentionally matched current state, and explicit regulatory relations recover an intermediate amount of that information.

The perturbation test is supportive of causal sensitivity in the synthetic model, but is not a biological causal claim.

## Open biological boundary

The next decisive step remains real multi-omic/time-resolved data with independent regulatory annotations and perturbations. No biological numerical result is claimed by this pass.
