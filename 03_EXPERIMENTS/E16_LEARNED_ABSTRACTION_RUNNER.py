#!/usr/bin/env python3
"""E16: learn graph form from raw adjacency, without hand-designed descriptors.

Requirements: Python 3.10+, numpy, networkx, pandas, torch, statsmodels.
This is an exploratory synthetic test, not biological evidence.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
import numpy as np
import networkx as nx
import pandas as pd
import torch
from torch import nn
from statsmodels.stats.proportion import proportion_confint

FAMILIES=("cycle","path","cycle_chord","two_cycles")
TRAIN_SIZES=(16,20,24)
TEST_SIZES=(28,32,36)
NOISES=(0.0,0.02,0.05,0.10)
N_TRAIN=40
N_TEST=100
DEFAULT_SEED=16017

def make_graph(n,family,seed,noise=0.0):
    rng=np.random.default_rng(seed)
    if family=="cycle": g=nx.cycle_graph(n)
    elif family=="path": g=nx.path_graph(n)
    elif family=="cycle_chord":
        g=nx.cycle_graph(n); g.add_edge(0,n//2)
    elif family=="two_cycles":
        k=n//2; g=nx.disjoint_union(nx.cycle_graph(k),nx.cycle_graph(k))
    else: raise ValueError(family)
    original=list(g.edges())
    for e in original:
        if rng.random()<noise: g.remove_edge(*e)
    nonedges=list(nx.non_edges(g))
    p=min(1.0,noise*len(original)/max(len(nonedges),1))
    if p: g.add_edges_from(e for e in nonedges if rng.random()<p)
    perm=rng.permutation(n)
    return nx.relabel_nodes(g,{i:int(perm[i]) for i in range(n)})

def tensor_graph(g):
    # Raw adjacency only. No engineered graph statistics are passed to the model.
    A=nx.to_numpy_array(g,nodelist=range(g.number_of_nodes()),dtype=np.float32)
    return torch.tensor(A),torch.ones((A.shape[0],1),dtype=torch.float32)

class AdjacencyMPNN(nn.Module):
    def __init__(self,hidden=32,depth=3):
        super().__init__()
        self.self_layers=nn.ModuleList()
        self.neighbor_layers=nn.ModuleList()
        dims=[1]+[hidden]*depth
        for i in range(depth):
            self.self_layers.append(nn.Linear(dims[i],dims[i+1]))
            self.neighbor_layers.append(nn.Linear(dims[i],dims[i+1],bias=False))
        self.head=nn.Sequential(nn.Linear(hidden*2,hidden),nn.ReLU(),nn.Linear(hidden,len(FAMILIES)))
    def forward_one(self,A,X):
        H=X
        for sl,nl in zip(self.self_layers,self.neighbor_layers):
            H=torch.relu(sl(H)+nl(A@H))
        pooled=torch.cat([H.mean(dim=0),H.max(dim=0).values],dim=0)
        return self.head(pooled)

def make_dataset(sizes,per_class,noise,seedbase):
    out=[]
    for n in sizes:
        for ci,fam in enumerate(FAMILIES):
            for j in range(per_class):
                g=make_graph(n,fam,seedbase+n*100000+ci*10000+j,noise)
                A,X=tensor_graph(g)
                out.append((A,X,ci,n,noise,fam,j))
    return out

def train_model(train,seed,epochs=8):
    torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
    model=AdjacencyMPNN()
    opt=torch.optim.Adam(model.parameters(),lr=0.001,weight_decay=1e-4)
    loss_fn=nn.CrossEntropyLoss()
    for epoch in range(epochs):
        order=np.random.default_rng(seed+epoch).permutation(len(train))
        model.train(); losses=[]
        for ix in order:
            A,X,y,*_=train[ix]
            opt.zero_grad()
            loss=loss_fn(model(A,X).view(1,-1),torch.tensor([y],dtype=torch.long))
            loss.backward(); opt.step(); losses.append(float(loss.detach()))
    return model,float(np.mean(losses))

def rewire_degree_preserving(g,rng):
    h=g.copy(); edges=[(int(u),int(v)) for u,v in h.edges()]
    if len(edges)<2: return h
    for _ in range(max(20*len(edges),100)):
        i,j=rng.integers(0,len(edges),size=2)
        if i==j: continue
        u,v=edges[i]; x,y=edges[j]
        if len({u,v,x,y})<4: continue
        if rng.random()<0.5: x,y=y,x
        if h.has_edge(u,y) or h.has_edge(x,v): continue
        h.remove_edge(u,v); h.remove_edge(x,y)
        h.add_edge(u,y); h.add_edge(x,v)
        edges[i]=(min(u,y),max(u,y)); edges[j]=(min(x,v),max(x,v))
    return h

def evaluate(model,ds,condition):
    model.eval(); rows=[]
    with torch.no_grad():
        for A,X,y,n,noise,fam,j in ds:
            pred=int(model(A,X).argmax().item())
            rows.append({"n":n,"noise":noise,"family":fam,"true":y,"pred":pred,
                         "correct":int(pred==y),"replicate":j,"condition":condition})
    return pd.DataFrame(rows)

def main():
    torch.set_num_threads(1)
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-dir",default="e16_output")
    ap.add_argument("--epochs",type=int,default=8)
    ap.add_argument("--n-test",type=int,default=N_TEST)
    ap.add_argument("--seed",type=int,default=DEFAULT_SEED)
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    train=make_dataset(TRAIN_SIZES,N_TRAIN,0.02,args.seed*1000000)
    model,final_loss=train_model(train,args.seed,args.epochs)
    all_results=[]
    for noise in NOISES:
        ds=make_dataset(TEST_SIZES,args.n_test,noise,args.seed*2000000+int(noise*1000)*1000000)
        all_results.append(evaluate(model,ds,"original"))
        null=[]
        for A,X,y,n,no,fam,j in ds:
            g=nx.from_numpy_array(A.numpy())
            gn=rewire_degree_preserving(g,np.random.default_rng(args.seed*3000000+int(no*1000)*1000000+n*100000+y*1000+j))
            An,Xn=tensor_graph(gn)
            null.append((An,Xn,y,n,no,fam,j))
        all_results.append(evaluate(model,null,"degree_preserving_rewire"))
    raw=pd.concat(all_results,ignore_index=True)
    raw.to_csv(out/"E16_LEARNED_ABSTRACTION_RAW.csv",index=False)
    summary=[]
    for (noise,n,condition),g in raw.groupby(["noise","n","condition"],sort=True):
        c=int(g.correct.sum()); N=len(g); lo,hi=proportion_confint(c,N,method="wilson")
        row={"noise":float(noise),"n":int(n),"condition":condition,"N":N,
             "accuracy":c/N,"ci_low":lo,"ci_high":hi}
        for fam in FAMILIES: row["acc_"+fam]=float(g[g.family==fam].correct.mean())
        summary.append(row)
    pd.DataFrame(summary).to_csv(out/"E16_LEARNED_ABSTRACTION_SUMMARY.csv",index=False)
    report={"seed":args.seed,"epochs":args.epochs,"train_graphs":len(train),
            "train_sizes":TRAIN_SIZES,"test_sizes":TEST_SIZES,"noise_levels":NOISES,
            "n_test_per_class_size_noise":args.n_test,"final_epoch_mean_loss":final_loss,
            "model":"3-layer adjacency message-passing neural network; constant node features; mean+max pooling; graph-label supervision only",
            "features":"raw adjacency only; no engineered graph descriptors",
            "negative_control":"degree-preserving double-edge swaps on each test graph","summary":summary}
    (out/"E16_LEARNED_ABSTRACTION_SUMMARY.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
