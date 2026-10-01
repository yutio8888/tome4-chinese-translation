import sys,json
sys.path.insert(0,'tools');sys.path.insert(0,'.')
import audit_dynamic as A
m=A.load_manifest(version=A.DEFAULT_VERSION)
loader=A.LocaleLoader(A.LuaRuntime(manifest=m))
docs=A.load_translation_documents(m,loader)
out=[]
for comp,doc in docs.items():
    for r in doc.translations:
        out.append(dict(c=comp,s=r.get("source") or "",t=r.get("target") or "",tag=r.get("source_tag"),sec=r.get("section")))
json.dump(out,open('.artifacts/i18n/term-completeness/entries.json','w'),ensure_ascii=False)
print(len(out))
