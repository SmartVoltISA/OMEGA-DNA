#!/usr/bin/env python3
"""Controlled repair-context gate: damage + chromatin context vs sequence."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.stats import ttest_rel
SEEDS=30; N=5000; out=[]
for s in range(SEEDS):
 rng=np.random.default_rng(2000+s); X=rng.normal(size=(N,8)); damage=rng.binomial(1,.35,N); chrom=rng.normal(size=N); access=rng.normal(size=N)
 z=1.7*damage+1.4*access+.9*chrom+rng.normal(0,1,N); y=(z>np.median(z)).astype(int); ix=rng.permutation(N); tr=ix[:3500]; te=ix[3500:]
 def auc(a,b):
  m=LogisticRegression(max_iter=1500).fit(a,y[tr]); return roc_auc_score(y[te],m.predict_proba(b)[:,1])
 A=auc(X[tr],X[te]); rel=np.c_[damage,chrom,access]; B=auc(np.c_[X[tr],rel[tr]],np.c_[X[te],rel[te]]); C=auc(np.c_[X[tr],rel[tr][rng.permutation(len(tr))]],np.c_[X[te],rel[te]]); out.append((A,B,C))
r=np.array(out); print(r.mean(0),r.std(0,ddof=1),ttest_rel(r[:,1],r[:,0]))
