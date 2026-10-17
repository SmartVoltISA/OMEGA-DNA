# E11 — Local Memory / Hysteresis Under Noise

**Status:** exploratory run; not preregistered.  
**Date:** 2026-10-17  
**Runner:** [E11_MEMORY_HYSTERESIS_RUNNER.py](E11_MEMORY_HYSTERESIS_RUNNER.py)

## Question
Does a node-local decaying memory trace help a network preserve a balanced initial pattern under state noise, and does any gain survive stronger perturbations?

## Protocol
- 80 binary nodes; random undirected graph; 200 steps per run.
- 100 seeds per condition; 3 noise levels: 0%, 1%, 3% independent state flips per node per step.
- Initial corruption: 15%.
- Memory strengths: 0, 0.5, 1, 2, 4. Memory trace decay factor: 0.8.
- Update score = sum of neighboring signed states + memory_strength × local memory trace. Ties preserve the current state.
- Memory trace is updated from the node's accepted state after each update.
- Negative control: at memory strength 2, initial memory traces are permuted across nodes.
- Target labels are used for initial-state construction and evaluation only, not by the update rule.
- 1,800 trials total. The same seed determines the target, initial corruption, disturbance schedule, and graph across conditions.
- Metric: mean fraction of nodes matching target over all 200 steps. Paired approximate 95% t intervals are reported for differences between conditions, pairing by seed.

## Main results

| Noise | Memory strength | Mean retention | SD across runs | Mean retention in final 50 steps |
|---:|---:|---:|---:|---:|
| 0% | 0 | 50.12% | 0.10 pp | 50.00% |
| 0% | 0.5 | 50.14% | 0.15 pp | 50.00% |
| 0% | 1 | 50.25% | 0.29 pp | 50.00% |
| 0% | 2 | 51.15% | 4.25 pp | 50.84% |
| 0% | 4 | 62.46% | 14.24 pp | 62.16% |
| 1% | 0 | 50.10% | 0.08 pp | 50.00% |
| 1% | 0.5 | 50.12% | 0.08 pp | 50.00% |
| 1% | 1 | 50.22% | 0.19 pp | 50.00% |
| 1% | 2 | 50.33% | 0.26 pp | 50.00% |
| 1% | 4 | 52.89% | 6.17 pp | 51.40% |
| 3% | 0 | 50.10% | 0.08 pp | 50.00% |
| 3% | 0.5 | 50.12% | 0.11 pp | 50.00% |
| 3% | 1 | 50.20% | 0.15 pp | 50.00% |
| 3% | 2 | 50.31% | 0.22 pp | 50.00% |
| 3% | 4 | 51.19% | 1.49 pp | 50.00% |

### Paired comparison: memory strength 4 versus no memory

| Noise | Retention gain | Approx. 95% CI |
|---:|---:|---:|
| 0% | +12.35 percentage points | +9.53 to +15.16 pp |
| 1% | +2.79 percentage points | +1.57 to +4.00 pp |
| 3% | +1.09 percentage points | +0.80 to +1.38 pp |

### Negative control: correctly aligned versus initially shuffled memory at strength 2

| Noise | Aligned memory | Shuffled memory | Paired difference (approx. 95% CI) |
|---:|---:|---:|---:|
| 0% | 51.15% | 50.10% | +1.05 pp [+0.21, +1.89] |
| 1% | 50.33% | 50.09% | +0.24 pp [+0.20, +0.29] |
| 3% | 50.31% | 50.08% | +0.23 pp [+0.20, +0.27] |

## Interpretation
Local memory can delay collapse toward global consensus, most noticeably at strength 4 with no noise. Under 1% noise the average benefit is much smaller, and under 3% noise the final 50 steps return to approximately 50% retention even at strength 4. Strong inertia therefore creates a tradeoff: it can preserve the initial pattern for longer, but does not reliably maintain the two-class organization under perturbation.

The shuffled-memory control shows that alignment between a node's memory trace and its own state matters for the small effect at strength 2. This does not establish a new law: the memory mechanism is explicitly designed to retain past states, the network is abstract, and the initial pattern is supplied at initialization.

**Conclusion:** E11 gives limited support for the narrow statement that local history can delay loss of an initially encoded pattern. It does not show spontaneous formation of memory, robust self-organization, biological identity, or a universal principle.

## Limitations
- Exploratory parameter sweep after earlier experiments; not preregistered.
- The memory term and decay were hand-selected; the strongest effect is sensitive to strength.
- No energy/resource accounting or adaptive edge changes.
- The target pattern is initialized in node states; it is not discovered by the network.
- The runner writes trial-level raw CSV on execution. The raw CSV is not included in this commit.

## Next test
Pre-register a comparison of memory decay, noise, and resource cost; include a shuffled-history control and an independent implementation. Test whether memory can preserve multiple functional states without simply delaying consensus.
