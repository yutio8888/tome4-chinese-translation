import pathlib,json
P=pathlib.Path('.ai/task/batch-35fcb3df1560de7c5b2d')
D={
'f7641a73':('confirmed',True,'timed_effects/other.lua:2614 CLOAK_OF_DECEPTION on_gain：斗篷在不死族身上制造幻象使其 appear human（看起来像人类，从而能进入人类城镇）；现译“看起来像活着一样”把“人类”换成“活着”，外观含义改变。整条修复为“看起来像人类”一类，#LIGHT_BLUE#/#Target#/%s 保持。'),
'f78b208a':('confirmed',True,'ingredients.lua 电鳗尾 desc：It doesn\'t much matter 意为“其实没多大关系”（紧接“最后十英寸左右就行”）；现译“没有确切的答案”语义改变。整条逐句核对后修复。'),
'f7bd4de1':('confirmed',True,'achievements/quests.lua:219：Freed Derth from the onslaught of the mad Tempest, Urkis.——现译“从风暴魔导师厄奇斯手里成功解救德斯镇”漏译 mad（疯狂的）与 onslaught（猛攻）。整条修复，Tempest 沿用本条现有“风暴魔导师”，不扩大为族内统一。'),
'f7dcde0d':('refuted',False,'class/Actor.lua:5754–5756：该日志仅在 turn_procs.forbid_instant_talents[ab.id] 已置位时输出，随后 return false 拒绝本次使用；译文补出“这回合无法再次使用”正是实现行为，不构成增译误导。'),
'f8180dfe':('confirmed',True,'general/objects/world-artifacts-far-east.lua:58 挂坠 desc：a hematite moon eclipsing a golden sun——赤铁矿（材质）之月遮蔽金色太阳；现译“红月吞日”丢失 hematite 材质与 golden。整条修复。'),
'f82b8760':('refuted',False,'talents/gifts/ooze.lua:250–270 Indiscernible Anatomy：passives 设 ignore_direct_crits=critResist；damage_types.lua:130–153 该属性按百分比削减暴击的额外倍率（reduce=(crit_power-1)*pct），并非按几率完全免疫。英文 info 与实现不符，现译“直接暴击的额外伤害降低 %d%%”贴合实现，判 refuted。'),
'f83a8191':('confirmed',True,'talents/misc/npcs.lua 腐化蒸汽 info：Corrupted vapour rises at the target location——现译“蒸腾目标区域”漏主语“腐化蒸汽”且把 rises at 误成及物“蒸腾”。整条修复，%0.2f/%d 与 \\n\\t\\t 保持。'),
'f894de79':('confirmed',True,'talents/gifts/ooze.lua Mitosis info：现译漏 within your line of sight（在视线内生成）、(limited by talent level and the summoning limit)、so long as this talent is active（仅在技能生效期间均摊），并把 take damage 缩窄为“受到攻击”。整条逐句核对后修复，占位符顺序与 \\n\\t\\t 保持。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review268-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==8,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 8 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
