# Initial Hypotheses

## H-DNA-01 — Relational structure

**Claim:** The functional organization of DNA depends not only on sequence but on a hierarchy of physical and regulatory relations.

**Prediction:** Models that explicitly represent relevant relations should explain some observations that a linear sequence representation alone cannot.

**Test:** Compare sequence-only and relation-aware models on predefined measurable tasks.

**Falsifier:** No reproducible improvement after controlling for model complexity and available information.

## H-DNA-02 — Complementarity as constraint

**Claim:** Base complementarity is a structural constraint that converts local molecular relations into a mechanism for information preservation during replication.

**Prediction:** A relational representation should recover complementarity as a high-value constraint rather than treating it as an arbitrary symbol mapping.

**Test:** Construct a minimal physical/graph model and compare its behavior with unconstrained and alternative pairing models.

## H-DNA-03 — Memory is structural persistence

**Claim:** Biological memory in DNA is not only an abstract stored sequence; it is information preserved by a physical structure and maintenance process.

**Prediction:** A useful model of DNA memory must include both the encoded state and the mechanisms that preserve, copy, repair, or alter it.

**Test:** Map replication and repair as explicit feedback/maintenance loops.

## H-DNA-04 — Function emerges from constrained relations

**Claim:** Biological function can emerge from interactions among DNA elements and their molecular context rather than from isolated sequence fragments alone.

**Prediction:** Context-dependent relational features should explain measurable functional differences between otherwise similar sequence representations.

**Test:** Define the context and metric before experiments; compare against appropriate null models.

## H-DNA-05 — Memory of abstract form

**Status:** HYPOTHESIS; E14 exploratory pilot and E15 corrected synthetic test completed; independent reproduction pending. Not an established biological principle.

**Claim:** A system's memory may encode not only specific elements and their pairwise relations, but also higher-level forms and invariant relations that can be reused across different concrete graphs.

**Operational distinction:**
- **Episodic/edge memory:** retains particular observed adjacency patterns.
- **Abstract/form memory:** retains general graph descriptors that are invariant to node relabeling and can be applied to graphs of different sizes.
- **Minimal baseline:** uses only graph density.

**Prediction:** Under node relabeling and graph-size holdout, a capacity-limited form representation will generalize better than exact adjacency exemplars and density-only baselines. Under sufficiently severe corruption, the abstraction may also fail; no universal superiority is assumed.

**Test:** E14 classifies three synthetic graph families (cycle, star, two-clique graph). Train the abstract classifier on sizes 16, 24, 28 with low edge noise; test on unseen examples at sizes 20, 32, 36, 40 under four edge-corruption levels. Compare with a raw-adjacency exemplar memory at size 20 and a density-only model. Node identities are randomly permuted. All models receive labels only in the training set.

**Null hypothesis:** The invariant-feature model does not outperform the density-only baseline on held-out graphs; any apparent gain does not survive node relabeling, size holdout, or stronger corruption.

**Primary metrics:** balanced classification accuracy; paired difference in per-example correctness; 95% Wilson intervals for accuracy and paired bootstrap intervals for model differences.

**Falsifier:** No advantage over density-only on held-out sizes at low/moderate noise, or loss of the advantage under repeated independent seeds. A result on these synthetic graph families does not establish biological abstraction, life, consciousness, or a universal law.

**Limitations declared in advance:** graph features are hand-designed; graph families are synthetic and structurally distinct; the task tests transfer of a compact representation, not spontaneous discovery of an abstraction from unrestricted experience. E14 is exploratory because implementation choices were iterated during initial analysis. E15's first run was invalid due size-dependent integer rounding in edge additions; the corrected runner uses Bernoulli additions and shows a bounded advantage under low/moderate noise, but independent reproduction is still required.

## Research discipline

No hypothesis becomes an accepted result without a defined metric, baseline/null model, reproducible procedure, and recorded result.
