# E7 Architecture Self-Stress Test — 2026-09-07

## Purpose

Test whether the OMEGA-DNA relational layer behaves selectively rather than winning by default.

The suite contains four controlled cases:

1. **Sequence sufficient:** sequence already contains the target information; relations should add little or nothing.
2. **Relation needed:** target contains information unavailable to sequence; relations should improve prediction.
3. **Relation redundant:** relational features duplicate information already present in sequence; no meaningful gain should occur.
4. **Causal relation proxy:** target depends on a relational variable; relation-aware prediction should improve and shuffled relations should collapse.

Protocol: 30 independent seeds, 5,000 samples/seed, fixed 70/30 holdout, logistic regression, AUROC, paired seed-wise t-test.

## Results

| Case | Sequence AUROC | Relational AUROC | Paired test |
|---|---:|---:|---:|
| Sequence sufficient | 0.992625 ± 0.001524 | 0.992471 ± 0.001590 | t=-3.465, p=0.00167 |
| Relation needed | 0.524284 ± 0.012339 | 0.987230 ± 0.002014 | t=208.116, p=1.37e-47 |
| Relation redundant | 0.991499 ± 0.001515 | 0.991409 ± 0.001529 | t=-3.584, p=0.00122 |
| Causal relation proxy | 0.501404 ± 0.013713 | 0.993618 ± 0.000934 | t=194.871, p=9.21e-47 |

Shuffled relation controls:

- Relation-needed shuffled AUROC: **0.523227 ± 0.012037**
- Causal-relation shuffled AUROC: **0.499204 ± 0.014453**

## Interpretation

The stress test behaves as intended. When sequence is sufficient or relations are redundant, adding unrelated relational features does not create a useful gain. When the target contains independent relational information, the relational model recovers it, while shuffled relations collapse toward chance.

The small negative differences in the sequence-sufficient/redundant cases are not interpreted as evidence that relations are harmful; they are finite-sample/model noise around an already near-ceiling sequence baseline.

This is a **synthetic architecture validation**, not biological evidence.

## Consequence for OMEGA-DNA

The architecture now has a negative-control principle at the architectural level:

> A relational layer should earn its predictive contribution; it must not be assumed useful merely because it exists.

The next stronger test is to apply the same logic to real biological data with independent labels, leakage-safe holdout, capacity-matched baselines and provenance tracking.
