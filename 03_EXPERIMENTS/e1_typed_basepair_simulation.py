"""E1 — deterministic toy model for typed DNA base-pair relations.

This is a structural toy model, not molecular dynamics and not a biological
energy calculation. It deliberately exposes assumptions so the result can be
reproduced and audited.
"""

from itertools import product

BASES = ("A", "C", "G", "T")
PURINES = {"A", "G"}
PYRIMIDINES = {"C", "T"}

# Canonical Watson-Crick donor/acceptor compatibility is represented only as
# a feature table. The scoring function itself contains no A-T/G-C lookup.
# Values are the conventional counts used by the toy model: A-T = 2, G-C = 3.
H_BOND_FEATURE = {
    ("A", "T"): 2, ("T", "A"): 2,
    ("G", "C"): 3, ("C", "G"): 3,
}

WEIGHTS = {
    "size": 1.0,
    "hbond": 1.0,
    "orientation": 0.0,  # fixed because all candidates use the same antiparallel setup
}


def size_feature(a: str, b: str) -> int:
    return int((a in PURINES and b in PYRIMIDINES) or
               (a in PYRIMIDINES and b in PURINES))


def hbond_feature(a: str, b: str) -> int:
    return H_BOND_FEATURE.get((a, b), 0)


def score(a: str, b: str, weights=WEIGHTS) -> float:
    return (
        weights["size"] * size_feature(a, b)
        + weights["hbond"] * hbond_feature(a, b)
        + weights["orientation"] * 1.0
    )


def rank_pairs(weights=WEIGHTS):
    rows = []
    for a, b in product(BASES, repeat=2):
        rows.append((a + b, size_feature(a, b), hbond_feature(a, b), score(a, b, weights)))
    return sorted(rows, key=lambda row: (-row[3], row[0]))


def run(label, weights=WEIGHTS):
    print(f"\n{label}")
    print("pair size hbond score")
    for pair, size, hbond, value in rank_pairs(weights):
        print(f"{pair:>4} {size:>4} {hbond:>5} {value:>5.1f}")


if __name__ == "__main__":
    run("N3 typed relational toy model")
    run("N1 size-only", {"size": 1.0, "hbond": 0.0, "orientation": 0.0})
    run("N2 hydrogen-bond-only", {"size": 0.0, "hbond": 1.0, "orientation": 0.0})
