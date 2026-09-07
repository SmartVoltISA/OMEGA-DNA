# E1 — Typed Base-Pair Compatibility Simulation

**Status:** preregistered model specification; no biological result claimed

## 1. Question

Can a small typed relational model distinguish the canonical DNA base-pair classes when compatibility is evaluated from declared structural constraints rather than from a hard-coded `A↔T, G↔C` lookup table?

## 2. Scope

This is a **toy structural model**, not a molecular-dynamics simulation and not a discovery of the chemistry of DNA. Its purpose is narrower: test whether the OMEGA representation can make several known constraints explicit and measurable.

Established structural facts used as model inputs:

- A and G are purines; C and T are pyrimidines.
- Canonical DNA pairing is A–T and G–C.
- Stable double-helical pairing requires a purine–pyrimidine arrangement and compatible hydrogen-bonding geometry.
- The two strands are antiparallel.

These constraints are documented in NCBI molecular-biology references and are not treated as experimental discoveries by E1.

## 3. Representation

For each candidate ordered pair `(x,y)`, define a feature vector:

`F(x,y) = [size, donor_acceptor, orientation]`

where:

- `size = 1` if the pair is purine–pyrimidine in either orientation, otherwise `0`;
- `donor_acceptor` is the number of compatible canonical hydrogen-bond donor/acceptor matches represented by the toy model;
- `orientation = 1` when the pair is evaluated in the declared antiparallel geometry, otherwise `0`.

The compatibility score is explicitly defined as:

`S(x,y) = w_size * size + w_H * donor_acceptor + w_orientation * orientation`

with weights fixed before execution.

## 4. Critical anti-circularity rule

The model must **not** contain a direct rule of the form `if x=A and y=T then score=...` or `if x=G and y=C then score=...`.

The pairing score must be generated from declared structural features. If the feature table itself encodes the canonical pair identity, the run is classified as a **model reconstruction from supplied chemistry**, not as an independent derivation.

## 5. Candidate space

Evaluate all 16 ordered base pairs:

`A,C,G,T × A,C,G,T`

Then evaluate the same set under perturbations:

1. remove the hydrogen-bond feature;
2. remove the purine/pyrimidine size constraint;
3. randomize one model weight within a preregistered range;
4. replace the canonical pairing feature table with a shuffled control preserving marginal feature counts.

## 6. Baselines / nulls

### N0 — Symbolic lookup
A direct canonical pairing table. This is a reference baseline, not an independent model.

### N1 — Size-only
Score depends only on purine–pyrimidine compatibility.

### N2 — Hydrogen-bond-only
Score depends only on donor/acceptor compatibility.

### N3 — Typed relational model
Combines the declared structural relation types.

## 7. Metrics

Primary:

- top-1 recovery of canonical pair classes;
- ranking of canonical vs noncanonical candidates;
- robustness under declared perturbations.

Secondary:

- number of noncanonical pairs tied with canonical pairs;
- score margin between canonical and nearest competitor;
- sensitivity to each relation type.

No p-value or biological effect size is claimed unless a later empirical dataset is introduced.

## 8. Acceptance / falsification

E1 supports the usefulness of the representation at the toy-model level only if:

1. the typed model produces a nontrivial ranking without a direct canonical-pair lookup;
2. the result is reproducible from the fixed parameters;
3. removing individual relation classes produces interpretable degradation;
4. the result survives the preregistered perturbation tests.

E1 does **not** support the broader hypothesis H-DNA-02 if the result depends on hidden canonical-pair encoding, arbitrary post-hoc weights, or an implementation-specific rule.

## 9. Expected interpretation

A positive E1 result would mean only that a typed relational representation can reproduce a known structural classification under an explicit toy model. It would justify moving to a less hand-specified test.

A negative result is useful: it would show that this abstraction does not add measurable value at the tested level.

## 10. Source basis

NCBI describes DNA as two antiparallel complementary nucleotide chains, with A–T and G–C pairing, and explains the importance of purine/pyrimidine geometry and hydrogen-bonding compatibility. See the NCBI Bookshelf references listed in the repository research notes.
