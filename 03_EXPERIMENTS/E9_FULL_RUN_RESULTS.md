# E9 Full Run — Degree-Preserving Null and Assortativity Sweep

**Status:** exploratory computational run; not preregistered; abstract network only.  
**Date:** 2026-10-17  
**Question:** Does target-aligned modular topology preserve a binary target pattern better than a degree-preserving rewired null under local majority dynamics and repeated state noise?

## Protocol
- 80 binary nodes; 200 update steps; 100 paired seeds per condition.
- Initial state corruption: 15%; per-step independent state flip probability: 3%.
- Local majority update only; ties preserve current state. The update rule never receives target labels.
- Topology is constructed using target labels, so the aligned graph encodes the pattern structurally; this is not spontaneous self-organization.
- Sweep: within-class neighbor selection fractions 0.5, 0.6, 0.7, 0.8, 0.9.
- Null: undirected double-edge swaps, preserving every node's degree exactly, with 20 × edge-count attempted swaps per graph. The number of accepted swaps is recorded.
- Same target, initial corruption, and disturbance schedule are paired between aligned and null runs for each seed.
- Outcome: average fraction of nodes matching the target across all 200 steps. Intervals below are approximate 95% t intervals across 100 paired replicates.

## Results

| Within-class selection fraction | Aligned mean retention (95% CI) | Degree-preserving null mean (95% CI) | Paired difference (95% CI) |
|---:|---:|---:|---:|
| 0.5 | 0.500615 [0.500520, 0.500710] | 0.500833 [0.500655, 0.501012] | -0.000218 [-0.000386, -0.000050] |
| 0.6 | 0.503549 [0.503110, 0.503987] | 0.500904 [0.500744, 0.501065] | 0.002644 [0.002224, 0.003065] |
| 0.7 | 0.941504 [0.912291, 0.970718] | 0.500748 [0.500606, 0.500889] | 0.440757 [0.411572, 0.469942] |
| 0.8 | 0.941504 [0.912291, 0.970718] | 0.500748 [0.500606, 0.500889] | 0.440757 [0.411572, 0.469942] |
| 0.9 | 0.999873 [0.999843, 0.999902] | 0.500873 [0.500709, 0.501036] | 0.499000 [0.498837, 0.499163] |

Fractions 0.7 and 0.8 map to the same integer neighbor count under K=8 and therefore are not distinct settings in this implementation.

Mean accepted degree-preserving swaps per graph ranged from about 7,594 to 7,708, with edge counts matched exactly within each aligned/null pair. The null preserves degree sequence but not connectedness, community structure, or all higher-order graph statistics.

## Interpretation
The target-aligned topology substantially preserves the target pattern at higher assortativity, while degree-preserving rewiring destroys that alignment and returns performance to approximately chance. This supports a narrow statement about **structural encoding and persistence in this toy model**.

It does **not** show that the network discovers the pattern, self-organizes it, is alive, or establishes a universal principle of nature. The pattern is inserted into the graph at construction time. No energy/resource accounting, adaptive edge turnover, alternative update rules, or independent implementation audit is included. The run is exploratory, not preregistered, and requires these controls before stronger conclusions.

## Next tests
1. Separate structural encoding from adaptation: begin with unaligned graphs and allow only a preregistered local adaptation rule.
2. Match additional graph statistics, including connected components and clustering, where feasible.
3. Add explicit resource/maintenance cost and edge turnover.
4. Sweep noise, network size, update rules, and class imbalance.
5. Freeze hypotheses and analysis before the next run; preserve raw trial-level data and code hash.

## Reproduction
The E7 and E8 runners are committed in this repository. The E9 sweep was executed in a local analysis session using the protocol above; the dedicated E9 runner and raw CSV have not yet been committed.
