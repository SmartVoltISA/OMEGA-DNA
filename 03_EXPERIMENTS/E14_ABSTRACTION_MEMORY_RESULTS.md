# E14 — Abstract Form Memory: Exploratory Results

**Run date:** 2026-10-17  
**Status:** exploratory pilot; not preregistered before initial analysis  
**Runner:** `E14_ABSTRACTION_MEMORY_RUNNER.py`  
**Protocol:** `E14_ABSTRACTION_MEMORY_PROTOCOL.md`

## Result summary

The abstract/form classifier was trained only on low-noise examples (5% edge deletion and 5% edge addition) at graph sizes 16, 24, and 28. It was tested on fresh, independently permuted examples at sizes 20, 32, 36, and 40, with edge deletion/addition levels of 5%, 15%, 30%, and 45%. Each test condition contains 900 graphs (300 per class).

| Test noise | Nodes | Abstract/form accuracy (95% Wilson CI) | Density-only accuracy | Raw adjacency exemplar accuracy* |
|---:|---:|---:|---:|---:|
| 5% | 20 | 100.0% [99.57, 100.0] | 73.0% | 100.0% |
| 5% | 32 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 5% | 36 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 5% | 40 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 15% | 20 | 100.0% [99.57, 100.0] | 70.6% | 99.3% |
| 15% | 32 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 15% | 36 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 15% | 40 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 30% | 20 | 100.0% [99.57, 100.0] | 71.6% | 95.6% |
| 30% | 32 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 30% | 36 | 100.0% [99.57, 100.0] | 66.7% | N/A |
| 30% | 40 | 99.9% [99.37, 99.98] | 66.7% | N/A |
| 45% | 20 | 87.7% [85.36, 89.66] | 68.3% | 93.4% |
| 45% | 32 | 88.7% [86.43, 90.58] | 66.7% | N/A |
| 45% | 36 | 84.3% [81.81, 86.56] | 66.7% | N/A |
| 45% | 40 | 83.8% [81.23, 86.04] | 66.7% | N/A |

\*The raw-adjacency exemplar model stores flattened adjacency patterns and is only defined for the fixed node count n=20. It is trained on n=20 examples and cannot directly score different-size graphs.

## Paired comparisons

At n=20, the abstract model's accuracy advantage over density-only was:
- 5% noise: +27.0 percentage points; paired bootstrap 95% CI +24.11 to +30.00 pp.
- 15% noise: +29.44 pp; CI +26.56 to +32.56 pp.
- 30% noise: +28.44 pp; CI +25.56 to +31.44 pp.
- 45% noise: +19.33 pp; CI +16.22 to +22.44 pp.

At held-out sizes n=32 and n=40, the abstract model exceeded density-only by approximately 33.3 percentage points at 5–30% noise. At 45% noise, the advantage remained positive but fell to 17.1–22.0 points depending on size.

At n=20, the abstract model and exact-adjacency exemplar tied at 5% noise. The exemplar was slightly worse at 15% and 30% noise (abstract advantage +0.67 pp, CI +0.22 to +1.22 pp; and +4.44 pp, CI +3.11 to +5.89 pp). At 45% noise, the exemplar performed better by 5.78 pp (paired 95% CI for abstract minus exemplar: -8.67 to -3.00 pp).

## Interpretation

**Supported in this synthetic task:** hand-designed graph-invariant features transfer across node relabeling and unseen graph sizes, and are more robust than density alone. They remain useful under substantial corruption, though performance drops at the highest tested noise level.

**Not supported:** universal superiority of abstraction over exact examples. At high corruption on the same graph size, the adjacency exemplar performed better. The result therefore suggests a tradeoff: form memory offers size/relabeling transfer; episodic adjacency memory can remain competitive when test conditions match its representation.

## Limits

- This is a synthetic classification benchmark, not a biological experiment.
- The graph families are structurally distinct and the feature set is hand-designed.
- The experiment tests transfer using a preselected abstraction representation; it does not show that a system autonomously invents abstractions.
- The exploratory implementation was iterated before the protocol was frozen. The numerical result is not confirmatory.
- No inference about life, consciousness, or a universal physical principle follows from this benchmark.

## Decision

**H-DNA-05: provisional support for the narrow computational prediction; no biological claim.** Keep the hypothesis open. The next gate is E15: freeze the runner and protocol, use fresh seeds, add more confusable graph families and matched-capacity controls, and evaluate whether the abstraction is learned rather than manually encoded in the feature extractor.
