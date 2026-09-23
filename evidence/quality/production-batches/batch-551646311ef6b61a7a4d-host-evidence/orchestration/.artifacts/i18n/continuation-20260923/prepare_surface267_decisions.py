import pathlib,json
P=pathlib.Path('.ai/task/batch-551646311ef6b61a7a4d')
D={
'f6a545d0':('confirmed',True,'talents/celestial/sunlight.lua:69 技能名 Sun Flare（光系球形爆发，致盲并造成光伤）；flare 为“耀斑”，现译“日珥闪耀”的日珥（prominence）是另一种太阳现象。全库“日珥”“耀斑”各仅此一处，无引用同步与冲突，改为“太阳耀斑”一类属单条纠错而非全局重命名。'),
'f6cc31f2':('pending',False,'damage_types.lua:909 枯萎伤害 death_message 列表中的 debilitated by noxious blight before falling；现译“死前吸入过多剧毒瘴气”增出“吸入/过量”。死亡描述词表整族已由用户 2026-09-16 裁定继续 pending（pending-user-review 第 13 项先例），单改一条会造成族内不一致，列入待用户审阅。'),
'f6e111a3':('confirmed',True,'talents/techniques/agility.lua:71 盾牌敏捷格挡：delayedLogDamage 显示被抵消的伤害量 ("%s(%d deflected)#LAST#"，lastdam - dam)；现译“(%d 敏捷防御)”把偏转量说成防御名称。改为“(%d 被偏转)”一类，%s/%d 与 #LAST# 保持。'),
'f6e9cd9b':('refuted',False,'dialogs/CharacterSheet.lua:225 免疫表列标题：英文末尾空格仅为与 Physical Status 等宽对齐；同族 All Status/Mental Status 的英文填充空格在中文译文中同样去掉（mod-tome.lua:41361–41363），中文标签等宽，不存在拼接失距。'),
'f6eae8d3':('confirmed',True,'lore/blighted-ruins.lua:27 原文为单段连续文本（0 个 LF），现译在首段后插入 \\n\\t（一级换行不变量）。整条修复：删去该换行与制表符，其余逐句对照。'),
'f6f9c010':('confirmed',True,'birth/classes/psionic.lua:139 Solipsist 职业说明引语：the world is the collective dream of those that live in it（世界是其居民共同的梦）；unlock the potential of your dreams（发掘你梦境的潜能）。现译“由许多个梦境组成”“打开通往梦境之门”偏离原意。整条修复。'),
'f72ac3de':('confirmed',True,'talents/psionic/charged-mastery.lua:119–122 静电网：add %0.1f additional Lightning damage to your next attack for each turn you spend within its area——每在网中停留一回合累加一次；现译漏“每停留一回合”，读作固定一次加成（删限定词类缺陷）。整条修复，%d/%0.1f/%d%% 顺序与 \\n\\t\\t 保持。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review267-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==7,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 7 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
