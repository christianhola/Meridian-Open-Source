#!/usr/bin/env python3
"""Collect public Refero style pages discovered from the active browser session."""
from __future__ import annotations
import json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE='https://styles.refero.design'
DISCOVERY=Path('/home/ubuntu/upload/styles.refero.design__q_Notion_1791332316091.html')
OUT=Path('/home/ubuntu/Meridian-Open-Source/skills/meridian-design-research/references/meridian-design-library-30.json')
REPORT=Path('/home/ubuntu/Meridian-Open-Source/skills/meridian-design-research/references/meridian-design-library-30.md')

def clean(s: str) -> str:
    return re.sub(r'\s+', ' ', s or '').strip()

def discover():
    soup=BeautifulSoup(DISCOVERY.read_text(errors='ignore'),'html.parser')
    out=[]; seen=set()
    for a in soup.find_all('a', href=True):
        if '/style/' not in a['href']: continue
        href=urljoin(BASE,a['href']); name=clean(a.get_text(' ',strip=True))
        # strip the short description from the visible card
        parts=name.split(' ',1)
        brand=parts[0] if parts else name
        if brand in seen: continue
        seen.add(brand); out.append({'brand':brand,'label':name,'url':href})
    # Keep a broad, diverse first batch and explicitly retain requested/top brands.
    required={'Notion','Stripe','Figma','Anthropic','Cohere','Linear','Vercel','ElevenLabs'}
    chosen=[]
    for row in out:
        if len(chosen)<36 or row['brand'] in required:
            chosen.append(row)
    # Top cards from the main index, discovered in the active browser session.
    extras=[
      ('Linear','/style/90ce5883-bb24-4466-93f7-801cd617b0d1'),
      ('Vercel','/style/f24daf3a-d43f-4dec-85a9-8ac1d5148a03'),
      ('ElevenLabs','/style/031056ff-7af1-46db-8daa-115f731c5d26'),
      ('Raycast','/style/3b6a17f0-3bdf-418c-a95e-0b89e5a8b2f8'),
      ('OpenAI','/style/dc541737-8bf2-4b31-b729-0352f696e82f'),
      ('Cursor','/style/4e3b4717-84c8-4599-baaf-a343c3d619b6'),
      ('Brex','/style/b58d92f6-68a8-4358-8fc9-6ea58e6d483b'),
      ('Wise','/style/367c0c6e-73a7-441c-a8ff-91d139ac60dc'),
      ('Ramp','/style/b38702a0-75ab-474c-9106-00b624535825')
    ]
    existing={r['brand'] for r in chosen}
    for brand,path in extras:
        if brand not in existing:
            chosen.append({'brand':brand,'label':brand,'url':urljoin(BASE,path)})
            existing.add(brand)
    return chosen

def fetch(row):
    try:
        r=requests.get(row['url'],timeout=30,headers={'User-Agent':'Mozilla/5.0 Refero research collector'})
        r.raise_for_status()
        soup=BeautifulSoup(r.text,'html.parser')
        title=clean(soup.title.get_text() if soup.title else row['brand'])
        # The rendered DESIGN.md is in a highlighted code block; choose the most complete one.
        candidates=[]
        for node in soup.find_all(['pre','code']):
            text=node.get_text('\n',strip=False)
            if 'Style Reference' in text or '## Tokens' in text:
                candidates.append(text)
        design=max(candidates,key=len) if candidates else ''
        # Compact page-level visual description and color tokens for the index.
        colors=sorted(set(re.findall(r'#[0-9a-fA-F]{6}', design)))
        return {**row,'title':title,'status':r.status_code,'bytes':len(r.content),'design_md':design,'colors':colors,'ok':bool(design)}
    except Exception as e:
        return {**row,'ok':False,'error':str(e)}

def main():
    rows=discover(); results=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures=[pool.submit(fetch,row) for row in rows]
        for f in as_completed(futures): results.append(f.result())
    results.sort(key=lambda x: rows.index(next(r for r in rows if r['url']==x['url'])))
    OUT.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Refero Style Library — 30+ fichas públicas','', 'Fuente de descubrimiento: búsqueda pública de Refero Styles para `Notion`, realizada desde el navegador activo.','', 'Se recopilaron fichas individuales cuando el HTML público incluía su DESIGN.md. Las entradas fallidas se conservan con error; no se inventan tokens.','', '| # | Marca | URL | Estado | Colores detectados | DESIGN.md |','|---:|---|---|---:|---:|---:|']
    for i,x in enumerate(results,1):
        lines.append(f"| {i} | {x['brand']} | [{x['url']}]({x['url']}) | {x.get('status','ERR')} | {len(x.get('colors',[]))} | {'sí' if x.get('ok') else 'no'} |")
    lines += ['', '## Fichas extraídas', '']
    for i,x in enumerate(results,1):
        lines += [f"### {i}. {x['brand']}", f"- **URL:** {x['url']}", f"- **Estado:** {x.get('status','ERR')}", f"- **Colores:** {', '.join(x.get('colors',[])) or 'no detectados'}", '']
        if x.get('design_md'):
            # Include the full public DESIGN.md for each successful page.
            lines += ['```markdown', x['design_md'].rstrip(), '```', '']
        else:
            lines += [f"- **Error de extracción:** {x.get('error','contenido no encontrado')}", '']
    REPORT.write_text('\n'.join(lines),encoding='utf-8')
    ok=sum(bool(x.get('ok')) for x in results)
    print(json.dumps({'discovered':len(rows),'successful':ok,'failed':len(rows)-ok,'json':str(OUT),'report':str(REPORT)},ensure_ascii=False))
if __name__=='__main__': main()
