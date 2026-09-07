# OMEGA-DNA — How to Use

## Purpose

OMEGA-DNA is a research architecture for studying DNA as a system of sequence, structure, typed relations, cellular state, processes, persistence and measurable outputs.

It is not a claim that DNA is already decoded. It is a framework for organizing and testing such claims.

## Core chain

```text
sequence
→ local structure
→ typed relations
→ regulatory architecture
→ 3D organization
→ cellular state
→ process
→ measurable output
→ feedback / maintenance
→ persistence / memory
→ future response
```

## For a researcher

1. Define one biological question.
2. State H1 and H0 before analysis.
3. Identify the biological unit and condition.
4. Record assembly, accession, assay, sample and provenance.
5. Build a sequence-only baseline.
6. Add only relations that are available independently of the target label.
7. Use a relation-shuffled null.
8. Use a biologically meaningful holdout where possible: chromosome, cell type, individual or species.
9. Fix primary metrics before the final test.
10. Report effect size, uncertainty and limitations.
11. Separate observation, inference, hypothesis and established biological evidence.
12. If data are missing, leave the gate OPEN; never fabricate a result.

## For an AI

The AI should act as a research instrument, not as an authority.

```text
question
→ data audit
→ hypothesis
→ preregistration
→ baseline
→ relational model
→ controls
→ holdout
→ analysis
→ robustness
→ interpretation
→ provenance
→ next test
```

The AI must not silently change the hypothesis, split, metric or acceptance criterion after seeing the test result.

The AI must not convert synthetic experiments into biological evidence.

## Region representation

```yaml
location:
sequence:
sequence_features:
local_structure:
relations:
architecture:
state:
processes:
outputs:
persistence:
evidence_class:
source:
confidence:
```

Missing information is `UNKNOWN`, not `FALSE`.

## Evidence classes

- `OBSERVED` — directly measured.
- `ANNOTATED` — independently annotated by a recognized source.
- `INFERRED` — derived from measured data or a model.
- `HYPOTHESIS` — proposed and not established.
- `UNKNOWN` — currently unresolved.

## Causality

A correlation is not a causal claim.

For causality, use an intervention whenever possible:

```text
baseline
→ perturbation
→ measured response
```

Add negative controls, positive controls, random interventions and independent replication when appropriate.

## Provenance

Every important claim should be traceable:

```text
claim
→ measurement
→ dataset
→ processing
→ model
→ result
```

Conflicting measurements must be preserved and investigated rather than silently discarded.

## What success means

Success is not a high score on a synthetic toy model. The strongest evidence is improvement on untouched real biological data, with independent labels, leakage control, capacity-matched baselines, relation-shuffled nulls and, ultimately, perturbation experiments.

## Human authority

The human researcher chooses the scientific objective, acceptable risk, interpretation threshold and whether a result is sufficient for the intended use. The AI can propose, calculate, test and document; it does not replace scientific or clinical judgment.
