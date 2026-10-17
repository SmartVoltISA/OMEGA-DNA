# Research: Stability, Identity, and Mirror Life

**ID:** ODNA-R-2026-10-17-01  
**Status:** Proposal / preregistration draft — no experiment executed  
**Scope:** Conceptual and computational research only. This document does not propose constructing mirror organisms or provide a wet-lab protocol.

## 1. Research question

Why is a complete, self-sustaining mirror organism not currently available, even though some mirror-image biomolecules can be synthesized? More generally: what conditions allow a living system to preserve its organization over time, and what distinguishes one organization from another?

These are related but distinct questions. The first concerns a specific technical and biological frontier. The second concerns general principles of system stability and identity.

## 2. Evidence status

### Established or well-supported background

- Many biological molecules are chiral: a molecule and its mirror image cannot be superimposed by rotation or translation.
- Natural life uses characteristic molecular handedness in major biomolecular classes. Molecular interactions are therefore not automatically interchangeable with their mirror-image counterparts.
- Some mirror-image molecular components have been synthesized, but a complete self-replicating mirror organism has not been created.
- Building a synthetic non-mirror cell is itself a major challenge. The path from biological molecules to a fully functioning, self-replicating cell is not completely understood.
- In February 2025, the Spirit of Asilomar summit produced an entreaty signed by 96 experts recommending that mirror life not be created unless future research convincingly demonstrates that it would not pose severe risks.

### Interpretation, not established fact

The inability to create a complete mirror organism does not by itself prove that scientists do not understand stability or life. It does show that knowledge of individual components is not sufficient to guarantee that a complete autonomous system can be assembled. Technical limitations, missing biological knowledge, and system-level dependencies may all contribute.

## 3. Core distinction

A system's **components**, **organization**, **state**, **history**, and **environment** must not be treated as interchangeable explanations.

- **Components:** what entities the system contains.
- **Relations:** physical, chemical, spatial, regulatory, or informational dependencies between entities.
- **Organization:** the arrangement and dynamics of relations that enable specified functions.
- **State:** the system's current configuration.
- **History / memory:** information about prior states that persists and influences future behavior.
- **Boundary:** the operational distinction between the system and its environment; its physical and functional meaning must be specified per model.
- **Maintenance:** processes that compensate for damage, loss, or disturbance.
- **Energy and matter flows:** resources required to sustain non-equilibrium processes.

A graph alone is not a living system. A graph model becomes scientifically useful only when its nodes, typed edges, dynamics, resource constraints, and observable functions are explicitly defined.

## 4. Main hypothesis H-ODNA-STAB-01

**Hypothesis:** In a specified class of dynamical systems, persistence of organization under component turnover and external perturbation depends on the interaction of (a) functional relations, (b) maintenance or feedback mechanisms, and (c) sufficient resource availability. The identity of a system should therefore be operationalized through persistent functions and relational invariants, rather than requiring every component to remain unchanged.

This is deliberately narrower than the claim that relations are the universal foundation of life. It is a testable systems hypothesis, not a biological law.

### Predictions

1. Under matched resource and complexity budgets, some systems with effective maintenance feedback will preserve predefined functions longer than comparable systems without such feedback.
2. Removing a relation that is causally necessary for a function will impair that function more than removing a matched, non-critical relation.
3. Component replacement can occur without loss of operational identity when relevant functions and predefined relational invariants remain within declared tolerances.
4. The benefit of feedback will not be universal: excessive feedback strength, delays, insufficient resources, or poor topology may destabilize a system.

## 5. Null hypotheses and competing explanations

- **H0-A — No relational advantage:** Once model capacity, information, and resources are matched, explicit relation-aware models do not outperform simpler baselines on the selected outcomes.
- **H0-B — Topology is sufficient:** Stability differences are explained by static topology alone; adaptive maintenance contributes no reproducible benefit.
- **H0-C — Component identity dominates:** Replacing components causes loss of function even when the predefined relational invariants and functional constraints are preserved.
- **H0-D — Resource confounding:** Apparent stability improvements disappear when energy/resource budgets and computational cost are matched.
- **Alternative explanations:** redundancy, modularity, repair rules, feedback delay, environmental predictability, and parameter tuning may explain outcomes without implying a universal principle.

## 6. Safe computational experiment plan

The first stage uses abstract, non-biological dynamical networks. It does not model a build path for mirror organisms.

### Model groups

