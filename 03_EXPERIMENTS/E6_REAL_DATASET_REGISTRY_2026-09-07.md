# E6 — Real Dataset Registry (2026-09-07)

## Primary candidate: GSE188405 family

**Accession:** GSE188405

The GEO SuperSeries contains matched regulatory measurements across human cell types:
- GSE188398 — ATAC-seq
- GSE188401 — H3K27ac HiChIP
- GSE186947 — RNA-seq
- GSE188403 — MPRA validation

The SuperSeries reports 90 samples and a combined raw archive of about 216.2 MB. The design explicitly matches RNA expression, chromatin accessibility and enhancer-promoter looping across cell types.

### GM12878 subset
- ATAC: GSM5680698
- H3K27ac HiChIP: GSM5680734
- RNA: use the corresponding GM12878 samples in GSE186947

The GM12878 HiChIP processed loop file is reported as `GSM5680734_GM12878.loops.csv.gz` (~1.5 MB). The ATAC subseries is distributed as processed BED files. This is a practical first target because the relation file is small enough to inspect and the modalities are matched.

## Secondary candidate: GSE11348x family

- GSE113480 — ATAC-seq
- GSE113481 — promoter-capture Hi-C
- GSE113482 — RNA-seq

These datasets cover iPSC-derived excitatory neurons, lower motor neurons, hippocampal DG-like neurons and primary astrocytes. The PCHi-C study reports hundreds of thousands of promoter-distal cis interactions and experimental validation of several enhancer-target relationships.

The PCHi-C processed files are large (individual interaction files can be hundreds of MB), so this is better as a second-stage replication after the smaller GSE188405/GM12878 run.

## Coordinate caution

GSE188405 loop and ATAC processing uses **hg19**. GSE113481 also reports **hg19**. The runner must therefore either use a matching hg19 reference FASTA or perform a declared, checksum-recorded liftover to GRCh38. Mixing coordinate systems is prohibited.

## Gate status

**Dataset identification: PASS.**

**Payload ingestion in the current execution environment: OPEN.** The environment can inspect GEO metadata but cannot directly ingest the GEO binary archives. Therefore no biological AUROC/AUPRC number is recorded until the actual payloads are available to the runner.

## Source records

NCBI GEO records:
- GSE188405: matched ATAC/RNA/HiChIP/MPRA SuperSeries.
- GSE188398: ATAC-seq.
- GSE188401: H3K27ac HiChIP.
- GSE186947: RNA-seq.
- GSE113480: ATAC-seq.
- GSE113481: promoter-capture Hi-C.
- GSE113482: RNA-seq.

## No-result rule

Do not infer biological success from the existence of compatible public datasets. The biological gate is passed only by an actual held-out run using the declared E6 protocol.
