# OMEGA-DNA — Foundations

## 0. Status

This document separates established biological observations from the OMEGA architectural interpretation. The latter is a model to be tested, not a replacement for molecular biology.

## 1. Physical basis

DNA is a polymer of nucleotides. A DNA nucleotide contains deoxyribose, phosphate, and one of four bases: adenine (A), thymine (T), cytosine (C), or guanine (G). Nucleotides are connected by covalent phosphodiester bonds, producing a directional sugar-phosphate backbone.

Two DNA strands are complementary and antiparallel. A pairs with T and G pairs with C. Hydrogen bonding contributes to base-pair recognition; interactions between adjacent stacked bases also contribute substantially to helix stability.

## 2. First architectural distinction

The four letters A/C/G/T are not the complete physical state of DNA.

At minimum, the state contains:

- composition;
- order;
- orientation;
- complementary constraints;
- local chemical interactions;
- three-dimensional geometry;
- interactions with proteins and other molecules;
- accessibility and packaging;
- maintenance history.

Therefore the research must distinguish **sequence information** from the **physical state that carries and regulates that information**.

## 3. Minimal relational representation

At the nucleotide scale:

`node = nucleotide`

`edge_backbone = covalent phosphodiester relation`

`edge_pair = complementary base relation`

`edge_stack = local base-stacking interaction`

`state = geometry + chemical state + local environment`

`memory = persistent sequence/structural state`

`maintenance = replication + repair + quality control`

This is deliberately minimal. Additional edges must correspond to measurable biological relations.

## 4. The critical transition

The key question is not whether DNA contains information. That is established.

The research question is:

> How much of DNA's functional behavior can be explained by the organization and dynamics of its relations, beyond a linear sequence description?

This question can be tested by comparing models with controlled information content and complexity.

## 5. What must not be conflated

- Sequence is not identical to function.
- A graph representation is not automatically a biological explanation.
- Correlation between graph metrics and phenotype is not causation.
- Structural persistence is not automatically biological memory in every context.
- A useful abstraction does not prove that nature itself uses the abstraction.

## 6. Initial architectural chain

`atom → chemical relation → nucleotide → ordered chain → complementary pair → double helix → chromatin organization → regulatory context → cellular process → inherited state`

Each arrow is a proposed change of organizational level and must be independently justified.

## 7. Evidence boundary

Established molecular facts should be sourced to primary literature or authoritative scientific references. Model-derived claims must carry a hypothesis or experiment identifier.
