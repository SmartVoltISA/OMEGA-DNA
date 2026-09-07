# OMEGA-DNA Architecture Coverage Matrix — 2026-09-07

Legend: **PASS** = controlled computational test completed; **OPEN** = real empirical gate remains; **BLOCKED** = required payload unavailable; **LIMITED** = tested only by proxy/synthetic representation.

| Layer | Main test | Status | Evidence | Real-data gate / next test |
|---|---|---|---|---|
| 0 Molecular primitives | E1 foundation/base-pair models | PASS/LIMITED | OBSERVED computational | empirical physical calibration |
| 1 Primary sequence | E1 sequence extraction | PASS | OBSERVED computational | real functional benchmark |
| 2 Local physical structure | E2 thermodynamic + nucleosome-like models | PASS/LIMITED | OBSERVED computational | measured structure/occupancy |
| 2 State/accessibility | E2 accessibility | PASS/LIMITED | OBSERVED computational | ENCODE/GEO payload |
| 3 Typed regulatory relations | TF-like relation test | PASS/LIMITED | OBSERVED computational | ChIP/Factorbook payload |
| 3 Enhancer-promoter relation | pair benchmark | PASS/LIMITED | OBSERVED computational | measured contact + functional labels |
| 4 Regulatory topology | network topology | PASS/LIMITED | OBSERVED computational | genome-scale graph |
| 5 Cellular state | regulatory state transition | PASS/LIMITED | OBSERVED computational | cross-cell-type/state benchmark |
| 6 Memory/persistence | history model + ablation | PASS/LIMITED | OBSERVED computational | longitudinal/epigenetic data |
| 7 Replication context | remaining architecture pass | PASS/LIMITED | OBSERVED computational | measured replication timing/origins |
| 8 Repair context | remaining architecture pass | PASS/LIMITED | OBSERVED computational | lesion/repair-response data |
| 9 Evolutionary memory | multi-species proxy | PASS/LIMITED | OBSERVED computational | multi-species conservation/selection |
| 10 Variant context | variant-context proxy | PASS/LIMITED | OBSERVED computational | independent variant-effect assays |
| 11 Non-canonical DNA structure | structural proxy | PASS/LIMITED | OBSERVED computational | measured structure maps |
| 12 Causality | synthetic perturbation | PASS/LIMITED | OBSERVED computational | biological perturbation |
| 13 Long-context sequence | DNALongBench branch/audit | BLOCKED | dataset payload unavailable | obtain/reference FASTA, execute frozen benchmark |
| 14 Real relational biology | E6 | OPEN | HYPOTHESIS | qualifying public multimodal dataset |
| 15 Cross-assay provenance | registry/validator | OPEN | ANNOTATED | provenance/conflict graph |
| 16 Genome-scale functional map | master objective | OPEN | UNKNOWN | chromosome-level relational benchmark |

## Critical interpretation

The synthetic suite demonstrates that the architecture can represent information in sequence, typed relations, state and persistence, and that relation features can be made necessary in controlled worlds. It does **not** demonstrate that the same advantage exists in biological DNA.

A key self-stress requirement is that relations must sometimes be redundant and sometimes useless. The architecture must not award value merely because a relation channel exists. Therefore the real E6 gate remains the decisive discriminator.

## Acceptance discipline

A real gate can be marked PASS only if it includes:
1. capacity-matched sequence-only baseline;
2. typed relation model;
3. chromosome/region leakage-safe holdout;
4. relation-shuffled null;
5. label-shuffled null;
6. fixed primary metric;
7. uncertainty/effect size;
8. provenance and assembly audit;
9. independent replication or robustness analysis.
