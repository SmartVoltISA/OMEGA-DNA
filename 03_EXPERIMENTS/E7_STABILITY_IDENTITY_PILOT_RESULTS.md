# E7 — Stability and Identity in Abstract Networks: Pilot Results

**Experiment ID:** E7-ODNA-STAB-01  
**Status:** Exploratory computational pilot; not preregistered; not biological evidence  
**Date:** 2026-10-17  
**Runner:** `E7_STABILITY_IDENTITY_RUNNER.py`

## Question

In a deliberately simplified dynamical network, how do target-aligned topology and explicit restoring feedback affect retention of a predefined target state under repeated perturbation and small edge turnover?

This pilot operationalizes only one narrow aspect of stability. It does not model cells, metabolism, DNA chemistry, mirror organisms, or the origin of life.

## Model and fixed settings

- Nodes: 80 binary-state nodes.
- Target labels: balanced 0/1, assigned at random per replicate.
- Initial state corruption: 15% of nodes flipped.
- Run length: 200 update steps.
- Per-step state perturbation: 3% probability per node.
- Edge turnover: 1% probability per node per step.
- Replicates: 40 seeds per model.
- Graph degree target: 8 outgoing selections per node before symmetrization.
- Modular graph: approximately 80% of selected neighbors from the same target class, 20% from the other class.
- Feedback strength: 1.5 target-directed vote units in feedback conditions.
- Metric: fraction of nodes matching the model's predefined target state, averaged across all steps; also reported for the first and last 50 steps.

Because this was an exploratory pilot, the design and parameter choices were not frozen in a formal preregistration before execution. The results must not be presented as a confirmatory test.

## Conditions

1. **random_static:** random topology, no restoring feedback.
2. **modular_static:** topology aligned to target classes, no restoring feedback.
3. **modular_feedback:** target-aligned modular topology with an explicit restoring signal toward the predefined target.
4. **shuffled_feedback:** same modular graph construction, but target labels are shuffled after graph construction; restoring feedback remains, serving as a negative control for topology–target alignment.

## Results

| Model | Mean target retention over 200 steps | SD across 40 runs | First 50 steps | Last 50 steps |
|---|---:|---:|---:|---:|
| random_static | 0.5010 | 0.0008 | 0.5040 | 0.5000 |
| modular_static | 0.7411 | 0.1373 | 0.9318 | 0.5570 |
| modular_feedback | 0.9815 | 0.0300 | 0.9969 | 0.9468 |
| shuffled_feedback | 0.5032 | 0.0030 | 0.5127 | 0.5000 |

The values are fractions, not percentages. For example, 0.9815 corresponds to 98.15% mean target retention.

## Interpretation

- In this toy model, random topology without maintenance lost target alignment and approached chance-level retention.
- Target-aligned modular topology retained the target state better at first, but retention degraded over time under perturbation and edge turnover.
- Adding an explicit target-restoring signal produced high retention in the modular condition.
- When target labels were shuffled relative to the modular topology, feedback alone did not preserve the original target alignment in this setup.

## What this does and does not show

**Supported only within this toy model:** a known restoring signal plus topology aligned with the target labels can maintain a predefined state better than the tested baselines.

**Not established:** that relations are the universal basis of life; that this mechanism explains biological stability; that the result generalizes to cells; that a graph is alive; or that this tells us how to create a mirror organism.

A key limitation is that the feedback term is explicitly given the correct target labels. This makes the feedback condition an engineered controller, not an emergent self-maintenance mechanism. Its performance is therefore expected to be high when the target signal is strong enough. Feedback cost was not matched against the no-feedback models. Graph construction also changes the random-number stream, so same-numbered seeds are not fully paired trajectories.

## Decision

**Pilot outcome:** the toy implementation behaves consistently with its rules, but the result is largely built into the feedback design. It does not yet test the stronger claim that a system can infer or preserve its organization without being handed the target state.

**Do not count this as evidence for a new biological principle.**

## Required next experiment

Before a confirmatory run:

1. Freeze the protocol, metrics, parameter grid, and falsification rules.
2. Use common, pre-generated perturbation schedules across matched conditions.
3. Include equal-budget controls and explicitly account for feedback/resource cost.
4. Replace the privileged target signal with a maintenance rule based on observable error or local state only, then compare against a capacity-matched controller baseline.
5. Run ablations and topology-shuffle controls.
6. Report uncertainty intervals and all failed conditions.
7. Keep the abstract model separate from biological claims; any biological conclusion requires independent empirical evidence.

## Reproduction

Run from the repository root:

```bash
python 03_EXPERIMENTS/E7_STABILITY_IDENTITY_RUNNER.py
```

The script writes a per-replicate CSV to `03_EXPERIMENTS/E7_STABILITY_IDENTITY_RAW.csv` by default and prints aggregate metrics. It requires Python 3 and NumPy.

## Audit trail

- Runner commit: `e6541bf0df2bea88d0b8be4434cc9b1f7f050b93`
- Pilot parameters are encoded in the runner.
- This report records an exploratory run, not a preregistered confirmatory result.
