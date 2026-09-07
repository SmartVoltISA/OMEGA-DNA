#!/usr/bin/env python3
"""OMEGA-DNA self-stress test.

Tests whether relational features help only when they contain information
absent from sequence, and whether shuffled relations collapse. 30 seeds,
5,000 samples/seed, 70/30 holdout.
"""
import numpy as np
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def auc(X, y, tr, te):
    model = LogisticRegression(max_iter=1500).fit(X[tr], y[tr])
    return roc_auc_score(y[te], model.predict_proba(X[te])[:, 1])

def run(seed, n=5000):
    rng = np.random.default_rng(seed)
    seq = rng.normal(size=(n, 8)); rel = rng.normal(size=(n, 6))
    y_seq_sufficient = (seq[:,0] + .8*seq[:,1] + .2*rng.normal(size=n) > 0).astype(int)
    y_relation_needed = (.1*seq[:,0] + 1.2*rel[:,0] + .9*rel[:,1] + .3*rng.normal(size=n) > 0).astype(int)
    rel_duplicate = np.c_[seq[:,:2], rel[:,2:]]
    y_duplicate = (seq[:,0] + .7*seq[:,1] + .2*rng.normal(size=n) > 0).astype(int)
    y_causal_relation = (1.4*rel[:,2] + .2*rng.normal(size=n) > 0).astype(int)
    tr, te = np.arange(int(.7*n)), np.arange(int(.7*n), n)
    out={}
    for name,y,Xb,Xr in [
        ('sequence_sufficient',y_seq_sufficient,seq,np.c_[seq,rel]),
        ('relation_needed',y_relation_needed,seq,np.c_[seq,rel]),
        ('relation_redundant',y_duplicate,seq,np.c_[seq,rel_duplicate]),
        ('causal_relation',y_causal_relation,seq,np.c_[seq,rel])]:
        out[name]={'sequence':auc(Xb,y,tr,te),'relational':auc(Xr,y,tr,te)}
    out['relation_needed']['shuffled']=auc(np.c_[seq,rel[rng.permutation(n)]],y_relation_needed,tr,te)
    out['causal_relation']['shuffled']=auc(np.c_[seq,rel[rng.permutation(n)]],y_causal_relation,tr,te)
    return out

if __name__ == '__main__':
    rows=[run(1000+i) for i in range(30)]
    for task in rows[0]:
        print(task)
        for k in rows[0][task]:
            x=np.array([r[task][k] for r in rows]); print(f'  {k}: {x.mean():.6f} ± {x.std(ddof=1):.6f}')
        a=np.array([r[task]['relational'] for r in rows]); b=np.array([r[task]['sequence'] for r in rows])
        z=ttest_rel(a,b); print(f'  paired_t: {z.statistic:.6f}; p={z.pvalue:.6e}')
