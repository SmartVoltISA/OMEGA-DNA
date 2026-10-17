# E8 — Structural Memory

- Runner: `E8_STRUCTURAL_MEMORY_RUNNER.py`
- Results, confidence intervals, limitations: `E8_STRUCTURAL_MEMORY_RESULTS.md`

## Current finding

In this abstract model, topology constructed using a target pattern preserved that pattern under local-majority updates better than random or shuffled topology. The update rule did not receive target labels, but the aligned graph encoded them. This supports only structural pattern persistence in this toy model; it does not demonstrate spontaneous self-organization or a biological principle.

## Next gate

Match degree distributions and edge counts, add explicit topology turnover and resource accounting, preregister the parameter grid, and test whether the effect survives those controls.


## E9 — Degree-preserving null and assortativity sweep

- Runner: [E9_DEGREE_MATCHED_RUNNER.py](E9_DEGREE_MATCHED_RUNNER.py)
- Full-run results and limitations: [E9_FULL_RUN_RESULTS.md](E9_FULL_RUN_RESULTS.md)

The exploratory sweep found that strongly target-aligned topology can preserve the encoded binary pattern under noise, while degree-preserving rewiring returns retention to approximately chance. This is evidence about structural encoding in this toy model only. It does not demonstrate self-organization, life, or a universal principle. E9 was not preregistered; see the report for limitations and next controls.


## E10 — Local adaptation without target labels

- Runner: [E10_LOCAL_ADAPTATION_RUNNER.py](E10_LOCAL_ADAPTATION_RUNNER.py)
- Results and limitations: [E10_LOCAL_ADAPTATION_RESULTS.md](E10_LOCAL_ADAPTATION_RESULTS.md)

In this exploratory test, state-based degree-preserving rewiring did not robustly preserve the initial balanced pattern. The local-majority dynamics usually collapsed toward global consensus; stronger rewiring helped slightly at low noise but not reliably at 3% noise. This is a limited negative result for this rule, not a general disproof of self-organization.


## E11 — Local memory / hysteresis under noise

- Runner: [E11_MEMORY_HYSTERESIS_RUNNER.py](E11_MEMORY_HYSTERESIS_RUNNER.py)
- Results: [E11_MEMORY_HYSTERESIS_RESULTS.md](E11_MEMORY_HYSTERESIS_RESULTS.md)

The exploratory sweep found that stronger local memory can delay collapse toward consensus, but the benefit shrinks as noise rises. At 3% noise, even the strongest tested memory returned to about 50% target retention in the final 50 steps. This is limited evidence for history-dependent persistence in this toy model, not spontaneous memory or a universal law.


## E12 — Component turnover and memory continuity

- Runner: [E12_TURNOVER_MEMORY_RUNNER.py](E12_TURNOVER_MEMORY_RUNNER.py)
- Results: [E12_TURNOVER_MEMORY_RESULTS.md](E12_TURNOVER_MEMORY_RESULTS.md)

The exploratory model suggests that preserving a moderate local history trace across replacement can improve retention of an already encoded target pattern under noise and turnover. Stronger memory can become harmful when it goes stale. The graph and initial state encode the pattern, so this is a persistence result, not emergence or a biological law.
