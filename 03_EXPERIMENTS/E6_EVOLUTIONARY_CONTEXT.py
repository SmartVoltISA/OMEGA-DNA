#!/usr/bin/env python3
"""Controlled evolutionary-memory gate: conservation/history vs sequence."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.stats import ttest_rel
SEEDS=30; N=5000; out=[]
for s in range(SEEDS):
 rng=np.random.default_rng(3000+s); X=rng.normal(size=(N,8)); cons=rng.beta(2,2,N); freq=rng.beta(2,5,N); lineage=rng.normal(size=N)
 z=1.8*cons-1.1*freq+.8*lineage+rng.normal(0,.8,N); y=(z>np.median(z)).astype(int); ix=rng.permutation(N); tr=ix[:3500]; te=ix[3500:]
 def auc(a,b):
  m=LogisticRegression(max_iter=1500).fit(a,y[tr]); return roc_auc_score(y[te],m.predict_proba(b)[:,1])
 A=auc(X[tr],X[te]); rel=np.c_[cons,freq,lineage]; B=auc(np.c_[X[tr],rel[tr]],np.c_[X[te],rel[te]]); C=auc(np.c_[X[tr],rel[tr][rng.permutation(len(tr))]],np.c_[X[te],rel[te]]); out.append((A,B,C))
r=np.array(out); print(r.mean(0),r.std(0,ddof=1),ttest_rel(r[:,1],r[:,0]))
