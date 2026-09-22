from pathlib import Path
import sys,json,re
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
from i18nlib.lint import MARKUP_RE,AT_TOKEN_RE
P=Path(__file__).parent
load=LocaleLoader(LuaRuntime(load_manifest()))
a=load.load_path(P/'baseline/mod-tome.lua',logical_path='mod-tome.lua').records
b=load.load_path(Path('mod-tome.lua'),logical_path='mod-tome.lua').records
work=json.loads((P/'WORKSET.json').read_text())['items'];allowed={(i['section'],i['source'],i['source_tag']):i for i in work}
assert len(a)==len(b)
changed=[]
for x,y in zip(a,b):
 xx={k:v for k,v in x.items() if k!='line'}; yy={k:v for k,v in y.items() if k!='line'}
 if xx==yy:continue
 key=(x.get('section'),x.get('source'),x.get('source_tag'));assert key in allowed,key
 assert {k:v for k,v in xx.items() if k!='target'}=={k:v for k,v in yy.items() if k!='target'}
 for pattern in [r'%[-+ #0]*\d*(?:\.\d+)?[cdeEfgGiouXxqs%]',r'\n',r'\t']:
  expected=x['source'] if pattern in (r'\n',r'\t') and allowed[key]['entry_revision_identity'].startswith('e882cc8d4e') else x['target']
  assert re.findall(pattern,expected)==re.findall(pattern,y['target']),pattern
 assert MARKUP_RE.findall(x['target'])==MARKUP_RE.findall(y['target'])
 assert AT_TOKEN_RE.findall(x['target'])==AT_TOKEN_RE.findall(y['target'])
 changed.append({'revision':allowed[key]['entry_revision_identity'],'line':y['line'],'before':x['target'],'after':y['target']})
assert len(changed)==8,len(changed)
print(json.dumps({'verified':True,'records':len(a),'changed':changed},ensure_ascii=False,indent=2))
