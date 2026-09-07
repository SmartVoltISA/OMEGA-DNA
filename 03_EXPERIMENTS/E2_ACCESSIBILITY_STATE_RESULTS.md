# E2 — Chromatin Accessibility / State Gate

**Status:** protocol and real-data gate assessed; no fabricated biological score.

## Question

Does measured chromatin accessibility represent a state variable that cannot be reduced to sequence composition alone?

## Declared real-data target

ATAC-seq measures genome-wide chromatin accessibility. ENCODE's pipeline produces filtered alignments, nucleotide-resolution signal tracks and peak sets; ENCODE also requires replicate/reproducibility QC and distinguishes nucleosome-free regions from mononucleosome fragments.

A suitable public human dataset is GEO GSE140203, which contains three GM12878 ATAC-seq replicates and K562 ATAC-seq data together with matched RNA-seq. The processed supplementary archive is 7.4 GB, while raw data are in SRA.

## Experimental design

For each cell state:

1. Define independent genomic loci from the processed ATAC signal/peaks.
2. Extract the corresponding GRCh38 DNA sequence.
3. Predict accessibility from sequence-only features on held-out loci.
4. Add measured accessibility-state relations only where they are available independently of the target being predicted.
5. Use chromosome/group holdout rather than random neighboring windows where possible to reduce leakage.
6. Run composition-matched controls.
7. Shuffle accessibility-state labels across held-out loci as the null.
8. Repeat over multiple seeds.

Primary metrics: AUROC/AUPRC for accessible-vs-inaccessible loci and Pearson/Spearman correlation for continuous signal.

## Result of this execution

The real-data gate is **OPEN, not PASSED**. The public dataset and official processing standards are confirmed, but the present execution environment did not retrieve the 7.4-GB processed archive or raw SRA payload. Therefore no experimental AUROC, AUPRC or correlation is reported here.

This is intentional: an inferred or sequence-generated accessibility score would be circular and would not qualify as an independent measured-state channel.

## What is established

`sequence → local physical structure → chromatin state/accessibility`

The existence and measurement framework for the state layer are independently established by ENCODE/GEO. The OMEGA empirical gate remains pending until the measured accessibility track is actually ingested and evaluated under the preregistered holdout/null protocol.

## Next gate

Proceed to **typed relations / regulatory architecture** only after the accessibility real-data gate is either executed or explicitly frozen as unavailable. Do not substitute a model prediction for measured state.
