# OMEGA-DNA — Layer Map

## Purpose

Map DNA from physical chemistry to biological persistence without skipping levels.

| Level | Object | Dominant relations | Memory / state | Observable question |
|---|---|---|---|---|
| L0 | atoms | covalent, electrostatic, hydrogen-bond geometry | chemical state | What configurations are physically allowed? |
| L1 | nucleotide | internal chemical bonds | nucleotide identity | What makes a reusable unit? |
| L2 | strand | phosphodiester backbone + local stacking | ordered sequence | How does order constrain future structure? |
| L3 | base pair | complementarity | paired state | Why can one strand specify the other? |
| L4 | double helix | pairing + stacking + geometry | duplex structure | How do local relations create a stable global object? |
| L5 | DNA-protein complex | binding, wrapping, accessibility | packaging state | Which regions are accessible? |
| L6 | chromatin | spatial and regulatory interactions | accessibility/state history | How does organization constrain molecular access? |
| L7 | gene/regulatory region | transcription-factor, polymerase and regulatory relations | sequence + regulatory state | Which relations produce measurable expression? |
| L8 | chromosome/genome | long-range spatial and inheritance relations | genomic state | How is information organized at cellular scale? |
| L9 | replication/repair | template, enzyme, checkpoint relations | maintained state | How is persistence produced? |
| L10 | mutation/selection | change + differential persistence | altered lineage state | Which changes remain and why? |

## Important distinction

The levels are not independent boxes. A higher level constrains lower-level interactions, while lower-level physical changes can propagate upward.

This gives a bidirectional research structure:

`microstructure → constraint → emergent organization → function`

and

`function/context → access/regulation → local interaction`

The second direction must be handled carefully: biological context changes which physical relations are used or accessible, but it does not imply that higher-level function violates molecular causality.

## Candidate state vector

For a declared region R:

`X(R,t) = {S, C, G, A, P, E, M}`

where:

- `S` = sequence;
- `C` = complementarity state;
- `G` = geometry/topology;
- `A` = accessibility;
- `P` = protein/regulatory interactions;
- `E` = environmental/cellular context;
- `M` = maintenance/history variables.

The exact measurable definition of each variable must be specified per experiment.

## Research rule

Never compare two models unless the represented information, training data, parameter count, and evaluation target are declared. A more complicated relational model must earn its complexity by improving prediction, explanation, robustness, or mechanistic correspondence.
