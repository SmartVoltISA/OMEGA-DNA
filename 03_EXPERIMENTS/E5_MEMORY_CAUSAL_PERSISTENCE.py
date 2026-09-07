"""OMEGA-DNA E5: memory, persistence and causal intervention benchmark.
Synthetic controlled benchmark only; no biological claim.
"""
import numpy as np
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

SEEDS = 50
N = 4000
R = 16
G = 60

def run(seed):
    r = np.random.default_rng(seed)
    W = r.normal(0, .5, (G, R)) * (r.random((G, R)) < .15)
    rows = []
    for _ in range(N):
        previous_exposure = int(r.random() < .5)
        x0 = r.normal(0, .15, R)
        pulse = r.normal(0, 1, R)
        pulse[:3] += 2.0 * previous_exposure
        memory = previous_exposure + .15 * r.normal()
        msg = W @ (x0 + .25 * pulse)
        latent = .55 * memory + .25 * np.tanh(msg / 2).mean() + .25 * r.normal()
        y = int(latent > 0)
        seq = np.r_[x0[:6], np.mean(x0), np.std(x0)]
        rel = np.r_[seq, np.tanh(msg[:12] / 2)]
        mem = np.r_[rel, memory]
        rows.append((seq, rel, mem, y))
    Xs = np.array([x[0] for x in rows]); Xr = np.array([x[1] for x in rows]); Xm = np.array([x[2] for x in rows])
    y = np.array([x[3] for x in rows])
    cut = int(.7 * N)
    def auc(X):
        m = LogisticRegression(max_iter=500, C=.3).fit(X[:cut], y[:cut])
        return roc_auc_score(y[cut:], m.predict_proba(X[cut:])[:,1])
    seq_auc, rel_auc, mem_auc = auc(Xs), auc(Xr), auc(Xm)
    j = np.argmax(np.abs(W).sum(axis=0))
    x = r.normal(0, .15, R); pulse2 = r.normal(0, 1, R); pulse2[:3] += 2
    msg = W @ (x + .25*pulse2)
    msg_ko = msg - W[:,j]*(x[j] + .25*pulse2[j])
    causal = np.mean(np.abs(np.tanh(msg/2)-np.tanh(msg_ko/2)))
    jr = r.integers(R)
    msg_r = msg - W[:,jr]*(x[jr] + .25*pulse2[jr])
    causal_random = np.mean(np.abs(np.tanh(msg/2)-np.tanh(msg_r/2)))
    return seq_auc, rel_auc, mem_auc, causal, causal_random

if __name__ == '__main__':
    a = np.array([run(3000+s) for s in range(SEEDS)])
    for name, col in [('sequence',0),('relation',1),('memory',2),('causal_top',3),('causal_random',4)]:
        print(name, a[:,col].mean(), a[:,col].std(ddof=1))
    print('relation-vs-sequence', ttest_rel(a[:,1], a[:,0]))
    print('memory-vs-sequence', ttest_rel(a[:,2], a[:,0]))
    print('causal-top-vs-random', ttest_rel(a[:,3], a[:,4]))
