# OMEGA-DNA — Region Decoding Schema v1.0

## Purpose

A standard record for converting an arbitrary genomic interval into a structured, auditable relational description.

The schema deliberately separates **sequence, structure, relation, architecture, state, process, function, persistence and causality**.

---

## 1. Required identity

```yaml
region:
  id: stable_id
  genome_build: hg19 | hg38 | other
  chromosome: chrN
  start: integer
  end: integer
  strand: + | -
```

The coordinate system and reference build are mandatory.

---

## 2. Sequence layer

```yaml
sequence:
  reference_hash: ...
  bases: ...
  length: ...
  composition:
    gc: ...
    at: ...
  motifs: []
  repeats: []
  low_complexity: []
  variants: []
  conservation: ...
  coding_status: ...
```

A sequence feature is not automatically a functional claim.

---

## 3. Local structure layer

```yaml
local_structure:
  canonical_duplex: ...
  noncanonical_structures: []
  nucleosome_occupancy: ...
  dna_methylation: ...
  local_compaction: ...
```

Each value requires assay/source/context metadata.

---

## 4. Architecture layer

```yaml
architecture:
  chromatin_state: ...
  regulatory_elements: []
  domain: ...
  subdomain: ...
  compartment: ...
  contacts: []
  loops: []
  hubs: []
  boundaries: []
  chromosome_context: ...
```

Spatial contacts are represented as observations or inferences, never automatically as causal relations.

---

## 5. Typed relation layer

Each relation is an object:

```yaml
relation:
  source: entity_id
  type: binding | regulatory | spatial | structural | domain | state | temporal | repair | replication | evolutionary | other
  target: entity_id
  direction: forward | reverse | undirected | unknown
  context: ...
  time: ...
  measurement: ...
  evidence_class: ...
  source_record: ...
```

Examples:

```text
DNA → binds → protein
enhancer → regulates → gene
region A → contacts → region B
region → belongs_to → domain
region → active_in → cell_state
state(t) → influences → state(t+Δt)
```

An untyped `connected_to` edge is insufficient for a biological mechanism claim.

---

## 6. Cellular state layer

```yaml
state:
  organism: ...
  tissue: ...
  cell_type: ...
  developmental_stage: ...
  condition: ...
  cell_cycle: ...
  accessibility: ...
  transcriptional_activity: ...
  histone_state: ...
  methylation_state: ...
```

State is always interpreted relative to context.

---

## 7. Process layer

```yaml
processes:
  transcription: ...
  replication: ...
  repair: ...
  chromatin_maintenance: ...
  regulation: ...
  recombination: ...
```

Every process claim must point to an observable or validated annotation.

---

## 8. Function/output layer

```yaml
function:
  outputs: []
  target_genes: []
  expression_effect: ...
  enhancer_activity: ...
  replication_effect: ...
  repair_effect: ...
  phenotype_association: ...
```

A functional annotation is stronger when it includes a measurable effect and an experimental context.

---

## 9. Persistence / memory layer

```yaml
persistence:
  sequence_memory: ...
  structural_memory: ...
  epigenetic_memory: ...
  cellular_history: ...
  evolutionary_history: ...
  persistence_assay: ...
```

Operational definition:

> A past-dependent state or constraint that measurably changes the probability of a future state or response.

The memory classes must not be collapsed into one score.

---

## 10. Causal layer

```yaml
causality:
  hypothesis: ...
  perturbation: ...
  control: ...
  measured_outcome: ...
  effect_size: ...
  replication: ...
  causal_status: unsupported | correlational | inferred | experimentally_supported
```

Minimal test:

```text
IF relation R is necessary for function F,
THEN perturb R while controlling relevant sequence/background
and EXPECT a reproducible change in measurable F.
```

---

## 11. Evidence/provenance layer

```yaml
evidence:
  class: OBSERVED | ANNOTATED | INFERRED | HYPOTHESIS | UNKNOWN
  source: ...
  assay: ...
  organism: ...
  cell_context: ...
  condition: ...
  resolution: ...
  pipeline: ...
  version: ...
  timestamp: ...
  confidence: ...
```

### Evidence classes

- `OBSERVED` — directly measured experimentally;
- `ANNOTATED` — independently curated or benchmark annotation;
- `INFERRED` — derived from measured variables or validated models;
- `HYPOTHESIS` — proposed and not yet established;
- `UNKNOWN` — insufficient evidence.

No class may be silently upgraded.

---

## 12. Decoder levels

### L0 — letters

`A/C/G/T`

### L1 — sequence information

Motifs, k-mers, repeats, conservation, variants, coding/non-coding context.

### L2 — local physical structure

Double-strand constraints, nucleosomes, methylation, non-canonical structures.

### L3 — typed relations

Binding, regulatory, spatial, structural and domain relations.

### L4 — genome architecture

Chromatin states, domains, compartments, loops and hubs.

### L5 — dynamic state

Accessibility, transcriptional activity, cell type, condition and time.

### L6 — process

Transcription, replication, repair, recombination and chromatin maintenance.

### L7 — function

Measured biological output.

### L8 — persistence

Sequence, structural, epigenetic, cellular-history and evolutionary persistence.

### L9 — causality

Perturbation-based test of the proposed mechanism.

---

## 13. Completeness rule

A region is **not** considered fully decoded merely because it has a gene/enhancer/promoter label.

A region reaches a higher decoding level only when the corresponding fields are supported and linked by testable relations.

```text
annotation ≠ mechanism
correlation ≠ causation
prediction ≠ observation
contact ≠ function
conservation ≠ present-day function
sequence feature ≠ semantic meaning
```

---

## 14. Required output for every region

The decoder must return:

1. sequence;
2. local structure;
3. sequence features;
4. regulatory annotations;
5. typed relations;
6. 3D architecture;
7. cell/state context;
8. active processes;
9. measurable function;
10. persistence/memory evidence;
11. causal evidence;
12. confidence;
13. unknown fields;
14. falsifiable predictions.

The final product is a **functional relational profile**, not a single label.
