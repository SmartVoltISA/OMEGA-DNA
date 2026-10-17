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
