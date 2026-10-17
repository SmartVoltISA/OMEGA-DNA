#!/usr/bin/env python3
"""E12: component turnover and continuity of local memory.

Abstract binary network only. A target pattern is encoded both in initial node
states and in a target-aligned modular graph. The update rule never reads target
labels; they are used only for graph construction and evaluation.

Conditions:
- no_memory: no history term; replacement resets state only.
- memory_preserved: local history trace survives node replacement.
- memory_reset: same memory strength, but replacement resets the trace.
- memory_strong: stronger history term, with trace reset on replacement.

This tests persistence of an already encoded organization, not spontaneous
creation of organization or a biological mechanism.
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
NOISE_RATES = (0.0, 0.01, 0.03)
TURNOVER_RATES = (0.0, 0.005, 0.01, 0.03)
MEMORY_DECAY = 0.8
INITIAL_FLIP_RATE = 0.15
BASE_SEED = 3120000
CONDITIONS = ("no_memory", "memory_preserved", "memory_reset", "memory_strong")


def make_modular_graph(seed: int, target: np.ndarray) -> np.ndarray:
    rng = np.random.default_rng(seed)
    adjacency = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        candidates = np.delete(np.arange(N), i)
        same = candidates[target[candidates] == target[i]]
        other = candidates[target[candidates] != target[i]]
        within = min(round(K * 0.8), len(same))
        across = K - within
        chosen = list(rng.choice(same, within, replace=False)) if within else []
        if across:
            chosen += list(rng.choice(other, across, replace=False))
        adjacency[i, chosen] = 1
    adjacency = np.maximum(adjacency, adjacency.T)
    np.fill_diagonal(adjacency, 0)
    return adjacency


def run_trial(seed: int, noise: float, turnover: float, condition: str) -> dict:
    rng = np.random.default_rng(seed)
    target = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(target)
    state = target.copy()
    state[rng.random(N) < INITIAL_FLIP_RATE] ^= 1

    disturbances = rng.random((STEPS, N)) < noise
    replacements = rng.random((STEPS, N)) < turnover
    adjacency = make_modular_graph(seed + 777777, target)

    memory_strength = {
        "no_memory": 0.0,
        "memory_preserved": 2.0,
        "memory_reset": 2.0,
        "memory_strong": 4.0,
    }[condition]
    memory = 2 * state.astype(float) - 1
    retention = []

    for step in range(STEPS):
        replaced = replacements[step]
        if replaced.any():
            count = int(replaced.sum())
            state[replaced] = rng.integers(0, 2, size=count)
            # History continuity is the only distinction between these two
            # matched-strength conditions.
            if condition in ("no_memory", "memory_reset", "memory_strong"):
                memory[replaced] = 2 * state[replaced].astype(float) - 1

        state[disturbances[step]] ^= 1
        votes = adjacency @ (2 * state.astype(np.int16) - 1)
        score = votes + memory_strength * memory
        new_state = (score > 0).astype(np.int8)
        ties = score == 0
        new_state[ties] = state[ties]
        state = new_state
        memory = MEMORY_DECAY * memory + (1 - MEMORY_DECAY) * (2 * state.astype(float) - 1)
        retention.append(float(np.mean(state == target)))

    return {
        "seed": seed,
        "noise_rate": noise,
        "turnover_rate": turnover,
        "condition": condition,
        "mean_retention": float(np.mean(retention)),
        "first50_retention": float(np.mean(retention[:50])),
        "last50_retention": float(np.mean(retention[-50:])),
        "final_retention": float(retention[-1]),
        "mean_replacements": int(replacements.sum()),
        "nodes": N,
        "edges": int(adjacency.sum() // 2),
        "steps": STEPS,
        "initial_flip_rate": INITIAL_FLIP_RATE,
        "memory_decay": MEMORY_DECAY,
        "target_used_by_update": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E12_TURNOVER_MEMORY_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()

    rows = [
        run_trial(BASE_SEED + i, noise, turnover, condition)
        for noise in NOISE_RATES
        for turnover in TURNOVER_RATES
        for condition in CONDITIONS
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
        for turnover in TURNOVER_RATES:
            parts = []
            for condition in CONDITIONS:
                vals = [r["mean_retention"] for r in rows
                        if r["noise_rate"] == noise
                        and r["turnover_rate"] == turnover
                        and r["condition"] == condition]
                parts.append(f"{condition}={np.mean(vals):.5f}")
            print(f"noise={noise:.3f}; turnover={turnover:.3f}; " + "; ".join(parts))


if __name__ == "__main__":
    main()
