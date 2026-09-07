# E6 — Real Biological Gate: Sequence → Relations → Cellular State

**Status:** preregistered protocol; chunked execution path prepared; biological metrics remain OPEN until real payloads are actually processed.

## Objective
Test whether the relational architecture adds predictive information on independently measured human regulatory data beyond a capacity-matched sequence-only baseline.

## Primary task
For one matched human cell type, predict **high vs low target-gene expression** for promoter-linked distal regulatory regions.

A sample is an enhancer/promoter-gene candidate. The label is derived from RNA expression of the target gene, not from the contact call itself.

## Required independent data
1. Reference genome FASTA, GRCh38 or hg19 with matching coordinates.
2. ATAC-seq or DNase peaks for the same cell type.
3. H3K27ac/TF ChIP-seq peaks where available.
4. Enhancer-promoter contacts from HiChIP, promoter-capture Hi-C, ChIA-PET or equivalent.
5. RNA-seq expression for target genes.

A suitable public example is the GSE188405 family: matched human ATAC-seq, RNA-seq and H3K27ac HiChIP across human cell types. The GM12878 subset has dedicated ATAC and HiChIP records. Another suitable resource is the GSE113481/GSE113482/GSE113480 family, combining promoter-capture Hi-C, RNA-seq and ATAC-seq in human neural cell types.

## Chunked reference strategy
A multi-gigabyte reference FASTA is **not** loaded into RAM as one object.

`E6_CHUNKED_REFERENCE_EXTRACTOR.py` implements the intended pipeline:

`large reference → indexed byte ranges → ≤100 MiB chunks → interval extraction → compact candidate table → E6 runner`

The extractor:
- reads the `.fai` index;
- determines only the genomic intervals actually required by the candidate table;
- merges nearby byte ranges;
- downloads each merged range with HTTP Range requests;
- caps each range at `--chunk-mb` (default 100 MiB);
- caches completed chunks so interrupted runs can resume;
- refuses servers that silently ignore Range requests;
- discards chunk payloads after extracting the requested sequences.

Thus the full 3.16 GB DNALongBench hg19 reference can be treated as a stream of bounded pieces rather than a single memory allocation. The benchmark's published ETGP reference is approximately 3.16 GB. The same strategy applies to other large FASTA inputs.

## Models
### A — sequence-only baseline
Features are computed only from the enhancer and promoter sequences:
- GC fraction
- base entropy
- k-mer frequencies
- local dinucleotide relations
- motif counts if a fixed motif library is declared before the run

### B — relational model
Uses the same sequence feature budget plus pre-declared measured relations:
- enhancer accessibility
- promoter accessibility
- TF/H3K27ac occupancy indicators
- contact strength / contact significance
- genomic distance
- relation degree/count features

No feature may be computed from the target expression label.

## Capacity control
The two models must use the same train/test rows and comparable parameter count. A stronger sequence-only model must be run if the relational model has materially greater capacity.

## Holdout
Primary split is by genomic chromosome, not random rows. Recommended:
- train: chromosomes 1–16
- validation: 17–19
- test: 20–22 + X

No enhancer/promoter pair from a held-out chromosome may occur in training through duplicated coordinates.

## Null controls
1. Shuffle relation vectors within the training set while preserving marginal distributions.
2. Shuffle target labels within each cell type.
3. Distance-matched relation shuffle.
4. Sequence-only capacity-matched control.

## Primary endpoint
AUROC on the untouched chromosome holdout.

Secondary endpoints:
- AUPRC
- calibration error
- paired bootstrap difference in AUROC
- relation-shuffle degradation

## Acceptance rule
The relational model is considered a **biological gate pass** only if all are true:
1. relational AUROC > sequence-only AUROC on the untouched holdout;
2. the improvement survives chromosome-level bootstrap/permutation testing;
3. shuffled relations return to the sequence-only regime;
4. the result survives a capacity-matched sequence baseline;
5. no target-derived or post-label feature leakage is detected.

A single significant p-value is not sufficient.

## Causal extension
Only after the predictive gate passes, use independent perturbation data (CRISPRi/CRISPRa or regulator perturbation) to test whether measured relation changes predict expression changes. Predictive association and computational ablation are not biological causality.

## Current execution state
The controlled synthetic chain through memory/persistence is complete. The real biological gate is **OPEN**. The chunked execution path is now implemented, but no biological metric is claimed until the external genomic payload is successfully retrieved and processed. No result is fabricated merely because the file is large.

## Reproducibility
Record:
- dataset accession and sample IDs;
- genome build;
- exact input file checksums;
- coordinate liftover, if any;
- feature schema;
- split chromosomes;
- chunk size and Range manifest;
- random seeds;
- model hyperparameters;
- null permutations;
- software versions.
