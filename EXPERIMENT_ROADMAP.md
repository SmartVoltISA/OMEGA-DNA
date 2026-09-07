# OMEGA-DNA — Experiment Roadmap

## E0 — Minimal complementarity model

**Question:** Can the graph formalism recover A↔T and G↔C as structural constraints without hard-coding the result as a symbol rule?

**Null:** unconstrained four-symbol pairing.

**Positive reference:** canonical Watson-Crick complementarity.

**Output:** constraint satisfaction, stability proxy, and recovery accuracy.

**Status:** design only.

## E1 — Sequence versus relation representation

**Question:** Does adding explicitly defined local relations improve prediction on a predefined DNA task?

**Baseline:** sequence-only model.

**Alternative:** sequence + declared relational features.

**Controls:** equal data split, fixed evaluation set, parameter accounting, ablation of each relation class.

**Primary metric:** task-specific predictive metric fixed before execution.

**Decision:** report effect size and uncertainty, not only winner/loser.

## E2 — Complementarity and information preservation

**Question:** Does explicit complementary structure improve robustness to partial sequence loss or corruption?

**Baseline:** single-strand sequence representation.

**Alternative:** paired relational representation.

**Perturbations:** controlled deletion/substitution of symbols.

**Output:** recovery accuracy as a function of corruption level.

## E3 — Maintenance as feedback

**Question:** Can replication and repair be represented as maintenance loops that quantitatively predict persistence/error behavior?

**Model:** state → perturbation → detection → correction → new state.

**Null:** perturbation without feedback.

**Output:** persistence, error rate, recovery time, and sensitivity to perturbation.

## E4 — Structure and function

**Question:** Do relational/context features explain functional differences beyond sequence alone for a carefully selected biological dataset?

**Requirement:** choose one concrete function and one public dataset before preregistration.

**Critical control:** prevent leakage from labels, homologous sequences, or duplicated samples.

## E5 — Multiscale propagation

**Question:** When a relation changes at one level, which higher-level observables change?

**Direction:** local molecular perturbation → structural change → accessibility/regulation → measurable output.

**Goal:** test whether the proposed layer chain predicts propagation better than an unstructured feature set.

## Research status

All experiments above are proposals. No result is claimed until preregistration, execution, controls, and reproducibility checks are completed.
