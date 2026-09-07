# E6.4 — Variant Context / Functional Effect

**Status:** executed controlled architecture experiment; synthetic, not biological proof.

## Objective
Test whether variant-associated outcome can require regulatory context beyond local sequence.

## Protocol
30 seeds; 5,000 samples/seed; 70/30 holdout; sequence-only vs sequence + variant/regulatory/chromatin context; shuffled null; AUROC.

## Results
| Model | AUROC mean ± SD |
|---|---:|
| sequence-only | 0.498848 ± 0.013657 |
| relational/context | **0.926926 ± 0.006123** |
| shuffled relation | 0.518895 ± 0.122699 |

Paired relational vs sequence: **t=183.780, p=5.034e-46**.

## Interpretation
Variant context adds predictive information in the controlled generator and survives holdout. The experiment formalizes variant → relation → functional-effect as a distinct layer, without claiming biological causality.

## Biological gate
Open: test against ClinVar/dbSNP or population variants paired with independent molecular/phenotypic assays, with strict ancestry/population and chromosome holdouts where appropriate.
