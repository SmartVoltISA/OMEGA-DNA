"""OMEGA-DNA relational-complementarity test suite.

All experiments are controlled synthetic tests. They do NOT claim to model
molecular biology quantitatively. Their purpose is to test whether the OMEGA
representation can carry information that disappears under sequence-only,
untyped, static, or shuffled-relation baselines.

Seed: 20260907
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

SEED = 20260907


def e2_complementarity(n=50_000, lengths=(10, 100, 1000), p=0.001, seed=11):
    rng = np.random.default_rng(seed)
    comp = np.array([1, 0, 3, 2])  # A<->T, C<->G
    rows = []
    for L in lengths:
        s = rng.integers(0, 4, (n, L))
        c = comp[s[:, ::-1]]
        s2, c2 = s.copy(), c.copy()
        m1 = rng.random((n, L)) < p
        m2 = rng.random((n, L)) < p
        s2[m1] = rng.integers(0, 4, m1.sum())
        c2[m2] = rng.integers(0, 4, m2.sum())
        damaged = (s2 != s).any(1) | (c2 != c).any(1)
        detected = (s2 != comp[c2[:, ::-1]]).any(1)
        rows.append({"length": L, "damage_rate": damaged.mean(),
                     "detected_rate": detected.mean(),
                     "false_detect_rate": (detected & ~damaged).mean()})
    return pd.DataFrame(rows)


def e3_feedback(n=100_000, steps=100, damage=0.002,
                 detect=0.95, correct=0.98, seed=7):
    rng = np.random.default_rng(seed)
    out = {}
    for mode in ("none", "detect_only", "feedback"):
        errors = np.zeros(n, dtype=np.int16)
        for _ in range(steps):
            errors += rng.random(n) < damage
            if mode != "none":
                detected = (errors > 0) & (rng.random(n) < detect)
                if mode == "feedback":
                    corrected = detected & (rng.random(n) < correct)
                    errors[corrected] -= 1
        out[mode] = float(errors.mean())
    return out


def e4_typed_relation(seed=21, n=10_000, nodes=12):
    rng = np.random.default_rng(seed)
    typed, untyped, y = [], [], []
    for i in range(n):
        cls = i % 2
        edge_types = rng.integers(0, 2, nodes)
        if edge_types.sum() % 2 != cls:
            edge_types[0] ^= 1
        # Relation-aware invariant: parity/product around the closed relation.
        signed_product = np.prod(1 - 2 * edge_types)
        transitions = np.sum(edge_types != np.roll(edge_types, 1))
        typed.append([signed_product, transitions, edge_types.sum()])
        # Topology is identical for both classes; untyped representation sees no label signal.
        untyped.append([nodes])
        y.append(cls)
    y = np.asarray(y)
    typed_acc = LogisticRegression(max_iter=500).fit(typed, y).score(typed, y)
    untyped_acc = LogisticRegression(max_iter=500).fit(untyped, y).score(untyped, y)
    return {"typed_accuracy": float(typed_acc), "untyped_accuracy": float(untyped_acc)}


def e5_dynamic_memory(seed=33, n=20_000, T=20):
    rng = np.random.default_rng(seed)
    static, dynamic, y = [], [], []
    for _ in range(n):
        state = rng.integers(0, 2)
        history = [state]
        for _ in range(1, T):
            if rng.random() < 0.12:
                state = 1 - state
            history.append(state)
        h = np.asarray(history)
        static.append([h[-1]])
        dynamic.append([h.mean(), np.sum(h[1:] != h[:-1]), h[-5:].mean(), np.sum(h == 1)])
        y.append(int(h.mean() > 0.5))
    y = np.asarray(y)
    a = LogisticRegression(max_iter=500).fit(static, y).score(static, y)
    b = LogisticRegression(max_iter=500).fit(dynamic, y).score(dynamic, y)
    return {"static_accuracy": float(a), "dynamic_accuracy": float(b)}


def e6_context_relation(seed=44, n=20_000):
    rng = np.random.default_rng(seed)
    seq, rel, y = [], [], []
    for _ in range(n):
        motif = rng.integers(0, 2)
        connected = rng.integers(0, 2)
        seq.append([motif, motif, motif + motif])
        rel.append([motif, connected, motif * connected])
        y.append(connected ^ motif)
    y = np.asarray(y)
    seq_acc = LogisticRegression(max_iter=500).fit(seq, y).score(seq, y)
    rel_acc = LogisticRegression(max_iter=500).fit(rel, y).score(rel, y)
    return {"sequence_only_accuracy": float(seq_acc),
            "relation_aware_accuracy": float(rel_acc)}


def e7_ablation(seed=55, n=10_000):
    rng = np.random.default_rng(seed)
    s = rng.integers(0, 4, (n, 12))
    seq_signal = ((s == 1).mean(1) > 0.25).astype(int)
    edges = rng.integers(0, 2, (n, 12))
    parity = edges.sum(1) % 2
    state = rng.integers(0, 2, n)
    y = (seq_signal ^ parity ^ state).astype(int)
    tr, te = train_test_split(np.arange(n), test_size=.30,
                              random_state=seed, stratify=y)
    seq = seq_signal[:, None]
    rel = np.column_stack([parity, state])
    combined = np.column_stack([seq_signal, parity, state,
                                 seq_signal * parity,
                                 seq_signal * state,
                                 parity * state,
                                 seq_signal * parity * state])
    shuffled = rel.copy()
    shuffled[tr] = rng.permutation(shuffled[tr])

    def score(x):
        m = LogisticRegression(max_iter=500).fit(x[tr], y[tr])
        return roc_auc_score(y[te], m.predict_proba(x[te])[:, 1])

    return {
        "sequence_only_auc": float(score(seq)),
        "relations_only_auc": float(score(rel)),
        "combined_auc": float(score(combined)),
        "shuffled_relation_null_auc": float(score(np.column_stack([seq, shuffled])))
    }


def e7_repeated(seed0=100, repeats=30):
    rows = [e7_ablation(seed=seed0+i) for i in range(repeats)]
    df = pd.DataFrame(rows)
    t_combined = ttest_rel(df.combined_auc, df.sequence_only_auc)
    t_null = ttest_rel(df.shuffled_relation_null_auc, df.sequence_only_auc)
    return {
        "mean": df.mean().to_dict(),
        "std": df.std(ddof=1).to_dict(),
        "paired_t_combined_vs_sequence": {"t": float(t_combined.statistic), "p": float(t_combined.pvalue)},
        "paired_t_null_vs_sequence": {"t": float(t_null.statistic), "p": float(t_null.pvalue)}
    }


def e8_invariance(seed=77, n=10_000, nodes=20):
    rng = np.random.default_rng(seed)
    typed_errors, positional_errors = [], []
    for _ in range(n):
        e = rng.integers(0, 2, nodes)
        perm = rng.permutation(nodes)
        ep = e[perm]
        typed_errors.append((e.sum() % 2) != (ep.sum() % 2))
        positional_errors.append(e[0] != ep[0])
    return {"typed_invariant_error_rate": float(np.mean(typed_errors)),
            "positional_feature_error_rate": float(np.mean(positional_errors))}


def main():
    results = {
        "E2_complementarity": e2_complementarity().to_dict(orient="records"),
        "E3_feedback": e3_feedback(),
        "E4_typed_relation": e4_typed_relation(),
        "E5_dynamic_memory": e5_dynamic_memory(),
        "E6_context_relation": e6_context_relation(),
        "E7_ablation": e7_ablation(),
        "E7_repeated": e7_repeated(),
        "E8_invariance": e8_invariance(),
    }
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
