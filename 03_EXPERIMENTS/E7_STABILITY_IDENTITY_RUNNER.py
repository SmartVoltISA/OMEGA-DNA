#!/usr/bin/env python3
"""Reproducible abstract-network experiment for OMEGA-DNA stability research.

This is a toy dynamical systems model, not a biological model and not a model
for constructing mirror organisms. It tests whether topology aligned with a
declared target state and explicit restoring feedback affect state retention.
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
PERTURBATION_RATE = 0.03
TURNOVER_RATE = 0.01
INITIAL_FLIP_RATE = 0.15
FEEDBACK_STRENGTH = 1.5
SEED_BASE = 1000


def make_graph(n: int, k: int, targets: np.ndarray, mode: str,
               rng: np.random.Generator) -> np.ndarray:
    a = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        candidates = np.arange(n)
        candidates = candidates[candidates != i]
        if mode == "modular":
            same = candidates[targets[candidates] == targets[i]]
            other = candidates[targets[candidates] != targets[i]]
            within = min(int(round(k * 0.8)), len(same))
            across = k - within
            chosen = list(rng.choice(same, within, replace=False)) if within else []
            chosen_set = set(chosen)
            remaining = np.array([x for x in other if x not in chosen_set], dtype=int)
            if across and len(remaining):
                chosen += list(rng.choice(remaining, min(across, len(remaining)), replace=False))
            if len(chosen) < k:
                chosen_set = set(chosen)
                remaining = np.array([x for x in candidates if x not in chosen_set], dtype=int)
                chosen += list(rng.choice(remaining, min(k - len(chosen), len(remaining)), replace=False))
        else:
            chosen = list(rng.choice(candidates, k, replace=False))
        a[i, chosen] = 1
    a = np.maximum(a, a.T)
    np.fill_diagonal(a, 0)
    return a


def run_trial(seed: int, model: str, feedback_strength: float = FEEDBACK_STRENGTH) -> dict:
    rng = np.random.default_rng(seed)
    targets = np.array([0] * (N // 2) + [1] * (N - N // 2), dtype=np.int8)
    rng.shuffle(targets)

    graph_mode = "modular" if model in ("modular_static", "modular_feedback", "shuffled_feedback") else "random"
    adjacency = make_graph(N, K, targets, graph_mode, rng)

    # Negative control: shuffle target labels after constructing the modular graph.
    # Graph statistics remain similar, but topology is no longer aligned to target classes.
    if model == "shuffled_feedback":
        targets = targets.copy()
        rng.shuffle(targets)

    state = targets.copy()
    flip = rng.random(N) < INITIAL_FLIP_RATE
    state[flip] = 1 - state[flip]
    retention = []

    use_feedback = model in ("modular_feedback", "shuffled_feedback")
    for _ in range(STEPS):
        flip = rng.random(N) < PERTURBATION_RATE
        state[flip] = 1 - state[flip]

        # Small edge turnover models structural change, not any specific biology.
        for i in range(N):
            if rng.random() < TURNOVER_RATE:
                old = np.flatnonzero(adjacency[i])
                if len(old):
                    j = int(rng.choice(old))
                    adjacency[i, j] = adjacency[j, i] = 0
                candidates = np.arange(N)
                candidates = candidates[(candidates != i) & (adjacency[i] == 0)]
                if len(candidates):
                    j = int(rng.choice(candidates))
                    adjacency[i, j] = adjacency[j, i] = 1

        votes = adjacency @ (2 * state.astype(float) - 1)
        score = votes
        if use_feedback:
            score = score + feedback_strength * (2 * targets - 1)

        new_state = (score > 0).astype(np.int8)
        ties = score == 0
        new_state[ties] = state[ties]
        state = new_state
        retention.append(float(np.mean(state == targets)))

    return {
        "seed": seed,
        "model": model,
        "mean_retention": float(np.mean(retention)),
        "first50_retention": float(np.mean(retention[:50])),
        "last50_retention": float(np.mean(retention[-50:])),
        "feedback_strength": feedback_strength if use_feedback else 0.0,
        "steps": STEPS,
        "n_nodes": N,
        "initial_flip_rate": INITIAL_FLIP_RATE,
        "perturbation_rate": PERTURBATION_RATE,
        "turnover_rate": TURNOVER_RATE,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="03_EXPERIMENTS/E7_STABILITY_IDENTITY_RAW.csv")
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    args = parser.parse_args()

    models = ("random_static", "modular_static", "modular_feedback", "shuffled_feedback")
    rows = []
    for model in models:
        for replicate in range(args.replicates):
            rows.append(run_trial(SEED_BASE + replicate, model))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {out}")
    for model in models:
        subset = [r for r in rows if r["model"] == model]
        print(
            f"{model}: mean={np.mean([r['mean_retention'] for r in subset]):.4f}; "
            f"SD={np.std([r['mean_retention'] for r in subset], ddof=1):.4f}; "
            f"last50={np.mean([r['last50_retention'] for r in subset]):.4f}"
        )


if __name__ == "__main__":
    main()
