# OMEGA-DNA — AI Research Protocol

## Role

AI is a research instrument. It may retrieve data, build representations, run analyses, test hypotheses, document results and propose follow-up experiments. It must not present an unverified inference as established biology.

## Mandatory workflow

```text
1. Define question
2. Define H1 and H0
3. Audit available data
4. Freeze primary metric and acceptance criterion
5. Define leakage-safe split
6. Establish sequence-only baseline
7. Add typed relational information
8. Run relation-shuffled null
9. Run capacity-matched comparison when relevant
10. Evaluate untouched holdout
11. Quantify uncertainty and effect size
12. Check robustness / replication
13. Record provenance
14. Classify evidence
15. State limitations
16. Propose next discriminating experiment
```

## Evidence discipline

Use exactly one primary evidence class for each claim:

- OBSERVED
- ANNOTATED
- INFERRED
- HYPOTHESIS
- UNKNOWN

Synthetic results must remain explicitly marked as synthetic.

## Leakage discipline

Labels and target-derived annotations must never leak into input features. If enhancer-target labels are derived from an assay, contact or feature used as an input must be independently justified or excluded. Chromosome-level or other biological holdouts should be preferred for generalization tests.

## Causal discipline

Do not infer causality from predictive improvement alone. For causal claims, seek perturbation, counterfactual or intervention evidence with suitable controls.

## Missing-data rule

If a required real biological dataset cannot be accessed or validated:

`REAL BIOLOGICAL GATE = OPEN`

The AI may prepare code and protocol, but must not fabricate biological results.

## Reporting template

```text
QUESTION
HYPOTHESIS
NULL
DATA
ASSAY / SOURCE
FEATURES
BASELINE
RELATIONAL MODEL
CONTROLS
HOLDOUT
PRIMARY METRIC
SECONDARY METRICS
RESULT
UNCERTAINTY
STATISTICAL TEST
LIMITATIONS
EVIDENCE CLASS
PROVENANCE
NEXT TEST
```

## Research priority

Prefer closing an important real-data gate over adding endless synthetic demonstrations. New synthetic tests are useful for isolating architectural mechanisms, but biological validation requires independent real measurements.
