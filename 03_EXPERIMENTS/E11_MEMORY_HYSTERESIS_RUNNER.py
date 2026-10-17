#!/usr/bin/env python3
"""E11: local memory / hysteresis under state noise.

Abstract binary-network experiment only. Target labels are used only for
initialization and scoring, never by the update rule. This is not a biological
model. The run is exploratory and not preregistered.
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
MEMORY_STRENGTHS = (0.0, 0.5, 1.0, 2.0, 4.0)
MEMORY_DECAY = 0.8
INITIAL_FLIP_RATE = 0.15
SEED_BASE = 2110000


def make_graph(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    adjacency = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        candidates = np.delete(np.arange(N), i)
        adjacency[i, rng.choice(candidates, K, replace=False)] = 1
    adjacency = np.maximum(adjacency, adjacency.T)
    np.fill_diagonal(adjacency, 0)
    return adjacency


def run_trial(seed: int, noise_rate: float, memory_strength: float,
              shuffled_memory: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    target = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(target)
    state = target.copy()
    state[rng.random(N) < INITIAL_FLIP_RATE] ^= 1
    disturbances = rng.random((STEPS, N)) < noise_rate
    adjacency = make_graph(seed + 900000)

    # Memory is a decaying trace of each node's own accepted prior states.
    memory = 2 * state.astype(float) - 1
    if shuffled_memory:
        memory = memory[rng.permutation(N)].copy()

    retention = []
    first_consensus_step = None
    memory_alignment = []
    for step in range(STEPS):
        # External perturbation acts on visible state; memory trace remains.
        state[disturbances[step]] ^= 1
        votes = adjacency @ (2 * state.astype(np.int16) - 1)
        score = votes + memory_strength * memory
        new_state = (score > 0).astype(np.int8)
        ties = score == 0
        new_state[ties] = state[ties]
        state = new_state
        memory = MEMORY_DECAY * memory + (1 - MEMORY_DECAY) * (2 * state.astype(float) - 1)

        retention.append(float(np.mean(state == target)))
        memory_alignment.append(float(np.mean(np.sign(memory) == (2 * target - 1))))
        if first_consensus_step is None and (state.sum() == 0 or state.sum() == N):
            first_consensus_step = step + 1

    return {
        "seed": seed,
        "noise_rate": noise_rate,
        "memory_strength": memory_strength,
        "shuffled_memory_control": shuffled_memory,
        "mean_retention": float(np.mean(retention)),
        "first50_retention": float(np.mean(retention[:50])),
        "last50_retention": float(np.mean(retention[-50:])),
        "final_retention": float(retention[-1]),
        "mean_memory_alignment": float(np.mean(memory_alignment)),
        "first_consensus_step": first_consensus_step,
        "nodes": N,
        "edges": int(adjacency.sum() // 2),
        "steps": STEPS,
        "initial_flip_rate": INITIAL_FLIP_RATE,
        "memory_decay": MEMORY_DECAY,
        "target_labels_used_by_update": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E11_MEMORY_HYSTERESIS_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()

    rows = []
    for noise in NOISE_RATES:
        for strength in MEMORY_STRENGTHS:
            for i in range(args.replicates):
                rows.append(run_trial(SEED_BASE + i, noise, strength, False))
        # Negative control: memory trace initially assigned to the wrong nodes.
        for i in range(args.replicates):
            rows.append(run_trial(SEED_BASE + i, noise, 2.0, True))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {out}")
    for noise in NOISE_RATES:
        for strength in MEMORY_STRENGTHS:
            values = [r["mean_retention"] for r in rows
                      if r["noise_rate"] == noise
                      and r["memory_strength"] == strength
                      and not r["shuffled_memory_control"]]
            print(f"noise={noise:.2f}; memory={strength:.1f}; mean={np.mean(values):.6f}; SD={np.std(values, ddof=1):.6f}")
        values = [r["mean_retention"] for r in rows
                  if r["noise_rate"] == noise and r["shuffled_memory_control"]]
        print(f"noise={noise:.2f}; shuffled_memory_h=2.0; mean={np.mean(values):.6f}; SD={np.std(values, ddof=1):.6f}")


if __name__ == "__main__":
    main()
