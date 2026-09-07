#!/usr/bin/env python3
"""OMEGA-DNA dataset intake validator.

Conservative validator for CSV/TSV/BED-like tabular inputs. It does not infer
biological function; it audits whether a dataset is structurally suitable for
an OMEGA gate and emits READY/INCOMPLETE/INVALID.
"""
from __future__ import annotations
import argparse, csv, json, math, re
from pathlib import Path
from typing import Any

COORD = {"chrom", "chromosome", "chr", "start", "end", "position", "pos", "strand"}
ASSEMBLY = {"assembly", "genome", "reference", "genome_build", "build"}
SEQ = {"sequence", "seq", "dna", "sequence_context"}
LABEL = {"label", "target", "y", "class", "effect", "functional_effect", "response"}
REL = {"contact", "contacts", "interaction", "hic", "pchic", "loop", "distance", "occupancy", "accessibility", "atac", "dnase", "h3k27ac", "tf", "binding"}
PROV = {"source", "assay", "dataset", "sample", "accession", "provenance", "experiment", "cell_type", "celltype"}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.strip().lower()).strip("_")


def load_table(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(8192)
    delim = "\t" if "\t" in sample.splitlines()[0] else ","
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=delim))
    fields = [norm(x) for x in (rows[0].keys() if rows else [])]
    return delim, fields, rows


def classify(fields):
    s = set(fields)
    return {
        "sequence": sorted(s & SEQ),
        "label": sorted(s & LABEL),
        "coordinates": sorted(s & COORD),
        "assembly": sorted(s & ASSEMBLY),
        "relations": sorted(s & REL),
        "provenance": sorted(s & PROV),
    }


def missingness(rows, fields):
    out = {}
    n = len(rows)
    for f in fields:
        miss = sum(1 for r in rows if r.get(f) in (None, ""))
        out[f] = miss / n if n else 1.0
    return out


def numeric_summary(rows, fields):
    out = {}
    for f in fields:
        vals = []
        for r in rows:
            try:
                x = float(r.get(f, ""))
                if math.isfinite(x): vals.append(x)
            except (TypeError, ValueError): pass
        if vals:
            out[f] = {"n_numeric": len(vals), "min": min(vals), "max": max(vals)}
    return out


def validate(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"file": str(path), "status": "INVALID", "errors": [], "warnings": []}
    if not path.exists():
        result["errors"].append("file_not_found")
        return result
    if path.suffix.lower() not in {".csv", ".tsv", ".txt"}:
        result["warnings"].append("extension_not_guaranteed_tabular")
    try:
        delim, fields, rows = load_table(path)
    except Exception as e:
        result["errors"].append(f"parse_error:{e}")
        return result
    result.update({"format": "TSV" if delim == "\t" else "CSV", "rows": len(rows), "columns": len(fields), "fields": fields})
    result["schema_concepts"] = classify(fields)
    result["missingness"] = missingness(rows, fields)
    result["numeric_summary"] = numeric_summary(rows, fields)
    tuples = [tuple(r.get(f, "") for f in fields) for r in rows]
    result["duplicate_rows"] = len(tuples) - len(set(tuples))

    c = result["schema_concepts"]
    if not rows or not fields:
        result["errors"].append("empty_table")
    if not c["sequence"]:
        result["warnings"].append("no_sequence_column")
    if not c["label"]:
        result["warnings"].append("no_label_column")
    if not c["assembly"]:
        result["warnings"].append("no_genome_assembly_column")
    if not c["coordinates"]:
        result["warnings"].append("no_genomic_coordinates")
    if not c["provenance"]:
        result["warnings"].append("no_explicit_feature_or_assay_provenance")
    if not c["relations"]:
        result["warnings"].append("no_typed_relation_feature_detected")

    # Conservative leakage heuristics.
    leakage = []
    for f in fields:
        fl = f.lower()
        if any(x in fl for x in ("pred", "prediction", "model_score", "probability")):
            leakage.append(f"possible_model_output:{f}")
        if any(x in fl for x in ("fold", "split", "test", "train", "validation")):
            leakage.append(f"split_metadata:{f}")
        if any(x in fl for x in ("label", "target", "effect")) and any(x in fl for x in ("measured", "assay")):
            leakage.append(f"label_like_assay_field:{f}")
    result["leakage_flags"] = leakage

    if result["duplicate_rows"]:
        result["warnings"].append("duplicate_rows_present")
    for f, rate in result["missingness"].items():
        if rate > 0.5:
            result["warnings"].append(f"high_missingness:{f}:{rate:.3f}")

    # Gate recommendation is deliberately strict.
    complete_e6 = (
        len(rows) >= 1000 and c["sequence"] and c["label"] and c["coordinates"]
        and c["assembly"] and c["relations"] and c["provenance"]
        and not result["errors"]
    )
    if complete_e6:
        result["recommended_gate"] = "E6_REAL_BIOLOGICAL_GATE"
        result["status"] = "READY"
    elif rows and not result["errors"]:
        result["recommended_gate"] = "DATA_INTAKE_ONLY"
        result["status"] = "INCOMPLETE"
    result["biological_evidence"] = False
    result["note"] = "Structural intake only; validation does not establish biological function or causality."
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = validate(Path(args.path))
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else f"{r['status']}: {r['file']}\nGate: {r.get('recommended_gate')}\nWarnings: {len(r['warnings'])}\nErrors: {len(r['errors'])}")
    raise SystemExit(0 if r["status"] != "INVALID" else 2)

if __name__ == "__main__": main()
