# E15 — Confirmatory Form-Transfer Test: Corrected Rerun

**Date:** 2026-10-17  
**Status:** corrected computational rerun; independent reproduction still required  
**Protocol:** `E15_ABSTRACTION_CONFIRMATORY_PROTOCOL.md`  
**Runner:** `E15_ABSTRACTION_CONFIRMATORY_RUNNER.py`

## Execution integrity

The first execution was invalid because integer rounding caused the effective edge-addition noise to depend on graph size. That run is excluded. The runner was corrected to use Bernoulli edge additions with an expected count proportional to the original edge count. The results below come only from the corrected implementation. Because the correction followed an initial run, these numbers should be treated as provisional until independently reproduced.

## Design

- Four deliberately confusable graph families: cycle, path, cycle with chord, two disjoint cycles.
- Training: sizes 16, 20, 24; 400 examples per class per size; 2% deletion/addition.
- Testing: sizes 28, 32, 36; 250 examples per class per condition.
- Test deletion/addition rates: 2%, 5%, 10%, 20%.
- Fresh seeds and random node relabeling.
- Models: local degree-only descriptors, local + higher-order form invariants, density-only, and raw-adjacency exemplar memory at n=28.
- 1,000 test graphs per noise/size cell; 12,000 test graphs total.
- Accuracy intervals are 95% Wilson intervals; model differences use paired bootstrap intervals with 10,000 resamples.

## Results

| Noise | Nodes | Form model accuracy (95% CI) | Local degree-only | Density-only | Raw adjacency exemplar* |
|---:|---:|---:|---:|---:|---:|
| 2% | 28 | 67.1% [64.1, 69.9] | 48.8% | 25.0% | 26.0% |
| 2% | 32 | 64.9% [61.9, 67.8] | 48.1% | 25.0% | N/A |
| 2% | 36 | 58.1% [55.0, 61.1] | 45.4% | 25.0% | N/A |
| 5% | 28 | 46.7% [43.6, 49.8] | 38.8% | 25.0% | 27.6% |
| 5% | 32 | 43.5% [40.5, 46.6] | 35.4% | 25.0% | N/A |
| 5% | 36 | 42.6% [39.6, 45.7] | 35.1% | 25.0% | N/A |
| 10% | 28 | 33.4% [30.5, 36.4] | 28.8% | 25.0% | 28.1% |
| 10% | 32 | 32.6% [29.8, 35.6] | 29.7% | 25.0% | N/A |
| 10% | 36 | 29.0% [26.3, 31.9] | 26.2% | 25.0% | N/A |
| 20% | 28 | 25.8% [23.2, 28.6] | 23.9% | 25.0% | 25.7% |
| 20% | 32 | 26.0% [23.4, 28.8] | 24.6% | 25.0% | N/A |
| 20% | 36 | 24.9% [22.3, 27.7] | 22.4% | 25.0% | N/A |

\*The raw-adjacency exemplar is only defined for the fixed graph size n=28. Chance accuracy is 25% for four balanced classes.

## Paired differences: form minus local model

| Noise | n=28 | n=32 | n=36 |
|---:|---:|---:|---:|
| 2% | +18.3 pp [15.7, 21.0] | +16.8 pp [14.0, 19.6] | +12.7 pp [9.9, 15.6] |
| 5% | +7.9 pp [5.5, 10.4] | +8.1 pp [5.4, 10.8] | +7.5 pp [4.9, 10.1] |
| 10% | +4.6 pp [2.5, 6.8] | +2.9 pp [0.9, 4.9] | +2.8 pp [0.6, 5.0] |
| 20% | +1.9 pp [0.3, 3.5] | +1.4 pp [0.0, 2.8] | +2.5 pp [1.1, 4.0] |

At 2–10% corruption, the form model consistently outperformed the local degree-only model on unseen graph sizes. The advantage shrank substantially as corruption increased. At 20% corruption, the form model was near chance and did not reliably outperform density-only; the paired form-minus-density intervals included zero.

## Interpretation

**Narrow result:** higher-order graph descriptors added useful information beyond degree distribution for these four synthetic graph families, and the gain transferred to unseen graph sizes under low-to-moderate corruption.

**Important negative result:** the effect was not robust to heavy corruption. At 20% corruption, performance approached the 25% chance baseline. The abstraction did not make the system generally reliable; it provided a bounded advantage under specified conditions.

**What is not shown:** the model did not invent its own abstraction. We selected the descriptors in advance. This is a test of whether higher-order form representation helps, not a demonstration that abstraction spontaneously emerges from raw connections.

## Decision

H-DNA-05 receives **provisional support for the narrow computational claim** that explicit higher-order form descriptors can improve transfer beyond local degree statistics. E15 is not yet accepted as confirmatory until a clean independent run reproduces it. No biological or universal-law conclusion follows.
