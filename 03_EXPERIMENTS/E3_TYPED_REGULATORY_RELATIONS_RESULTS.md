# E3 — Typed Regulatory Relations

**Status:** controlled computational gate PASSED; real biological TF/enhancer gate remains open.

## Question
Does an explicit relation between binding sites add predictive information beyond motif count and GC composition?

## Protocol
- 30 independent seeds
- 8,000 sequences/seed
- 160 bp sequences
- 70/30 train/test split
- planted TF-like 8-bp motif
- baseline: motif count + GC
- relational model: baseline + number of motif pairs within 40 bp
- held-out null: shuffle the relational feature
- metrics: AUROC and average precision

## Results

| Model | AUROC | AP |
|---|---:|---:|
| motif count + GC | 0.80116 ± 0.00950 | 0.77862 ± 0.01381 |
| + cooperative spacing relation | **0.84652 ± 0.00738** | **0.87881 ± 0.00780** |
| shuffled relation | 0.68054 ± 0.01031 | 0.64199 ± 0.01221 |

Paired relation-vs-baseline AUROC: t = 51.33, p = 5.05e-30.
Paired shuffled-vs-relation AUROC: t = -80.80, p = 1.07e-35.

## Interpretation
The controlled relational gate passes: explicit spatial/cooperative relation information improves held-out prediction, and destroying that relation causes a large performance loss.

This supports the OMEGA representation transition:

`sequence features → typed relation → regulatory-state prediction`

It does **not** establish that the same effect size exists in real cells. The synthetic target was generated from the declared relation, so this is a representation/architecture test, not independent biological validation.

## Real biological gate
ENCODE provides human transcription-factor ChIP-seq binding tracks with processed peaks and signal, and Factorbook contains large collections of ENCODE TF-binding datasets and sequence/chromatin context. citeturn0search2turn0search4

A real gate should use independently measured TF binding, accessible chromatin, and enhancer/promoter annotations; chromosome or locus-group holdouts; motif-only versus relation-aware models; and shuffled relation nulls. No real-data score is claimed here until those measured tracks are ingested.

## Next
Proceed to enhancer–promoter / long-range regulatory relations. The key test is whether a measured spatial relation adds predictive information beyond local sequence and local chromatin state.
