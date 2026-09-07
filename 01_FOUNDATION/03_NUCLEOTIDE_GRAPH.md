# Nucleotide as a relational graph

## Scope

This document defines a structural graph for one DNA nucleotide. It is deliberately limited to established molecular architecture; no new biological law is claimed.

A DNA nucleotide contains a nitrogenous base, 2'-deoxyribose and phosphate group. The base is covalently attached to the sugar; the phosphate participates in the backbone linkage. Source: NCBI Bookshelf, *DNA Structure*.

## Graph levels

### G0 — atomic layer

Nodes: C, H, N, O, P atoms.

Edges: covalent bonds within the molecule.

### G1 — molecular-component layer

Nodes:
- nitrogenous base;
- 2'-deoxyribose;
- phosphate group.

Relations:
- base ↔ sugar: covalent glycosidic linkage;
- sugar ↔ phosphate: covalent phosphate linkage.

### G2 — nucleotide-unit layer

`base + sugar + phosphate → nucleotide`

The nucleotide is therefore not a primitive node. It is a higher-order structure assembled from lower-level elements and relations.

### G3 — polymer layer

Adjacent nucleotide residues are connected through phosphodiester bonds between the 3' hydroxyl and 5' phosphate positions. This creates the directional sugar-phosphate backbone and 5'→3' polarity. Source: NCBI Bookshelf, *DNA Structure*.

### G4 — paired layer

The base participates in a relation with a complementary base on the opposite strand. Canonical Watson-Crick pairing is A-T and G-C; A-T has two and G-C three hydrogen bonds in the conventional structural description. Source: NCBI Bookshelf, *DNA Structure*.

## Architectural interpretation

The important observation is hierarchical:

`atoms → covalent relations → molecular components → nucleotide → polymer relation → paired relation → double-stranded structure`

The same object can therefore be simultaneously:

- a **structure** at one scale;
- a **node** at a higher scale;
- a **constraint** on neighboring structures;
- a carrier of persistent sequence state.

This is a direct example of the OMEGA principle that a whole can become an element of a larger whole.

## Critical caution

Do not assign a single numerical "connection strength" to the nucleotide graph. Covalent bonding, hydrogen bonding, stacking, electrostatic effects and spatial constraints have different physical meanings. They must remain typed relations until a specific experiment defines a common quantitative representation.

## Research consequence

The next useful model is not a generic graph of A/C/G/T. It is a **typed multigraph** in which the same nucleotide can participate in several relation classes simultaneously.
