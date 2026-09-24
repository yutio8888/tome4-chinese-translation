import pathlib,json
P=pathlib.Path('.ai/task/batch-cfd398e96c387cc31dc0')
D={
'f8a2eb71':('advisory',False,'general/objects/egos/wizard-hat.lua:62–64 ego 名 starseer\'s（现译“观星者的”）的检索关键词 keywords={starseers=true}；现译关键词“观星”与另一文件 keyword starseer=“观星者”不一致，但关键词仅作简短标签、不误导机制，记 advisory。'),
'f8a393e3':('confirmed',True,'quests/start-yeek.lua:23：You have been tasked to remove at least one of the threats to the yeeks.——任务列出两处威胁（Murgol 水下巢穴、ritch 隧道），完成任一即可；现译“清除……两大威胁之一”删去 at least，读作只需且只清除其中一个（删限定词类）。整条修复为“至少清除一个”一类；yeek 保持“夺心魔”（用户 2026-09-16 裁定）。'),
'f8b95de7':('refuted',False,'timed_effects/physical.lua:1868–1876 效果 IMPLODING 来自技能 Implode，本库技能名译“碎骨压制”（mod-tome.lua:27501），效果名“碎骨压制（减速）”、失去提示“-碎骨压制”同族一致；“+碎骨压制”沿用技能名，不构成错译。'),
'f8f18f94':('confirmed',True,'talents/gifts/gifts.lua:44 技能类别 eyal\'s fury 说明：Unleash nature\'s fury against foes around you.——现译“向敌人释放自然的愤怒”漏 around you（周围的敌人）。整条修复。'),
'f8f3b8de':('refuted',False,'talents/techniques/agility.lua:265–272 callbackOnArcheryAttack 仅在 hitted 为真时给予回合（if hitted and not target.turn_procs.rapid_fire and dist < 5）；英文未写命中条件，现译“命中敌人的远程攻击”贴合实现，驳回。'),
'f8f6be5a':('confirmed',True,'timed_effects/magical.lua:2672–2692 ARCANE_VORTEX：每回合从漩涡向视野内随机敌人发射 beam（eff.src:project type="beam"），路径上所有目标都受 %0.2f 奥术伤害（to all）；现译“随机对附近视野内的目标造成伤害”漏掉射线贯穿、对路径上全部目标生效。整条修复。'),
'f95b1ff4':('refuted',False,'birth/descriptors.lua：Roguelike or Adventure permadeath mode 指永久死亡设置中的 Roguelike 或 Adventure 两档；本库 birth descriptor 名 Roguelike=“永久死亡模式”、Adventure=“冒险模式”（mod-tome.lua:3261/3266），现译按两档名称并列，含义一致，驳回。'),
'f9686ee9':('advisory',False,'talents/techniques/unarmed-training.lua:54：(or with gloves or gauntlets)——手部栏只能装备一件，现译“手套和臂铠”不致误读为同时装备；“仅装备”略有增译但不改机制，记 advisory。'),
'f96caa47':('advisory',False,'quests/grave-necromancer.lua:33：You do not plan to fail as she did——“不打算重蹈覆辙”与现译“相信不会重蹈覆辙”为意图/信念的语感差异，二级措辞，记 advisory。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review269-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==9,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 9 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
