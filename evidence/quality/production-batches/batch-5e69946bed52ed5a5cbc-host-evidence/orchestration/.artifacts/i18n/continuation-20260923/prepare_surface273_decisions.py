import pathlib,json
P=pathlib.Path('.ai/task/batch-5e69946bed52ed5a5cbc')
D={
'fc875950':('refuted',False,'egos/mindstars.lua entity keyword creative：同族 keyword 译法本就混用名词（horrifying=恐惧、hateful=仇恨、clarity=清晰），“创造力”与同族一致，非错译。'),
'fcb8219f':('confirmed',True,'class/interface/TooltipsData.lua Antimagic User 说明：The use of spells or arcane-powered equipment is impossible.——class/Actor.lua:5059、5139（624a673）反魔法技能设 forbid_arcane，奥术装备与法术被禁用，是硬性限制；现译“拒绝使用法术”把不能写成主动拒绝（一级 fidelity）。修复第三行为“无法使用法术，也无法使用奥术驱动的装备”一类，#GOLD#…#LAST#、3 个 LF 保持。'),
'fcf3c2b8':('refuted',False,'egos/wizard-hat.lua ego 后缀 " of the sentry"：前导空格用于英文拼接，中文 ego 译名“警卫之”按本库前缀式拼接，不保留空格（既往 ego 空格裁决先例）。'),
'fd22f1b0':('refuted',False,'class/Object.lua "Life regen: "：本库同类属性标签统一用全角冒号且不留尾空格（如“生命回复：”），显示无粘连，非缺陷。'),
'fd267689':('confirmed',True,'world-artifacts.lua:1134 领袖的皇冠（Crown of Command）描述：many disappeared without a trace into his numerous prisons——现译“这些人大部分都…消失了”把 many 夸大为“大部分”（一级 fidelity，数量限定被改）；另 ruled over the Nargol lands 译“纳格尔大陆”不当，Nargol 是半身人王国（本库 3794、3848 行“纳格尔半身人王国”）。整条修复：数量改“许多人”，“纳格尔大陆”改“纳格尔的领土/国土”一类，其余逐句对照。'),
'fd2afcd1':('refuted',False,'birth/classes/rogue.lua Cunning：本库属性名 Cunning=灵巧（mod-tome.lua:42158、43205），与属性面板一致，非错译。'),
'fd2e4f52':('refuted',False,'timed_effects/magical.lua Host of a Rime Wraith (Gelid Host)：Rime Wraith 本库技能名为“远古冰魂”（29441、35785），Gelid Host=霜寒宿主（29465），效果文本沿用技能名；改名属跨条命名决定，不在本批范围。'),
'fd365b0b':('refuted',False,'class/Actor.lua #0080FF#M. save#FFFFFF#:  ：同组 P. save/S. save（155、157 行）均为全角冒号不留空格，面板对齐一致，非缺陷。'),
'fd635c58':('refuted',False,'techniques/munitions.lua Alloyed Munitions：“%d%% 自然武器伤害”为本库同类写法（共 4 处）；末句 armor penetration 在 munitions.lua:432–446 实为 getArmorSaveReduction（护甲与豁免削减），现译“护甲和豁免削减”贴合实现（上游措辞与实现不一致的先例），驳回。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review273-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==9,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 9 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
