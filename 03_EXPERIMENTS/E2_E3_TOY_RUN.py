"""Reproducible E2/E3 toy experiments for OMEGA-DNA.

These are architectural demonstrations, not molecular simulations.
"""
from random import Random

BASES = "ACGT"
COMP = str.maketrans("ACGT", "TGCA")

def complement(s):
    return s.translate(COMP)[::-1]

def mutate(s, p, rng):
    out = []
    for x in s:
        out.append(rng.choice([z for z in BASES if z != x]) if rng.random() < p else x)
    return "".join(out)

def e2(length, p=0.001, trials=50000, seed=11):
    rng = Random(seed)
    detected = damaged = 0
    for _ in range(trials):
        s = "".join(rng.choice(BASES) for _ in range(length))
        a = mutate(s, p, rng)
        b = complement(mutate(s, p, rng))
        mismatch = any(x != y for x, y in zip(a, complement(b)))
        damaged += (a != s or b != complement(s))
        detected += mismatch
    return damaged / trials, detected / trials

def e3(trials=100000, steps=100, damage=0.002, detect=0.95,
       correct=0.98, seed=7):
    rng = Random(seed)
    no_feedback = detection_only = feedback = 0
    for _ in range(trials):
        errors = sum(rng.random() < damage for _ in range(steps))
        no_feedback += errors
        detection_only += errors
        residual = 0
        for _ in range(errors):
            if rng.random() < detect:
                if rng.random() >= correct:
                    residual += 1
            else:
                residual += 1
        feedback += residual
    return no_feedback/trials, detection_only/trials, feedback/trials

if __name__ == "__main__":
    for length in (10, 100, 1000):
        print("E2", length, e2(length))
    print("E3", e3())
