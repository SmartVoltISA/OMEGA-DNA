# E4 — Real-data benchmark data access

Date: 2026-09-07

## Candidate dataset reached

A public Hugging Face mirror of DNALongBench is available as `jzshared/dnalongbench`.
The enhancer-target-gene component contains the K562 CRISPRi target table and exposes
these fields:

- gene coordinates and chromosome;
- enhancer/region coordinates and chromosome;
- gene identifier and strand;
- binary target (`positive` / `negative`);
- train/valid/test subset;
- gene expression change;
- `distance_to_tss`;
- `ABC_score`.

The mirrored Gasperini table is 222 kB and is directly viewable as text. The standard
K562 table is 347 kB. The underlying DNALongBench benchmark defines enhancer-target
gene prediction as a 450-kbp sequence binary-classification task and reports 2,602
samples for the standard ETGP dataset.

## Important limitation

The target table alone is not sufficient for the preregistered OMEGA comparison.
It contains relation/annotation variables such as distance and ABC score, but the
sequence input itself is stored separately in a multi-gigabyte genome FASTA. We must
not call a relation-only benchmark a sequence-vs-relation benchmark.

Therefore no biological `Delta` is recorded from this table alone.

## Correct execution path

1. Acquire the matching hg19 sequence FASTA and the target table.
2. Reconstruct the exact 450-kbp sequence input used by DNALongBench.
3. Build a sequence-only baseline from the same samples.
4. Add explicitly declared relation/state channels only when their provenance is
   independent of the sequence input.
5. Run the shuffled-relation null and family ablations.
6. Keep the published train/valid/test assignments; do not re-split by row.
7. Report held-out AUROC, seed variance, capacity, and compute.

## Why this is a useful checkpoint

The data access search succeeded: the real benchmark is public and inspectable.
The remaining blocker is acquisition of the paired genome sequence plus a reproducible
sequence baseline, not discovery of a suitable task.

No real-data predictive advantage is claimed until that paired execution is run.
