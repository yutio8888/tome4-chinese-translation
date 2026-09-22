from pathlib import Path
import json,hashlib,sys,collections
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
P=Path(__file__).parent
before=(P/'BEFORE-FIX-2.lua').read_text();expected=before
records=LocaleLoader(LuaRuntime(load_manifest())).load_path(P/'BEFORE-FIX-2.lua',logical_path='mod-tome.lua').records
work={i['entry_revision_identity']:i for i in json.loads((P/'WORKSET.json').read_text())['items']}
bykey=collections.defaultdict(list)
for f in json.loads((P/'FIX-2-REPLACEMENTS.json').read_text()):bykey[f['revision_key']].append(f)
for key,fixes in bykey.items():
 item=work[key];matches=[r for r in records if all(r.get(k)==item[k] for k in ('source','section','source_tag'))];assert len(matches)==1
 target=matches[0]['target'];new=target
 for f in fixes:
  assert new.count(f['before'])==1,f['id'];new=new.replace(f['before'],f['after'],1)
 assert expected.count(target)==1,key
 expected=expected.replace(target,new,1)
assert Path('mod-tome.lua').read_text()==expected
print(json.dumps(dict(verified=True,exact_replacements=2,changed_revisions=1,sha256=hashlib.sha256(expected.encode()).hexdigest())))
