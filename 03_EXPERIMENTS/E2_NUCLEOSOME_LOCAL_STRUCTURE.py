"""E2 nucleosome/local-structure controlled benchmark.

Purpose
-------
Test whether sequence order carries predictive information for a declared,
periodic nucleosome-wrapping proxy beyond GC composition alone.

This is a controlled computational experiment. The target is NOT an
experimental nucleosome-occupancy measurement. It is a fixed toy physical
proxy inspired by the ~10 bp helical periodicity of DNA wrapped on a
nucleosome. The experiment therefore tests representation/information
preservation, not a new biological law.

Design
------
- 6,000 random 147-bp sequences per seed
- 30 independent seeds
- 70/30 held-out split
- baseline: GC fraction
- relation model 1: global dinucleotide frequencies
- relation model 2: phase-resolved dinucleotide frequencies at a 10-bp period
- null: shuffle phase-resolved relation features in the held-out set
- matched-composition control: paired sequences with nearly identical GC
  but different order

The real-data gate is separate: ENCODE/NCBI provide experimental MNase-seq
nucleosome-position data, but the present execution environment cannot fetch
the required binary/raw data payloads. No experimental result is fabricated.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

N = 6000
L = 147
N_SEEDS = 30
DINUC = 16
FAVORED = np.array([0, 15, 3, 12])  # AA, TT, AT, TA for A,C,G,T encoding


def one_seed(seed: int):
    rng = np.random.default_rng(10_000 + seed)
    x = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    pair = x[:, :-1] * 4 + x[:, 1:]
    gc = ((x == 1) | (x == 2)).mean(axis=1)
    global_di = np.stack([(pair == k).mean(axis=1) for k in range(DINUC)], axis=1)
    phase = np.stack(
        [
            np.stack(
                [(pair[:, p::10] == k).mean(axis=1) for k in range(DINUC)],
                axis=1,
            )
            for p in range(10)
        ],
        axis=1,
    )
    y = phase[:, :, FAVORED].sum(axis=2).mean(axis=1)
    X = np.concatenate([gc[:, None], global_di, phase.reshape(N, 160)], axis=1)

    split = np.random.default_rng(seed).permutation(N)
    cut = int(0.70 * N)
    tr, te = split[:cut], split[cut:]

    gc_model = Ridge(alpha=1e-3).fit(X[tr, :1], y[tr])
    dinuc_model = Ridge(alpha=1e-3).fit(X[tr, :17], y[tr])
    relation_model = Ridge(alpha=1e-3).fit(X[tr], y[tr])

    shuffled = X[te].copy()
    np.random.default_rng(seed).shuffle(shuffled)

    return {
        "seed": seed,
        "gc_mae": mean_absolute_error(y[te], gc_model.predict(X[te, :1])),
        "gc_r2": r2_score(y[te], gc_model.predict(X[te, :1])),
        "global_dinuc_mae": mean_absolute_error(y[te], dinuc_model.predict(X[te, :17])),
        "global_dinuc_r2": r2_score(y[te], dinuc_model.predict(X[te, :17])),
        "phase_relation_mae": mean_absolute_error(y[te], relation_model.predict(X[te])),
        "phase_relation_r2": r2_score(y[te], relation_model.predict(X[te])),
        "shuffled_phase_mae": mean_absolute_error(y[te], relation_model.predict(shuffled)),
    }


def matched_gc_control():
    rng = np.random.default_rng(20260907)
    n = 10000
    x = rng.integers(0, 4, size=(n, L), dtype=np.int8)
    pair = x[:, :-1] * 4 + x[:, 1:]
    gc = ((x == 1) | (x == 2)).mean(axis=1)
    y = np.stack(
        [
            (np.isin(pair[:, p::10], FAVORED)).mean(axis=1)
            for p in range(10)
        ],
        axis=1,
    ).mean(axis=1)
    order = np.argsort(gc)
    diffs = []
    for a, b in zip(order[::2], order[1::2]):
        if abs(gc[a] - gc[b]) < 0.01:
            diffs.append(abs(y[a] - y[b]))
    diffs = np.asarray(diffs)
    return {
        "n_pairs": int(len(diffs)),
        "mean_abs_target_difference": float(diffs.mean()),
        "median_abs_target_difference": float(np.median(diffs)),
        "p90_abs_target_difference": float(np.quantile(diffs, 0.90)),
        "p99_abs_target_difference": float(np.quantile(diffs, 0.99)),
    }


def main():
    results = pd.DataFrame([one_seed(s) for s in range(N_SEEDS)])
    print(results.to_string(index=False))
    print("\nMEAN")
    print(results.mean(numeric_only=True))
    print("\nSTD")
    print(results.std(numeric_only=True))
    print("\nMATCHED_GC")
    print(matched_gc_control())


if __name__ == "__main__":
    main()
