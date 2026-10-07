#!/usr/bin/env python3
from __future__ import annotations
import json,re
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

ROOT=Path('/home/ubuntu/Meridian-Open-Source/skills/refero-design-research')
UPLOAD=Path('/home/ubuntu/upload')
OUT=ROOT/'references/refero-style-library-expanded.jsonl'
SUMMARY=ROOT/'references/refero-style-library-expanded.md'
BASE='https://styles.refero.design'

def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def discover():
    seen={}
    for p in sorted(UPLOAD.glob('styles.refero.design__q_*.html')):
        soup=BeautifulSoup(p.read_text(errors='ignore'),'html.parser')
        query=p.name.split('__q_',1)[-1].rsplit('_',1)[0]
        for a in soup.find_all('a',href=True):
            href=a['href']
            if '/style/' not in href: continue
            url=urljoin(BASE,href)
            label=clean(a.get_text(' ',strip=True))
            brand=label.split(' ',1)[0] if label else url.rsplit('/',1)[-1]
            if url not in seen: seen[url]={'brand':brand,'label':label,'url':url,'queries':[query]}
            elif query not in seen[url]['queries']: seen[url]['queries'].append(query)
    # Explicit requested Ramp page.
    ramp=BASE+'/style/b38702a0-75ab-474c-9106-00b624535825'
    seen.setdefault(ramp,{'brand':'Ramp','label':'Ramp','url':ramp,'queries':['requested-direct-style']})
    return list(seen.values())

def fetch(row):
    try:
        r=requests.get(row['url'],timeout=45,headers={'User-Agent':'Mozilla/5.0 Refero design research'})
        r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
        candidates=[]
        for node in soup.find_all(['pre','code']):
            t=node.get_text('\n',strip=False)
            if 'Style Reference' in t or '## Tokens' in t: candidates.append(t)
        design=max(candidates,key=len) if candidates else ''
        colors=sorted(set(re.findall(r'#[0-9a-fA-F]{6}',design)))
        return {**row,'status':r.status_code,'bytes':len(r.content),'colors':colors,'design_md':design,'ok':bool(design)}
    except Exception as e: return {**row,'ok':False,'error':str(e)}

def main():
    rows=discover(); results=[]
    with ThreadPoolExecutor(max_workers=16) as pool:
        fs=[pool.submit(fetch,row) for row in rows]
        for i,f in enumerate(as_completed(fs),1):
            results.append(f.result())
            if i%50==0: print('fetched',i,'/',len(rows),flush=True)
    order={r['url']:i for i,r in enumerate(rows)}; results.sort(key=lambda x:order[x['url']])
    with OUT.open('w',encoding='utf-8') as f:
        for x in results: f.write(json.dumps(x,ensure_ascii=False)+'\n')
    ok=sum(x.get('ok',False) for x in results)
    lines=[f'# Refero Style Library — expansión sin límite práctico ({len(results)} fichas)', '', 'Fuentes: búsquedas públicas realizadas en la pestaña activa en Refero Styles: Kids & family product, Non-boring enterprise, Neon crypto dark, Friendly startup, Immersive 3D scenes, Like Stripe, Newsletter landing y Bauhaus geometry.', '', 'Cada ficha conserva su URL, consultas de descubrimiento, colores hex detectados y el DESIGN.md público extraído. No se inventan valores para fichas fallidas.', '', f'**Resultado:** {ok} fichas con DESIGN.md / {len(results)-ok} fallidas.', '', '| # | Marca | Consultas | Estado | Colores | DESIGN.md |', '|---:|---|---|---:|---:|---:|']
    for i,x in enumerate(results,1): lines.append(f"| {i} | {x['brand']} | {', '.join(x['queries'])} | {x.get('status','ERR')} | {len(x.get('colors',[]))} | {'sí' if x.get('ok') else 'no'} |")
    lines += ['', '## Uso', '', 'El JSONL asociado contiene una línea por ficha con el DESIGN.md completo y permite filtrar por marca o consulta sin cargar todo el documento.', '']
    SUMMARY.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'discovered':len(rows),'successful':ok,'failed':len(rows)-ok,'jsonl':str(OUT),'summary':str(SUMMARY)},ensure_ascii=False))
if __name__=='__main__': main()
