# E2 — Local Physical Structure: Sequence Order Beyond GC

**Run:** 2026-09-07  
**Status:** executed controlled molecular-physics benchmark

## Question

Does sequence order contain predictive information about a fixed local physical proxy beyond GC composition alone?

## Target

Nearest-neighbor DNA duplex melting temperature (`Tm_NN`) as implemented by Biopython's declared DNA nearest-neighbor thermodynamic model.

This is deliberately a **physical proxy**, not a biological function annotation.

## Design

- sequence length: 60 bp;
- 20,000 independently generated sequences;
- fixed alphabet A/C/G/T;
- 70/30 train/test split;
- 30 independent seeds;
- baseline: GC fraction only;
- relational/local model: GC + 16 dinucleotide frequencies;
- null: test-set relational features shuffled before prediction;
- metric: MAE and R².

## Results

| Model | MAE mean ± SD | R² mean ± SD |
|---|---:|---:|
| GC only | 0.51825 ± 0.00398 °C | 0.9545 ± 0.0007 |
| GC + dinucleotide relations | **0.02235 ± 0.00024 °C** | **0.99988 ± 0.00001** |
| shuffled relations | 3.40342 ± 0.03070 °C | not used as primary metric |

A separate matched-composition check generated 10,000 sequence pairs with identical length and GC composition but different ordering. The mean absolute Tm difference was **2.2959 °C**, median **2.2657 °C**, 90th percentile **3.4124 °C**, and 99th percentile **4.3264 °C**.

## Interpretation

The result is strong evidence that **local sequence order carries physical information not recoverable from GC composition alone** under the declared nearest-neighbor model.

The OMEGA interpretation is precise:

```text
sequence letters
      ↓
ordered local relations (dinucleotides)
      ↓
physical interaction terms
      ↓
local duplex property
```

This supports the architectural distinction between **primary sequence information** and **local physical structure**.

## Controls

1. Independent 70/30 holdout: PASS.
2. 30 seeds: PASS; same direction in every run.
3. Relation shuffle destroys the advantage: PASS.
4. Matched GC / different order produces different physical prediction: PASS.
5. Fixed sequence length: PASS.

## Important limitation

`Tm_NN` is a computational thermodynamic model. The experiment therefore demonstrates that the OMEGA representation can preserve sequence-order information relevant to a declared physical model; it does **not** by itself establish a new physical law or prove that every genomic region follows this simple proxy.

The next D2 tests should therefore move from this controlled duplex proxy toward independent structural observations: nucleosome positioning/occupancy, methylation, accessibility and experimentally measured non-canonical structures.

## Verdict

**D2 local physical structure — controlled test supported.**

The next target is **nucleosome/chromatin state**, where the physical structure becomes context-dependent and experimentally measured rather than purely sequence/thermodynamic.
