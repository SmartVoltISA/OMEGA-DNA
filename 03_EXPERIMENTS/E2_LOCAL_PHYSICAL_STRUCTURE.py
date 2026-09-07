"""E2 local physical structure benchmark.

Tests whether sequence-order relations carry predictive information about a
fixed physical proxy (nearest-neighbor DNA duplex melting temperature)
beyond GC composition alone.

This is a controlled molecular-physics benchmark, not a claim of biological
function. Conditions are held fixed by Biopython's declared Tm_NN model.
"""
from __future__ import annotations
import random
import numpy as np
import pandas as pd
from Bio.SeqUtils import MeltingTemp as mt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

BASES = "ACGT"
DINUCS = [a+b for a in BASES for b in BASES]
N = 60
N_ROWS = 20_000
N_SEEDS = 30


def features(seq: str):
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    d = {k: 0 for k in DINUCS}
    for i in range(len(seq)-1):
        d[seq[i:i+2]] += 1
    return [gc] + [d[k] / (len(seq)-1) for k in DINUCS]


def build(seed=20260907):
    rng = random.Random(seed)
    rows = []
    for _ in range(N_ROWS):
        seq = "".join(rng.choice(BASES) for _ in range(N))
        rows.append(features(seq) + [mt.Tm_NN(seq)])
    return pd.DataFrame(rows, columns=["gc"] + DINUCS + ["tm"])


def run():
    df = build()
    X_gc = df[["gc"]].to_numpy()
    X_rel = df[["gc"] + DINUCS].to_numpy()
    y = df.tm.to_numpy()
    out = []
    for seed in range(N_SEEDS):
        rng = np.random.RandomState(seed)
        idx = rng.permutation(len(df))
        cut = int(.70 * len(df))
        tr, te = idx[:cut], idx[cut:]
        gc_model = LinearRegression().fit(X_gc[tr], y[tr])
        rel_model = LinearRegression().fit(X_rel[tr], y[tr])
        shuffled = X_rel[te].copy()
        rng.shuffle(shuffled)
        out.append({
            "seed": seed,
            "gc_mae": mean_absolute_error(y[te], gc_model.predict(X_gc[te])),
            "gc_r2": r2_score(y[te], gc_model.predict(X_gc[te])),
            "relation_mae": mean_absolute_error(y[te], rel_model.predict(X_rel[te])),
            "relation_r2": r2_score(y[te], rel_model.predict(X_rel[te])),
            "shuffled_relation_mae": mean_absolute_error(y[te], rel_model.predict(shuffled)),
        })
    return pd.DataFrame(out)


if __name__ == "__main__":
    r = run()
    print(r.to_string(index=False))
    print("\nMEAN")
    print(r.mean(numeric_only=True))
    print("\nSTD")
    print(r.std(numeric_only=True))
