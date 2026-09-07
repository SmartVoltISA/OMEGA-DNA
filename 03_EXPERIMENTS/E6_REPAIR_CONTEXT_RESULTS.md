# E6.2 — Repair Context

**Status:** executed controlled architecture experiment; synthetic, not biological proof.

## Objective
Test whether repair outcome requires damage and locus context beyond local sequence.

## Protocol
30 seeds; 5,000 samples/seed; 70/30 holdout; sequence-only vs sequence + damage/chromatin context; shuffled-relation null; AUROC.

## Results
| Model | AUROC mean ± SD |
|---|---:|
| sequence-only | 0.498874 ± 0.013982 |
| relational/context | **0.928113 ± 0.006533** |
| shuffled relation | 0.509134 ± 0.127233 |

Paired relational vs sequence: **t=162.064, p=1.9237e-44**.

## Interpretation
Context adds predictive information in the controlled generator and survives holdout. The shuffled relation control returns toward chance. Architecture result only.

## Biological gate
Open: replace synthetic variables with measured lesion/repair kinetics and chromatin context.
