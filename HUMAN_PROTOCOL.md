# OMEGA-DNA — Human Research Protocol

## Purpose

This document explains how a human researcher, clinician, biologist or data scientist can independently evaluate OMEGA-DNA.

## Recommended first test

Do not begin by trying to validate the entire architecture. Choose one measurable biological question for which both sequence data and independent contextual measurements exist.

Good examples include:

- enhancer → target-gene prediction;
- chromatin accessibility;
- TF binding;
- regulatory state;
- variant functional effect;
- replication timing;
- repair response;
- non-canonical DNA structure.

## Minimum comparison

Run three conditions:

```text
A. sequence-only
B. sequence + biologically justified relations
C. sequence + shuffled relations
```

Use an untouched biological holdout.

## Recommended data package

Provide, where permitted and de-identified:

- genome assembly;
- genomic coordinates;
- sequence or reference accession;
- cell/tissue type;
- experimental condition;
- assay type;
- independent labels;
- relevant relational measurements;
- sample identifiers or replication structure;
- processing information.

Do not send patient-identifying information to an external system merely to test the architecture.

## What to ask

The key question is:

> Does relational information improve prediction or explanation on independent biological data beyond a properly controlled sequence-only baseline, and does the improvement survive relation-shuffling and leakage controls?

## Interpretation

A positive result means that the tested relational representation contains useful predictive information under the tested conditions. It does not automatically establish a universal biological law.

A negative result is also valuable. It may show that sequence is sufficient for that task, that the chosen relations add no information, or that the representation/model is inadequate.

## Clinical use

OMEGA-DNA is a research architecture, not a diagnostic or treatment system. Clinical conclusions must be made under appropriate professional, institutional and regulatory procedures.

## Suggested independent evaluation

1. Select one dataset.
2. Freeze the question and metric.
3. Run sequence-only baseline.
4. Run relational model.
5. Run shuffled-relation control.
6. Use a strict holdout.
7. Repeat across samples or biological contexts if possible.
8. Inspect false positives and false negatives.
9. Report whether the result replicates.
10. Send the result back as an independent validation report.
