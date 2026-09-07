"""E3 — Regulatory network topology gate.

Controlled synthetic benchmark for:
    enhancer -> TF -> promoter/gene -> regulatory network architecture

Compares sequence-only, typed pairwise relation, and full network-topology
representations. The benchmark is deliberately synthetic and does not claim
biological validity of any individual edge.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import ttest_rel
from sklearn.metrics import roc_auc_score, average_precision_score

N_SEEDS = 30
N_ENHANCERS = 100
N_TFS = 35
N_GENES = 50


def one_seed(seed: int):
    rng = np.random.default_rng(seed)

    # Typed regulatory graph: enhancer--TF and TF--gene relations.
    enhancer_tf = (rng.random((N_ENHANCERS, N_TFS)) < 0.12).astype(int)
    tf_gene = (rng.random((N_TFS, N_GENES)) < 0.10).astype(int)

    # Sequence/local state proxies.
    enhancer_state = rng.normal(size=N_ENHANCERS)
    gene_state = rng.normal(size=N_GENES)
    enhancer_pos = rng.integers(0, 100_000_000, N_ENHANCERS)
    gene_pos = rng.integers(0, 100_000_000, N_GENES)
    distance = np.abs(enhancer_pos[:, None] - gene_pos[None, :])
    distance_norm = np.log1p(distance) / np.log(100_000_001)
    compatibility = np.tanh(
        (enhancer_state[:, None] + gene_state[None, :]
         + 0.8 * rng.normal(size=(N_ENHANCERS, N_GENES))) / 2.0
    )

    # Direct chromatin-contact relation.
    contact = (
        (distance < 18_000_000)
        & (rng.random((N_ENHANCERS, N_GENES)) < 0.20)
    ).astype(int)

    # Network topology: number of enhancer -> TF -> gene paths.
    two_hop_paths = enhancer_tf @ tf_gene

    # Synthetic target-generating process. Topology is causal in this declared
    # benchmark; this is intentional and is NOT a claim about real biology.
    sequence_score = 0.9 * compatibility - 0.4 * distance_norm
    latent = (
        sequence_score
        + 0.9 * contact
        + 1.4 * np.log1p(two_hop_paths)
    )
    probability = 1.0 / (1.0 + np.exp(-latent))
    target = (rng.random((N_ENHANCERS, N_GENES)) < probability).astype(int)

    # Fixed 70/30 holdout over enhancer-gene candidate edges.
    order = rng.permutation(N_ENHANCERS * N_GENES)
    test = order[int(0.70 * len(order)):]
    y = target.ravel()[test]

    seq = sequence_score.ravel()[test]
    relation = (sequence_score + 0.9 * contact).ravel()[test]
    graph = (
        sequence_score + 0.9 * contact + 1.4 * np.log1p(two_hop_paths)
    ).ravel()[test]

    # Relation-destruction null: shuffle only topology on the held-out set.
    null_paths = two_hop_paths.ravel()[test].copy()
    rng.shuffle(null_paths)
    graph_null = (
        sequence_score.ravel()[test]
        + 0.9 * contact.ravel()[test]
        + 1.4 * np.log1p(null_paths)
    )

    metrics = []
    for score in (seq, relation, graph, graph_null):
        metrics.append((roc_auc_score(y, score), average_precision_score(y, score)))

    # Network perturbation: remove the highest-degree TF vs a random TF and
    # measure loss of two-hop enhancer->gene paths.
    tf_degree = enhancer_tf.sum(0) + tf_gene.sum(1)
    high_tf = int(np.argmax(tf_degree))
    random_tf = int(rng.integers(N_TFS))
    total_paths = two_hop_paths.sum()

    perturbed_high = enhancer_tf.copy()
    perturbed_high[:, high_tf] = 0
    loss_high = (total_paths - (perturbed_high @ tf_gene).sum()) / total_paths

    perturbed_random = enhancer_tf.copy()
    perturbed_random[:, random_tf] = 0
    loss_random = (total_paths - (perturbed_random @ tf_gene).sum()) / total_paths

    return metrics, loss_high, loss_random


def main():
    rows = []
    perturb = []
    for seed in range(N_SEEDS):
        metrics, loss_high, loss_random = one_seed(seed)
        rows.append([v for pair in metrics for v in pair])
        perturb.append([loss_high, loss_random])

    a = np.asarray(rows)
    p = np.asarray(perturb)
    names = [
        "sequence_only_auc", "sequence_only_ap",
        "relation_auc", "relation_ap",
        "graph_auc", "graph_ap",
        "graph_null_auc", "graph_null_ap",
    ]
    print("metric,mean,std")
    for i, name in enumerate(names):
        print(f"{name},{a[:, i].mean():.9f},{a[:, i].std(ddof=1):.9f}")

    print("paired_graph_vs_relation_auc", ttest_rel(a[:, 4], a[:, 2]))
    print("paired_relation_vs_sequence_auc", ttest_rel(a[:, 2], a[:, 0]))
    print("paired_graph_null_vs_graph_auc", ttest_rel(a[:, 6], a[:, 4]))
    print(
        "perturb_high_degree_mean_std",
        p[:, 0].mean(), p[:, 0].std(ddof=1),
    )
    print(
        "perturb_random_mean_std",
        p[:, 1].mean(), p[:, 1].std(ddof=1),
    )
    print("paired_perturbation", ttest_rel(p[:, 0], p[:, 1]))


if __name__ == "__main__":
    main()
