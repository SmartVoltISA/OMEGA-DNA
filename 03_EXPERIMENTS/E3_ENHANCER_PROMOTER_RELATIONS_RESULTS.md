# E3 — Enhancer–Promoter / Long-Range Relation Gate

**Status:** controlled computational gate completed; real biological gate remains open.

## Question
Does an explicit long-range relation between regulatory elements add predictive information beyond local sequence-derived features?

## Protocol
- 12,000 synthetic enhancer/promoter pairs per seed
- 30 independent seeds
- 70/30 holdout
- Sequence model: enhancer state + promoter state + compatibility
- Relation model: sequence features + explicit loop/contact relation + genomic distance
- Null: shuffle the loop relation in the held-out set
- Metrics: AUROC and average precision

## Results

| Model | AUROC | AP |
|---|---:|---:|
| Sequence-only | **0.65555 ± 0.01010** | **0.54232 ± 0.01226** |
| Sequence + long-range relation | **0.75156 ± 0.00845** | **0.69220 ± 0.01225** |
| Relation shuffled | **0.57435 ± 0.01046** | not used as primary endpoint |

Paired AUROC relation-vs-sequence: **t = 51.57, p = 4.43×10⁻³⁰**.

Paired AUROC shuffled-vs-sequence: **t = −37.93, p = 2.89×10⁻²⁶**.

## Interpretation
The controlled gate passes. The explicit long-range relation channel contributes substantial predictive information beyond the local sequence representation, while destroying that relation removes most of the added signal.

This is evidence about the information value of typed long-range relations in the declared synthetic system. It is **not** evidence that a particular human enhancer controls a particular gene.

## Biological gate
ENCODE ChIA-PET resources directly define long-range chromatin interactions as spatially proximal genomic regions that can be far apart along the chromosome. ENCODE ChIA-PET processing produces loop BEDPE files and filters to high-confidence loops with PET count >=3. These provide a suitable independent real-data relation channel.

The biological gate is not declared passed until measured ChIA-PET/Hi-C relations and independently defined regulatory targets are ingested under chromosome/group holdout, composition-matched controls and relation-shuffling nulls.

## Chain position
`sequence → local structure → typed relations → long-range regulatory architecture`

Next: real-data long-range relation benchmark, then enhancer–promoter target linkage and regulatory network structure.
