# OMEGA-DNA — Complete Relational Genome Map v1.0

**Date:** 2026-09-07  
**Status:** research architecture / evidence-tracked / falsifiable  
**Purpose:** make the DNA-to-function chain explicit enough that every assigned role can be measured, sourced, tested and, where possible, causally perturbed.

> This is not a claim that the genome has already been decoded. It is the complete target ontology and measurement architecture for doing so without collapsing sequence, structure, state, relation, memory and function into one label.

---

## 0. Master equation

The decoder treats a genomic region `R` as a time- and context-dependent object:

```text
R(t, c) = {
  sequence,
  local_structure,
  relations,
  architecture,
  state,
  processes,
  outputs,
  persistence,
  evidence
}
```

The working causal chain is:

```text
SEQUENCE
   ↓
LOCAL STRUCTURE
   ↓
TYPED RELATIONS
   ↓
GENOME ARCHITECTURE
   ↓
CELLULAR STATE
   ↓
PROCESS
   ↓
MEASURABLE OUTPUT
   ↓
FEEDBACK / MAINTENANCE
   ↓
PERSISTENCE / MEMORY
   ↓
FUTURE RESPONSE
```

The central prediction is not that sequence is unimportant. It is that sequence alone may be insufficient for some functions whose biological realization depends on relations, architecture and state.

---

# 1. LEVEL 0 — MOLECULAR PRIMITIVES

## 1.1 Nucleotides

Entities:

- A, C, G, T;
- phosphate;
- deoxyribose;
- 5' and 3' orientation;
- backbone linkage;
- base-pairing capability.

Measurements:

- sequence;
- strand orientation;
- chemical modification where measured;
- lesion/damage state where measured.

Evidence classes are assigned per measurement, not per region.

## 1.2 Canonical complementarity

```text
A ↔ T
C ↔ G
```

This is simultaneously:

- a chemical relation;
- a structural constraint;
- a replication/repair constraint;
- an error-detection opportunity.

It must not be treated as a semantic dictionary.

## 1.3 Non-canonical structures

The map must allow structures beyond the canonical double helix, including experimentally supported cases such as i-motifs and other context-dependent secondary structures.

These become typed structural states rather than exceptions outside the model. Recent literature describes i-motifs as a dynamic regulatory layer beyond the classical double helix. 

---

# 2. LEVEL 1 — PRIMARY INFORMATION

For every interval:

```text
sequence
├── bases
├── k-mer composition
├── GC / AT composition
├── motifs
├── repeats
├── low-complexity regions
├── variants
├── conservation
├── coding status
├── non-coding status
└── orientation
```

Important distinction:

```text
sequence feature ≠ function
```

A motif is a candidate binding or regulatory signal until supported by independent evidence.

### Required measurements

- reference genome build;
- exact coordinates;
- strand;
- sequence hash;
- variant source and version;
- conservation source;
- annotation release.

---

# 3. LEVEL 2 — LOCAL PHYSICAL STRUCTURE

The sequence is embedded in physical organization.

```text
DNA
 ↓
DNA-protein interactions
 ↓
nucleosome
 ↓
chromatin fiber / local domain
```

Candidate variables:

- nucleosome occupancy;
- histone marks;
- DNA methylation;
- chromatin accessibility;
- local compaction;
- experimentally detected non-canonical structures.

These are state-dependent variables. They must be indexed by cell type, condition and assay whenever available.

---

# 4. LEVEL 3 — TYPED RELATIONS

The fundamental graph object is:

```text
(source, relation_type, target, context, time, evidence)
```

## 4.1 Relation ontology

| Type | Source | Target | Example measurable evidence |
|---|---|---|---|
| complementarity | base | base | paired sequence |
| binding | DNA | protein | ChIP/CUT&RUN/SELEX-like evidence |
| occupancy | protein | region | binding/occupancy assay |
| regulatory | enhancer | gene/promoter | perturbation + expression |
| spatial | region | region | Hi-C/Micro-C/3C or imaging |
| structural | DNA | nucleosome | occupancy/positioning |
| domain | region | domain | domain annotation/contact map |
| boundary | boundary element | domain | insulation/contact changes |
| state | region | cell state | ATAC/RNA/epigenomic state |
| temporal | state(t) | state(t+Δt) | longitudinal experiment |
| repair | lesion | repair machinery | repair kinetics/assay |
| replication | locus | replication program | replication timing/origin evidence |
| evolutionary | variant | population | allele frequency/selection evidence |

