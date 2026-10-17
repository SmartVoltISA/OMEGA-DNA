# E14 — Abstract Form Memory: Protocol and Status

**Experiment ID:** E14-ODNA-ABSTRACT-MEMORY-01  
**Date:** 2026-10-17  
**Status:** exploratory computational pilot; protocol frozen for reproduction, but not preregistered before initial analysis  
**Hypothesis:** H-DNA-05 in `HYPOTHESES.md`

## Question

Can a compact, node-relabeling-invariant representation of graph form transfer to unseen graph sizes and tolerate corruption better than a memory of exact adjacency examples or a density-only baseline?

## Task

Classify synthetic graphs into three families:
- cycle;
- star;
- two dense cliques joined by one bridge.

For each graph, randomly permute node identities, delete a fraction of original edges, and add a small fraction of edges from the non-edge set. Node IDs therefore have no stable semantic meaning.

## Models

1. **Abstract/form model:** logistic regression over general graph descriptors: degree histogram, density, clustering, transitivity, connected-component summaries, normalized cycle rank, and normalized degree quantiles. These features are hand-designed and are not claimed to emerge spontaneously.
2. **Episodic edge-memory baseline:** 1-nearest-neighbor over flattened adjacency matrices using Hamming distance. It is only applicable to the fixed node count n=20.
3. **Density-only baseline:** logistic regression using graph density alone.

## Split and perturbations

- Training for the abstract model: n = 16, 24, 28; 500 graphs per family per size; 5% edge deletion and 5% edge addition.
- Episodic baseline training: n = 20; 500 graphs per family; same low-noise setting.
- Density baseline training: n = 16, 24, 28; 500 graphs per family per size.
- Test: n = 20, 32, 36, 40; 300 graphs per family per condition.
- Test edge deletion/addition rates: 5%, 15%, 30%, 45%.
- All test seeds are distinct from training seeds.
- Node identities are independently permuted.
- Primary metric: balanced accuracy (the test set is class-balanced).
- Uncertainty: 95% Wilson intervals for accuracy; paired bootstrap intervals (10,000 resamples) for per-example accuracy differences.

## Null and falsification

The minimal null is that the abstract model does not outperform density-only on held-out sizes. The exact-edge baseline provides a second comparison at n=20. Failure to transfer across sizes, failure at moderate corruption, or non-replication under fresh seeds would weaken H-DNA-05.

## Result discipline and limitations

This pilot was iterated during exploratory analysis, so it cannot be represented as a preregistered confirmatory result. The graph families are deliberately distinct; the descriptor set is hand-designed; and the task is classification, not self-maintenance, biological prediction, consciousness, or spontaneous discovery of abstractions. A confirmatory E15 must freeze the code and use fresh seeds before running.
