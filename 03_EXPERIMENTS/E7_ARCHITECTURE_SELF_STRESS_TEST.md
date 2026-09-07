# E7 Architecture Self-Stress Test

## Purpose
Test whether the OMEGA relational channel is falsely rewarded merely because it is present.

## Controlled cases
30 seeds × 5,000 samples/seed; 70/30 split; fixed logistic-regression evaluator.

| Case | Sequence-only | + relations | Interpretation |
|---|---:|---:|---|
| Sequence already sufficient | 0.9926 | 0.9925 | relation adds no value |
| Relations necessary | 0.5243 | 0.9872 | relation carries independent information |
| Relation redundant | 0.9915 | 0.9914 | redundant channel stays redundant |
| Relation duplicates sequence | ~0.991 | ~0.991 | no artificial gain |
| Causal-information control | ~0.499 | ~0.9936 | independent relational signal recoverable |

Relation-shuffled nulls were approximately chance (~0.5232 and ~0.4992 in the informative controls).

## Conclusion
The architecture/evaluator can distinguish useful relations from redundant relations in controlled data. This is a guard against architectural confirmation bias. It is **not biological evidence**.

The real E6 benchmark must reproduce this discipline with capacity matching, chromosome-level holdout, independently measured relations and independent labels.