No biological claim may rely on an untyped generic `connected_to` edge alone.

---

# 5. LEVEL 4 — REGULATORY ARCHITECTURE

The map must represent at least:

```text
promoter
enhancer
silencer
insulator / boundary
regulatory cluster
TAD / sub-TAD where supported
compartment
chromosome territory
nuclear neighborhood
```

The architecture is multi-scale. Recent work describes nanoscale chromatin domains as important units of mammalian genome organization, while 2026 reviews emphasize organization below classical TAD/compartment scales. citeturn0search1turn0search5

The model therefore cannot stop at linear coordinates.

---

# 6. LEVEL 5 — 3D GENOME RELATIONS

Represent:

```text
region A
   │
   ├── contact_frequency ── region B
   ├── loop_relation ───── region B
   ├── hub_membership ──── region B/C/...
   └── domain_membership ── domain
```

Important limitation:

```text
contact ≠ causation
```

Hi-C and related methods measure contact probabilities and can hide cell-to-cell heterogeneity. Single-cell imaging and biochemical perturbation provide complementary evidence. A 2026 review explicitly frames 3D genome architecture as coupled to biochemical state and discusses its possible role as a cellular memory substrate. citeturn0search3

Therefore every spatial edge gets an evidence and assay field.

---

# 7. LEVEL 6 — ENHANCER–PROMOTER / REGULATORY NETWORK

The minimum regulatory relation is:

```text
enhancer → promoter → gene → RNA → protein / phenotype-associated output
```

But the real model permits:

```text
many enhancers ↔ many promoters ↔ hubs ↔ genes
```

Recent reviews describe multiway enhancer-promoter hubs and emphasize that long-range regulation is dynamic and context-dependent. citeturn0search2turn0search7

Candidate relation variables:

- genomic distance;
- contact probability;
- enhancer accessibility;
- TF occupancy;
- promoter state;
- cell-type specificity;
- expression correlation;
- perturbation effect;
- directionality where experimentally justified.

Distance is a feature, not a complete mechanism.

---

# 8. LEVEL 7 — CELLULAR STATE

Every functional annotation should answer:

```text
In which cell?
Under which condition?
At which time?
At which developmental state?
At which cell-cycle state?
```

State variables:

- ATAC/DNase accessibility;
- RNA expression;
- histone modification state;
- DNA methylation;
- transcription factor occupancy;
- replication timing;
- chromatin contacts;
- cell type;
- tissue;
- developmental stage;
- environmental/stress condition.

The same sequence may therefore have different functional outputs under different states.

---

# 9. LEVEL 8 — PROCESSES

The map must connect structure/state to processes:

## 9.1 Transcription

```text
regulatory state
 → transcription machinery access
 → initiation / elongation
 → RNA output
```

## 9.2 Replication

```text
replication context
 → origin / timing / fork progression
 → copied DNA
```

## 9.3 Repair

```text
damage
 → recognition
 → repair pathway
 → restored / altered sequence state
```

## 9.4 Chromatin maintenance

```text
state perturbation
 → reader/writer/remodeler activity
 → restored or changed chromatin state
```

## 9.5 Regulation

```text
relation + state + architecture
 → regulatory decision
 → measurable expression/output
```

Each process requires an observable endpoint.

---

# 10. LEVEL 9 — FUNCTION

Function is operationally defined by measurable consequence.

```text
FUNCTION(R, context) = measurable change in system behavior attributable to R
```

Candidate outputs:

- RNA abundance;
- transcription rate;
- protein abundance;
- enhancer activity;
- promoter activity;
- accessibility change;
- replication timing;
- repair rate;
- contact architecture change;
- cell-state transition;
- phenotype-associated effect.

A label such as `enhancer` is therefore incomplete without:

```text
enhancer
+ target relation
+ cell context
+ state
+ measurable output
+ evidence
```

---

# 11. LEVEL 10 — MEMORY / PERSISTENCE

Memory is not a metaphor here. It has an operational definition:

> A past-dependent state or constraint that measurably changes the probability of a future state or response.

## M1 — Sequence memory

