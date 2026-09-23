import pathlib,json
P=pathlib.Path('.ai/task/batch-88cfb30f797898ed8ef5')
D={
'ebc83778':('confirmed',True,'lore/trollmire.lua:40–45（624a6732）trollmire-note-2：get wind of me 是习语“察觉到我”，译文“掩住气味、不让他循迹找到我”按字面误作嗅觉追踪；且原文 "...ack again…" 段后与 "..." 前后各有一个空行（41/42/43/44/45 行），译文删去两处空行，属换行不变量缺陷。整条有界修复（保留两处空行，译为“不让他察觉到我”一类）。'),
'ebcb3ef0':('confirmed',True,'corruptions/torment.lua:132–159：callbackOnHit 判定 cb.value >= max_life * l / 100（含等于，基数为扣除 Blood Grasp 临时生命后的最大生命值）；译文“超过至少 %d%%”自相矛盾且“超过”排除等于。修为“至少 %d%% 最大生命值”一类。'),
'ec13c4e9':('confirmed',True,'general/events/rat-lich.lua:44–51：RATLICH_SKULL（subtype="skull"）未鉴定名 dusty rat skull，鉴定名 Skull of the Rat Lich 现译“鼠巫妖头骨”；“鼠骷髅”把头骨误作整具骷髅且与鉴定名不一致，dusty 为“落满灰尘的”而非“肮脏的”。修为“落满灰尘的鼠头骨”一类。'),
'eccfcfca':('confirmed',True,'dialogs/CharacterSheet.lua:1277–1300：Effect resistances 标题下每项显示 100-canBe 概率或 attr×100 的 0–100% 抵抗百分比，并非绝对免疫；译文“状态效果免疫”把部分抗性说成免疫，属保真缺陷。修为“状态效果抗性”。'),
'ecd90981':('advisory',False,'class/Actor.lua:2128 tooltip 中 "#0080FF#P. save#FFFFFF#:  " 后接数值；译文用全角冒号“：”本身提供视觉间距，同族 S. save / M. save（mod-tome.lua:157/159）同一约定，Accuracy/Defense 以全角空格对齐。属排版风格，无功能影响，记 advisory。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review257-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==5,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 5 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
