#!/usr/bin/env python3
"""Controlled replication-context gate: sequence vs origin/accessibility/timing."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.stats import ttest_rel

SEEDS=30; N=5000
rows=[]
for s in range(SEEDS):
    rng=np.random.default_rng(1000+s); X=rng.normal(size=(N,6)); origin=rng.binomial(1,.25,N); access=rng.normal(size=N); timing=rng.normal(size=N)
    z=1.8*origin+1.2*access-.9*timing+rng.normal(0,.7,N); y=(z>np.median(z)).astype(int); ix=rng.permutation(N); tr=ix[:3500]; te=ix[3500:]
    def auc(a,b):
        m=LogisticRegression(max_iter=1500).fit(a,y[tr]); return roc_auc_score(y[te],m.predict_proba(b)[:,1])
    A=auc(X[tr],X[te]); B=auc(np.c_[X[tr],origin[tr],access[tr],timing[tr]],np.c_[X[te],origin[te],access[te],timing[te]])
    rel=np.c_[origin,access,timing]; C=auc(np.c_[X[tr],rel[tr][rng.permutation(len(tr))]],np.c_[X[te],rel[te]])
    rows.append((A,B,C))
r=np.array(rows); print('mean',r.mean(0),'sd',r.std(0,ddof=1),'paired_t',ttest_rel(r[:,1],r[:,0]))
