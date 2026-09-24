import pathlib,json
P=pathlib.Path('.ai/task/batch-54be748f9582a3f09434')
D={
'fc0f5daa':('confirmed',True,'talents/psionic/psionic.lua:49（624a673）技能系 Thought-Forms（思维形态）说明：Manifest your thoughts as psionic summons.——该系技能召唤思维形态实体，psionic summons 指灵能召唤物；现译“灵能召唤术”把召唤物写成召唤技能（一级 fidelity）。修复为“使你的思维具象化为灵能召唤物”一类。'),
'fc3dc9f6':('confirmed',True,'lore/misc.lua:86–90 起 letter to Weisman (1)：现译把 bloated, oozing and chittering horror / the giant ants\' repulsive progenitor 改写为“最犀利最凶猛的生物”“史前巨型白蚁…蚁王”，漏 Such pluck and derring-do，并把第三段拆成两段、末尾署名前少一个空行，LF 10→9（一级 fidelity + 换行不变量）。整条逐段重译，段落与空行对齐原文；地名用本库译名 Old Forest=古老树林、Derth=德斯。'),
'fc5311ff':('confirmed',True,'general/objects/world-artifacts.lua:5675–5683 The Titan\'s Quiver（泰坦的箭袋）描述：现译漏 honed to a vicious sharpness 与 appear to be nearly unbreakable 两个分句，并把 They seem more like spikes than any arrow you\'ve ever seen 压成“不，与其说是箭，不如说是长钉”（一级 completeness）。整条逐句修复。'),
'fc60ee27':('confirmed',True,'zones/sandworm-lair/objects.lua 阿塔玛森的红宝石眼睛描述：原文 1 个 LF，现译在第二、三句之间多加 1 个 LF（一级换行不变量）；且漏 managed to deal a crippling blow（给兽人以重创）。修复：恢复 1 个 LF，末句补“重创兽人”，阿塔玛森、吞噬者加库尔、烈火纪保持。'),
'fc753883':('confirmed',True,'quests/love-melinda.lua 任务结局日志 Melinda died to a Yaech raiding party at the beach.——现译漏 raiding party（袭击队伍），读作零星遭遇（一级 completeness）。修复为“梅琳达在沙滩上死于夺魂魔袭击队之手”一类；Yaech 保持本库既定“夺魂魔”（mod-tome.lua:9037、39138）。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review272-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==5,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 5 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
