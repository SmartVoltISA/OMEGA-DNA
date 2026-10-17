#!/usr/bin/env python3
"""E13: can local adaptive rewiring preserve a differentiated pattern without labels?

Abstract binary-network simulation only. No target labels are created or supplied.
Nodes begin in random binary states and the graph begins random. Adaptive rewiring
uses only current endpoint states. The state update is local majority with ties
preserving the current state. This tests whether the chosen local rule maintains
diversity or collapses toward consensus; it is not a biological model.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np

N = 80
K = 8
STEPS = 200
REPLICATES = 40
NOISE_RATES = (0.0, 0.01, 0.03)
MODES = ("static", "adaptive_assortative", "shuffled_state_control", "random_rewire")
REWIRE_ATTEMPTS_PER_STEP = 100
SEED_BASE = 4130000


def make_graph(seed):
    rng = np.random.default_rng(seed)
    a = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        candidates = np.delete(np.arange(N), i)
        a[i, rng.choice(candidates, K, replace=False)] = 1
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0)
    edges = [(int(i), int(j)) for i, j in zip(*np.where(np.triu(a, 1) > 0))]
    return a, edges


def swap_edges(a, edges, states, rng, attempts, mode):
    accepted = 0
    if len(edges) < 2:
        return accepted
    labels = states[rng.permutation(N)] if mode == "shuffled_state_control" else states
    m = len(edges)
    for _ in range(attempts):
        ix, iy = rng.integers(0, m, size=2)
        if ix == iy:
            continue
        u, v = edges[ix]
        x, y = edges[iy]
        if len({u, v, x, y}) < 4:
            continue
        if mode in ("adaptive_assortative", "shuffled_state_control"):
            if not (labels[u] != labels[v] and labels[x] != labels[y]):
                continue
            if labels[u] == labels[x] and labels[v] == labels[y]:
                pass
            elif labels[u] == labels[y] and labels[v] == labels[x]:
                x, y = y, x
            else:
                continue
        elif mode == "random_rewire":
            if rng.random() < 0.5:
                x, y = y, x
        if a[u, x] or a[v, y]:
            continue
        a[u, v] = a[v, u] = 0
        a[x, y] = a[y, x] = 0
        a[u, x] = a[x, u] = 1
        a[v, y] = a[y, v] = 1
        edges[ix] = (min(u, x), max(u, x))
        edges[iy] = (min(v, y), max(v, y))
        accepted += 1
    return accepted


def entropy_binary(p):
    h = 0.0
    if p > 0:
        h -= p * np.log2(p)
    if p < 1:
        h -= (1 - p) * np.log2(1 - p)
    return float(h)


def run_trial(seed, noise, mode, rewiring_attempts=REWIRE_ATTEMPTS_PER_STEP):
    rng = np.random.default_rng(seed)
    state = rng.integers(0, 2, N, dtype=np.int8)
    adjacency, edges = make_graph(seed + 500000)
    initial_degrees = adjacency.sum(axis=1).copy()
    disturbance_rng = np.random.default_rng(seed + 800000)
    disturbances = disturbance_rng.random((STEPS, N)) < noise
    rewire_rng = np.random.default_rng(
        seed + 900000 + MODES.index(mode) * 100000 + int(noise * 100000)
    )

    minority_trace, entropy_trace, assortativity_trace = [], [], []
    accepted_total = 0
    consensus_step = None
    for step in range(STEPS):
        state = state.copy()
        state[disturbances[step]] ^= 1
        if mode != "static":
            accepted_total += swap_edges(
                adjacency, edges, state, rewire_rng, rewiring_attempts, mode
            )
        votes = adjacency @ (2 * state.astype(np.int16) - 1)
        new_state = (votes > 0).astype(np.int8)
        ties = votes == 0
        new_state[ties] = state[ties]
        state = new_state

        p = float(np.mean(state))
        minority_trace.append(min(p, 1.0 - p))
        entropy_trace.append(entropy_binary(p))
        assortativity_trace.append(
            float(np.mean([state[i] == state[j] for i, j in edges]))
        )
        if consensus_step is None and (state.sum() == 0 or state.sum() == N):
            consensus_step = step + 1

    degree_preserved = bool(np.array_equal(initial_degrees, adjacency.sum(axis=1)))
    if not degree_preserved:
        raise RuntimeError("Degree sequence changed during edge rewiring")

    return {
        "seed": seed,
        "noise_rate": noise,
        "mode": mode,
        "mean_minority_fraction": float(np.mean(minority_trace)),
        "last50_minority_fraction": float(np.mean(minority_trace[-50:])),
        "mean_binary_entropy": float(np.mean(entropy_trace)),
        "last50_binary_entropy": float(np.mean(entropy_trace[-50:])),
        "mean_state_assortativity": float(np.mean(assortativity_trace)),
        "consensus_step": consensus_step,
        "accepted_swaps": accepted_total,
        "degree_preserved": degree_preserved,
        "target_labels_used": False,
        "nodes": N,
        "steps": STEPS,
        "noise_rate_per_node_step": noise,
        "rewiring_attempts_per_step": rewiring_attempts if mode != "static" else 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E13_EMERGENCE_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    parser.add_argument("--rewiring-attempts", type=int, default=REWIRE_ATTEMPTS_PER_STEP)
    args = parser.parse_args()

    rows = [
        run_trial(SEED_BASE + i, noise, mode, args.rewiring_attempts)
        for noise in NOISE_RATES
        for mode in MODES
        for i in range(args.replicates)
    ]
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} trial rows to {output}")
    for noise in NOISE_RATES:
        for mode in MODES:
            vals = [r for r in rows if r["noise_rate"] == noise and r["mode"] == mode]
            print(
                f"noise={noise:.2f}; mode={mode}; "
                f"minority={np.mean([r['mean_minority_fraction'] for r in vals]):.6f}; "
                f"last50_entropy={np.mean([r['last50_binary_entropy'] for r in vals]):.6f}; "
                f"consensus_rate={np.mean([r['consensus_step'] is not None for r in vals]):.3f}; "
                f"median_consensus={np.median([r['consensus_step'] if r['consensus_step'] is not None else STEPS+1 for r in vals]):.1f}"
            )


if __name__ == "__main__":
    main()
