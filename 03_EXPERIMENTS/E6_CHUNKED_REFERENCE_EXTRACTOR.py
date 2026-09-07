#!/usr/bin/env python3
"""Stream genomic intervals from a remote/local FASTA in bounded chunks.

The E6 biological benchmark does not need the whole hg19/GRCh38 FASTA in RAM.
Given a .fai index and a candidate TSV, this utility merges nearby byte ranges
and downloads them with HTTP Range requests, capped by --chunk-mb. It extracts
only the requested enhancer/promoter intervals and writes them as sequence
columns for E6_REAL_BIOLOGICAL_GATE_RUNNER.py.

Default chunk size: 100 MiB. Chunks are cached on disk and can be resumed.
The program refuses a server that silently ignores Range requests, preventing
an accidental full multi-GB download.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, urllib.request
from pathlib import Path


def read_fai(path_or_url):
    if path_or_url.startswith(('http://','https://')):
        with urllib.request.urlopen(path_or_url) as r:
            text = r.read().decode()
    else:
        text = Path(path_or_url).read_text()
    out = {}
    for line in text.splitlines():
        if not line.strip(): continue
        chrom, length, offset, line_bases, line_width = line.split('\t')[:5]
        out[chrom] = dict(length=int(length), offset=int(offset),
                          line_bases=int(line_bases), line_width=int(line_width))
    return out


def byte_pos(idx, base):
    return idx['offset'] + (base // idx['line_bases']) * idx['line_width'] + (base % idx['line_bases'])


def range_for_interval(idx, start, end):
    # Include complete FASTA lines covering [start,end).
    if end <= start: return byte_pos(idx, start), byte_pos(idx, start)
    a = byte_pos(idx, start)
    b = byte_pos(idx, end - 1) + 1
    return a, b


def fetch_range(url, start, end, cache_dir):
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(f'{url}|{start}|{end}'.encode()).hexdigest()
    p = cache_dir / f'{key}.{start}-{end}.part'
    if p.exists() and p.stat().st_size == end-start:
        return p.read_bytes()
    req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end-1}'})
    with urllib.request.urlopen(req) as r:
        data = r.read()
        cr = r.headers.get('Content-Range','')
        if r.status != 206 or not cr.startswith(f'bytes {start}-{end-1}/'):
            raise RuntimeError('Remote FASTA did not honor HTTP Range; refusing full download')
    if len(data) != end-start:
        raise RuntimeError(f'Range length mismatch: {len(data)} != {end-start}')
    p.write_bytes(data)
    return data


def decode_interval(raw, idx, start, end, range_start):
    # Raw bytes may include headers/newlines; convert to sequence and trim by
    # mapping byte positions through the indexed line geometry.
    seq = bytearray()
    for i, b in enumerate(raw):
        absolute = range_start + i
        rel = absolute - idx['offset']
        if rel < 0: continue
        col = rel % idx['line_width']
        if col < idx['line_bases']:
            base = (rel // idx['line_width']) * idx['line_bases'] + col
            if start <= base < end and b in b'ACGTNacgtn':
                seq.append(b)
    return seq.decode().upper()


def load_rows(path):
    with open(path, newline='') as fh:
        rows = list(csv.DictReader(fh, delimiter='\t'))
    if not rows: raise ValueError('empty pairs TSV')
    required={'chrom','start','end','promoter_chrom','promoter_start','promoter_end'}
    missing=required-set(rows[0])
    if missing: raise ValueError('missing columns: '+','.join(sorted(missing)))
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pairs', required=True)
    ap.add_argument('--fasta-url', required=True)
    ap.add_argument('--fai', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--cache-dir', default='.e6_fasta_cache')
    ap.add_argument('--chunk-mb', type=int, default=100)
    args=ap.parse_args()
    chunk=max(1,args.chunk_mb)*1024*1024
    rows=load_rows(args.pairs)
    fai=read_fai(args.fai)
    fasta_url=args.fasta_url
    cache=Path(args.cache_dir)

    requests=[]
    for i,r in enumerate(rows):
        for kind,chrom,st,en in [('enhancer_seq',r['chrom'],int(r['start']),int(r['end'])),
                                  ('promoter_seq',r['promoter_chrom'],int(r['promoter_start']),int(r['promoter_end']))]:
            if chrom not in fai: raise ValueError(f'{chrom} absent from FAI')
            a,b=range_for_interval(fai[chrom],st,en)
            requests.append((chrom,a,b,i,kind,st,en))

    # Merge nearby byte ranges, never exceeding the configured chunk size.
    grouped={}
    for x in requests: grouped.setdefault(x[0],[]).append(x)
    seqs=[{} for _ in rows]
    manifest=[]
    for chrom, items in grouped.items():
        items.sort(key=lambda x:x[1])
        bundles=[]
        cur=[]; a=b=None
        for x in items:
            xa,xb=x[1],x[2]
            if not cur or xb-a <= chunk and max(b,xb)-min(a,xa) <= chunk:
                cur.append(x); a=xa if a is None else min(a,xa); b=xb if b is None else max(b,xb)
            else:
                bundles.append((a,b,cur)); cur=[x]; a=xa; b=xb
        if cur: bundles.append((a,b,cur))
        for a,b,bundle in bundles:
            raw=fetch_range(fasta_url,a,b,cache)
            manifest.append({'chrom':chrom,'start':a,'end':b,'bytes':len(raw)})
            for _,_,_,row_i,kind,st,en in bundle:
                seqs[row_i][kind]=decode_interval(raw,fai[chrom],st,en,a)

    with open(args.out,'w',newline='') as fh:
        fields=list(rows[0].keys())+['enhancer_seq','promoter_seq']
        w=csv.DictWriter(fh,fieldnames=fields,delimiter='\t'); w.writeheader()
        for i,r in enumerate(rows):
            r=dict(r); r.update(seqs[i]); w.writerow(r)
    Path(str(args.out)+'.manifest.json').write_text(json.dumps({
        'fasta_url':fasta_url,'chunk_bytes':chunk,'n_rows':len(rows),
        'n_http_ranges':len(manifest),'ranges':manifest},indent=2)+'\n')
    print(json.dumps({'status':'ok','rows':len(rows),'ranges':len(manifest),'chunk_bytes':chunk,'out':args.out},indent=2))

if __name__=='__main__': main()
