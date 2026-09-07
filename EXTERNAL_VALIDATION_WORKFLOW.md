# OMEGA-DNA — External Validation Workflow

## Purpose

This document is the entry point for an independent researcher, physician, biologist, data scientist or another AI system that has been given the OMEGA-DNA repository.

Repository:
https://github.com/SmartVoltISA/OMEGA-DNA

The objective is not to trust the project. The objective is to test it.

## 1. First action

Open the repository and read, in this order:

1. `README.md`
2. `ARCHITECTURE.md`
3. `HOW_TO_USE.md`
4. `HUMAN_PROTOCOL.md` or `AI_PROTOCOL.md`
5. `HYPOTHESES.md`
6. `RESEARCH_PROTOCOL.md`
7. the relevant experiment protocol and results under `03_EXPERIMENTS/`

Do not start with the numerical results alone. First understand what was preregistered, what was synthetic, and what remains an open biological gate.

## 2. What the external researcher provides

The researcher may provide a real dataset, a subset of an existing database, or a pointer to a public dataset.

Useful inputs include:

- genomic coordinates;
- reference genome / assembly;
- DNA sequence or a reference FASTA accession;
- cell or tissue type;
- experimental condition;
- assay type;
- independently measured target labels;
- regulatory or structural measurements;
- replicate/sample information;
- metadata and provenance.

Patient-identifying or otherwise sensitive data should not be uploaded to an external system merely for exploratory testing. Use de-identified or appropriately authorized data and follow the institution's rules.

## 3. If a file is uploaded to an AI

The AI must not immediately train a model.

First perform a data audit:

```text
file format
columns
sample count
missingness
duplicates
assembly
coordinate system
label definition
feature provenance
assay provenance
possible leakage
```

Then report whether the file is suitable for an OMEGA-DNA test.

## 4. Map the file onto the OMEGA-DNA architecture

The AI should identify which columns correspond to:

```text
sequence
local structure
relations
architecture
state
process
output
persistence
```

A column must not be assigned a biological meaning merely because its name sounds appropriate. Its provenance and experimental definition must be checked.

## 5. Select one testable gate

Do not try to validate the entire architecture in one run.

Choose one question such as:

- Does regulatory contact information improve enhancer-target prediction?
- Does chromatin accessibility add information beyond sequence?
- Does TF binding context improve prediction?
- Does measured replication timing add information beyond sequence?
- Does repair/lesion context improve prediction?
- Does variant context improve functional-effect prediction?

## 6. Required comparison

At minimum run:

```text
A: sequence-only baseline
B: sequence + biologically justified relations
C: sequence + shuffled relations
```

Where appropriate, add a capacity-matched sequence-only model so that an apparent gain cannot simply be attributed to model size or feature count.

## 7. Holdout

Use an untouched biological holdout.

Preferred choices depend on the question:

- chromosomes;
- cell types;
- individuals;
- tissues;
- species;
- experimental batches.

Random row splitting alone can be inadequate for genomic data because nearby or related observations can leak information across the split.

## 8. Labels

The target label must be independently defined from the input features.

For example, if the task predicts gene activation, the label should preferably come from an independent expression measurement rather than being reconstructed from the same contact or chromatin feature used as input.

## 9. Required outputs

Report:

```text
QUESTION
DATASET
ASSEMBLY
ASSAY
SAMPLES
LABEL DEFINITION
TRAIN / VALIDATION / TEST SPLIT
SEQUENCE-ONLY RESULT
RELATIONAL RESULT
SHUFFLED-RELATION RESULT
CAPACITY-MATCHED RESULT (if applicable)
PRIMARY METRIC
SECONDARY METRICS
UNCERTAINTY / CI
STATISTICAL TEST
LEAKAGE AUDIT
LIMITATIONS
EVIDENCE CLASS
PROVENANCE
```

## 10. Interpretation

A relational improvement supports the limited statement:

> The tested relational information contains additional predictive information under the tested conditions.

It does NOT automatically prove:

- a universal biological law;
- causality;
- clinical utility;
- that the entire OMEGA-DNA architecture is correct.

Causal claims require perturbation or another appropriate causal design.

## 11. If the result is negative

Record it.

A negative result can mean:

- sequence is sufficient for this task;
- the proposed relation adds no measurable information;
- the relation was measured too noisily;
- the model could not use the relation;
- the chosen representation is inadequate;
- the biological context is wrong.

Do not force a positive result.

## 12. If real data cannot be used

The AI may run an existing synthetic control or prepare a runner, but must report:

`REAL BIOLOGICAL GATE = OPEN`

No synthetic result may be presented as biological validation.

## 13. Returning the result to OMEGA-DNA

The independent researcher should return either:

1. the complete reproducible analysis;
2. a report containing the fields above;
3. or, if possible, code + metadata + summary statistics.

The project should record independent results separately from internal experiments.

## 14. Recommended first external experiment

For a researcher who already has genomic and regulatory data, the preferred first test is a small, reproducible enhancer-target or regulatory-state benchmark with:

```text
sequence-only
vs
sequence + measured relations
vs
shuffled relations
```

using independent labels and a chromosome- or cell-type-level holdout.

This is intentionally small. A clean independent test is more valuable than a large uncontrolled analysis.

## 15. Principle

The repository is not asking the external researcher to believe OMEGA-DNA.

It is asking them to try to break it.

If the architecture survives independent real-data tests, its credibility increases.

If it fails, the failure must be recorded and used to correct the architecture.
