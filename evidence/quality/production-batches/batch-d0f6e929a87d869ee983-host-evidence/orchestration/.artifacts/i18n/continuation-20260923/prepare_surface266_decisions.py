import pathlib,json
P=pathlib.Path('.ai/task/batch-d0f6e929a87d869ee983')
D={
'f58a8172':('confirmed',True,'general/objects/world-artifacts.lua:5010 Telekinetic Core desc：This heavy torque appears to draw nearby matter towards it——“似乎”吸引附近物质；该物品被动并不牵引物体（仅 use_talent T_PSIONIC_PULL 主动使用），现译“将周围的所有物体拉向它”删去 appears 并增“所有”，把外观描述说成确定的机制。整条修复。'),
'f5928e33':('confirmed',True,'general/npcs/horror.lua:264 eldritch eye desc：bloodshot eye 为“充血/布满血丝的眼睛”（本库同族 a bloodshot eye=充血的眼球、Small and bloodshot=小而充血）；现译“带血的小眼睛”误作沾血。整条修复。'),
'f5d4f8ef':('confirmed',True,'talents/spells/death.lua:241–242：At level 3 the thrill of the death invigorates you（击杀触发 EFF_DEATH_RUSH）指杀戮/死亡带来的快感；现译“对死亡的渴望”意为渴求死亡，语义相反。整条修复，%0.1f/%d/50%% 与 \\n\\t\\t 保持。'),
'f5f90d5b':('confirmed',True,'dialogs/GameOptions.lua:672：Version checks: Addons will not be checked for new versions——只是不再检查插件新版本；现译“插件版本更新：无法更新插件的版本”误称插件不能更新（上一条明言仍可手动安装）。整条逐句核对后修复。'),
'f603e1fb':('confirmed',True,'talents/spells/spells.lua:32 spell/temporal 类别说明 The school of time manipulation. 指操控时间的法术学派；现译“学习操控时间。”误作学习行为。整条修复（同族 Conveyance is the school of travel 现译“学习传送”属另一条，本批不扩）。'),
'f603f432':('refuted',False,'objects/egos/mindstars.lua:745 hungering 心灵之星：who 以取自 target 的精神能量喂养自己的心灵之星（随后对 target 造成精神伤害并回复 psi/hate）；现译“%s用%s%s吸收%s的精神力量”表达能量从目标流入心灵之星，方向一致，占位符顺序与原文相同，不构成反向。'),
'f6060b57':('confirmed',True,'achievements/quests.lua:267 成就 Savior of the damsels in distress（MELINDA_SAVED：Saved Melinda from her terrible fate in the Crypt of Kryl-Feijan）；Melinda 是被邪教掳去献祭，不是迷路；damsel in distress 为“落难少女”，现译“迷路少女拯救者”误导。整条修复。'),
'f62d40cf':('confirmed',True,'zones/ardhungol/objects.lua:43 Rod of Spydric Poison 未鉴定名 poison dripping wand；本库 wand 统一译“魔杖”（entity subtype wand=魔杖，榆木/白蜡/紫杉魔杖等），现译“枝条”不符物品类别。整条修复。'),
'f66c15e3':('advisory',False,'talents/cursed/shadows.lua:410：Call Shadows 在已有阴影未达上限时每次尝试再召唤一个，仇恨不足 5 时记此日志；现译“无法召唤阴影”未写“再/另一个”，语境中仍可理解，不误导机制，记 advisory。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review266-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==9,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 9 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
