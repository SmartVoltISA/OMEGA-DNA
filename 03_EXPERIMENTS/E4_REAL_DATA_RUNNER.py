"""E4 real-data benchmark runner.

Purpose
-------
Run a capacity-controlled, relation-aware benchmark on a tabular real-data
export without inventing biological relations. The input must contain:

  target        binary 0/1 label
  group         split/group identifier (chromosome, locus group, etc.)
  sequence_*    numeric sequence-derived features
  relation_*   numeric experimentally measured relation/state features

The runner evaluates:
  A: sequence only
  B: sequence + typed relation/state
  C: sequence + shuffled relation null
  D: relation-family ablations

It deliberately does NOT derive "relations" from the sequence. A relation
column must be supplied by the dataset and documented as measured/annotated.

Example
-------
python E4_REAL_DATA_RUNNER.py --input benchmark.csv --target target \
  --group chromosome --sequence-prefix sequence_ --relation-prefix relation_ \
  --seeds 7 11 19 23 --out results.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--target", default="target")
    p.add_argument("--group", default="group")
    p.add_argument("--sequence-prefix", default="sequence_")
    p.add_argument("--relation-prefix", default="relation_")
    p.add_argument("--seeds", nargs="+", type=int, default=[7, 11, 19, 23])
    p.add_argument("--test-group", nargs="+", default=None)
    p.add_argument("--valid-fraction", type=float, default=0.2)
    p.add_argument("--out", default="E4_real_data_results.json")
    return p.parse_args()


def make_model(seed: int):
    return make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=seed),
    )


def grouped_split(df, group_col, seed, test_groups=None, valid_fraction=0.2):
    groups = df[group_col].astype(str).unique()
    rng = np.random.default_rng(seed)
    if test_groups is None:
        shuffled = groups.copy()
        rng.shuffle(shuffled)
        n_test = max(1, int(round(len(groups) * 0.2)))
        test_groups = set(shuffled[:n_test])
    else:
        test_groups = set(map(str, test_groups))

    remain = [g for g in groups if g not in test_groups]
    rng.shuffle(remain)
    n_valid = max(1, int(round(len(remain) * valid_fraction)))
    valid_groups = set(remain[:n_valid])

    test = df[group_col].astype(str).isin(test_groups).to_numpy()
    valid = df[group_col].astype(str).isin(valid_groups).to_numpy()
    train = ~(test | valid)
    return train, valid, test


def score_fit(X, y, train, test, seed):
    if len(np.unique(y[train])) < 2 or len(np.unique(y[test])) < 2:
        return np.nan
    model = make_model(seed)
    model.fit(X[train], y[train])
    return float(roc_auc_score(y[test], model.predict_proba(X[test])[:, 1]))


def run(args):
    df = pd.read_csv(args.input)
    if args.target not in df or args.group not in df:
        raise ValueError(f"Input must contain {args.target!r} and {args.group!r}")

    seq_cols = [c for c in df.columns if c.startswith(args.sequence_prefix)]
    rel_cols = [c for c in df.columns if c.startswith(args.relation_prefix)]
    if not seq_cols or not rel_cols:
        raise ValueError("Need both sequence_* and relation_* columns")

    y = df[args.target].astype(int).to_numpy()
    seq = df[seq_cols].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    rel = df[rel_cols].apply(pd.to_numeric, errors="coerce").to_numpy(float)
    combined = np.column_stack([seq, rel])

    families = {}
    for c in rel_cols:
        family = c.split("_", 2)[1] if c.count("_") >= 2 else c
        families.setdefault(family, []).append(c)

    rows = []
    for seed in args.seeds:
        train, valid, test = grouped_split(
            df, args.group, seed, args.test_group, args.valid_fraction
        )
        rng = np.random.default_rng(seed)
        shuffled = rel.copy()
        shuffled[train] = shuffled[train][rng.permutation(train.sum())]

        variants = {
            "sequence_only": seq,
            "combined": combined,
            "shuffled_relation_null": np.column_stack([seq, shuffled]),
            "relations_only": rel,
        }
        for family, cols in families.items():
            keep = [i for i, c in enumerate(rel_cols) if c not in cols]
            variants[f"ablation_without_{family}"] = np.column_stack([seq, rel[:, keep]])

        for name, X in variants.items():
            rows.append({
                "seed": seed,
                "variant": name,
                "auc": score_fit(X, y, train, test, seed),
                "n_train": int(train.sum()),
                "n_valid": int(valid.sum()),
                "n_test": int(test.sum()),
                "n_sequence_features": int(seq.shape[1]),
                "n_relation_features": int(rel.shape[1]),
            })

    result_df = pd.DataFrame(rows)
    pivot = result_df.pivot(index="seed", columns="variant", values="auc")
    summary = {}
    for col in pivot.columns:
        vals = pivot[col].dropna()
        summary[col] = {"mean_auc": float(vals.mean()), "std_auc": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0}

    if {"combined", "sequence_only"}.issubset(pivot.columns):
        a = pivot["combined"].dropna()
        b = pivot["sequence_only"].reindex(a.index)
        t = ttest_rel(a, b, nan_policy="omit")
        delta = float((a - b).mean())
        paired = {"mean_delta": delta, "t": float(t.statistic), "p": float(t.pvalue)}
    else:
        paired = None

    null_test = None
    if {"shuffled_relation_null", "sequence_only"}.issubset(pivot.columns):
        a = pivot["shuffled_relation_null"].dropna()
        b = pivot["sequence_only"].reindex(a.index)
        t = ttest_rel(a, b, nan_policy="omit")
        null_test = {"mean_delta": float((a - b).mean()), "t": float(t.statistic), "p": float(t.pvalue)}

    output = {
        "status": "executed",
        "input": str(Path(args.input)),
        "target": args.target,
        "group": args.group,
        "sequence_features": seq_cols,
        "relation_features": rel_cols,
        "relation_families": families,
        "seeds": args.seeds,
        "summary": summary,
        "combined_vs_sequence": paired,
        "shuffled_null_vs_sequence": null_test,
        "interpretation_guardrail": (
            "A positive combined-vs-sequence delta is not sufficient by itself. "
            "The relation columns must be independently documented as measured/annotated, "
            "the shuffled null must fail to reproduce the gain, and the result must survive "
            "independent seeds and capacity controls."
        ),
    }
    Path(args.out).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run(parse_args())
