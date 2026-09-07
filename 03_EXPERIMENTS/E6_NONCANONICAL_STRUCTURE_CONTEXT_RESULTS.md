# E6.5 — Non-Canonical DNA Structure Context

**Status:** executed controlled architecture experiment; synthetic, not biological proof.

## Objective
Test whether a context-dependent DNA structural state can add predictive information beyond local sequence features.

## Results
| Model | AUROC mean ± SD |
|---|---:|
| sequence-only | 0.496320 ± 0.017299 |
| structural-context | **0.906359 ± 0.007079** |
| shuffled context | 0.497481 ± 0.121137 |

Paired structural-context vs sequence: **t=129.330, p=1.324e-41**.

## Interpretation
The controlled experiment supports treating non-canonical structure as a typed, context-dependent state rather than an exception outside the architecture. It is not evidence that a particular biological structure has this predictive effect in vivo.

## Biological gate
Open: use experimentally measured G-quadruplex/i-motif or other non-canonical-structure maps with matched chromatin/state measurements.
