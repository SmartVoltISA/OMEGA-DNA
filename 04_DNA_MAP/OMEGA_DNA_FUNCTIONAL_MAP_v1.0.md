# OMEGA-DNA — Functional Architecture Map v1.0

**Date:** 2026-09-07  
**Status:** research architecture / falsifiable map  
**Purpose:** define a complete, inspectable map from DNA sequence to structure, relations, state, memory and measurable function.

> This document is a map, not a claim that every DNA base has been functionally decoded. Each statement must carry an evidence class.

## 1. Core model

OMEGA-DNA represents genomic organization as:

```text
sequence → structure → relations → constraints → state → process → function → result → feedback → persistence
```

The central question is not simply **"what does this base mean?"**, but:

```text
What is present?
What is it connected to?
What state is the system in?
What process does that state permit or prevent?
What measurable result follows?
What persists after change?
```

## 2. Six principal layers

### A. INFORMATION

Observable or inferable sequence-level information:

- bases: A/C/G/T;
- motifs and sequence patterns;
- repeats;
- variants and mutations;
- conservation;
- sequence composition;
- coding/non-coding context.

**Primary object:** `sequence`.

**Question:** what information is physically encoded in the polymer sequence?

### B. ARCHITECTURE

Physical and organizational structure:

```text
nucleotide
  ↓
DNA strand
  ↓
double-stranded DNA
  ↓
nucleosome
  ↓
chromatin
  ↓
regulatory domain
  ↓
3D contacts / loops
  ↓
chromosome
  ↓
genome
```

**Question:** how is the sequence physically organized across scales?

### C. RELATIONS

Explicit typed relations between entities:

| Relation | Example |
|---|---|
| complementarity | A ↔ T, C ↔ G |
| chemical | nucleotide ↔ nucleotide |
| binding | DNA ↔ transcription factor |
| regulatory | enhancer ↔ promoter |
| spatial | region ↔ region |
| structural | DNA ↔ nucleosome |
| domain | region ↔ regulatory domain |
| cellular | locus ↔ cell state |
| temporal | state(t) ↔ state(t+1) |

**Question:** what information exists only because two or more elements are related?

### D. STATE

The same sequence can participate in different functional states.

Candidate state variables:

- chromatin accessibility;
- nucleosome occupancy;
- histone modification state;
- DNA methylation;
- transcriptional activity;
- cell type;
- developmental condition;
- environmental condition;
- cell-cycle state.

**Question:** what is the state of the system when the sequence is interpreted?

### E. MEMORY / PERSISTENCE

Memory is defined operationally as:

> a state or constraint produced by the past that changes the probability of future system behavior.

Separate memory classes:

1. **sequence memory** — inherited nucleotide information;
2. **structural memory** — persistence/re-establishment of chromatin organization;
3. **epigenetic memory** — persistence of regulatory state through cell divisions;
4. **cellular history** — prior state affecting future response;
5. **evolutionary memory** — population-level persistence of selected variants.

These must not be collapsed into one variable.

### F. FUNCTION

Function is context-dependent:

```text
F = f(sequence, relations, architecture, state, cell context, time)
```

Candidate measurable outputs:

- transcription;
- RNA abundance;
- protein abundance;
- replication behavior;
- repair efficiency;
- chromatin accessibility;
- enhancer activity;
- gene regulation;
- phenotype-associated effect.

## 3. Feedback layer

OMEGA-DNA treats maintenance processes as feedback candidates:

```text
state
  ↓
process
  ↓
result
  ↓
measurement
  ↓
comparison / constraint
  ↓
repair or regulatory response
  ↓
new state
```

This is a testable architecture, not a statement that every genomic process implements a single universal controller.

## 4. Evidence classes

Every annotation in the future genome map must carry one of these classes:

- **OBSERVED** — directly measured experimentally;
- **ANNOTATED** — independently curated/annotated;
- **INFERRED** — derived from measured variables or validated models;
- **HYPOTHESIS** — proposed by OMEGA-DNA and requiring testing;
- **UNKNOWN** — insufficient evidence.

No inference may silently become an observation.

## 5. Unit record for a genomic region

Each region should eventually be represented as:

