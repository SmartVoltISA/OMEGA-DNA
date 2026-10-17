# E15 — Confirmatory Test of Higher-Order Form Memory

**Experiment ID:** E15-ODNA-FORM-TRANSFER-01  
**Protocol frozen:** 2026-10-17, before E15 execution  
**Status:** confirmatory synthetic computational test; biological relevance not assumed  
**Hypothesis:** H-DNA-05

## Question

Does a representation that includes higher-order graph invariants generalize to unseen graph sizes better than local degree statistics and density alone, when the graph families are deliberately more confusable than E14?

## Graph families

1. **Cycle:** one closed path.
2. **Path:** one open path.
3. **Cycle with chord:** a cycle plus one additional edge joining opposite nodes.
4. **Two disjoint cycles:** two disconnected cycles of equal size.

These classes are designed to share local degree patterns in important pairs: a cycle and two disjoint cycles have the same degree distribution before corruption; path and cycle differ mainly at endpoints; cycle-with-chord introduces a small local perturbation plus a higher-order cycle change.

## Models

- **Local model:** logistic regression on degree histogram and normalized degree quantiles only.
- **Form model:** same local features plus density, clustering, transitivity, largest-component fraction, component count normalized by n, and cycle rank normalized by n.
- **Density-only baseline:** logistic regression on edge density.
- **Raw adjacency exemplar:** 1-nearest-neighbor over flattened adjacency matrices, evaluated only at n=28.

The models share the same train/test labels, training sample counts, and low-noise training distribution. The form model has more features; this is an explicit ablation test, not a compute- or parameter-matched proof that abstraction is inherently superior.

## Frozen protocol

- Train abstract/local/density models at n = 16, 20, 24.
- 400 training examples per family per size.
- Training edge deletion and addition rates: 2% each.
- Test at n = 28, 32, 36.
- 250 test examples per family per size and noise condition.
- Test edge deletion/addition rates: 2%, 5%, 10%, 20%.
- Node labels are randomly permuted independently for every graph.
- Train and test seeds are disjoint and fixed in the runner.
- Primary metric: balanced accuracy.
- Uncertainty: 95% Wilson intervals; paired bootstrap (10,000 resamples) for form-minus-local and form-minus-density differences.
- Secondary analysis: confusion matrices by class and performance by graph size.

## Null and decision rule

Primary null: adding higher-order form descriptors does not improve balanced accuracy over local degree descriptors on held-out sizes. Evidence for the narrow hypothesis requires positive paired differences with 95% bootstrap intervals excluding zero at 2%, 5%, and 10% test noise, and no dependence on node identity.

The 20% corruption condition is a stress test, not a required pass.

## Falsifiers and limitations

Failure to improve over the local model at low/moderate noise weakens the hypothesis. Success only on familiar sizes, or collapse under node permutation, also weakens it. The test uses synthetic graph families and hand-designed features; it cannot establish biological abstraction, life, consciousness, or spontaneous discovery of the right abstraction. Results are valid only for this declared benchmark.