Inherited nucleotide sequence and stable variants.

## M2 — Structural memory

Persistence or reproducible re-establishment of chromatin organization after perturbation or replication.

## M3 — Epigenetic memory

Persistence of regulatory state through cell divisions or after transient stimuli.

## M4 — Cellular-history memory

Past exposure or state modifies future response even when the immediate stimulus is restored.

## M5 — Evolutionary memory

Population-level persistence of variants shaped by selection/drift and historical constraints.

These classes must be measured separately.

---

# 12. LEVEL 11 — FEEDBACK AND MAINTENANCE

The universal candidate loop is:

```text
state
 ↓
process
 ↓
output
 ↓
error / deviation / environmental change
 ↓
response
 ↓
corrected or shifted state
```

Examples:

- DNA damage → repair response → restored state;
- chromatin perturbation → remodeling → altered accessibility;
- transcriptional state → regulatory feedback → new transcriptional state;
- replication error → checkpoint/repair → persistence or correction.

This is a hypothesis framework, not a claim that all biological systems share one controller.

---

# 13. LEVEL 12 — CAUSALITY

The strongest relation record is not:

```text
A correlates with B
```

but:

```text
perturb A
↓
control relevant confounders
↓
measure B
↓
compare against control
```

### Causal test template

```text
H: relation R contributes causally to output F.

IF R is necessary:
  perturb R while preserving as much of sequence/background as possible.
  EXPECT measurable change in F.

IF R is sufficient:
  introduce/restore R under controlled conditions.
  EXPECT reproducible change in F.

IF R is only correlated:
  perturbation should not produce the predicted effect after controls.
```

3D architecture is a priority because the literature continues to identify causal gaps between observed contacts and function. Targeted engineering of chromatin loops is one route to testing those links. citeturn0search8

---

# 14. LEVEL 13 — EVOLUTIONARY MEMORY

Evolutionary information must be separated from present-day function.

Represent:

```text
variant
 → frequency
 → conservation
 → lineage history
 → selection evidence
 → present functional effect
```

A conserved region is not automatically functional in every context. Conservation is evidence for historical constraint, not a complete functional annotation.

Transposable elements are an explicit class in this layer because recent work emphasizes their contributions to genome architecture, chromatin organization and regulatory functions at individual loci. citeturn0search11

---

# 15. COMPLETE REGION RECORD

Every future region card should be representable as:

```yaml
region:
  id: stable_region_id
  genome_build: hg19 | hg38 | other
  coordinates:
    chromosome: chrN
    start: 0
    end: 0
    strand: + | -

  sequence:
    reference_hash: ...
    bases: ...
    composition:
      gc: ...
      at: ...
    motifs: []
    repeats: []
    variants: []
    conservation: ...

  local_structure:
    canonical_duplex: ...
    noncanonical_structures: []
    nucleosome: ...
    methylation: ...

  architecture:
    chromatin_state: ...
    regulatory_elements: []
    domain: ...
    compartment: ...
    contacts: []
    hubs: []

  relations:
    proteins: []
    enhancers: []
    promoters: []
    genes: []
    boundaries: []
    regions: []

  state:
    cell_type: ...
    tissue: ...
    condition: ...
    developmental_stage: ...
    cell_cycle: ...
    accessibility: ...
    transcriptional_activity: ...
    histone_state: ...

  processes:
    transcription: ...
    replication: ...
    repair: ...
    regulation: ...

  function:
    outputs: []
    target_genes: []
    effect_size: ...
    direction: ...

  memory:
    sequence_persistence: ...
    structural_persistence: ...
    epigenetic_persistence: ...
    cellular_history: ...
    evolutionary_history: ...

  causality:
    perturbation: ...
    control: ...
    outcome: ...

  evidence:
    class: OBSERVED | ANNOTATED | INFERRED | HYPOTHESIS | UNKNOWN
    source: ...
    assay: ...
    sample_context: ...
    resolution: ...
    confidence: ...
    version: ...
    timestamp: ...
```

---

# 16. EVIDENCE HIERARCHY

Use the following precedence for claims:

```text
CAUSALLY PERTURBED / DIRECTLY MEASURED
        ↓
INDEPENDENT EXPERIMENTAL ANNOTATION
        ↓
VALIDATED INFERENCE
        ↓
COMPUTATIONAL PREDICTION
        ↓
OMEGA HYPOTHESIS
```

