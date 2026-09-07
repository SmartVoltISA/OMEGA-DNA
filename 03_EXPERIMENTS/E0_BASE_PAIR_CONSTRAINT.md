# E0 — Base-pair constraint

**Status:** preregistration draft; no result claimed.

## Research question

Can a relational model recover canonical DNA base-pair constraints without simply inserting the known A-T/G-C rule as a hard-coded answer?

## Hypothesis

H-DNA-02: complementarity can be represented as a structural constraint arising from declared molecular properties.

## Null hypothesis

A symbolic pairing table is sufficient for the target task; adding relational structure provides no reproducible benefit after accounting for model complexity.

## Critical design requirement

The target task, input representation, scoring metric and acceptance criterion must be fixed before execution.

## Candidate observables

- compatibility score;
- predicted pairing preference;
- structural stability proxy;
- robustness under perturbation.

These are candidate metrics only until one is preregistered for a concrete experiment.

## Controls

**Negative control:** randomized pairing assignments preserving the same number of pair relations.

**Positive control:** canonical A-T/G-C pairing may be used only as an independently established reference, not as evidence for the new model.

## Falsification

Reject H-DNA-02 for the tested abstraction if the relational model cannot outperform the declared symbolic/null baselines under the preregistered metric, or if the result depends on post-hoc parameter selection.

## Current conclusion

No conclusion. This file defines the test boundary only.