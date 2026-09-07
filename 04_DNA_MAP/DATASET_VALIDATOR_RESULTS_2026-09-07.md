# OMEGA-DNA Dataset Validator — 2026-09-07

## Input
`test_omega.csv` (toy/local validator fixture)

Observed schema:
- rows: 2
- columns: `sequence, contact, label, assembly`
- assembly: `hg38`
- sequence: present
- relation-like feature: `contact`
- label: present

## Result
**INCOMPLETE — DATA INTAKE ONLY**

The file is structurally readable and contains a minimal sequence + relation + label pattern, but it is not sufficient for the E6 real biological gate.

Missing/insufficient requirements include:
- genomic chromosome/start/end coordinates;
- explicit assay/source provenance for relation and labels;
- sample/cell-state metadata;
- sufficient independent observations;
- chromosome-level leakage-safe split;
- independently measured accessibility/occupancy/contact modalities;
- independent RNA/functional assay provenance.

## Evidence classification
`UNKNOWN` for biological function.

The two rows are a validator test fixture, not biological evidence and must not be used as an E6 result.

## Pipeline decision
`FILE → FORMAT → SCHEMA → DATA QUALITY → ASSEMBLY → COORDINATES → PROVENANCE → LEAKAGE → AVAILABLE OMEGA LAYERS → RECOMMENDED GATE`

Recommended next gate: `E6_REAL_BIOLOGICAL_GATE` only after a qualifying public dataset passes this intake audit.
