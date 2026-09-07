"""Controlled enhancer-promoter relation benchmark.

Tests whether an explicit long-range relation channel adds predictive
information beyond local sequence-derived features. Synthetic only.
"""
import numpy as np
from scipy.stats import ttest_rel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score

N=12000; SEEDS=30

def run(seed):
    r=np.random.default_rng(seed)
    e=r.integers(0,2,N); p=r.integers(0,2,N)
    compat=(e==p).astype(float)
    distance=r.integers(1,1001,N)
    loop=(r.random(N)<(0.15+0.55*compat*np.exp(-distance/600))).astype(int)
    prob=1/(1+np.exp(-(-2+0.9*e+0.7*p+0.5*compat+1.8*loop)))
    y=(r.random(N)<prob).astype(int)
    idx=r.permutation(N); tr=idx[:8400]; te=idx[8400:]
    xs=np.c_[e,p,compat]
    xr=np.c_[e,p,compat,loop,np.log1p(distance)]
    m1=LogisticRegression(max_iter=1000).fit(xs[tr],y[tr])
    m2=LogisticRegression(max_iter=1000).fit(xr[tr],y[tr])
    sh=xr[te].copy(); sh[:,3]=r.permutation(sh[:,3])
    ps=m1.predict_proba(xs[te])[:,1]
    pr=m2.predict_proba(xr[te])[:,1]
    pn=m2.predict_proba(sh)[:,1]
    return [roc_auc_score(y[te],ps),average_precision_score(y[te],ps),
            roc_auc_score(y[te],pr),average_precision_score(y[te],pr),
            roc_auc_score(y[te],pn),average_precision_score(y[te],pn)]

if __name__=='__main__':
    a=np.array([run(s) for s in range(SEEDS)])
    print('means',a.mean(0)); print('std',a.std(0,ddof=1))
    print('paired AUC relation-v-sequence',ttest_rel(a[:,2],a[:,0]))
    print('paired AUC shuffled-v-sequence',ttest_rel(a[:,4],a[:,0]))
