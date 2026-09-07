# OMEGA-DNA — Remaining Architecture Pass

**Date:** 2026-09-07
**Status:** controlled computational extension completed; real biological gates remain open.

## Purpose
Extend the DNA architecture beyond the already tested sequence, local structure, regulatory network, cellular state, feedback and memory layers.

## New layers tested

### A. Replication context
`sequence → origin/context → replication outcome`

30 seeds × 5,000 samples; 70/30 holdout.
Sequence-only AUROC: **0.496564 ± 0.013866**.
Context-aware AUROC: **0.952626 ± 0.005685**.
Shuffled context: **0.510516 ± 0.169613**.
Paired t=187.234, p=2.935e-46.

Biological gate: OPEN. Required evidence includes experimentally measured replication timing/origin information.

### B. Repair context
`sequence → lesion/context → repair outcome`

Sequence-only: **0.498874 ± 0.013982**.
Context-aware: **0.928113 ± 0.006533**.
Shuffled context: **0.509134 ± 0.127233**.
Paired t=162.064, p=1.9237e-44.

Biological gate: OPEN. Computational context is not biological repair causality.

### C. Evolutionary memory
`sequence → historical constraint → present outcome`

Sequence-only: **0.497901 ± 0.013120**.
Context-aware: **0.853976 ± 0.010355**.
Shuffled context: **0.523818 ± 0.091629**.
Paired t=116.999, p=2.408e-40.

Biological gate: OPEN. Conservation/history must be separated from present function.

### D. Variant context
`variant → regulatory relation/context → functional effect`

Sequence-only: **0.498848 ± 0.013657**.
Context-aware: **0.926926 ± 0.006123**.
Shuffled context: **0.518895 ± 0.122699**.
Paired t=183.780, p=5.034e-46.

Biological gate: OPEN. Independent molecular or phenotype measurements are required.

### E. Non-canonical structure context
`sequence → context-dependent structure → state/output`

Sequence-only: **0.496320 ± 0.017299**.
Structural-context: **0.906359 ± 0.007079**.
Shuffled context: **0.497481 ± 0.121137**.
Paired t=129.330, p=1.324e-41.

Biological gate: OPEN. The next test must use measured G-quadruplex/i-motif or other structure maps.

## What is now covered conceptually

The architecture now explicitly contains:

`molecular primitive → sequence → local physical structure → typed relation → regulatory architecture → 3D organization → cellular state → process → output → feedback → memory → causality → evolution`

with additional explicit branches for:

- replication;
- repair;
- variants;
- non-canonical structures;
- evolutionary history.

## Important result
The same experimental pattern recurs across independent synthetic layers: when the generator contains information in a typed relation/context channel, a sequence-only representation cannot recover all of it, while the relation-aware representation can. Relation shuffling removes the advantage.

This is evidence about **representational capacity**, not evidence that biology implements the synthetic generator in exactly this form.

## Remaining major empirical gates

1. E6 real genomic benchmark with chunked FASTA ingestion.
2. Strong long-context sequence-only capacity-matched baseline.
3. Measured 3D genome relation benchmark.
4. Measured replication timing/origin benchmark.
5. Measured repair/lesion-response benchmark.
6. Measured non-canonical DNA structure benchmark.
7. Variant functional-effect benchmark with independent molecular assays.
8. Multi-species/evolutionary constraint benchmark.
9. Causal perturbation benchmark.
10. Genome-scale relational functional map.
11. Cross-cell-type/state generalization.
12. Cross-assay provenance consistency and conflict resolution.

## Architectural rule retained

No observed annotation is silently converted into a causal claim. Every region remains represented as a context-dependent object with provenance and evidence class.
