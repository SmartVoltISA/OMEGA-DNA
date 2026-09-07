# E4 — Parallel Branch Comparison

Date: 2026-09-07

## Design

Two parallel branches were created from the same `main` base:

- `exp/e4-sequence-only` — Branch A, sequence-only control.
- `exp/e4-relational` — Branch B, identical input plus explicitly typed relation/state channels.

The branches are not substitutes for one another. The comparison is A vs B under the same data-generating process, split, target and seeds.

## Full controlled A/B run

30 independent seeds, n=10,000 per seed, stratified 70/30 train/test split.

### Results

| Variant | Mean AUC | SD |
|---|---:|---:|
| A — sequence-only | 0.498467 | 0.007832 |
| B — sequence + relations | 1.000000 | 0.000000 |
| Shuffled-relation null | 0.494651 | 0.037132 |
| Relations-only | 0.500225 | 0.010538 |

### Paired comparisons

- B − A: mean delta = +0.501533; t = 350.7493; p = 3.6764e-54.
- Shuffled null − A: t = -0.5502; p = 0.5864.
- Relations-only − A: t = 0.7807; p = 0.4413.

## Full synthetic architecture suite

- E2 complementarity: L=10 detection 0.01480; L=100 detection 0.13912; L=1000 detection 0.77770; false-detect rate 0.
- E3 feedback: no feedback residual 0.20015; detection-only 0.20164; feedback 0.00012.
- E4 typed relation: typed accuracy 1.000; untyped topology 0.500.
- E5 dynamic memory: static 0.6494; history-aware 1.000.
- E6 contextual relation: sequence-only 0.5063; relation-aware 1.000.
- E8 invariance: relational invariant error 0.000; positional control error 0.4716.

## Interpretation

The controlled experiment demonstrates that the relational channel can carry predictive information that is absent from the sequence-only control in a synthetic system. The shuffled relation null removes the gain, while relations-only do not outperform sequence-only. This supports the architectural claim of complementarity within the controlled model.

It is NOT evidence of a new biological law. The real-data gate remains the preregistered DNALongBench benchmark: identical official split, sequence-only vs sequence+independently measured relations, shuffled-relation null, capacity matching and independent seeds.

## Real-data status

DNALongBench ETGP contains 2,602 samples, 450 kb sequence context and AUROC evaluation. The public dataset includes sequence FASTA plus target/split metadata. The FASTA mirror is approximately 3.16 GB. The current execution environment cannot download that multi-GB FASTA, so a real sequence+relation biological A/B run has NOT been fabricated or claimed here.

The real-data runner is already hardened for official train/validation/test splits and training-only relation shuffling. Its generic interface is documented in `E4_REAL_DATA_RUNNER.py`.
