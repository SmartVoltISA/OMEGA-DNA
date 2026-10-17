# E8 — Structural Memory Without a Target-Aware Controller

**Experiment ID:** E8-ODNA-STRUCT-01  
**Status:** Exploratory computational test; not a preregistered confirmatory experiment  
**Date:** 2026-10-17  
**Runner:** `E8_STRUCTURAL_MEMORY_RUNNER.py`

## Question

Can a network preserve a predefined state under perturbation when its update rule sees only local neighbor states and never receives the target labels directly?

This is a narrower test than the E7 pilot. It removes the direct target-restoring term. However, the aligned network's topology is deliberately constructed using the target labels. The experiment therefore tests whether structure can encode and preserve a pattern, not whether the pattern emerges spontaneously.

## Design

- 80 binary-state nodes; balanced target classes.
- 200 update steps.
- 100 replicate seeds per condition.
- Initial state corruption: 15% of nodes.
- State perturbation: 3% probability per node per step.
- Target and perturbation schedule are generated before graph construction, allowing common starting conditions and disturbances across conditions for each seed.
- Update rule: local majority of neighboring states; ties preserve the current state.
- No target labels are supplied to the update rule.
- No adaptive feedback controller and no explicit edge turnover in this experiment.
- Metric: fraction of nodes matching the target state, averaged over 200 steps. First/last 50-step means are also reported.

## Conditions

1. **random:** random graph; target labels are not used to design topology.
2. **modular_aligned:** graph construction favors connections between nodes in the same target class. The target is encoded in the topology, not supplied to the state-update rule.
3. **modular_shuffled:** modular graph construction uses shuffled target labels, breaking the alignment between topology and the evaluated target.

The modular graph has approximately 80% of selected neighbors within the construction label class and 20% across classes, before graph symmetrization. Symmetrization changes final node degrees, so degree is not exactly matched.

## Results

| Condition | Mean retention over 200 steps | SD across 100 runs | First 50 steps | Last 50 steps |
|---|---:|---:|---:|---:|
| random | 0.5008 | 0.0008 | 0.5032 | 0.5000 |
| modular_aligned | 0.9276 | 0.1647 | 0.9324 | 0.9216 |
| modular_shuffled | 0.5030 | 0.0140 | 0.5054 | 0.5022 |

Approximate 95% confidence intervals for mean retention:
- random: 0.5006–0.5010
- modular_aligned: 0.8953–0.9599
- modular_shuffled: 0.5002–0.5057

The aligned condition exceeded random by 0.4268 in mean retention (paired-by-seed difference; approximate 95% interval 0.3945–0.4590). It exceeded the shuffled condition by 0.4246 (approximate 95% interval 0.3920–0.4571).

## Interpretation

In this model, a target pattern encoded in network topology was much more persistent under local-majority dynamics than the same target evaluated against random or misaligned modular topology.

The update rule itself did not know the target labels. Nonetheless, the aligned graph had been constructed using those labels. The result is therefore evidence of **structural encoding and persistence in this specific toy model**, not evidence that the network discovered its own target or that topology alone creates life.

## Limitations and audit

1. This is an abstract binary network, not a cell or molecular model.
2. The target pattern is used to construct the aligned graph; the experiment does not test spontaneous emergence of organization.
3. The symmetrized graph can have different degree distributions across conditions.
4. There is no explicit energy/resource accounting, repair cost, or edge turnover.
5. The model's local-majority rule is fixed by the researcher.
6. The result does not establish a universal advantage for modular networks or relations.
7. The experiment is exploratory and was not formally preregistered before execution.

## Decision

**Narrow finding:** in this toy model, a pattern encoded in the topology can persist under local perturbations without a target-aware update rule.

**Not established:** self-organization, biological stability, a new law of life, or a causal explanation of mirror-life feasibility.

## Next gate: E9

1. Pre-register the parameter grid and falsification rules.
2. Compare topologies with matched degree distributions and edge counts.
3. Add edge turnover and explicitly report the cost of restoring or rebuilding edges.
4. Compare local-majority dynamics with a capacity-matched alternative update rule.
5. Include random, aligned, and shuffled controls under identical perturbation schedules.
6. Test a range of modularity levels instead of choosing a single favorable value.
7. Reject a broad claim if the advantage disappears under degree/resource matching or across parameter ranges.

## Reproduction

From the repository root:

```bash
python 03_EXPERIMENTS/E8_STRUCTURAL_MEMORY_RUNNER.py
```

The script writes per-replicate rows to `03_EXPERIMENTS/E8_STRUCTURAL_MEMORY_RAW.csv` and prints mean, standard deviation, and approximate 95% confidence intervals. Requires Python 3 and NumPy.

## Audit trail

- Runner commit: `a2e5ba13e932ab62bbd10bdefda90cf62fd26bb7`
- Results describe an exploratory execution of the declared model.
