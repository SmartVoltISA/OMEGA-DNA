# Minimal base-pair model

## Objective

Test the smallest useful relational representation of canonical DNA base pairing.

## Elements

`A, T, G, C`

These symbols identify nucleotide bases at the sequence level. They are not treated as fundamental physical objects.

## Canonical pair relations

`A ↔ T`

`G ↔ C`

The arrow denotes a pairing relation, not an undirected physical bond. The actual molecular interaction contains specific hydrogen-bonding geometry and surrounding interactions.

## Minimal graph

Nodes: `{A,T,G,C}`

Edges: `{A-T, G-C}`

Constraints:

- canonical complementarity;
- strand antiparallel organization;
- local molecular geometry;
- chemical compatibility.

## Null models

### N0 — Unconstrained pairing
Any base may pair with any base with equal prior probability.

### N1 — Symbolic complementarity
A-T and G-C are encoded only as a lookup rule, without physical relations.

### N2 — Relational model
Pairing is represented together with declared molecular constraints.

## Question

Does adding physically meaningful relations provide explanatory or predictive value beyond a symbolic complementarity table?

## Important limitation

A minimal graph cannot reproduce the full thermodynamics, sequence dependence, solvent effects, protein interactions or cellular context of DNA. It is a controlled abstraction for testing the role of constraints.

## Next measurement

Define a quantitative task where N0, N1 and N2 make distinguishable predictions before running the experiment.