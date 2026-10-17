#!/usr/bin/env python3
"""E10: local state-based rewiring versus static random topology.

Abstract binary network only. The algorithm never reads target labels for its
updates. It uses current states to choose rewiring swaps. This is a toy test of
whether local adaptation alone preserves an initial balanced pattern; it is
not a biological model.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np

N = 80
K = 8
STEPS = 250
REPLICATES = 40
INITIAL_FLIP_RATE = 0.15
NOISE_RATES = (0.0, 0.01, 0.03)
REWIRE_ATTEMPTS = (0, 8, 32, 80)
SEED_BASE = 2030000


def make_graph(n, k, rng):
    a = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        candidates = np.delete(np.arange(n), i)
        a[i, rng.choice(candidates, k, replace=False)] = 1
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0)
    return a


def assortativity(a, state):
    i, j = np.where(np.triu(a, 1) > 0)
    return float(np.mean(state[i] == state[j])) if len(i) else float("nan")


def assortative_swap(a, labels, rng, attempts):
    """Undirected double-edge swaps preserving every node degree."""
    edges = [(int(i), int(j)) for i, j in zip(*np.where(np.triu(a, 1) > 0))]
    if len(edges) < 2:
        return a, 0
    accepted = 0
    for _ in range(attempts):
        ix, iy = rng.integers(0, len(edges), size=2)
        if ix == iy:
            continue
        u, v = edges[ix]
        x, y = edges[iy]
        if len({u, v, x, y}) < 4:
            continue
        if labels[u] == labels[x] and labels[v] == labels[y] and labels[u] != labels[v]:
            pass
        elif labels[u] == labels[y] and labels[v] == labels[x] and labels[u] != labels[v]:
            x, y = y, x
        else:
            continue
        if a[u, x] or a[v, y]:
            continue
        a[u, v] = a[v, u] = 0
        a[x, y] = a[y, x] = 0
        a[u, x] = a[x, u] = 1
        a[v, y] = a[y, v] = 1
        edges[ix] = (min(u, x), max(u, x))
        edges[iy] = (min(v, y), max(v, y))
        accepted += 1
    return a, accepted


def run_trial(seed, rewire_attempts, noise_rate):
    rng = np.random.default_rng(seed)
    target = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(target)
    state = target.copy()
    state[rng.random(N) < INITIAL_FLIP_RATE] ^= 1
    a = make_graph(N, K, np.random.default_rng(seed + 500000))
    disturbance_rng = np.random.default_rng(seed + 800000)
    disturbances = disturbance_rng.random((STEPS, N)) < noise_rate
    rewire_rng = np.random.default_rng(
        seed + 900000 + rewire_attempts * 1000 + int(noise_rate * 100000)
    )
    original_degree = a.sum(axis=1).copy()
    retention, assort, minority = [], [], []
    accepted_total = 0
    first_consensus_step = None

    for step in range(STEPS):
        state[disturbances[step]] ^= 1
        if rewire_attempts:
            a, accepted = assortative_swap(a, state, rewire_rng, rewire_attempts)
            accepted_total += accepted
        votes = a @ (2 * state.astype(np.int16) - 1)
        new_state = (votes > 0).astype(np.int8)
        ties = votes == 0
        new_state[ties] = state[ties]
        state = new_state
        retention.append(float(np.mean(state == target)))
        assort.append(assortativity(a, state))
        minority.append(float(min(state.mean(), 1.0 - state.mean())))
        if first_consensus_step is None and (state.sum() == 0 or state.sum() == N):
            first_consensus_step = step + 1

    degree_preserved = bool(np.array_equal(original_degree, a.sum(axis=1)))
    if not degree_preserved:
        raise RuntimeError("Degree sequence changed during rewiring")
    return {
        "seed": seed,
        "rewire_attempts_per_step": rewire_attempts,
        "noise_rate": noise_rate,
        "mean_retention": float(np.mean(retention)),
        "last50_retention": float(np.mean(retention[-50:])),
        "final_retention": float(retention[-1]),
        "mean_state_assortativity": float(np.mean(assort)),
        "final_minority_fraction": float(minority[-1]),
        "first_consensus_step": first_consensus_step,
        "accepted_swaps": accepted_total,
        "degree_preserved": degree_preserved,
        "steps": STEPS,
        "nodes": N,
        "initial_flip_rate": INITIAL_FLIP_RATE,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E10_LOCAL_ADAPTATION_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()
    rows = []
    for rewires in REWIRE_ATTEMPTS:
        for noise in NOISE_RATES:
            for i in range(args.replicates):
                rows.append(run_trial(SEED_BASE + i, rewires, noise))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")
    for rewires in REWIRE_ATTEMPTS:
        for noise in NOISE_RATES:
            vals = [r["mean_retention"] for r in rows
                    if r["rewire_attempts_per_step"] == rewires and r["noise_rate"] == noise]
            print(f"rewires={rewires}; noise={noise:.2f}; mean={np.mean(vals):.6f}; SD={np.std(vals, ddof=1):.6f}")


if __name__ == "__main__":
    main()
