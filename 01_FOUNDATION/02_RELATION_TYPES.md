# DNA relation types

The OMEGA-DNA model distinguishes relations instead of treating every connection as equivalent.

| ID | Relation | Example | Measurable property |
|---|---|---|---|
| R01 | Covalent | backbone bond | bond length, geometry, energy |
| R02 | Hydrogen-bonding | A–T, G–C | geometry, interaction energy |
| R03 | Base stacking | adjacent bases | stacking interaction, geometry |
| R04 | Topological | strand linkage | topology, linking constraints |
| R05 | Spatial | DNA–protein proximity | distance, contact frequency |
| R06 | Regulatory | regulatory element → transcriptional effect | expression/activity |
| R07 | Replication | template → copied strand | copying fidelity |
| R08 | Repair | damaged state → restored state | repair efficiency/fidelity |
| R09 | Epigenetic/contextual | chromatin state → accessibility | accessibility/activity |
| R10 | Evolutionary | variant → persistence | frequency/change across generations |

## Rule

A relation may only receive a weight when the weight has a declared definition and measurable interpretation.

For example, "strong connection" is invalid without specifying whether strength means binding energy, contact probability, persistence, affinity, statistical association, or another quantity.

## Architecture

`elements + typed relations + state + constraints + dynamics → observable behavior`

The model must preserve relation type. A covalent bond and a regulatory association are not interchangeable merely because both can be represented as graph edges.

## Open question

Determine which relation types are necessary at each research scale and whether a smaller universal basis can reproduce the relevant observations without erasing biologically important distinctions.