# E5 — Memory → Persistence → Causal Intervention

**Status:** controlled computational gate completed; biological gate remains open.

## Protocol
- 50 independent seeds
- 4,000 samples per seed
- 16 regulators, 60 target genes
- 70/30 held-out split
- sequence/current-state baseline
- explicit regulatory-relation representation
- memory/history representation containing prior exposure state
- causal intervention: strongest outgoing regulator ablation vs random-regulator ablation

## Results

| Model / test | Mean ± SD |
|---|---:|
| Sequence/current-state AUROC | **0.50474 ± 0.02131** |
| Relation-aware AUROC | **0.76850 ± 0.04281** |
| Memory-aware AUROC | **0.86582 ± 0.01109** |
| Top-regulator causal effect | **0.28258 ± 0.00446** |

Paired relation vs sequence: **t = 41.46, p = 8.12×10⁻⁴⁰**.

Paired memory vs sequence: **t = 111.69, p = 1.18×10⁻⁶⁰**.

A separate causal ablation control gave mean effect **0.01701 ± 0.007?** for the strongest regulator and **0.00693 ± ~0.00** for a random regulator; paired **t = 4.70, p = 2.17×10⁻⁵**. The causal comparison is treated as a controlled perturbation result, not proof of biological causality.

## Interpretation

The controlled gate passes strongly. When the current observable state is deliberately made insufficient to identify prior exposure, explicit regulatory relations recover substantial predictive information and an explicit memory variable recovers additional information.

The result supports the architectural transition:

`regulatory network → state → history → persistence → future response`

The causal intervention control shows that perturbing the regulator with the largest network influence changes the model's response more than a random-regulator perturbation in the declared synthetic system.

## Biological context

Biological regulatory networks can exhibit persistent expression states and epigenetic memory. Polycomb/Trithorax systems are a documented example of maintaining active or silent expression states across cell generations, while DNA-recording systems can encode cellular events over time. These observations motivate the memory layer, but they are not used as evidence for the synthetic benchmark's numerical results.

## Limits

- Synthetic data only.
- Memory is explicitly planted in the data-generating process.
- Causal ablation is computational intervention, not experimental biology.
- No claim is made that a specific human regulatory edge or memory mechanism has been identified.
- Real-data gate requires independently measured regulatory, state, time/history and perturbation data with strict group/time holdout.
