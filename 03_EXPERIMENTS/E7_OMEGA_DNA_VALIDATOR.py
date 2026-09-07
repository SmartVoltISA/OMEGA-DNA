#!/usr/bin/env python3
"""Pre-flight audit for external OMEGA-DNA datasets.

Usage: python E7_OMEGA_DNA_VALIDATOR.py dataset.csv
"""
import argparse, json
from pathlib import Path
import pandas as pd

CONCEPTS={
 'sequence':['sequence','seq','dna'],
 'relation':['relation','contact','interaction','tf','access','accessibility','loop'],
 'state':['state','expression','rna','condition','cell_type','cell'],
 'output':['label','target','phenotype','expression','effect','response','output'],
 'provenance':['source','accession','sample','assembly','assay','dataset']}

def audit(path):
    p=Path(path); df=pd.read_csv(p,sep=None,engine='python'); cols=[str(c).lower() for c in df.columns]
    found={k:[c for c in cols if any(x in c for x in terms)] for k,terms in CONCEPTS.items()}
    return {'file':str(p),'rows':len(df),'columns':len(df.columns),'duplicate_rows':int(df.duplicated().sum()),
            'missing_top10':df.isna().mean().sort_values(ascending=False).head(10).to_dict(),
            'concept_columns':found,'status':'AUDIT_REQUIRED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--json'); args=ap.parse_args()
    result=audit(args.file); print(json.dumps(result,indent=2,ensure_ascii=False))
    if args.json: Path(args.json).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
