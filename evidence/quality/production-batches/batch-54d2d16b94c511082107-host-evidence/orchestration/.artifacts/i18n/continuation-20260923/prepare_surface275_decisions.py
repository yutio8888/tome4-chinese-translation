import pathlib,json
P=pathlib.Path('.ai/task/batch-54d2d16b94c511082107')
D={
'fe5a84a1':('confirmed',True,'spells/enhancement.lua 燃烧之手（Fiery Hands）：enhancement.lua:83–85（624a673）melee_project 火焰伤害作用于近战命中（含武器），体力回复为 stamina_regen_on_hit，仅命中时触发；现译第二行“每次攻击同时也会回复”把命中写成攻击（未命中也回复，一级 fidelity），首句亦漏“（及武器）”。修复：第一行补“双手（及武器）”，第二行改“每次命中”，%0.2f/%d%%、两处 LF+制表符保持。'),
'fe6310c9':('refuted',False,'egos/helm.lua ego 前缀 "bladed "：尾随空格用于英文拼接，中文 ego 译名“刀刃的”按本库拼接不保留空格（既往 ego 空格先例）。'),
'fe90619e':('confirmed',True,'corruptions/shadowflame.lua 恶魔空间（Fearscape）：原文 burn both of you … each turn，灼烧是持续每回合结算的光环（shadowflame.lua:219 设 level.demonfire_dam，zones/demon-plane-spell/grids.lua:23–26 熔岩地面 on_stand 每回合对站立者结算 DEMONFIRE）；现译“造成 %0.2f 火焰伤害”删去“每回合”，读作一次性伤害（删量词缺陷类，一级 fidelity）。另 When the spell ends 涵盖主动结束、目标死亡与活力耗尽，现译“当技能中断时”收窄，同句修为“法术结束时”。其余行与 LF+制表符不变。'),
'feba8a65':('refuted',False,'quests/orc-pride.lua：同组四条 You have destroyed Rak\'shor/Vor/Grushnak/Gorbat 本库一致作“你击败了X部落”（mod-tome.lua:20499–20505），部落名与目标行“拉克·肖部落”（20500）一致；指的是摧毁该部落据点/首领，“击败”可接受，属同族一致，不单改。'),
'fec0939b':('confirmed',True,'lore/last-hope.lua 黑暗者古尔莫特墓志铭：原文斜体诗三行（In this bright age / Of new adventures / You are not forgotten），现译合并前两行为一行，LF 由 6 变 5（换行不变量，一级）。修复：拆回三行，例如“在这光明的时代\\n在崭新的冒险中\\n你不会被遗忘”，#{bold}#/#{normal}#/#{italic}# 与其余 LF 保持。'),
'fec33d86':('refuted',False,'dialogs/LevelupDialog.lua "Max life: "：本库属性标签统一用全角冒号不留尾空格（既往冒号标签先例），非缺陷。'),
'fede357f':('refuted',False,'egos/mindstars.lua ego 前缀 "horrifying "：同 ego 空格先例，“恐惧的”按本库拼接，不保留空格。'),
'ff084e54':('refuted',False,'cursed/crimson-templar.lua：crimson-templar.lua:106 持续时间经 self:spellCrit(t.getDuration(...)) 计算，“持续时间可以暴击”正是实现所述（暴击即延长持续时间），非错译。'),
'ff47fb86':('confirmed',True,'init.lua 加载提示：原意是回复纹身效果持续数回合，因此可预判即将承受的伤害并提前使用；现译删去“预判伤害、提前准备”这一要点，改写成泛泛的“更加从容”（一级 fidelity），且物品名本库为“回复纹身”（mod-tome.lua:12070 entity name）而非“恢复纹身”。整句修复。'),
'ff585d0b':('confirmed',True,'quests/deep-bellow.lua 任务名 From bellow, it devours：同一短语在本库另一处作“来自深渊，吞噬四方。”（mod-tome.lua:38225，Deep Bellow=深渊咆哮），任务名却改成名词“地下吞噬者”，同一英文句两种不相容译法（跨条一致性/术语，一级）。修复为“来自深渊，吞噬四方”（任务名不带句号），与 38225 对齐。'),
'ff658fab':('confirmed',True,'world-artifacts.lua unided_name wispy purple cloak：wispy 指轻薄缥缈（同物系靴子 12911 行 wispy purple aura 作“紫色光环”），“脆弱的”义为易损，错译（一级 fidelity）。改“缥缈的紫色斗篷”一类。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review275-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==11,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 11 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
