# E2 — Nucleosome / Local Physical Structure

**Status:** controlled computational gate completed; experimental-data gate remains open.

## Question

Does DNA sequence order contain information relevant to a nucleosome-like local wrapping constraint beyond GC composition alone?

## Important scope

This experiment does **not** measure biological nucleosome occupancy. The target is a fixed synthetic proxy using 10-bp periodicity of selected dinucleotide classes (AA/TT/AT/TA) across a 147-bp nucleosome-length window. It is therefore evidence about the information carried by local sequence order and the relational representation, not evidence for a new biological law.

## Protocol

- 6,000 random 147-bp sequences per seed
- 30 independent seeds
- 70/30 train/test split
- Baseline: GC fraction
- Model 1: GC + 16 global dinucleotide frequencies
- Model 2: GC + global dinucleotides + 10-phase-resolved dinucleotide relations
- Null: shuffle the phase-resolved relation features in the held-out set
- Separate matched-GC ordering control: 10,000 sequences

## Results

| Model | MAE | R² |
|---|---:|---:|
| GC only | 0.016562 ± 0.000317 | 0.798395 ± 0.010323 |
| GC + global dinucleotides | 0.001150 ± 0.000023 | 0.999029 ± 0.000042 |
| + phase-resolved local relations | 0.000001 ± 0.00000003 | 1.000000 ± 0.00000000006 |
| shuffled local relations | 0.052432 ± 0.001096 MAE | — |

### Matched composition control

For 5,000 matched pairs with GC fractions differing by <0.01:

- mean absolute target difference: **0.023126**
- median: **0.019524**
- 90th percentile: **0.048095**
- 99th percentile: **0.076190**

Thus sequences with nearly the same composition can have materially different values of the declared wrapping proxy solely because their order differs.

## Interpretation

The controlled gate passes strongly:

`base composition → sequence order → local/phase relations → physical wrapping proxy`

The important result is not the near-perfect score itself. It is the controlled separation between composition and order: GC alone leaves substantial unexplained variation, while local relational information recovers it; destroying the relational structure in the held-out set collapses performance.

This extends the previous Tm_NN experiment from **thermodynamic duplex behavior** toward a **147-bp nucleosome-length periodic local-structure constraint**.

## Real-data gate

Experimental nucleosome positioning is available publicly. NCBI GEO accession **GSE35586** contains ENCODE MNase-seq nucleosome-position data for human GM12878 and K562 cells. ENCODE describes nucleosomes as the first level of chromatin packaging and notes the 147-bp core DNA wrapped around the histone octamer. citeturn0search3

The real-data gate was not declared passed because the present compute environment cannot retrieve the required raw/binary sequencing payloads. No experimental performance number is substituted for the missing data.

## Next gate

Proceed to **chromatin accessibility / state**. ENCODE ATAC-seq provides genome-wide accessibility profiles and processed signal/peak outputs, including replicated peaks and nucleosome-related fragment-length information. citeturn0search0turn0search2

The next experiment must keep measured accessibility independent from sequence-derived predictors and use held-out loci/cell states, with shuffled-state and composition-matched nulls.
