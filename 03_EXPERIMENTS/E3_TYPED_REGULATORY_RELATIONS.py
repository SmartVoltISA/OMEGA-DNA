"""E3 controlled typed-regulatory-relation benchmark.

Tests whether an explicit relational feature (cooperative spacing between
TF-binding sites) adds predictive information beyond motif count and GC.
This is a controlled architecture benchmark, not a biological claim.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score

MOTIF = np.array([0,1,2,3,0,1,2,3])

def run(seed: int, n: int = 8000, L: int = 160):
    r=np.random.default_rng(seed); X=r.integers(0,4,(n,L)); W=L-7
    p1=r.integers(0,L-8,n); copies=r.integers(0,3,n)
    for i,p in enumerate(p1): X[i,p:p+8]=MOTIF
    p2=np.minimum(p1+r.integers(10,81,n),L-8)
    for i,p in enumerate(p2):
        if copies[i]>=2: X[i,p:p+8]=MOTIF
    score=np.zeros((n,W),int)
    for j in range(8): score += X[:,j:j+W]==MOTIF[j]
    hit=score==8; hits=hit.sum(1)
    coop=np.zeros(n,int)
    for d in range(1,41): coop += (hit[:,:-d]&hit[:,d:]).sum(1)
    gc=((X==1)|(X==2)).sum(1)
    z=.8*hits+1.5*(coop>0)+r.normal(0,.8,n)
    y=(z>np.median(z)).astype(int)
    base=np.c_[hits,gc]; rel=np.c_[hits,gc,coop]
    idx=r.permutation(n); tr=idx[:int(.7*n)]; te=idx[int(.7*n):]
    m1=LogisticRegression(max_iter=500).fit(base[tr],y[tr])
    m2=LogisticRegression(max_iter=500).fit(rel[tr],y[tr])
    p1=m1.predict_proba(base[te])[:,1]; p2=m2.predict_proba(rel[te])[:,1]
    sh=rel[te].copy(); r.shuffle(sh[:,2]); ps=m2.predict_proba(sh)[:,1]
    return [roc_auc_score(y[te],p1),average_precision_score(y[te],p1),
            roc_auc_score(y[te],p2),average_precision_score(y[te],p2),
            roc_auc_score(y[te],ps),average_precision_score(y[te],ps)]

if __name__=='__main__':
    a=np.array([run(s) for s in range(30)])
    print('mean',a.mean(0)); print('std',a.std(0))
    print('paired AUC relation-vs-baseline',ttest_rel(a[:,2],a[:,0]))
    print('paired AUC shuffled-vs-relation',ttest_rel(a[:,4],a[:,2]))
