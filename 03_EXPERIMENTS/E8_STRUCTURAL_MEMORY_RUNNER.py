#!/usr/bin/env python3
"""E8: Structural memory without a target-aware controller.

Abstract binary-network experiment only. This is not a biological model and
must not be interpreted as evidence about how to build mirror life.

The update rule sees only neighboring states. It never receives target labels.
In the aligned condition, target classes influence graph construction, so the
graph itself carries information about the target. This tests structural
encoding/persistence, not spontaneous self-organization.
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
CONDITIONS = ("random", "modular_aligned", "modular_shuffled")


def make_graph(n: int, k: int, labels: np.ndarray, mode: str,
               rng: np.random.Generator) -> np.ndarray:
    adjacency = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        candidates = np.arange(n)
        candidates = candidates[candidates != i]
        if mode == "modular":
            same = candidates[labels[candidates] == labels[i]]
            other = candidates[labels[candidates] != labels[i]]
            within = min(round(k * 0.8), len(same))
            across = k - within
            chosen = list(rng.choice(same, within, replace=False)) if within else []
            if across and len(other):
                chosen.extend(list(rng.choice(other, min(across, len(other)), replace=False)))
            if len(chosen) < k:
                chosen_set = set(chosen)
                remaining = np.array([j for j in candidates if j not in chosen_set], dtype=int)
                chosen.extend(list(rng.choice(remaining, min(k-len(chosen), len(remaining)), replace=False)))
        else:
            chosen = list(rng.choice(candidates, k, replace=False))
        adjacency[i, chosen] = 1
    adjacency = np.maximum(adjacency, adjacency.T)
    np.fill_diagonal(adjacency, 0)
    return adjacency


def run_trial(seed: int, condition: str) -> dict:
    # Generate target, initial condition, and disturbance schedule before
    # graph generation so the same seed shares these across conditions.
    rng = np.random.default_rng(seed)
    target = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(target)
    state = target.copy()
    initial_flip = rng.random(N) < INITIAL_FLIP_RATE
    state[initial_flip] = 1 - state[initial_flip]
    disturbances = rng.random((STEPS, N)) < PERTURBATION_RATE

    if condition == "modular_aligned":
        graph_labels = target.copy()
        graph_mode = "modular"
    elif condition == "modular_shuffled":
        graph_labels = target.copy()
        rng.shuffle(graph_labels)
        graph_mode = "modular"
    elif condition == "random":
        graph_labels = target.copy()
        graph_mode = "random"
    else:
        raise ValueError(f"unknown condition: {condition}")

    adjacency = make_graph(N, K, graph_labels, graph_mode, rng)
    retention = []
    for step in range(STEPS):
        state[disturbances[step]] = 1 - state[disturbances[step]]
        # Local majority rule only. Target is used for evaluation, never by controller.
        votes = adjacency @ (2 * state.astype(np.int16) - 1)
        new_state = (votes > 0).astype(np.int8)
        ties = votes == 0
        new_state[ties] = state[ties]
        state = new_state
        retention.append(float(np.mean(state == target)))

    return {
        "seed": seed,
        "condition": condition,
        "mean_retention": float(np.mean(retention)),
        "first50_retention": float(np.mean(retention[:50])),
        "last50_retention": float(np.mean(retention[-50:])),
        "nodes": N,
        "degree_target_before_symmetrization": K,
        "steps": STEPS,
        "initial_flip_rate": INITIAL_FLIP_RATE,
        "perturbation_rate": PERTURBATION_RATE,
        "controller_uses_target": False,
        "target_influences_graph": condition == "modular_aligned",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E8_STRUCTURAL_MEMORY_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()
    rows = [
        run_trial(SEED_BASE + i, condition)
        for condition in CONDITIONS
        for i in range(args.replicates)
    ]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")
    for condition in CONDITIONS:
        values = np.array([r["mean_retention"] for r in rows if r["condition"] == condition])
        mean = float(values.mean())
        sd = float(values.std(ddof=1))
        half = 1.96 * sd / np.sqrt(len(values))
        print(f"{condition}: mean={mean:.6f}; SD={sd:.6f}; approx95CI=[{mean-half:.6f}, {mean+half:.6f}]")


if __name__ == "__main__":
    main()
