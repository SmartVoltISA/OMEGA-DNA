# OMEGA-DNA — Relational Graph Model

## 1. Objective

Construct a graph representation that preserves biologically meaningful relations while avoiding the assumption that every biological fact is reducible to a generic graph.

## 2. Node classes

- `ATOM`
- `NUCLEOTIDE`
- `BASE`
- `BASE_PAIR`
- `REGION`
- `PROTEIN`
- `REGULATORY_ELEMENT`
- `CHROMATIN_STATE`
- `CELLULAR_PROCESS`

The node class must always be recorded because graph meaning changes with scale.

## 3. Edge classes

- `COVALENT`
- `HYDROGEN_BOND`
- `STACKING`
- `COMPLEMENTARY`
- `SPATIAL`
- `BINDING`
- `REGULATORY`
- `DEPENDENCY`
- `TEMPLATE`
- `MAINTENANCE`

An edge is not merely a line between two nodes. It represents a defined relation with a measurable or formally specified meaning.

## 4. Edge attributes

Candidate attributes:

`w = {strength, distance, orientation, stability, probability, accessibility, time}`

Not every relation has every attribute. Missing values must remain missing rather than being invented.

## 5. Directed and undirected relations

Chemical and spatial relations may be represented as undirected where appropriate. Processes such as replication, regulation, and maintenance are generally directional and should retain direction.

## 6. Dynamic graph

The graph should be treated as `G(t)`, not necessarily a static object.

A minimal transition is:

`G(t) + process + context → G(t+Δt)`

Examples include replication, repair, binding/unbinding, chromatin accessibility changes, transcriptional regulation, and mutation.

## 7. Memory

Define memory operationally as information/state that persists across a specified transition.

Possible categories:

- `sequence_memory` — persistence of nucleotide order;
- `structural_memory` — persistence of a physical organization;
- `regulatory_memory` — persistence of a regulatory state;
- `lineage_memory` — persistence across cell divisions or generations.

These categories must not be treated as equivalent without evidence.

## 8. Candidate graph metrics

Potential metrics for later testing:

- degree and weighted degree;
- path structure;
- clustering;
- modularity;
- spectral gap / algebraic connectivity;
- motif frequency;
- robustness under edge/node perturbation;
- accessibility centrality;
- persistence of subgraphs through transitions.

No metric is privileged in advance. Metric selection must follow the biological question and preregistration.

## 9. Main falsification test

If a relation-aware representation provides no reproducible gain over an appropriately controlled sequence/structure baseline, the claim that relational architecture adds explanatory or predictive value must be reduced or rejected for that task.

## 10. Guardrail

Do not infer causality from graph topology alone. Biological mechanisms require independent evidence about physical interactions, temporal order, perturbation, or experimentally supported mechanisms.
