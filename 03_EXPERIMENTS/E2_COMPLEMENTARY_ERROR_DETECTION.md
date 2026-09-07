# E2 — Complementary Redundancy and Error Detection

**Status:** executed toy experiment; not a biological mutation-rate estimate.

## Question

Does representing DNA as two complementary strands create a measurable error-detection relation that is absent from a single-strand representation?

## Model

Generate a random DNA strand `S` of length `L`.

Construct its ideal complement `C(S)`. Independently mutate each strand with probability `p` per position. Compare the observed strand with the reverse complement of the other strand.

A mismatch is treated as an **alarm signal**, not as proof that the system can identify which strand is correct.

## Fixed run

- seed = 11
- mutation probability `p = 0.001`
- trials = 50,000
- lengths = 10, 100, 1000
- substitution = uniformly sampled from the other three bases

## Results

| L | probability of true damage | probability of detected mismatch |
|---:|---:|---:|
| 10 | ~0.0189 | ~0.0189 |
| 100 | ~0.1813 | ~0.1812 |
| 1000 | ~0.8660 | ~0.8659 |

The near equality is expected in this toy model because a single-strand substitution normally creates a complementary mismatch. Longer sequences provide more opportunities for detection.

## Interpretation

The experiment demonstrates a systems property of **redundant complementary representation**: the second strand provides a consistency check.

It does **not** demonstrate autonomous DNA repair. A mismatch alone does not specify which strand contains the original state. Real repair requires additional molecular mechanisms and contextual information.

## Architectural result

The useful OMEGA mapping is:

`stored state → coupled redundant state → consistency constraint → mismatch detection → repair process`

The first three components arise directly from the paired representation; the final repair step must be supplied by biological machinery.

## Control

A single-strand model has no independent complementary copy, so this particular consistency check is unavailable.

## Limitation

The model ignores base-specific chemistry, lesion types, polymerase proofreading, mismatch-repair proteins, chromatin state and cellular context.

## Conclusion

**E2 passes as a toy architectural demonstration:** complementarity can be represented as an active consistency relation rather than merely a lookup rule. It does not establish a new biological mechanism.
