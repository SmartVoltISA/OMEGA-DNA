# E16 — Learned Abstraction From Raw Graph Examples: Results

**Status:** exploratory limitation test; two independent model/data seeds (16017, 16018)  
**Runner:** `E16_LEARNED_ABSTRACTION_RUNNER.py`  
**Protocol:** `E16_LEARNED_ABSTRACTION_PROTOCOL.md`

## Headline

The generic message-passing model did **not** learn a reliable reusable abstraction across these graph families. At zero corruption it reached 75% accuracy, but this was misleading: across the two seeds it learned to classify path and cycle-with-chord correctly, while the cycle versus two-disjoint-cycles distinction flipped between seeds. This is the expected limitation of a local message-passing model with constant initial node features: all nodes in both clean cycle families have the same degree and the same local neighborhoods, so the model has no signal to distinguish one connected cycle from two disconnected cycles.

Under edge corruption, overall performance fell toward chance (25% for four balanced classes).

## Pooled results

The table pools two runs, each with 30 test examples per class, size, and noise condition. N=240 per row; intervals are descriptive Wilson intervals.

| Test corruption | Nodes | Accuracy (95% CI) | Chance |
|---:|---:|---:|---:|
| 0% | 28 | 75.0% [69.2, 80.1] | 25% |
| 0% | 32 | 75.0% [69.2, 80.1] | 25% |
| 0% | 36 | 75.0% [69.2, 80.1] | 25% |
| 2% | 28 | 47.1% [40.9, 53.4] | 25% |
| 2% | 32 | 43.8% [37.6, 50.1] | 25% |
| 2% | 36 | 41.2% [35.2, 47.6] | 25% |
| 5% | 28 | 35.8% [30.0, 42.1] | 25% |
| 5% | 32 | 34.2% [28.5, 40.4] | 25% |
| 5% | 36 | 32.9% [27.3, 39.1] | 25% |
| 10% | 28 | 33.3% [27.7, 39.5] | 25% |
| 10% | 32 | 32.1% [26.5, 38.2] | 25% |
| 10% | 36 | 32.9% [27.3, 39.1] | 25% |

## Class-level diagnosis

At 0% corruption:
- Path accuracy: 100% in both seeds.
- Cycle-with-chord accuracy: 100% in both seeds.
- Cycle and two-disjoint-cycles: the model's preference flipped across seeds. Each class reached 50% pooled accuracy, but not because the model robustly recognized both forms.

At 2–10% corruption, performance was uneven: the model retained some ability to identify paths and chorded cycles, but recognition of the two regular cycle families collapsed.

## Negative control

Degree-preserving edge rewiring disrupts the original topology while retaining local degree sequences. In this test, the model's scores on the rewired graphs remained close to those on the original graphs for many conditions. This is a warning sign: the learned representation relied heavily on local degree/neighborhood patterns rather than reliably capturing the global graph form. It is not evidence of successful abstract-form memory.

## Decision

**E16 does not support the claim that this generic message-passing model learned a robust higher-order abstraction.** It identifies a clear boundary: local message passing with constant node features can fail to distinguish global forms that share the same local structure.

This is a useful negative result, not a refutation of H-DNA-05 in general. The next experiment should use a genuinely higher-order learner (for example, pair-state / 2-WL-style message passing) and compare it with the same local MPNN and hand-designed E15 features. The model, controls, and decision criteria must be fixed before running that comparison.