- **A — Random/static baseline:** fixed network with no adaptive maintenance.
- **B — Structured/static:** predefined modular or cyclic topology, with no adaptive maintenance.
- **C — Feedback-maintained:** relation changes follow a declared rule responding to deviations from target functions.
- **D — Ablation controls:** same as C, but remove one maintenance mechanism at a time.
- **E — Shuffled control:** preserve basic graph statistics while shuffling relation assignments, to test whether specific organization matters beyond density alone.

### Controlled perturbations

Apply abstract node failures, edge loss, parameter drift, and bounded environmental changes. Use identical perturbation schedules for paired model runs. Do not translate these simulations into biological construction instructions.

### Metrics (predefine before execution)

- **Functional retention:** fraction of target functions still within declared operating bounds.
- **Recovery time:** steps required to return to the accepted functional region after a perturbation.
- **Persistence:** time until a predefined failure criterion is reached.
- **Component turnover tolerance:** function retained after a controlled fraction of component substitutions.
- **Resource cost:** total maintenance cost under the same accounting rule.
- **Robustness across seeds:** variation in outcomes across independent random seeds.
- **Identity invariant retention:** fraction of preregistered relational/functional invariants retained within tolerance.

No single metric should be treated as a universal measure of life.

## 7. Experimental controls and fairness

- Match node/edge budget, parameter count, information available to each model, perturbation schedule, and resource budget as closely as possible.
- Include a negative control in which relevant relations are shuffled.
- Include a simple baseline and a baseline with matched computational capacity.
- Pre-register random seeds or seed-generation procedure, sample size, parameter ranges, stopping criteria, metrics, and statistical analysis before running the experiment.
- Run ablations to identify which mechanism, if any, accounts for an effect.
- Correct for multiple comparisons where applicable.
- Report null and negative results, not only successful runs.
- Preserve source code, environment, exact configuration, raw outputs, and commit hash for reproducibility.

## 8. Falsification criteria

The main hypothesis receives no support if any apparent advantage disappears under matched resource/capacity controls, fails to reproduce across seeds, or cannot outperform the null/shuffled controls on preregistered metrics.

The hypothesis must be narrowed or rejected if:
- feedback does not improve stability relative to fair baselines;
- the effect is entirely explained by redundancy, topology, or extra resources;
- component turnover does not preserve functions under the specified invariants;
- outcomes depend on post-hoc metric or parameter selection.

A positive result in an abstract network supports only a statement about that model class. It does not prove that living cells follow the same rule.

## 9. Relation to mirror life

Mirror life is a motivating case, not a direct test of the general hypothesis. A complete mirror cell would require coordinated mirror-compatible molecular machinery and a self-maintaining organization. The current inability to create such a system may reflect multiple bottlenecks; the evidence does not isolate a single universal missing principle.

This research must remain distinct from efforts to construct mirror organisms. The near-term objective is to clarify system-level concepts and test them in abstract, auditable models.

## 10. Decision gates

- **G0 — Definitions:** operationally define system, function, identity, stability, turnover, and resource cost.
- **G1 — Preregistration:** freeze hypotheses, baselines, parameters, metrics, and falsification rules.
- **G2 — Implementation audit:** test code on toy cases with analytically predictable behavior.
- **G3 — Controlled simulation:** run paired trials, ablations, and shuffled controls.
- **G4 — Reproduction:** reproduce results independently from a clean environment.
- **G5 — Scope decision:** determine whether results justify a narrower next hypothesis. Do not extrapolate to biology without external biological evidence.

**Current decision:** G0 draft only. No simulation result is claimed by this document.

## 11. Sources

1. UK Government Office for Science, **Mirror life**, updated 16 July 2025. Expert roundtable summary; distinguishes mirror components from self-replicating organisms and describes major technical and scientific unknowns.  
   https://www.gov.uk/government/publications/mirror-life/mirror-life

2. Spirit of Asilomar, **Entreaty: Risks from Mirror Life**, February 2025. The summit statement calls for not creating mirror life unless future research convincingly demonstrates that severe risks would not arise.  
   https://repository.rice.edu/server/api/core/bitstreams/03831782-2fe2-4b00-82ef-781e9c8a0353/content

3. Adamala et al., **Confronting risks of mirror life**, *Science* (2024).  
   https://doi.org/10.1126/science.ads9158

## 12. Research record

- Version: 0.1
- Date: 2026-10-17
- Status: proposal only; not executed
- Next action: review definitions and preregister an abstract-network experiment before implementation
