# Typed multigraph specification

## Purpose

Represent DNA without collapsing chemically different relations into one generic edge.

## Graph tuple

`G = (V, E, τ, w, s, M)`

- `V` — entities at the declared scale;
- `E` — relations between entities;
- `τ(e)` — relation type;
- `w(e)` — optional measured quantity with declared units/meaning;
- `s` — system state;
- `M` — persistent state or memory representation.

## Relation typing

Minimum initial types:

`covalent | hydrogen | stacking | spatial | topological | regulatory | maintenance`

The model may add relation types only when the added distinction corresponds to an observable or operational difference.

## Node typing

Minimum initial node types:

`atom | base | sugar | phosphate | nucleotide | strand | base-pair | protein | regulatory-region`

Node types are scale-dependent. A nucleotide may be a composite node at one scale and a subgraph at another.

## No hidden weights

If `w(e)` is absent, the edge is qualitative/typed only. A numerical value must never be inferred merely because the graph permits one.

## State transition

A process is represented as:

`G(t) → operation → G(t+Δt)`

Examples include replication, repair, binding, opening/closing, recombination and mutation.

## Architectural test

The model earns scientific value only if this typed representation produces a reproducible improvement on a declared task compared with a simpler baseline containing the same relevant information.

## Failure condition

If relation typing adds complexity but no measurable explanatory or predictive value, remove the unnecessary layer.