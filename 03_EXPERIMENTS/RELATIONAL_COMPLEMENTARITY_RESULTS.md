# OMEGA-DNA — Relational Complementarity Test Suite

Date: 2026-09-07  
Status: complete synthetic/architectural pass; real-data benchmark gate defined but not claimed as executed.

## 1. Question

Can the OMEGA architecture add information that is not already present in a sequence-only representation?

The test is deliberately stricter than "the graph description fits biology". A useful addition must survive:

1. sequence-only baseline;
2. relation-shuffled null;
3. untyped relation baseline;
4. static-state baseline;
5. node-relabeling / invariance check;
6. perturbation of relations;
7. repeated seeds with statistical comparison.

A positive toy result is only an architectural proof-of-capacity. It is not evidence of a new biological mechanism.

## 2. Executed tests

| Test | OMEGA claim tested | Result | Interpretation |
|---|---|---:|---|
| E2 | Complementary relation creates a consistency constraint | PASS | Coupled redundant state detects corruption in the toy model |
| E3 | Maintenance/feedback is distinct from stored state | PASS | Correction strongly lowers persistent error |
| E4 | Relation type can carry information invisible to topology | PASS | Typed relation invariant reaches 1.00 accuracy; untyped topology 0.50 |
| E5 | Memory can require history, not only current state | PASS | Static state 0.649 accuracy; history-aware representation 1.00 |
| E6 | Function can depend on context/relations, not local sequence alone | PASS | Sequence-only 0.506; relation-aware 1.00 |
| E7 | Relations can add predictive information beyond sequence | PASS | Combined AUC 1.00 vs sequence-only ~0.498; shuffled relation null ~0.495 |
| E8 | Typed relational representation is invariant to node relabeling | PASS | Invariant error 0.000; positional control error ~0.472 |

## 3. E2 — Complementarity

50,000 trials per length, mutation probability 0.001, seed 11.

Observed damage / mismatch detection:

- L=10: damage 0.01480; detection 0.01480.
- L=100: damage 0.13914; detection 0.13912.
- L=1000: damage 0.77774; detection 0.77770.

The result is exactly what the architectural hypothesis predicts: a second coupled state supplies a consistency constraint. It does **not** identify the correct strand and is not autonomous repair.

## 4. E3 — Maintenance feedback

100,000 trials, 100 steps, damage=0.002/step, detection=0.95, correction=0.98, seed 7.

Mean residual errors per trial:

- no feedback: 0.20015
- detection only: 0.20164
- detection + correction: 0.00012

Therefore detection alone does not constitute maintenance. The architecture requires the loop:

`state → deviation → detection → correction → new state`.

## 5. E4 — Typed relations

The topology was identical in both classes. Only the binary relation types around a closed cycle carried the class information.

- typed relational representation: 1.00 accuracy;
- untyped topology-only representation: 0.50 accuracy.

This is a direct demonstration that `relation type` is not equivalent to `edge existence`.

## 6. E5 — Memory

The label depended on the trajectory/history of a binary state. The final state alone was insufficient.

- current-state baseline: 0.649 accuracy;
- history-aware representation: 1.00 accuracy.

This supports the OMEGA distinction between stored structure and maintenance/history state. It does not prove that every biological memory mechanism has the proposed form.

## 7. E6 — Context

Local sequence features were deliberately insufficient. The target depended on whether two elements were related in a contextual graph.

- sequence-only accuracy: ~0.506;
- relation-aware accuracy: 1.00.

This is the cleanest toy demonstration of the proposed architecture's intended complement: sequence describes local content; relations can encode context.

## 8. E7 — Ablation + null

30 independent seeds, n=10,000 per run.

Mean AUC ± SD:

- sequence-only: 0.4985 ± 0.0078
- relations-only: 0.5002 ± 0.0105
- combined: 1.0000 ± 0.0000
- shuffled-relation null: 0.4947 ± 0.0371

Paired tests across the 30 seeds:

- combined vs sequence-only: t=350.75, p=3.68×10^-54
- shuffled relation null vs sequence-only: t=-0.55, p=0.587

The null behaves as expected: arbitrary relation labels do not add reliable information. The true relational representation does.

## 9. E8 — Invariance

A typed relational invariant was evaluated before and after random node relabeling.

- relational invariant error: 0.000
- positional first-edge control error: ~0.472

This supports using relational invariants rather than accidental node ordering as architecture-level features.

## 10. What survives

The synthetic suite establishes five nontrivial properties of the OMEGA representation:

