# E6.3 — Evolutionary Context / Memory

**Status:** executed controlled architecture experiment; synthetic, not biological proof.

## Objective
Test whether present outcome can require evolutionary context beyond local sequence.

## Protocol
30 seeds; 5,000 samples/seed; 70/30 holdout; sequence-only vs sequence + conservation/allele-frequency/lineage context; shuffled null; AUROC.

## Results
| Model | AUROC mean ± SD |
|---|---:|
| sequence-only | 0.497901 ± 0.013120 |
| relational/context | **0.853976 ± 0.010355** |
| shuffled relation | 0.523818 ± 0.091629 |

Paired relational vs sequence: **t=116.999, p=2.408e-40**.

## Interpretation
Historical context adds predictive information in the controlled generator and survives holdout. This formalizes evolutionary history as a separate relation layer; it does not imply conservation itself proves function.

## Biological gate
Open: use multi-species alignments, population variation and independent functional assays.
