# E4 — Real-data benchmark protocol

Date: 2026-09-07
Status: preregistered design; execution requires a machine with access to the public benchmark files.

## Question

Does an explicit OMEGA relational/state representation add predictive information beyond DNA sequence alone on a real functional-genomics task?

## Primary benchmark

Use the public Enformer/DNALongBench regulatory-sequence benchmark family. Inputs are long human/mouse DNA windows (~196,608 bp) and experimentally measured epigenomic/transcriptional tracks. DNALongBench explicitly defines this as a long-range sequence-to-function benchmark.

## Primary comparison

A. Sequence-only baseline: DNA sequence only.

B. OMEGA-typed model: same sequence representation plus explicitly measured relation/state channels available from the benchmark, with relation types kept separate rather than collapsed into one feature channel.

C. Shuffled-relation null: same B architecture, but relation assignments are shuffled within the training split while preserving marginal distributions.

D. Ablations: remove each relation family independently.

## Fairness controls

- identical train/validation/test split;
- identical target and evaluation metric;
- matched parameter budget as closely as practical;
- same early-stopping rule;
- same random seeds;
- no test-set tuning;
- no relation information crossing split boundaries;
- report compute and wall-clock cost;
- report uncertainty over independent seeds.

## Primary endpoint

Delta = performance(OMEGA typed) - performance(sequence-only).

A positive result is considered evidence of complementarity only if:

1. Delta is positive on the held-out test set;
2. the relation-shuffled null does not reproduce the gain;
3. at least two independent seeds reproduce the direction;
4. the gain survives capacity-matched ablation;
5. the relation channel contains experimentally measured information unavailable to the sequence input.

## Stronger endpoint

Variant or state intervention: modify/remove a declared relation while keeping the underlying sequence fixed, then test whether the predicted functional change agrees with an independently measured outcome.

## Failure criteria

OMEGA does not demonstrate additional predictive value if the gain disappears under relation shuffling, capacity matching, or independent test replication.

A null result is scientifically useful: it means the explicit relational representation adds no measurable value for this task, even if it remains a valid descriptive architecture.

## Important boundary

This protocol does not allow the claim that a graph representation is novel merely because graph terminology is used. Modern genomic models already learn long-range interactions and context. The test is strictly incremental predictive value from explicit typed biological relations/state.
