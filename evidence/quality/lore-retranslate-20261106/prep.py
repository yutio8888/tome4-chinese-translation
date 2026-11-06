import sys,re,json,csv,glob
sys.path.insert(0,'tools');sys.argv=['x']
import lite_review as L
import os
IDS=os.environ.get('IDS','').split()
terms=[]
for f in sorted(glob.glob('terminology/*.tsv')):
  for r in csv.DictReader(open(f,encoding='utf-8'),delimiter='\t'):
    if r['source'] and r['target'] and (re.search('[A-Z]',r['source']) or ' ' in r['source']): terms.append(r)
E={}
for u in L.units():
  k=u['unit_id'][:12]
  if k in IDS: E[k]=L.entry(u)
GAME={'mod-tome':"ToME4 本体（Tales of Maj'Eyal）",'tome-cults':'DLC「Forgotten Cults」','tome-orcs':'DLC「Embers of Rage」（兽人战役）'}
from pathlib import Path
for k in IDS:
  e=E[k]; d=Path('/tmp/gem-lore')/k; d.mkdir(parents=True,exist_ok=True)
  src=e['source']; (d/'source.txt').write_text(src,encoding='utf-8'); (d/'current.txt').write_text(e['target'],encoding='utf-8')
  seen={}; 
  for r in terms:
    s=r['source']
    if re.search(r'(?<![A-Za-z])'+re.escape(s)+r'(?![a-z])',src) and s not in seen:
      seen[s]=r
  g=sorted(seen.values(),key=lambda r:(r['status']!='preferred',r['source']))[:120]
  (d/'glossary.tsv').write_text('英文\t译名\t状态\n'+''.join(f"{r['source']}\t{r['target']}\t{r['status']}\n" for r in g),encoding='utf-8')
  tags=sorted(set(re.findall(r'\[/?[a-z]+\]|#[A-Z_]+#|%[-+0-9.]*[sdf]|\$\w+',src)))
  nl=src.count('\n'); comp=e['section'].split('/')[0]; lore=e['section'].split('/')[-1]
  p=f'''你是资深的中文游戏本地化译者。请把 /tmp/gem-lore/{k}/source.txt 中的英文（游戏 {GAME[comp]} 里一篇名为 {lore.replace('.lua','')} 的传说（lore）文本）完整重新翻译成自然、流畅、准确的简体中文。/tmp/gem-lore/{k}/current.txt 是现有译文，只用来参考专名译法，不要沿用它的句子结构。/tmp/gem-lore/{k}/glossary.tsv 是本译本已定的专名与术语表，出现的专名必须照表使用；表里没有的专名参考现有译文，现有译文也没有时自行音译或意译并全文统一。

硬性要求：
1. 忠实原文：不增删信息，不改变人物关系、因果、时间顺序、语气与叙述视角；对话保持口语化，叙述保持书面但通顺。
2. 格式完全保留：换行数量和位置与原文一致（原文共 {nl} 个换行符；空行也要保留为空行）{('；以下标记原样保留在对应位置：'+' '.join(tags)) if tags else ''}。引号用中文全角“”，括号用全角（）。
3. 距离单位：yard 译「码」，foot/feet 译「英尺」，inch 译「英寸」。
4. 严格检查语法：不要出现语序错误、成分残缺、搭配不当、句式杂糅、指代不清、量词错误。译完后请自己从头到尾通读一遍再修改。

输出：把完整译文（仅译文，不要任何说明、标题或代码块标记）写入文件 /tmp/gem-lore/{k}/out.txt。最终回复只写一行：`DONE {k} 换行数=<你的译文中的换行符数>`。
'''
  (d/'prompt.md').write_text(p,encoding='utf-8')
  print(k,comp,lore,len(src),'nl',nl,'tags',tags,'gloss',len(g))

# second pass: names from short library entries
import collections
lib=collections.defaultdict(collections.Counter)
for f in ['mod-tome.lua','tome-cults.lua','tome-orcs.lua','tome-ashes-urhrok.lua','engine.lua']:
  for m in re.finditer(r'^t\("([A-Z][^"\n]{2,40})", "([^"\n]+)"',open(f,encoding='utf-8').read(),re.M):
    s,t=m.group(1),m.group(2)
    if re.search('[一-鿿]',t) and not re.search(r'[%#:!?.]',s): lib[s][t]+=1
for k in IDS:
  d=Path('/tmp/gem-lore')/k; src=(d/'source.txt').read_text(encoding='utf-8')
  rows=(d/'glossary.tsv').read_text(encoding='utf-8').splitlines()
  have={r.split('\t')[0] for r in rows}
  add=[]
  for s in sorted(lib,key=len,reverse=True):
    if s in have: continue
    if re.search(r'(?<![A-Za-z])'+re.escape(s)+r'(?![A-Za-z])',src):
      t=lib[s].most_common(1)[0][0]; add.append(f'{s}\t{t}\t库内译名')
  (d/'glossary.tsv').write_text('\n'.join(rows+add[:150])+'\n',encoding='utf-8')
  print(k,'+',len(add))
