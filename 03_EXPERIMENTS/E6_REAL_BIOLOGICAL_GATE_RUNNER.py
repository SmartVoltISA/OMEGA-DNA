#!/usr/bin/env python3
"""E6 real biological gate runner.

Consumes a precomputed, leakage-controlled candidate table. Labels must be
constructed independently from target RNA expression before this script runs.
The script never derives labels from contact features.

Input TSV columns:
  chrom,start,end,promoter_chrom,promoter_start,promoter_end,gene,label,
  contact_score,enh_access,prom_access,tf_score,h3k27ac_score

Optional sequence columns may be supplied directly as enhancer_seq and
promoter_seq. Otherwise a FASTA reference is required and coordinates are
used to extract sequences.
"""
from __future__ import annotations
import argparse, csv, math, hashlib, json
from pathlib import Path
import numpy as np

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
except Exception as exc:
    raise SystemExit("scikit-learn is required: %s" % exc)

BASES = "ACGT"


def parse_fasta(path):
    seqs, name, buf = {}, None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    seqs[name] = "".join(buf).upper()
                name, buf = line[1:].split()[0], []
            else:
                buf.append(line)
        if name is not None:
            seqs[name] = "".join(buf).upper()
    return seqs


def seq_features(seq, k=3):
    s = seq.upper().replace("N", "")
    n = len(s)
    if n == 0:
        return [0.0] * (4 + 1 + 16 + 64)
    gc = (s.count("G") + s.count("C")) / n
    counts = np.array([s.count(b) for b in BASES], dtype=float) / n
    entropy = -sum(p * math.log2(p) for p in counts if p > 0)
    dinuc = np.zeros(16, dtype=float)
    idx = {a + b: i for i, a in enumerate(BASES) for b in BASES}
    for a, b in zip(s[:-1], s[1:]):
        if a + b in idx:
            dinuc[idx[a + b]] += 1
    if n > 1:
        dinuc /= (n - 1)
    kmer = np.zeros(64, dtype=float)
    if k == 3 and n >= 3:
        idx3 = {a + b + c: i for i, a in enumerate(BASES) for b in BASES for c in BASES}
        for i in range(n - 2):
            t = s[i:i+3]
            if t in idx3:
                kmer[idx3[t]] += 1
        kmer /= max(1, n - 2)
    return [gc, entropy, *counts, *dinuc, *kmer]


def get_seq(row, key, fasta):
    direct = row.get(key)
    if direct:
        return direct
    chrom = row["chrom"] if key == "enhancer_seq" else row["promoter_chrom"]
    start = int(row["start"] if key == "enhancer_seq" else row["promoter_start"])
    end = int(row["end"] if key == "enhancer_seq" else row["promoter_end"])
    if chrom not in fasta:
        raise ValueError(f"chromosome {chrom} absent from FASTA")
    return fasta[chrom][start:end]


def load_rows(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    required = {"chrom", "start", "end", "promoter_chrom", "promoter_start", "promoter_end", "gene", "label"}
    missing = required - set(rows[0]) if rows else required
    if missing:
        raise ValueError("missing columns: " + ",".join(sorted(missing)))
    return rows


def relation_features(r):
    names = ["contact_score", "enh_access", "prom_access", "tf_score", "h3k27ac_score"]
    vals = [float(r.get(k, 0.0) or 0.0) for k in names]
    e_mid = (int(r["start"]) + int(r["end"])) / 2
    p_mid = (int(r["promoter_start"]) + int(r["promoter_end"])) / 2
    dist = abs(e_mid - p_mid)
    vals.append(math.log1p(dist))
    return vals


def chromosome_split(rows):
    train = {str(i) for i in range(1, 17)}
    val = {"17", "18", "19"}
    test = {"20", "21", "22", "X"}
    out = []
    for r in rows:
        c = r["chrom"].removeprefix("chr")
        out.append("train" if c in train else "val" if c in val else "test" if c in test else "excluded")
    return np.array(out)


def standardize_fit(Xtr, Xte):
    mu = Xtr.mean(0)
    sd = Xtr.std(0)
    sd[sd < 1e-12] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd


def evaluate(name, Xtr, ytr, Xte, yte, seed):
    Xtr, Xte = standardize_fit(Xtr, Xte)
    clf = LogisticRegression(max_iter=3000, C=1.0, solver="lbfgs", random_state=seed)
    clf.fit(Xtr, ytr)
    p = clf.predict_proba(Xte)[:, 1]
    return {
        "model": name,
        "auroc": float(roc_auc_score(yte, p)),
        "auprc": float(average_precision_score(yte, p)),
        "brier": float(brier_score_loss(yte, p)),
        "n_test": int(len(yte)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--fasta", default=None)
    ap.add_argument("--out", default="E6_REAL_BIOLOGICAL_GATE_RESULTS.json")
    ap.add_argument("--seed", type=int, default=20260907)
    args = ap.parse_args()

    rows = load_rows(args.pairs)
    fasta = parse_fasta(args.fasta) if args.fasta else {}
    seq_X, rel_X, y, split = [], [], [], chromosome_split(rows)
    for r in rows:
        es = get_seq(r, "enhancer_seq", fasta)
        ps = get_seq(r, "promoter_seq", fasta)
        seq_X.append(seq_features(es) + seq_features(ps))
        rel_X.append(relation_features(r))
        y.append(int(r["label"]))
    seq_X, rel_X, y = np.asarray(seq_X), np.asarray(rel_X), np.asarray(y)

    train = split == "train"
    test = split == "test"
    if train.sum() < 20 or test.sum() < 20:
        raise SystemExit("insufficient chromosome-level train/test rows")
    if len(np.unique(y[train])) < 2 or len(np.unique(y[test])) < 2:
        raise SystemExit("both train and test require positive and negative labels")

    results = []
    results.append(evaluate("sequence_only", seq_X[train], y[train], seq_X[test], y[test], args.seed))
    combined = np.concatenate([seq_X, rel_X], axis=1)
    results.append(evaluate("relational", combined[train], y[train], combined[test], y[test], args.seed))

    rng = np.random.default_rng(args.seed)
    shuffled = rel_X.copy()
    shuffled[train] = shuffled[rng.permutation(np.where(train)[0])]
    shuffled_combined = np.concatenate([seq_X, shuffled], axis=1)
    results.append(evaluate("relation_shuffled_null", shuffled_combined[train], y[train], shuffled_combined[test], y[test], args.seed))

    payload = {
        "protocol": "E6_REAL_BIOLOGICAL_GATE_PROTOCOL.md",
        "pairs_sha256": hashlib.sha256(Path(args.pairs).read_bytes()).hexdigest(),
        "fasta_sha256": hashlib.sha256(Path(args.fasta).read_bytes()).hexdigest() if args.fasta else None,
        "seed": args.seed,
        "n_total": int(len(rows)),
        "n_train": int(train.sum()),
        "n_test": int(test.sum()),
        "results": results,
        "status": "executed_biological_input" if args.fasta else "executed_precomputed_sequence_input",
        "notes": [
            "Labels must be independently derived from RNA expression before this runner.",
            "Chromosome-level holdout is primary.",
            "The relation-shuffle null preserves the relation feature marginal distribution.",
        ],
    }
    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
