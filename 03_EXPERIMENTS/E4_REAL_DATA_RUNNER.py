"""E4 real-data benchmark runner with official-split support.

The runner compares sequence-only, sequence+measured-relations, relation-shuffled
null, relation-only, and relation-family ablations. It never derives biological
relations from sequence. Relation columns must be independently measured or
annotated by the dataset.

Required columns: target, group, sequence_*, relation_*
Optional: split (official train/valid/test assignment).
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True); p.add_argument('--target',default='target')
    p.add_argument('--group',default='group'); p.add_argument('--split',default=None)
    p.add_argument('--sequence-prefix',default='sequence_'); p.add_argument('--relation-prefix',default='relation_')
    p.add_argument('--seeds',nargs='+',type=int,default=[7,11,19,23])
    p.add_argument('--test-group',nargs='+',default=None); p.add_argument('--valid-fraction',type=float,default=.2)
    p.add_argument('--out',default='E4_real_data_results.json'); return p.parse_args()


def model(seed):
    return make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=2000,random_state=seed))


def official_split(df,col):
    s=df[col].astype(str).str.lower(); tr=s.eq('train').to_numpy(); va=s.isin(['valid','validation']).to_numpy(); te=s.eq('test').to_numpy()
    if not tr.any() or not va.any() or not te.any(): raise ValueError('Official split must contain train, valid/validation and test')
    return tr,va,te


def grouped_split(df,col,seed,test_groups=None,valid_fraction=.2):
    groups=df[col].astype(str).unique(); rng=np.random.default_rng(seed)
    if test_groups is None:
        g=groups.copy(); rng.shuffle(g); test_groups=set(g[:max(1,int(round(len(g)*.2)))])
    else: test_groups=set(map(str,test_groups))
    remain=[g for g in groups if g not in test_groups]; rng.shuffle(remain)
    valid_groups=set(remain[:max(1,int(round(len(remain)*valid_fraction)))])
    test=df[col].astype(str).isin(test_groups).to_numpy(); valid=df[col].astype(str).isin(valid_groups).to_numpy()
    return ~(test|valid),valid,test


def score(X,y,tr,te,seed):
    if len(np.unique(y[tr]))<2 or len(np.unique(y[te]))<2:return np.nan
    m=model(seed); m.fit(X[tr],y[tr]); return float(roc_auc_score(y[te],m.predict_proba(X[te])[:,1]))


def run(a):
    df=pd.read_csv(a.input); req=[a.target,a.group]+([a.split] if a.split else [])
    missing=[c for c in req if c not in df.columns]
    if missing: raise ValueError(f'Missing required columns: {missing}')
    seq_cols=[c for c in df if c.startswith(a.sequence_prefix)]; rel_cols=[c for c in df if c.startswith(a.relation_prefix)]
    if not seq_cols or not rel_cols: raise ValueError('Need both sequence_* and relation_* columns')
    y=df[a.target].astype(int).to_numpy(); seq=df[seq_cols].apply(pd.to_numeric,errors='coerce').to_numpy(float); rel=df[rel_cols].apply(pd.to_numeric,errors='coerce').to_numpy(float)
    combined=np.column_stack([seq,rel]); families={}
    for c in rel_cols: families.setdefault(c.split('_')[1] if '_' in c else c,[]).append(c)
    rows=[]; split_mode='official' if a.split else 'grouped_random'
    for seed in a.seeds:
        tr,va,te=official_split(df,a.split) if a.split else grouped_split(df,a.group,seed,a.test_group,a.valid_fraction)
        rng=np.random.default_rng(seed); sh=rel.copy(); sh[tr]=sh[tr][rng.permutation(tr.sum())]
        variants={'sequence_only':seq,'combined':combined,'shuffled_relation_null':np.column_stack([seq,sh]),'relations_only':rel}
        for fam,cols in families.items():
            keep=[i for i,c in enumerate(rel_cols) if c not in cols]
            if keep: variants[f'ablation_without_{fam}']=np.column_stack([seq,rel[:,keep]])
        for name,X in variants.items(): rows.append({'seed':seed,'variant':name,'auc':score(X,y,tr,te,seed),'n_train':int(tr.sum()),'n_valid':int(va.sum()),'n_test':int(te.sum()),'split_mode':split_mode})
    pivot=pd.DataFrame(rows).pivot(index='seed',columns='variant',values='auc'); summary={}
    for c in pivot:
        v=pivot[c].dropna(); summary[c]={'mean_auc':float(v.mean()),'std_auc':float(v.std(ddof=1)) if len(v)>1 else 0.0}
    def paired(x,z):
        if not {x,z}.issubset(pivot): return None
        A=pivot[x].dropna(); B=pivot[z].reindex(A.index); m=B.notna(); A=A[m]; B=B[m]
        if len(A)<2:return {'mean_delta':float((A-B).mean()) if len(A) else np.nan,'t':np.nan,'p':np.nan}
        t=ttest_rel(A,B); return {'mean_delta':float((A-B).mean()),'t':float(t.statistic),'p':float(t.pvalue)}
    out={'status':'executed','input':str(Path(a.input)),'target':a.target,'group':a.group,'split_column':a.split,'split_mode':split_mode,'sequence_features':seq_cols,'relation_features':rel_cols,'relation_families':families,'seeds':a.seeds,'summary':summary,'combined_vs_sequence':paired('combined','sequence_only'),'shuffled_null_vs_sequence':paired('shuffled_relation_null','sequence_only'),'relations_only_vs_sequence':paired('relations_only','sequence_only'),'interpretation_guardrail':'Positive delta is evidence only if relation fields are independently measured/annotated, the shuffled null fails, official splits are respected, and capacity-matched controls survive.'}
    Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))

if __name__=='__main__': run(parse_args())
