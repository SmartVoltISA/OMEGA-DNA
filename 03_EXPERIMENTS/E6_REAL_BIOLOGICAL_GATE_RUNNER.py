#!/usr/bin/env python3
"""E6 real biological gate runner with leakage-safe relation null."""
from __future__ import annotations
import argparse, csv, math, hashlib, json
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
BASES="ACGT"
def parse_fasta(path):
    seqs={}; name=None; buf=[]
    with open(path) as fh:
        for line in fh:
            line=line.strip()
            if not line: continue
            if line.startswith('>'):
                if name is not None: seqs[name]=''.join(buf).upper()
                name,buf=line[1:].split()[0],[]
            else: buf.append(line)
        if name is not None: seqs[name]=''.join(buf).upper()
    return seqs
def seq_features(seq):
    s=seq.upper().replace('N',''); n=len(s)
    if not n: return [0.0]*85
    counts=np.array([s.count(b) for b in BASES],float)/n
    gc=counts[1]+counts[2]; ent=-sum(p*math.log2(p) for p in counts if p>0)
    idx={a+b:i for i,a in enumerate(BASES) for b in BASES}; di=np.zeros(16)
    for a,b in zip(s[:-1],s[1:]):
        if a+b in idx: di[idx[a+b]]+=1
    if n>1: di/=n-1
    idx3={a+b+c:i for i,a in enumerate(BASES) for b in BASES for c in BASES}; km=np.zeros(64)
    for i in range(max(0,n-2)):
        t=s[i:i+3]
        if t in idx3: km[idx3[t]]+=1
    if n>2: km/=n-2
    return [gc,ent,*counts,*di,*km]
def get_seq(r,key,fasta):
    if r.get(key): return r[key]
    chrom=r['chrom'] if key=='enhancer_seq' else r['promoter_chrom']
    a=int(r['start'] if key=='enhancer_seq' else r['promoter_start']); b=int(r['end'] if key=='enhancer_seq' else r['promoter_end'])
    if chrom not in fasta: raise ValueError(f'chromosome {chrom} absent from FASTA')
    return fasta[chrom][a:b]
def load_rows(path):
    with open(path,newline='') as fh: rows=list(csv.DictReader(fh,delimiter='\t'))
    req={'chrom','start','end','promoter_chrom','promoter_start','promoter_end','gene','label'}
    if not rows: raise ValueError('empty table')
    missing=req-set(rows[0])
    if missing: raise ValueError('missing columns: '+','.join(sorted(missing)))
    return rows
def relation_features(r):
    names=['contact_score','enh_access','prom_access','tf_score','h3k27ac_score']
    vals=[float(r.get(k,0.0) or 0.0) for k in names]
    em=(int(r['start'])+int(r['end']))/2; pm=(int(r['promoter_start'])+int(r['promoter_end']))/2
    return vals+[math.log1p(abs(em-pm))]
def chromosome_split(rows):
    tr={str(i) for i in range(1,17)}; va={'17','18','19'}; te={'20','21','22','X'}
    out=[]
    for r in rows:
        c=r['chrom'].removeprefix('chr'); out.append('train' if c in tr else 'val' if c in va else 'test' if c in te else 'excluded')
    return np.array(out)
def standardize_fit(Xtr,Xte):
    mu=Xtr.mean(0); sd=Xtr.std(0); sd[sd<1e-12]=1
    return (Xtr-mu)/sd,(Xte-mu)/sd
def evaluate(name,Xtr,ytr,Xte,yte,seed):
    Xtr,Xte=standardize_fit(Xtr,Xte); clf=LogisticRegression(max_iter=3000,C=1.0,solver='lbfgs',random_state=seed); clf.fit(Xtr,ytr); p=clf.predict_proba(Xte)[:,1]
    return {'model':name,'auroc':float(roc_auc_score(yte,p)),'auprc':float(average_precision_score(yte,p)),'brier':float(brier_score_loss(yte,p)),'n_test':int(len(yte))}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pairs',required=True); ap.add_argument('--fasta'); ap.add_argument('--out',default='E6_REAL_BIOLOGICAL_GATE_RESULTS.json'); ap.add_argument('--seed',type=int,default=20260907); args=ap.parse_args()
    rows=load_rows(args.pairs); fasta=parse_fasta(args.fasta) if args.fasta else {}; split=chromosome_split(rows)
    sx=[]; rx=[]; y=[]
    for r in rows:
        sx.append(seq_features(get_seq(r,'enhancer_seq',fasta))+seq_features(get_seq(r,'promoter_seq',fasta))); rx.append(relation_features(r)); y.append(int(r['label']))
    sx,rx,y=np.asarray(sx),np.asarray(rx),np.asarray(y); train=split=='train'; test=split=='test'
    if train.sum()<20 or test.sum()<20: raise SystemExit('insufficient chromosome-level train/test rows')
    if len(np.unique(y[train]))<2 or len(np.unique(y[test]))<2: raise SystemExit('both train and test require positive and negative labels')
    res=[evaluate('sequence_only',sx[train],y[train],sx[test],y[test],args.seed)]
    combined=np.c_[sx,rx]; res.append(evaluate('relational',combined[train],y[train],combined[test],y[test],args.seed))
    # Correct null: independently permute relation rows within train and test.
    rng=np.random.default_rng(args.seed); shuffled=rx.copy(); ti=np.where(train)[0]; ei=np.where(test)[0]; shuffled[ti]=rx[rng.permutation(ti)]; shuffled[ei]=rx[rng.permutation(ei)]
    res.append(evaluate('relation_shuffled_null',np.c_[sx,shuffled][train],y[train],np.c_[sx,shuffled][test],y[test],args.seed))
    payload={'protocol':'E6_REAL_BIOLOGICAL_GATE_PROTOCOL.md','pairs_sha256':hashlib.sha256(Path(args.pairs).read_bytes()).hexdigest(),'fasta_sha256':hashlib.sha256(Path(args.fasta).read_bytes()).hexdigest() if args.fasta else None,'seed':args.seed,'n_total':int(len(rows)),'n_train':int(train.sum()),'n_test':int(test.sum()),'results':res,'status':'executed_biological_input' if args.fasta else 'executed_precomputed_sequence_input','notes':['Labels must be independently derived from RNA expression before this runner.','Chromosome-level holdout is primary.','Relation-shuffled null independently breaks relation/label pairing in train and test while preserving relation marginals.']}
    Path(args.out).write_text(json.dumps(payload,indent=2)+'\n'); print(json.dumps(payload,indent=2))
if __name__=='__main__': main()