The evidence class is mandatory.

A model-derived relation must never be silently relabeled as an independently measured relation.

---

# 17. DATA PROVENANCE

Every dataset field must preserve:

```text
source
assay
organism
reference genome
cell type
condition
sample ID where appropriate
resolution
processing pipeline
version
access date
checksum/hash where available
```

This makes the map reproducible and prevents incompatible annotations from being merged as if they were simultaneous observations.

---

# 18. LONG-RANGE BENCHMARK GATE

DNALongBench explicitly contains five long-range tasks: enhancer-target gene prediction, eQTL prediction, contact-map prediction, regulatory sequence activity and transcription-initiation prediction. The enhancer-target task uses 450,000 bp inputs, 2,602 samples and AUROC. The published benchmark reports an expert score of 0.926, CNN 0.797, HyenaDNA 0.828, Caduceus-Ph 0.826 and Caduceus-PS 0.821. citeturn0search0

OMEGA-DNA must test the relational claim without changing the target task.

```text
A = sequence-only
B = sequence + independent relation/state channels
N = shuffled relation/state null
```

Primary quantity:

```text
Δ = AUROC(B) - AUROC(A)
```

Acceptance requires:

```text
Δ > 0 on held-out test
AND
B > N
AND
capacity-matched comparison
AND
same official split
AND
multiple seeds
AND
no test tuning
AND
independent relation provenance
```

The benchmark repository provides loaders and the ETGP data package, so the implementation should target the official split rather than reconstructing a new split. citeturn0search0

---

# 19. OMEGA-SPECIFIC PREDICTIVE TESTS

For every relation class, create three models:

```text
M0 = sequence/base covariates
M1 = sequence + relation
M2 = sequence + relation with shuffled relation null
```

Then run:

1. held-out evaluation;
2. repeated seeds;
3. capacity matching;
4. ablation by relation type;
5. relation-only model;
6. permutation/null test;
7. subgroup analysis by context;
8. calibration/error analysis.

The main scientific question is incremental information:

```text
Does relation R explain held-out variance not already explained by sequence S?
```

---

# 20. LEAKAGE RULES

The following are forbidden as independent relation evidence if they were generated from the same target or model family being evaluated:

- target-derived labels disguised as relations;
- predictions from the same model used for evaluation;
- post-hoc annotations created using test labels;
- relations computed using the target expression outcome without strict separation;
- train/test contamination through overlapping genomic regions when the task requires locus independence.

Every relation channel must have a provenance statement.

---

# 21. DECODER OUTPUT

Given a genomic interval, the final decoder should return:

```text
1. SEQUENCE
2. LOCAL STRUCTURE
3. MOTIFS / FEATURES
4. REGULATORY ANNOTATIONS
5. TYPED RELATIONS
6. 3D ARCHITECTURE
7. CELLULAR STATE
8. ACTIVE PROCESSES
9. MEASURABLE FUNCTION
10. MEMORY / PERSISTENCE
11. CAUSAL EVIDENCE
12. CONFIDENCE
13. UNKNOWN EDGES
14. FALSIFIABLE PREDICTIONS
```

The final answer for a region must therefore be a structured profile, not a single semantic label.

---

# 22. WHAT REMAINS UNKNOWN

The decoder must explicitly preserve unknowns such as:

```text
unknown target gene
unknown causal relation
unknown cell-state dependence
unknown temporal persistence
unknown structural state
unknown mechanism
unknown functional output
```

An unknown edge is a valid scientific result.

---

# 23. FINAL OMEGA FORMULATION

The genome is represented as:

```text
GENOME
 = sequence
 + structure
 + typed relations
 + architecture
 + state
 + processes
 + outputs
 + feedback
 + persistence
 + history
```

And a functional claim is represented as:

```text
CLAIM =
  entity
  + relation
  + context
  + state
  + process
  + measurable output
  + evidence
  + falsifiable test
```

The objective is therefore not:

> "Find the meaning of DNA letters."

It is:

> **Construct a genome-scale, evidence-tracked relational model in which sequence, structure, relations, state, memory and function remain distinguishable, measurable and causally testable.**

That is the completed architecture target. The remaining work is empirical population of its fields, validation and falsification.