1. **Redundancy can become a consistency constraint.**
2. **Relations need explicit types.**
3. **Memory can be represented as persistence/history, not only a snapshot.**
4. **Context can carry information absent from local sequence content.**
5. **A valid relation channel can add information, while a shuffled relation channel does not.**

These are architectural properties, not discoveries about DNA.

## 11. Comparison with existing genomics work

Modern sequence models already cover a large part of the territory we initially hoped would be distinctive. Enformer integrates long-range sequence interactions up to roughly 100 kb and predicts chromatin/gene-expression tracks; it outperformed Basenji2 on several benchmark measures. citeturn0search1

Recent benchmarks also show that specialized sequence-to-function models remain stronger than generic DNA foundation embeddings on several functional-genomics tasks, while long-context models improve some tasks. citeturn0search2turn0search6

DeepSEA established sequence-to-chromatin prediction from 1-kb DNA windows and 919 chromatin features, with chromosome-held-out evaluation. citeturn1search1turn1search5

Therefore the claim "DNA is a network with long-range relations" is **not novel by itself**. Existing models already learn interactions and long-range dependencies.

## 12. Where OMEGA may actually complement existing work

The remaining potentially useful distinction is not another generic graph layer. It is an explicit, typed, dynamic state model whose edges have declared biological semantics and whose state changes are tested as interventions:

`state → typed relations → constraint → process → changed state → maintenance`.

Potentially complementary targets:

### A. Explicit relation semantics

Instead of one learned attention/edge channel, retain separate relation classes such as:

- chemical;
- complementary;
- topological;
- spatial/3D;
- regulatory;
- replication;
- repair;
- epigenetic/contextual;
- evolutionary.

The hypothesis is useful only if typed relations improve prediction or intervention performance after controlling parameter count and information content.

### B. Dynamic genome state

Current sequence-to-function models are excellent at sequence-conditioned prediction, but personal-genome studies show limitations in predicting individual expression variation and variant-effect direction. citeturn0search0turn0search5

This leaves a concrete test: does adding measured state/context relations improve out-of-sample individual or cell-state prediction beyond the sequence model?

### C. Maintenance and repair

Recent expert reviews emphasize that DNA repair depends on chromatin state, chromosome topology, nuclear compartments, loop extrusion and dynamic genome organization. citeturn0search2turn0search4

This is closer to the OMEGA architecture than a static sequence classifier because the biological system is explicitly dynamic and maintenance-oriented.

### D. Causal intervention

A graph becomes scientifically interesting when removing or changing a declared relation produces a predicted change in an observable outcome. A higher score on a passive prediction benchmark is not enough.

## 13. What failed / what is not established

No experiment in this suite establishes:

- a new DNA mechanism;
- a new repair pathway;
- a new physical law;
- causal superiority over Enformer/Basenji2/AlphaGenome/other current models;
- improved performance on a real biological dataset.

The real-data benchmark remains the decisive gate.

## 14. Real-data gate

The appropriate next benchmark is a controlled comparison on a public functional-genomics dataset with:

`sequence-only` vs `sequence + measured typed relations/state`.

Candidate benchmark families include DeepSEA/ENCODE chromatin prediction, Enformer long-range regulatory prediction, and DNALongBench. DNALongBench explicitly frames long-range regulatory sequence activity as prediction of epigenomic/transcriptional profiles from 196,608-bp DNA windows. citeturn1search1turn0search11

The benchmark must use the same splits, same target, matched model capacity, relation-shuffle null, and ablations. A gain of the combined model over the sequence baseline is the criterion for claiming complementarity.

The public 5,000-row smoke dataset located during this pass was 15.3 MB and was not directly readable through the connected GitHub file interface; therefore no fabricated real-data result is reported. fileciteturn41file0

## 15. Final scientific verdict

**OMEGA-DNA passes the architectural complementarity test, but not yet the biological novelty test.**

More precisely:

- `architecture can add information`: **YES, demonstrated in controlled toy systems**;
- `architecture is compatible with known DNA biology`: **YES**;
- `architecture already exists implicitly in modern models`: **YES, to a substantial degree**;
- `explicit typed/dynamic relations add measurable information on real biological data`: **NOT YET ESTABLISHED**;
- `OMEGA has discovered a new biological principle`: **NO EVIDENCE YET**.

The project therefore should not claim that it replaces existing genomics models. The scientifically defensible claim is narrower and stronger: **OMEGA provides a testable representation for making relation type, state, persistence, maintenance and intervention explicit, and this representation is now ready for a controlled real-data benchmark.**
