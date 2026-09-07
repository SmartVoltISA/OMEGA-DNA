# OMEGA-DNA Architecture Coverage Matrix — 2026-09-07

## Purpose

Single map of what has been modeled, what has been tested synthetically, and what still requires real biological validation.

| Layer / branch | Synthetic controlled test | Real-data gate | Status |
|---|---|---|---|
| Primary sequence information | D1 sequence benchmark, 30 seeds | Full-genome / task-specific | Synthetic PASS; biological OPEN |
| Local physical structure / thermodynamic proxy | E2 thermodynamic | Measured physical/biophysical data | Synthetic PASS; biological OPEN |
| Nucleosome-like local structure | E2 nucleosome proxy | MNase/nucleosome occupancy | Synthetic PASS; biological OPEN |
| Chromatin accessibility | E2 accessibility | ATAC-seq | Synthetic PASS; biological OPEN |
| Typed regulatory relations | E3 TF-like relation | TF ChIP/Factorbook | Synthetic PASS; biological OPEN |
| Enhancer-promoter / long-range relations | E3 enhancer-promoter | Hi-C/HiChIP/ChIA-PET/PCHiC | Synthetic PASS; biological OPEN |
| Regulatory network topology | E3 topology | Measured regulatory network | Synthetic PASS; biological OPEN |
| Cellular state | E4 network → state | Matched RNA/chromatin/state assays | Synthetic PASS; biological OPEN |
| Feedback / maintenance | E4 feedback | Time-series perturbation | Synthetic PASS; biological OPEN |
| Persistence / memory | E5 memory | Longitudinal/epigenetic memory data | Synthetic PASS; biological OPEN |
| Causal intervention | E5 computational ablation | Biological perturbation | Computational PASS; biological OPEN |
| Replication context | E6 replication context | Replication timing/origin data | Synthetic PASS; biological OPEN |
| Repair context | E6 repair context | Lesion/repair-response data | Synthetic PASS; biological OPEN |
| Evolutionary memory | E6 evolutionary context | Multi-species/constraint data | Synthetic PASS; biological OPEN |
| Variant context | E6 variant context | Independent functional assays | Synthetic PASS; biological OPEN |
| Non-canonical DNA structure | E6 non-canonical context | Structure-specific experimental data | Synthetic PASS; biological OPEN |
| Architecture self-stress | E7 self-stress | External real-data stress test | Synthetic PASS; external OPEN |
| External dataset ingestion | Validator + audit workflow | User-provided/public data | Tool READY |
| Genome-scale relational map | Architecture defined | Real genome-scale integration | OPEN |
| Cross-cell-type generalization | Partial synthetic state tests | Independent cell types | OPEN |
| Provenance/conflict resolution | Protocol defined | Multi-assay real data | OPEN |

## Interpretation

`Synthetic PASS` means the declared computational mechanism behaved as expected under controlled assumptions. It does not mean biological validation has passed.

`Biological OPEN` means the real-data test is either not yet run, not independently labeled, or not sufficiently reproducible to support a biological conclusion.

## Current architectural chain

```text
molecular primitive
→ sequence
→ local physical structure
→ typed relation
→ regulatory architecture
→ 3D organization
→ cellular state
→ process
→ output
→ feedback / maintenance
→ persistence / memory
→ causality
→ evolution
```

Additional branches:

```text
replication
repair
variants
non-canonical structures
recombination
transcription
splicing
translation
chromosome dynamics
mitochondrial genome
```

## Next priority order

1. Run the real external biological gate on an independently supplied or public dataset.
2. Add capacity-matched long-context sequence-only baselines.
3. Test measured 3D relations with independent labels.
4. Test real replication and repair contexts.
5. Test real variant functional effects.
6. Add causal perturbation where available.
7. Build genome-scale relational representation.
8. Test cross-cell-type/state generalization.
9. Formalize multi-assay provenance and conflict resolution.

## Rule

Do not mark a biological layer PASS merely because its synthetic analogue passed. The matrix deliberately keeps those evidence classes separate.
