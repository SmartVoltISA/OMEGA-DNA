# OMEGA-DNA — Region Decoding Schema v1.0

## Purpose

A standard record for converting an arbitrary genomic interval into a structured, auditable relational description.

## Required fields

| Field | Meaning | Evidence requirement |
|---|---|---|
| `location` | genomic coordinates | reference genome |
| `sequence` | nucleotide sequence | FASTA/reference |
| `sequence_features` | motifs, repeats, composition | computed/annotated |
| `relations` | typed links to other entities | independent annotation/measurement |
| `architecture` | nucleosome/chromatin/3D context | experiment/annotation |
| `state` | accessibility/activity/cell context | experiment |
| `processes` | transcription/replication/repair/etc. | assay or validated annotation |
| `outputs` | measurable consequences | experiment |
| `persistence` | evidence of state/history persistence | longitudinal/division evidence |
| `evidence_class` | OBSERVED/ANNOTATED/INFERRED/HYPOTHESIS/UNKNOWN | mandatory |
| `source` | provenance | mandatory |
| `confidence` | confidence/quality | mandatory |

## Decoding levels

### Level 0 — letters

`A/C/G/T`

### Level 1 — local information

Motifs, k-mers, repeats, conservation, variants.

### Level 2 — physical structure

Double-strand constraints, nucleosomes, chromatin state.

### Level 3 — typed relations

Protein binding, enhancer-promoter relations, spatial contacts, domain membership.

### Level 4 — dynamic state

Accessibility, activity, cell type, condition, time.

### Level 5 — function

Measured transcriptional, regulatory, replication, repair or phenotype-linked output.

### Level 6 — persistence

Evidence that sequence, structure or regulatory state persists and changes future behavior.

### Level 7 — causal test

Perturb the proposed relation/feature and test whether the predicted output changes.

## Rule

A region is not considered "decoded" merely because it has an annotation. A region is decoded to the degree that its sequence, relations, state, function and persistence are independently supported and connected by testable predictions.

## Minimal prediction format

```text
IF relation R is necessary for function F,
THEN perturbing R while controlling sequence/background
SHOULD change measurable output F.
```

This converts a descriptive map into an experimental map.
