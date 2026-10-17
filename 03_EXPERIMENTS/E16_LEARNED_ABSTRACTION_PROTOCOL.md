# E16 — Can a Model Learn Abstract Form From Examples?

**Experiment ID:** E16-ODNA-LEARNED-FORM-01  
**Date:** 2026-10-17  
**Status:** exploratory negative/limitation test; two independent random seeds  
**Hypothesis under test:** H-DNA-05, specifically whether higher-order form can be learned from raw relational examples rather than supplied as hand-designed descriptors.

## Question

Can a generic message-passing neural network, trained only on graph labels and raw adjacency, learn a reusable representation of graph form that transfers to unseen graph sizes and survives mild edge corruption?

## Data

Four synthetic families:
- cycle;
- path;
- cycle with one added chord;
- two disjoint cycles.

Training sizes are 16, 20, and 24 nodes. Test sizes are 28, 32, and 36 nodes. Every graph is independently node-permuted. Training uses 2% edge deletion/addition; testing uses 0%, 2%, 5%, and 10% corruption.

Per seed:
- 40 training graphs per class per training size (480 training graphs total);
- 30 test graphs per class per test size and noise level (1,440 original test graphs);
- degree-preserving double-edge-swap null on each test graph (1,440 null graphs).

Two independent seeds: 16017 and 16018.

## Model

Three-layer message-passing neural network:
- input: constant node features plus the raw adjacency matrix;
- learned neighbor aggregation using adjacency multiplication;
- shared node-update weights;
- mean and max graph pooling;
- graph-label supervision only;
- no degree histogram, clustering, component count, spectral descriptor, positional encoding, or family-specific feature is supplied.

The model uses a standard local message-passing architecture. This choice is intentionally limited: the experiment asks what this model can learn without manually supplying global invariants.

## Null control

For each test graph, random double-edge swaps preserve node degrees while disrupting higher-order topology. The trained model is evaluated on these rewired graphs using the original labels. This is a stress/null condition, not a semantically equivalent graph.

## Metrics

Accuracy, class-wise accuracy, and 95% Wilson intervals. Summary intervals pool the two seed runs and are descriptive; two seeds are not sufficient for a strong confirmatory claim.

## Decision rule

Evidence for learned abstract-form transfer would require reproducible accuracy clearly above 25% chance across held-out sizes and classes, not just success on path/chord classes, plus a meaningful drop under the degree-preserving null. A failure to distinguish cycle from two disjoint cycles is recorded as a model limitation, not hidden or repaired after seeing the result.

## Limitations

This is a synthetic architecture test, not biology. Graph families are selected by us. A negative result constrains this particular message-passing architecture; it does not prove that no model can learn abstractions. The experiment is exploratory and requires broader seeds and alternative architectures before general conclusions.
