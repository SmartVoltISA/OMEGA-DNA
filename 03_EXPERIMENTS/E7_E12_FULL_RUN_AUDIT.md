# E7–E12 Full Experiment Audit

**Run date:** 2026-10-17  
**Status:** all six committed runner scripts were executed successfully in GitHub Actions on Python 3.12 with NumPy. Workflow run: [#1 — OMEGA full experiment suite](https://github.com/SmartVoltISA/OMEGA-DNA/actions/runs/39013821290). All six run steps and the artifact upload completed successfully.  
**Total trial rows:** 8,540.  
**Scope:** abstract binary-network simulations only; no biological or mirror-organism model.

## Run inventory

| Suite | Trials | Design |
|---|---:|---|
| E7 | 160 | Random/modular topology; explicit feedback and shuffled-feedback control |
| E8 | 300 | Random, target-aligned modular, and shuffled modular topology |
| E9 | 1,000 | Five assortativity levels; target-aligned graph vs degree-preserving rewired null |
| E10 | 480 | State-based rewiring at four strengths and three noise levels |
| E11 | 1,800 | Local memory strength sweep, three noise levels, shuffled-memory control |
| E12 | 4,800 | Component turnover × state noise × memory-continuity conditions |

## E7 — Feedback and topology

| Condition | Mean target retention | SD across trials | Mean retention, final 50 steps |
|---|---:|---:|---:|
| Random static | 50.10% | 0.08 pp | 50.00% |
| Modular static | 74.11% | 13.73 pp | 55.70% |
| Modular + feedback | 98.15% | 3.00 pp | 94.68% |
| Shuffled-feedback control | 50.32% | 0.30 pp | 50.00% |

**Interpretation:** direct target-aware feedback is highly effective in this toy model, but because the controller receives target labels, this is not evidence of emergent organization.

## E8 — Structural encoding

| Condition | Mean target retention | SD across trials |
|---|---:|---:|
| Random topology | 50.08% | 0.08 pp |
| Target-aligned modular topology | 92.76% | 16.47 pp |
| Shuffled modular topology | 50.30% | 1.40 pp |

**Interpretation:** target-aligned topology preserves an already encoded pattern; the network does not discover the pattern.

## E9 — Degree-preserving null

| Within-class fraction | Aligned topology | Degree-preserving rewired null | Paired difference (approx. 95% CI) |
|---:|---:|---:|---:|
| 0.5 | 50.06% | 50.08% | -0.02 pp [-0.04, -0.01] |
| 0.6 | 50.35% | 50.09% | +0.26 pp [+0.22, +0.31] |
| 0.7 | 94.15% | 50.07% | +44.08 pp [+41.16, +46.99] |
| 0.8 | 94.15% | 50.07% | +44.08 pp [+41.16, +46.99] |
| 0.9 | 99.99% | 50.09% | +49.90 pp [+49.88, +49.92] |

The 0.7 and 0.8 conditions map to the same integer neighbor count with K=8, so they are not distinct effective settings. The null preserved every node's degree exactly; it did not preserve all higher-order graph properties.

## E10 — Local state-based rewiring

Mean retention by noise and attempted rewiring swaps per step:

| Noise | 0 swaps | 8 swaps | 32 swaps | 80 swaps |
|---:|---:|---:|---:|---:|
| 0% | 50.09% | 50.64% | 50.14% | 52.71% |
| 1% | 50.08% | 50.09% | 50.10% | 52.18% |
| 3% | 50.08% | 50.08% | 50.11% | 50.47% |

The strongest rewiring condition improved retention by +2.62 pp at 0% noise (approx. 95% paired CI +0.79 to +4.45 pp) and +2.10 pp at 1% noise (+0.28 to +3.91 pp). At 3% noise the +0.40 pp difference was inconclusive (-0.22 to +1.01 pp). Degree sequences were checked and preserved.

**Interpretation:** local rewiring under this rule does not robustly maintain the balanced two-class pattern; consensus dynamics remain a failure mode.

## E11 — Local memory

| Noise | No memory | Memory strength 4 | Paired gain (approx. 95% CI) | Last 50 steps, strength 4 |
|---:|---:|---:|---:|---:|
| 0% | 50.12% | 62.46% | +12.35 pp [+9.53, +15.16] | 62.16% |
| 1% | 50.10% | 52.89% | +2.79 pp [+1.57, +4.00] | 51.40% |
| 3% | 50.10% | 51.19% | +1.09 pp [+0.80, +1.38] | 50.00% |

**Interpretation:** stronger local history can delay collapse to consensus, but its effect shrinks as noise rises. At 3% noise, final-50-step retention returns to chance.

## E12 — Component turnover and memory continuity

At 3% state noise:

| Turnover per step | No memory | Memory strength 2, preserved history | Memory strength 2, reset history | Memory strength 4, reset history |
|---:|---:|---:|---:|---:|
| 0% | 95.40% | 98.70% | 98.70% | 98.27% |
| 0.5% | 94.87% | 98.19% | 98.10% | 97.45% |
| 1% | 94.65% | 98.18% | 98.03% | 94.56% |
| 3% | 92.02% | 98.14% | 96.50% | 83.93% |

At 3% noise and 3% turnover, preserving history versus resetting the same-strength memory improved retention by **+1.65 pp** (approx. 95% paired CI **+0.32 to +2.97 pp**). Preserved moderate memory versus no memory improved it by **+6.12 pp** (**+3.38 to +8.86 pp**). Strong memory with reset history underperformed preserved moderate memory by **14.21 pp** (**-17.20 to -11.23 pp**).

**Interpretation:** in this model, continuity of a moderate historical trace helps preserve a target-aligned organization during component turnover. Strong stale memory becomes a liability. The target pattern is pre-encoded in the graph and initialization.

## Overall conclusion

1. **E7:** explicit target-aware feedback maintains the target, but the target is supplied to the controller.
2. **E8–E9:** topology can store and preserve a pattern; degree-preserving rewiring destroys its alignment.
3. **E10:** local state-based rewiring alone is insufficient under the tested rule and noise.
4. **E11:** local memory can delay consensus, but robustness declines with noise.
5. **E12:** moderate history continuity improves persistence under turnover in the pre-encoded model; excessive/stale memory can hurt.

The experiments do not establish a universal law of life, spontaneous self-organization, or a biological mechanism. Most runs begin with the target encoded in states or topology. E13 should remove this target-alignment confound, preregister its hypotheses and metrics, and compare adaptive versus non-adaptive systems under matched resources.

## Reproduction and artifacts

Canonical runners:
- [E7 runner](E7_STABILITY_IDENTITY_RUNNER.py)
- [E8 runner](E8_STRUCTURAL_MEMORY_RUNNER.py)
- [E9 runner](E9_DEGREE_MATCHED_RUNNER.py)
- [E10 runner](E10_LOCAL_ADAPTATION_RUNNER.py)
- [E11 runner](E11_MEMORY_HYSTERESIS_RUNNER.py)
- [E12 runner](E12_TURNOVER_MEMORY_RUNNER.py)

A combined raw trial-level CSV and aggregate summary CSV are provided as downloadable artifacts in the conversation response. Raw CSV generation by the repository runners is reproducible; raw outputs have not been committed to this repository.


## E13 — Emergence without target labels (follow-up)

E13 adds 480 exploratory trials (40 replicates × 3 noise levels × 4 conditions), bringing the combined E7–E13 trial count to **9,020** across the recorded suites.

| Noise | Condition | Mean minority fraction | Last-50-step entropy | Consensus rate | Median consensus step |
|---:|---|---:|---:|---:|---:|
| 0% | Static | 0.31% | 0.000 | 100% | 3 |
| 0% | Adaptive assortative | 3.46% | 0.073 | 92.5% | 3 |
| 0% | Shuffled-state control | 0.29% | 0.000 | 100% | 3 |
| 0% | Random rewiring | 0.31% | 0.000 | 100% | 3 |
| 1% | Static | 0.29% | 0.000 | 100% | 3 |
| 1% | Adaptive assortative | 1.35% | 0.024 | 97.5% | 4 |
| 1% | Shuffled-state control | 0.31% | 0.000 | 100% | 3 |
| 1% | Random rewiring | 0.29% | 0.000 | 100% | 3 |
| 3% | Static | 0.29% | 0.000 | 100% | 3 |
| 3% | Adaptive assortative | 0.41% | 0.000 | 100% | 4 |
| 3% | Shuffled-state control | 0.29% | 0.000 | 100% | 3 |
| 3% | Random rewiring | 0.33% | 0.000 | 100% | 3 |

**E13 conclusion:** the tested local-majority dynamics generally collapse to consensus in 3–4 steps. Adaptive rewiring briefly retains more minority-state nodes at low noise, but no stable differentiated organization emerges. This is a limited negative result for this rule set, not a general disproof of self-organization.

The E13 runner and report are linked from [E13_EMERGENCE_RESULTS.md](E13_EMERGENCE_RESULTS.md). The full GitHub Actions workflow includes E13, but no hosted workflow run had been observed at the time this report was updated. E13 values were obtained in a local Python analysis using the same algorithm; independent clean-environment reproduction remains pending.
