"""E2 accessibility/state controlled benchmark.

Synthetic gate only. The target is a declared hidden accessibility state; it is
not experimental ATAC-seq. The purpose is to test whether relational sequence
features can recover state information under held-out evaluation, with a
shuffled-state null.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split

N=10000; L=200; SEEDS=30

def run(seed):
    r=np.random.default_rng(seed)
    X=r.integers(0,4,size=(N,L))
    gc=np.mean((X==1)|(X==2),1)
    m1=np.max(np.array([np.all(X[:,i:i+4]==[0,1,2,3],1) for i in range(L-3)]),0)
    m2=np.max(np.array([np.all(X[:,i:i+4]==[1,1,2,2],1) for i in range(L-3)]),0)
    din=np.mean(X[:,:-1]*4+X[:,1:],1)/15
    z=2*(gc-.5)+1.5*m1+m2+1.2*(din-.5)+r.normal(0,.7,N)
    y=(z>np.median(z)).astype(int)
    codes=X[:,:-1]*4+X[:,1:]
    d=np.zeros((N,16))
    for k in range(16): d[:,k]=np.mean(codes==k,1)
    Fgc=gc[:,None]; Frel=np.c_[gc,d]; Fcomb=np.c_[gc,d,m1,m2]
    tr,te=train_test_split(np.arange(N),test_size=.30,random_state=seed,stratify=y)
    out={"seed":seed}
    for name,F in [("gc",Fgc),("relations",Frel),("combined",Fcomb)]:
        model=LogisticRegression(max_iter=500).fit(F[tr],y[tr]); p=model.predict_proba(F[te])[:,1]
        out[name+"_auc"]=roc_auc_score(y[te],p); out[name+"_ap"]=average_precision_score(y[te],p)
    model=LogisticRegression(max_iter=500).fit(Fcomb[tr],y[tr])
    sh=Fcomb[te].copy(); np.random.default_rng(seed+10000).shuffle(sh)
    out["shuffled_features_auc"]=roc_auc_score(y[te],model.predict_proba(sh)[:,1])
    sy=np.random.default_rng(seed+20000).permutation(y[te])
    out["shuffled_labels_auc"]=roc_auc_score(sy,model.predict_proba(Fcomb[te])[:,1])
    return out

if __name__=='__main__':
    r=pd.DataFrame([run(s) for s in range(SEEDS)])
    print(r.to_string(index=False)); print('\nMEAN'); print(r.mean(numeric_only=True)); print('\nSTD'); print(r.std(numeric_only=True))
