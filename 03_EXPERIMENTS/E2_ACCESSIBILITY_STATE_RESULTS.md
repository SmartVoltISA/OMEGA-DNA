# E2 — Chromatin accessibility / state

**Status:** synthetic controlled gate completed; real ATAC-seq biological gate remains OPEN.

## Question
Can relational sequence features carry predictive information about a context/state variable beyond GC composition, under held-out evaluation?

## Controlled protocol
- 10,000 synthetic 200-bp sequences per seed
- 30 independent seeds
- 70/30 stratified holdout
- State generated from a declared hidden accessibility-like variable combining GC, sequence-order statistics, two short motifs and noise
- Baseline: GC fraction
- Relation model: GC + 16 dinucleotide frequencies
- Combined: relation model + motif indicators
- Nulls: shuffled held-out features and shuffled held-out labels

## Results

| Model | AUROC mean ± SD | AUPRC mean ± SD |
|---|---:|---:|
| GC only | 0.564666 ± 0.008439 | 0.554983 ± 0.008253 |
| GC + dinucleotide relations | 0.617808 ± 0.011665 | 0.607208 ± 0.013535 |
| Combined relational + motifs | 0.885601 ± 0.006126 | 0.884097 ± 0.007808 |
| Shuffled combined features | 0.499299 ± 0.008578 | — |

Independent one-run shuffled-label null AUROC: **0.495579**.

## Interpretation
The controlled state benchmark passes: relational sequence information improves held-out prediction over GC alone, while destroying the relational structure collapses AUROC to chance. This establishes a reproducible synthetic state-transition gate, not a biological ATAC-seq result.

## Real biological gate
GEO GSE140203 contains GM12878 ATAC-seq replicates 1–3 and K562 ATAC-seq, with processed fragment, count and peak files. GM12878 replicate 1 has a 184.5 MB fragments file and 3.8 MB peak file; replicate 2 has a 124.3 MB fragments file and 3.8 MB peak file. The complete series raw archive is 7.4 GB. NCBI identifies the study as simultaneous chromatin-accessibility and gene-expression profiling in the same cells.

ENCODE also provides deeply profiled GM12878 ATAC-seq files such as ENCFF415FEC; that BAM is 2.34 GB and contains 23.66M distinct fragments after processing.

The real-data gate is **not passed** because the present compute environment cannot retrieve/process the required binary sequencing payloads. No real ATAC-seq score is fabricated.

## Next step
Proceed to **typed relations / regulatory architecture**, while keeping the real accessibility gate recorded as OPEN for later execution when binary data are available.
