# OMEGA-DNA — Genome-Scale Decoding Roadmap v1.0

## Goal

Build the map in layers rather than pretending the genome can be decoded in one step.

## Phase D0 — Evidence foundation

Create a provenance table for every dataset and annotation:

```text
feature → source → assay → cell/context → resolution → evidence class
```

## Phase D1 — Sequence information

Extract and index:

- sequence;
- GC/composition;
- motifs;
- repeats;
- conservation;
- variants;
- coding/non-coding context.

Output: sequence-information layer.

## Phase D2 — Architecture

Attach:

- nucleosome information;
- chromatin states;
- regulatory domains;
- chromosome organization;
- 3D contact information.

Output: physical architecture layer.

## Phase D3 — Relations

Build a typed graph:

```text
DNA ↔ protein
DNA ↔ DNA
enhancer ↔ promoter
gene ↔ regulator
region ↔ domain
region ↔ cell state
```

Output: relational genome graph.

## Phase D4 — Dynamic state

Add:

- accessibility;
- transcriptional activity;
- histone state;
- DNA methylation;
- cell type;
- condition;
- time.

Output: state-aware genome graph.

## Phase D5 — Memory

Separate and test:

- sequence inheritance;
- chromatin persistence;
- epigenetic persistence;
- cellular history;
- evolutionary persistence.

Output: persistence layer.

## Phase D6 — Function

Connect genomic structures and relations to measurable outputs.

```text
feature + relation + state
          ↓
        process
          ↓
        output
```

Output: functional annotations with evidence.

## Phase D7 — Causality

For high-value hypotheses:

```text
observe → predict → perturb → measure → compare
```

Prioritize enhancer/promoter relations, chromatin boundaries, accessibility and repair-related relations.

## Phase D8 — Genome-scale synthesis

Create a graph where every edge has:

- type;
- direction where meaningful;
- source;
- evidence class;
- confidence;
- context;
- timestamp/version.

## Phase D9 — Predictive decoder

Given a region, the system should return:

1. what is encoded;
2. what it is connected to;
3. what state it is in;
4. what process it participates in;
5. what output is expected;
6. what evidence supports the claim;
7. what experiment would falsify it.

## Phase D10 — Full biological benchmark

Use public long-range DNA tasks as external validation. DNALongBench provides enhancer-target gene, eQTL, contact-map, regulatory sequence activity and transcription-initiation tasks, including a 450 kb enhancer-target task with 2,602 samples. citeturn0search0turn0search1

Primary test:

```text
A: sequence only
B: sequence + independent relations/state
N: shuffled relations
```

The key result is not whether B is simply accurate. It is whether B provides reproducible information beyond A under matched capacity and controls.

## End state

The final object is not a dictionary of DNA letters.

It is:

```text
GENOME
  ↓
RELATIONAL MODEL
  ↓
STATE MODEL
  ↓
FUNCTIONAL MODEL
  ↓
PERSISTENCE / MEMORY MODEL
  ↓
CAUSAL PREDICTIONS
```

The map is successful when it makes both known structure and unknown structure explicit.
