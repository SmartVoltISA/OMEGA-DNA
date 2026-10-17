#!/usr/bin/env python3
"""E14 exploratory pilot: abstract form memory vs adjacency exemplar memory.

Requires Python 3.10+, numpy, networkx, scikit-learn, pandas, statsmodels.
The graph families are synthetic; results are not biological evidence.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from statsmodels.stats.proportion import proportion_confint

FAMILIES = ("cycle", "star", "two_cliques")
NOISES = (0.05, 0.15, 0.30, 0.45)
TEST_SIZES = (20, 32, 36, 40)
TRAIN_SIZES = (16, 24, 28)
PER_CLASS_TRAIN = 500
PER_CLASS_TEST = 300
BOOTSTRAPS = 10000

def make_graph(n, family, seed, delete_rate=0.05, add_rate=0.05):
    rng = np.random.default_rng(seed)
    if family == "cycle":
        g = nx.cycle_graph(n)
    elif family == "star":
        g = nx.star_graph(n - 1)
    elif family == "two_cliques":
        k = n // 2
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(nx.complete_graph(k).edges())
        g.add_edges_from((u+k, v+k) for u, v in nx.complete_graph(n-k).edges())
        g.add_edge(k-1, k)
    else:
        raise ValueError(family)
    original_edges = list(g.edges())
    for edge in original_edges:
        if rng.random() < delete_rate:
            g.remove_edge(*edge)
    nonedges = list(nx.non_edges(g))
    n_add = min(len(nonedges), int(round(add_rate * len(original_edges))))
    if n_add:
        chosen = rng.choice(len(nonedges), size=n_add, replace=False)
        g.add_edges_from(nonedges[int(i)] for i in chosen)
    perm = rng.permutation(n)
    return nx.relabel_nodes(g, {i: int(perm[i]) for i in range(n)})

def form_features(g):
    n = g.number_of_nodes()
    deg = np.asarray([d for _, d in g.degree()], dtype=float)
    hist = np.asarray([np.mean(deg == k) for k in range(9)] + [np.mean(deg >= 9)])
    comps = list(nx.connected_components(g))
    cycle_rank = g.number_of_edges() - n + len(comps)
    quantiles = np.quantile(deg, [0, .25, .5, .75, 1]) / max(n-1, 1)
    return np.concatenate([hist, np.asarray([
        nx.density(g), nx.average_clustering(g), nx.transitivity(g),
        max(map(len, comps), default=0)/n, len(comps)/n,
        cycle_rank/n, deg.mean()/max(n-1, 1), deg.std()/max(n-1, 1)
    ]), quantiles])

def adjacency_vector(g, n):
    return nx.to_numpy_array(g, nodelist=list(range(n)), dtype=np.int8)[np.triu_indices(n, 1)]

def wilson(correct, total):
    lo, hi = proportion_confint(int(correct), int(total), method="wilson")
    return float(lo), float(hi)

def build_training():
    xf, yf, xd, yd, xr, yr = [], [], [], [], [], []
    for n in TRAIN_SIZES:
        for ci, family in enumerate(FAMILIES):
            for j in range(PER_CLASS_TRAIN):
                g = make_graph(n, family, 81000000+n*100000+ci*10000+j, .05, .05)
                xf.append(form_features(g)); yf.append(ci)
                gd = make_graph(n, family, 82000000+n*100000+ci*10000+j, .05, .05)
                xd.append([nx.density(gd)]); yd.append(ci)
    for ci, family in enumerate(FAMILIES):
        for j in range(PER_CLASS_TRAIN):
            g = make_graph(20, family, 83000000+ci*10000+j, .05, .05)
            xr.append(adjacency_vector(g, 20)); yr.append(ci)
    abstract = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))
    abstract.fit(np.asarray(xf), np.asarray(yf))
    density = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))
    density.fit(np.asarray(xd), np.asarray(yd))
    episodic = KNeighborsClassifier(n_neighbors=1, metric="hamming")
    episodic.fit(np.asarray(xr), np.asarray(yr))
    return abstract, density, episodic

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="e14_output")
    ap.add_argument("--bootstraps", type=int, default=BOOTSTRAPS)
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    abstract, density, episodic = build_training()
    rows = []
    for noise in NOISES:
        for n in TEST_SIZES:
            for ci, family in enumerate(FAMILIES):
                for j in range(PER_CLASS_TEST):
                    seed = 84000000 + int(noise*1000)*1000000 + n*100000 + ci*10000 + j
                    g = make_graph(n, family, seed, noise, noise)
                    fa = int(abstract.predict(np.asarray([form_features(g)]))[0])
                    fd = int(density.predict(np.asarray([[nx.density(g)]]))[0])
                    fe = int(episodic.predict(np.asarray([adjacency_vector(g, 20)]))[0]) if n == 20 else None
                    rows.append({"noise": noise, "n": n, "family": family, "replicate": j,
                                 "true": ci, "abstract_pred": fa, "density_pred": fd,
                                 "episodic_pred": fe})
    raw = pd.DataFrame(rows)
    raw.to_csv(out / "E14_ABSTRACTION_MEMORY_RAW.csv", index=False)
    rng = np.random.default_rng(314159)
    summaries = []
    for (noise, n), group in raw.groupby(["noise", "n"], sort=True):
        row = {"noise": float(noise), "n": int(n), "N": len(group)}
        correct_arrays = {}
        for model in ("abstract", "density") + (("episodic",) if n == 20 else ()):
            correct = (group[f"{model}_pred"] == group["true"]).to_numpy()
            count = int(correct.sum()); lo, hi = wilson(count, len(group))
            row[f"{model}_accuracy"] = count/len(group)
            row[f"{model}_ci_low"] = lo; row[f"{model}_ci_high"] = hi
            correct_arrays[model] = correct.astype(float)
        diff = correct_arrays["abstract"] - correct_arrays["density"]
        boot = np.mean(rng.choice(diff, size=(args.bootstraps, len(diff)), replace=True), axis=1)
        row["abstract_minus_density"] = float(diff.mean())
        row["abstract_minus_density_ci_low"], row["abstract_minus_density_ci_high"] = map(float, np.quantile(boot, [.025, .975]))
        if n == 20:
            diff2 = correct_arrays["abstract"] - correct_arrays["episodic"]
            boot2 = np.mean(rng.choice(diff2, size=(args.bootstraps, len(diff2)), replace=True), axis=1)
            row["abstract_minus_episodic"] = float(diff2.mean())
            row["abstract_minus_episodic_ci_low"], row["abstract_minus_episodic_ci_high"] = map(float, np.quantile(boot2, [.025, .975]))
        summaries.append(row)
    pd.DataFrame(summaries).to_csv(out / "E14_ABSTRACTION_MEMORY_SUMMARY.csv", index=False)
    with open(out / "E14_ABSTRACTION_MEMORY_SUMMARY.json", "w", encoding="utf-8") as f:
        json.dump({"protocol": {"train_sizes": TRAIN_SIZES, "test_sizes": TEST_SIZES,
            "noise_levels": NOISES, "per_class_train": PER_CLASS_TRAIN,
            "per_class_test": PER_CLASS_TEST, "bootstraps": args.bootstraps},
            "summary": summaries}, f, ensure_ascii=False, indent=2)
    print(pd.DataFrame(summaries).to_string(index=False))

if __name__ == "__main__":
    main()