```yaml
region:
  location: chromosome:start-end
  sequence:
    bases: ...
    motifs: ...
    variants: ...
  architecture:
    nucleosome: ...
    chromatin_state: ...
    domain: ...
    contacts: ...
  relations:
    proteins: ...
    enhancers: ...
    promoters: ...
    genes: ...
    regions: ...
  state:
    accessibility: ...
    activity: ...
    cell_type: ...
    condition: ...
  processes:
    transcription: ...
    replication: ...
    repair: ...
    regulation: ...
  memory:
    sequence_persistence: ...
    structural_persistence: ...
    epigenetic_persistence: ...
  function:
    measurable_output: ...
  evidence:
    class: OBSERVED | ANNOTATED | INFERRED | HYPOTHESIS | UNKNOWN
    source: ...
    confidence: ...
```

## 6. Proposed genome graph

```text
BASE
 │
 ├── sequence relation ── BASE
 │
 └── belongs_to ── REGION
                     │
                     ├── contains ── MOTIF
                     ├── binds ── PROTEIN
                     ├── participates_in ── CHROMATIN_STATE
                     ├── contacts ── REGION
                     ├── regulates ── GENE
                     ├── belongs_to ── DOMAIN
                     └── produces ── MEASURABLE_OUTPUT
                                            │
                                            ▼
                                        CELL STATE
                                            │
                                            ▼
                                      FUTURE STATE
```

The graph must remain **typed**. An untyped edge is insufficient for a claim about biological mechanism.

## 7. Information / architecture / memory separation

A useful diagnostic is:

```text
INFORMATION = what can be encoded
ARCHITECTURE = how the encoded system is organized
RELATION = what constrains or connects elements
STATE = what is currently active/accessible
MEMORY = what past state remains causally relevant
FUNCTION = what measurable behavior results
```

A single genomic feature may participate in several layers simultaneously, but the layers must remain analytically distinguishable.

## 8. Decoding protocol

For a region `R`, the decoder should execute:

```text
1. Read sequence.
2. Detect local sequence features.
3. Attach experimentally supported annotations.
4. Construct typed relations.
5. Add physical/3D architecture.
6. Add cell/state context.
7. Identify measurable processes.
8. Trace outputs.
9. Search for persistence across time/division.
10. Assign evidence classes.
11. Generate falsifiable predictions.
```

The output is therefore not a single label such as `gene` or `enhancer`, but a **functional relational profile**.

## 9. Biological benchmark gate

The first real-data gate remains a long-range genomic prediction task. DNALongBench provides five tasks spanning enhancer-target linking, eQTL prediction, contact-map prediction, regulatory sequence activity and transcription-initiation prediction. The enhancer-target task uses 450,000 bp input and 2,602 samples with AUROC as the metric.

OMEGA-DNA's decisive comparison remains:

```text
A = sequence-only
B = sequence + independently measured/annotated relations/state
N = shuffled relation null
```

Required controls:

- identical official split;
- matched target and metric;
- capacity matching;
- same early stopping policy;
- multiple seeds;
- no test tuning;
- relation shuffle only inside training where appropriate;
- independent relation measurements;
- report delta B-A;
- report null behavior.

Derived scores such as ABC-like model outputs are not sufficient by themselves to establish an independent relational information source.

## 10. What would count as success

The architecture receives biological support if:

```text
B > A on held-out data
AND
B > shuffled-relation null
AND
result survives capacity controls
AND
result repeats across seeds
AND
relation variables are independently measured/annotated
```

A failure under these controls is equally valuable: it would constrain or falsify the proposed relational advantage.

## 11. What this document does NOT claim

It does not claim:

- that every DNA base has a unique semantic meaning;
- that all non-coding DNA has one universal function;
- that graph representation itself is novel;
- that correlation proves causation;
- that synthetic experiments prove biology;
- that DNA alone determines cellular phenotype;
- that OMEGA-DNA has already decoded the genome.

## 12. Final target

The long-term target is:

> **A genome-scale relational functional map in which every assigned role is connected to an observable measurement, a relation type, a state, a persistence mechanism and an evidence class.**

The scientific objective is not to make the map look complete. The objective is to make every missing edge visible.
