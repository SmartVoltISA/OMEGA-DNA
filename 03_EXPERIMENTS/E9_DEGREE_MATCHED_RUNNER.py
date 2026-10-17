#!/usr/bin/env python3
"""E9 degree-preserving null and assortativity sweep.

Exploratory abstract binary network only. The graph is built using target labels
in aligned conditions, so this tests structural encoding/persistence, not
spontaneous self-organization or a biological mechanism.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np

N = 80
K = 8
STEPS = 200
REPLICATES = 100
PERTURBATION_RATE = 0.03
INITIAL_FLIP_RATE = 0.15
SEED_BASE = 1000
WITHIN_FRACTIONS = (0.5, 0.6, 0.7, 0.8, 0.9)


def make_graph(n, k, labels, within_fraction, rng):
    a = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        candidates = np.delete(np.arange(n), i)
        same = candidates[labels[candidates] == labels[i]]
        other = candidates[labels[candidates] != labels[i]]
        within = min(int(round(k * within_fraction)), len(same))
        across = k - within
        chosen = list(rng.choice(same, within, replace=False)) if within else []
        if across and len(other):
            chosen += list(rng.choice(other, min(across, len(other)), replace=False))
        if len(chosen) < k:
            chosen_set = set(chosen)
            remaining = np.array([x for x in candidates if x not in chosen_set], dtype=int)
            chosen += list(rng.choice(remaining, min(k-len(chosen), len(remaining)), replace=False))
        a[i, chosen] = 1
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0)
    return a


def degree_preserving_rewire(a, rng, swaps_factor=20):
    """Undirected double-edge swaps; accepted swaps preserve every node degree."""
    edges = [(int(i), int(j)) for i in range(len(a)) for j in range(i+1, len(a)) if a[i, j]]
    b = a.copy()
    m = len(edges)
    accepted = 0
    attempts = max(m * swaps_factor, 1000)
    for _ in range(attempts):
        e1, e2 = rng.integers(0, m, size=2)
        if e1 == e2:
            continue
        u, v = edges[e1]
        x, y = edges[e2]
        if len({u, v, x, y}) < 4:
            continue
        if rng.random() < 0.5:
            x, y = y, x
        if b[u, y] or b[x, v]:
            continue
        b[u, v] = b[v, u] = 0
        b[x, y] = b[y, x] = 0
        b[u, y] = b[y, u] = 1
        b[x, v] = b[v, x] = 1
        edges[e1] = (min(u, y), max(u, y))
        edges[e2] = (min(x, v), max(x, v))
        accepted += 1
    return b, accepted, attempts


def run_trial(seed, within_fraction, null=False):
    rng = np.random.default_rng(seed)
    target = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(target)
    state = target.copy()
    initial_flip = rng.random(N) < INITIAL_FLIP_RATE
    state[initial_flip] = 1 - state[initial_flip]
    disturbances = rng.random((STEPS, N)) < PERTURBATION_RATE

    graph_rng = np.random.default_rng(seed + 700000)
    adjacency = make_graph(N, K, target, within_fraction, graph_rng)
    accepted_swaps = 0
    swap_attempts = 0
    if null:
        adjacency, accepted_swaps, swap_attempts = degree_preserving_rewire(
            adjacency, np.random.default_rng(seed + 900000), 20
        )

    degree_before = adjacency.sum(axis=1).copy()
    retention = []
    for step in range(STEPS):
        state[disturbances[step]] = 1 - state[disturbances[step]]
        votes = adjacency @ (2 * state.astype(np.int16) - 1)
        new_state = (votes > 0).astype(np.int8)
        ties = votes == 0
        new_state[ties] = state[ties]
        state = new_state
        retention.append(float(np.mean(state == target)))

    return {
        "seed": seed,
        "within_fraction": within_fraction,
        "condition": "degree_preserving_null" if null else "target_aligned",
        "mean_retention": float(np.mean(retention)),
        "first50_retention": float(np.mean(retention[:50])),
        "last50_retention": float(np.mean(retention[-50:])),
        "nodes": N,
        "edges": int(adjacency.sum() // 2),
        "steps": STEPS,
        "initial_flip_rate": INITIAL_FLIP_RATE,
        "perturbation_rate": PERTURBATION_RATE,
        "controller_uses_target": False,
        "target_influences_graph": True,
        "degree_sequence_sum": int(degree_before.sum()),
        "accepted_swaps": accepted_swaps,
        "swap_attempts": swap_attempts,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E9_DEGREE_MATCHED_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()
    rows = []
    for fraction in WITHIN_FRACTIONS:
        for replicate in range(args.replicates):
            seed = SEED_BASE + replicate
            aligned = run_trial(seed, fraction, False)
            null = run_trial(seed, fraction, True)
            rows.extend((aligned, null))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")
    for fraction in WITHIN_FRACTIONS:
        for condition in ("target_aligned", "degree_preserving_null"):
            vals = [r["mean_retention"] for r in rows
                    if r["within_fraction"] == fraction and r["condition"] == condition]
            print(f"within={fraction:.1f} {condition}: mean={np.mean(vals):.6f}; SD={np.std(vals, ddof=1):.6f}")


if __ ( __name__ == "__main__" ):
    main()
