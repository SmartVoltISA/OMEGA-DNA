"""OMEGA-DNA E4: regulatory network -> cellular state -> feedback.
Controlled synthetic benchmark; not a biological claim.
"""
import numpy as np
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score


def state_run(seed, n_tf=20, n_gene=100, T=12):
    rng = np.random.default_rng(seed)
    A = (rng.random((n_gene, n_tf)) < 0.08) * rng.choice([-1, 1], size=(n_gene, n_tf))
    A = A.astype(float)
    tf = np.tanh(rng.normal(size=n_tf))
    gene = np.tanh(rng.normal(size=n_gene))
    rows, targets = [], []
    for _ in range(T):
        drive = A @ tf + 0.35 * gene + 0.25 * rng.normal(size=n_gene)
        new = np.tanh(0.55 * gene + 0.75 * drive)
        rows.append((gene.copy(), tf.copy(), A.copy()))
        targets.append((new > 0).astype(int))
        gene = new
        tf = np.tanh(0.7 * tf + 0.3 * rng.normal(size=n_tf))

    def feat(item, kind):
        g, t, a = item
        if kind == 'sequence_state':
            return g[:, None]
        msg = (a @ t)[:, None]
        if kind == 'relational_state':
            return np.hstack([g[:, None], msg])
        return np.hstack([g[:, None], msg, np.sum(np.abs(a), axis=1)[:, None], (a @ np.tanh(t))[:, None]])

    aucs, aps = [], []
    for kind in ['sequence_state', 'relational_state', 'full_state']:
        Xtr = np.vstack([feat(rows[t], kind) for t in range(8)])
        ytr = np.concatenate(targets[:8])
        Xte = np.vstack([feat(rows[t], kind) for t in range(8, 12)])
        yte = np.concatenate(targets[8:12])
        model = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
        p = model.predict_proba(Xte)[:, 1]
        aucs.append(roc_auc_score(yte, p)); aps.append(average_precision_score(yte, p))

    # Feedback-control gate: compare error before and after one regulatory correction.
    tf = np.tanh(rng.normal(size=n_tf)); no_fb = []; fb = []
    for _ in range(15):
        target = np.tanh(rng.normal(size=n_gene))
        pred = np.tanh(A @ tf)
        no_fb.append(np.mean((target - pred) ** 2))
        grad = A.T @ (target - pred) / n_gene
        tf = np.tanh(tf + 0.15 * grad)
        pred2 = np.tanh(A @ tf)
        fb.append(np.mean((target - pred2) ** 2))
    return aucs + aps + [float(np.mean(no_fb)), float(np.mean(fb))]


if __name__ == '__main__':
    R = np.array([state_run(s) for s in range(50)])
    mean, sd = R.mean(axis=0), R.std(axis=0, ddof=1)
    print('means', mean); print('sd', sd)
    print('rel-vs-seq', ttest_rel(R[:,1], R[:,0]))
    print('full-vs-seq', ttest_rel(R[:,2], R[:,0]))
    print('feedback', ttest_rel(R[:,4], R[:,3]))
