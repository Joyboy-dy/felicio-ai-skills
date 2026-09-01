#!/usr/bin/env python3
"""Print a compact catalog of skills and their bundled resources."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def fm(path: Path) -> dict[str,str]:
    text=path.read_text(encoding='utf-8'); out={}
    if not text.startswith('---\n'): return out
    end=text.find('\n---\n',4)
    for line in text[4:end].splitlines():
        if ':' in line and not line.startswith((' ','\t')):
            k,v=line.split(':',1); out[k.strip()]=v.strip().strip('"\'')
    return out

def main()->int:
    ap=argparse.ArgumentParser(description='List skills, descriptions, scripts, references and assets.')
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); rows=[]
    for d in sorted((args.root/'skills').iterdir()):
        if not d.is_dir() or not (d/'SKILL.md').is_file(): continue
        data=fm(d/'SKILL.md')
        def names(part):
            p=d/part; return sorted(x.name for x in p.iterdir() if x.is_file()) if p.is_dir() else []
        rows.append({'name':data.get('name',d.name),'description':data.get('description',''),'scripts':names('scripts'),'references':names('references'),'assets':names('assets')})
    if args.json: print(json.dumps(rows,indent=2)); return 0
    for row in rows:
        print(row['name']); print(f"  {row['description']}")
        for key in ('scripts','references','assets'):
            if row[key]: print(f"  {key}: {', '.join(row[key])}")
    return 0
if __name__=='__main__': raise SystemExit(main())
