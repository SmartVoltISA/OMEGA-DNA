# OMEGA-DNA — Full Relational Pass — 2026-09-07

## Scope
Completed controlled pass from primary sequence through local structure, typed relations, long-range regulation, regulatory network, cellular state and feedback. Real biological gates remain explicitly separated from synthetic results.

## Chain
`sequence → local structure → typed relation → long-range relation → regulatory network → cellular state → feedback`

## Completed controlled gates

### 1. Primary sequence
30-seed controlled motif benchmark:
- accuracy **0.996444 ± 0.002580**
- AUROC **0.996465 ± 0.002536**
- shuffled-label AUROC **0.497741 ± 0.020964**
- reverse-complement max error **0**

### 2. Local physical structure
30-seed nearest-neighbor thermodynamic proxy:
- GC-only MAE **0.51825 °C**
- GC + dinucleotide MAE **0.02235 °C**
- shuffled relation MAE **3.40342 °C**
- matched-GC sequences still differed in predicted Tm, demonstrating order dependence in the declared model.

### 3. Nucleosome-length local structure proxy
30 seeds, 147-bp synthetic periodic wrapping target:
- GC-only R² **0.7984 ± 0.0103**
- global dinucleotide R² **0.9990 ± 0.00004**
- phase-resolved relation model ≈ **1.0**
- shuffled phase relation MAE **0.05243**

### 4. Typed regulatory relations
30 seeds:
- baseline AUROC **0.8012 ± 0.0095**
- typed/cooperative relation AUROC **0.8465 ± 0.0074**
- shuffled relation AUROC **0.6805 ± 0.0103**

### 5. Long-range enhancer–promoter relation
30 seeds:
- sequence-only AUROC **0.65555 ± 0.01010**
- sequence + long-range relation **0.75156 ± 0.00845**
- shuffled relation **0.57435 ± 0.01046**
- relation vs sequence **t=51.57, p=4.43×10⁻³⁰**

### 6. Regulatory network → cellular state
50 seeds, temporal holdout:
- sequence/state AUROC **0.91914 ± 0.02088**
- relational state AUROC **0.96714 ± 0.00996**
- full topology/state AUROC **0.96709 ± 0.01004**
- relational vs sequence **t=21.35, p=1.83×10⁻²⁶**
- full topology vs sequence **t=21.12, p=2.91×10⁻²⁶**

### 7. Feedback / maintenance
50 seeds:
- no-feedback error **0.530745 ± 0.026956**
- feedback error **0.514994 ± 0.024866**
- paired **t=-45.91, p=6.18×10⁻⁴²**

## What the full controlled pass supports

The evidence consistently supports the narrower architectural statement:

`explicit relation/state/history can carry predictive information that is not contained in the corresponding local representation alone`

The effect survives independent holdout tests and relation-shuffle controls in the declared synthetic systems.

## What is NOT claimed

- DNA is not declared fully decoded.
- Synthetic targets are not biological measurements.
- Predicted regulatory edges are not experimental edges.
- No human enhancer→gene mechanism is declared proven.
- No new biological law is claimed.

## Real-data boundary

The decisive remaining work is biological validation using independently measured or independently annotated data: TF binding, accessibility, 3D contacts, enhancer/promoter annotations, gene expression and cellular state. The real DNALongBench sequence payload is multi-gigabyte and is not available in the current execution environment; therefore no fabricated biological score is inserted.

## Current architectural endpoint

`sequence → structure → relation → regulatory architecture → network → state → feedback → persistence/memory`

The remaining major empirical layer is to connect this architecture to real genomic measurements and then test persistence/memory and causal perturbation under the same strict controls.
