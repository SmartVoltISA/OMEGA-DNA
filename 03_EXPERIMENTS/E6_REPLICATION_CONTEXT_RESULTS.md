# E6.1 — Replication Context

**Status:** executed controlled architecture experiment; synthetic, not biological proof.

## Objective
Test whether replication outcome requires locus context beyond local sequence.

## Protocol
30 seeds; 5,000 samples/seed; 70/30 holdout; sequence-only vs sequence + origin/accessibility/timing; relation-shuffled null; AUROC primary endpoint.

## Results
| Model | AUROC mean ± SD |
|---|---:|
| sequence-only | 0.496564 ± 0.013866 |
| relational/context | **0.952626 ± 0.005685** |
| shuffled relation | 0.510516 ± 0.169613 |

Paired relational vs sequence: **t=187.234, p=2.935e-46**.

## Interpretation
Replication context adds predictive information in the controlled generator and survives an independent holdout. The shuffled relation control returns toward chance. This is an architecture result, not biological proof.

## Biological gate
Open: replace synthetic origin/accessibility/timing variables with independently measured replication-origin and replication-timing data.
