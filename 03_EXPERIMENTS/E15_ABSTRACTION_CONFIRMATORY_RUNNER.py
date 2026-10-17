#!/usr/bin/env python3
"""E15 confirmatory synthetic test of higher-order graph-form descriptors.

Protocol: E15_ABSTRACTION_CONFIRMATORY_PROTOCOL.md.
Requires Python 3.10+, numpy, networkx, pandas, scikit-learn, statsmodels.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from statsmodels.stats.proportion import proportion_confint

FAMILIES = ("cycle", "path", "cycle_chord", "two_cycles")
TRAIN_SIZES = (16, 20, 24)
TEST_SIZES = (28, 32, 36)
NOISES = (0.02, 0.05, 0.10, 0.20)
N_TRAIN = 400
N_TEST = 250
N_BOOT = 10000

def make_graph(n, family, seed, deletion, addition):
    rng = np.random.default_rng(seed)
    if family == "cycle":
        g = nx.cycle_graph(n)
    elif family == "path":
        g = nx.path_graph(n)
    elif family == "cycle_chord":
        g = nx.cycle_graph(n)
        g.add_edge(0, n//2)
    elif family == "two_cycles":
        if n % 2:
            raise ValueError("two_cycles requires even n")
        k = n//2
        g = nx.disjoint_union(nx.cycle_graph(k), nx.cycle_graph(k))
    else:
        raise ValueError(family)
    original = list(g.edges())
    for e in original:
        if rng.random() < deletion:
            g.remove_edge(*e)
    nonedges = list(nx.non_edges(g))
    # Bernoulli additions preserve the intended expected noise rate across sizes.
    # Rounding to an integer would give zero additions for small training graphs
    # but one or more additions for larger test graphs, causing size-dependent shift.
    add_probability = min(1.0, addition * len(original) / max(len(nonedges), 1))
    if nonedges and add_probability > 0:
        chosen = [e for e in nonedges if rng.random() < add_probability]
        g.add_edges_from(chosen)
    perm = rng.permutation(n)
    return nx.relabel_nodes(g, {i: int(perm[i]) for i in range(n)})

def local_features(g):
    n = g.number_of_nodes()
    deg = np.asarray([d for _, d in g.degree()], dtype=float)
    hist = np.asarray([np.mean(deg == k) for k in range(9)] + [np.mean(deg >= 9)])
    quantiles = np.quantile(deg, [0, .25, .5, .75, 1]) / max(n-1, 1)
    return np.concatenate([hist, quantiles])

def form_features(g):
    n = g.number_of_nodes()
    comps = list(nx.connected_components(g))
    local = local_features(g)
    cycle_rank = g.number_of_edges() - n + len(comps)
    high = np.asarray([
        nx.density(g), nx.average_clustering(g), nx.transitivity(g),
        max(map(len, comps), default=0)/n, len(comps)/n, cycle_rank/n
    ])
    return np.concatenate([local, high])

def adjacency_vector(g, n):
    return nx.to_numpy_array(g, nodelist=list(range(n)), dtype=np.int8)[np.triu_indices(n, 1)]

def wilson(correct, total):
    lo, hi = proportion_confint(int(correct), int(total), method="wilson")
    return float(lo), float(hi)

def train_models():
    xl, xf, xd, y = [], [], [], []
    for n in TRAIN_SIZES:
        for ci, fam in enumerate(FAMILIES):
            for j in range(N_TRAIN):
                seed = 151000000 + n*100000 + ci*10000 + j
                g = make_graph(n, fam, seed, .02, .02)
                xl.append(local_features(g)); xf.append(form_features(g))
                xd.append([nx.density(g)]); y.append(ci)
    local = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)).fit(xl, y)
    form = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)).fit(xf, y)
    density = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)).fit(xd, y)
    xa, ya = [], []
    for ci, fam in enumerate(FAMILIES):
        for j in range(N_TRAIN):
            g = make_graph(28, fam, 152000000 + ci*10000 + j, .02, .02)
            xa.append(adjacency_vector(g, 28)); ya.append(ci)
    episodic = KNeighborsClassifier(n_neighbors=1, metric="hamming").fit(xa, ya)
    return local, form, density, episodic

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="e15_output")
    ap.add_argument("--bootstraps", type=int, default=N_BOOT)
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    local, form, density, episodic = train_models()
    rows = []
    for noise in NOISES:
        for n in TEST_SIZES:
            for ci, fam in enumerate(FAMILIES):
                for j in range(N_TEST):
                    seed = 153000000 + int(noise*1000)*1000000 + n*100000 + ci*10000 + j
                    g = make_graph(n, fam, seed, noise, noise)
                    rows.append({
                        "noise": noise, "n": n, "family": fam, "replicate": j, "true": ci,
                        "local_pred": int(local.predict([local_features(g)])[0]),
                        "form_pred": int(form.predict([form_features(g)])[0]),
                        "density_pred": int(density.predict([[nx.density(g)]])[0]),
                        "episodic_pred": int(episodic.predict([adjacency_vector(g, 28)])[0]) if n == 28 else None
                    })
    raw = pd.DataFrame(rows)
    raw.to_csv(out / "E15_ABSTRACTION_CONFIRMATORY_RAW.csv", index=False)
    rng = np.random.default_rng(271828)
    summary = []
    for (noise, n), group in raw.groupby(["noise", "n"], sort=True):
        row = {"noise": float(noise), "n": int(n), "N": len(group)}
        correct = {}
        models = ("local", "form", "density") + (("episodic",) if n == 28 else ())
        for model in models:
            ok = (group[f"{model}_pred"] == group["true"]).to_numpy()
            count = int(ok.sum()); lo, hi = wilson(count, len(group))
            row[f"{model}_accuracy"] = count/len(group)
            row[f"{model}_ci_low"] = lo; row[f"{model}_ci_high"] = hi
            correct[model] = ok.astype(float)
        for other in ("local", "density"):
            diff = correct["form"] - correct[other]
            boot = np.mean(rng.choice(diff, size=(args.bootstraps, len(diff)), replace=True), axis=1)
            row[f"form_minus_{other}"] = float(diff.mean())
            row[f"form_minus_{other}_ci_low"], row[f"form_minus_{other}_ci_high"] = map(float, np.quantile(boot, [.025, .975]))
        if n == 28:
            diff = correct["form"] - correct["episodic"]
            boot = np.mean(rng.choice(diff, size=(args.bootstraps, len(diff)), replace=True), axis=1)
            row["form_minus_episodic"] = float(diff.mean())
            row["form_minus_episodic_ci_low"], row["form_minus_episodic_ci_high"] = map(float, np.quantile(boot, [.025, .975]))
        summary.append(row)
    pd.DataFrame(summary).to_csv(out / "E15_ABSTRACTION_CONFIRMATORY_SUMMARY.csv", index=False)
    with open(out / "E15_ABSTRACTION_CONFIRMATORY_SUMMARY.json", "w", encoding="utf-8") as f:
        json.dump({"protocol": {"train_sizes": TRAIN_SIZES, "test_sizes": TEST_SIZES,
            "noise_levels": NOISES, "n_train_per_class_per_size": N_TRAIN,
            "n_test_per_class_per_condition": N_TEST, "bootstraps": args.bootstraps},
            "summary": summary}, f, ensure_ascii=False, indent=2)
    print(pd.DataFrame(summary).to_string(index=False))

if __name__ == "__main__":
    main()
