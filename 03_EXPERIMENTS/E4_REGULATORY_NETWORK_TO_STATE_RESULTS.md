# E4 — Regulatory Network → Cellular State → Feedback

**Status:** controlled computational gate completed; biological gate remains open.

## Protocol
- 50 independent seeds
- 20 regulators, 100 target genes
- 12 temporal states per run
- temporal holdout: first 8 states train, final 4 test
- sequence/state-only baseline
- explicit regulatory-message model
- full topology model: message + degree + signed nonlinear regulatory channel
- feedback correction compared with no-feedback control

## Primary endpoint: AUROC

| Model | AUROC |
|---|---:|
| Sequence/state only | **0.91914 ± 0.02088** |
| Relational state | **0.96714 ± 0.00996** |
| Full topology/state | **0.96709 ± 0.01004** |

Paired AUROC relational vs sequence: **t = 21.3460, p = 1.83×10⁻²⁶**.

Paired AUROC full topology vs sequence: **t = 21.1229, p = 2.91×10⁻²⁶**.

The direct relational channel captures essentially all of the available network gain in this synthetic system; therefore the result is not overclaimed as evidence that every graph statistic adds independent information.

### Feedback gate
Mean prediction/control error:

- no feedback: **0.530745 ± 0.026956**
- feedback correction: **0.514994 ± 0.024866**
- paired t = **−45.91**, p = **6.18×10⁻⁴²**

## Interpretation

The controlled gate passes. Explicit regulatory relations substantially improve prediction of future cellular state over the sequence/state-only representation. Feedback correction further reduces state error.

Architectural transition supported by this controlled system:

`regulatory network → cellular state → feedback → maintained/updated state`

This remains a synthetic systems result. It does not establish a biological regulatory mechanism or a specific human gene network.

## Biological gate

The real gate requires independently measured/annotated TF binding, chromatin accessibility, 3D contacts and expression/state data with chromosome/cell-group holdout and relation-shuffle nulls. No real biological AUROC is claimed here.
