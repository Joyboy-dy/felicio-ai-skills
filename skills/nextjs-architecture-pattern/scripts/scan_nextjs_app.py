#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
def main():
 ap=argparse.ArgumentParser(description='Read-only detection of Next.js version, router roots, route files and client boundaries.')
 ap.add_argument('root',type=Path);ap.add_argument('--max-files',type=int,default=5000);ap.add_argument('--json',action='store_true');a=ap.parse_args();root=a.root.resolve()
 if not root.is_dir():ap.error(f'not a directory: {root}')
 version=None
 try:
  pkg=json.loads((root/'package.json').read_text());version=(pkg.get('dependencies',{}).get('next') or pkg.get('devDependencies',{}).get('next'))
 except Exception:pass
 roots=[]
 for rel in ('app','src/app','pages','src/pages'):
  if (root/rel).is_dir():roots.append(rel)
 route_names={'page.tsx','page.jsx','page.js','page.ts','layout.tsx','layout.jsx','route.ts','route.js','loading.tsx','error.tsx','not-found.tsx'}
 routes=[];clients=[];n=0
 for p in root.rglob('*'):
  if n>=a.max_files:break
  if not p.is_file() or any(x in {'.git','node_modules','.next','dist','build'} for x in p.parts):continue
  if p.suffix.lower() in {'.js','.jsx','.ts','.tsx'}:
   n+=1
   rel=str(p.relative_to(root))
   if p.name in route_names or any(r in rel.split('/') for r in ('pages',)):routes.append(rel)
   try:t=p.read_text(encoding='utf-8',errors='ignore')[:1000]
   except OSError:t=''
   if re.search(r"^[\s;]*['\"]use client['\"]",t):clients.append(rel)
 print(json.dumps({'root':str(root),'next_version':version,'router_roots':roots,'route_files':routes[:500],'client_boundaries':clients[:500],'files_scanned':n},indent=2))
if __name__=='__main__':main()
