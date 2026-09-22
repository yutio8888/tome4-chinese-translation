import pathlib,json
P=pathlib.Path('.ai/task/batch-ba766c90924912867b02')
D={
'e803':('confirmed',True,'plague.lua:20–38 按 e.subtype.disease 枚举全部疾病，Cyst Burst:128–168 逐项传播；译文额外限定四种疾病缩小适用范围。'),
'e823':('refuted',False,'physical.lua:1076–1090 MIGHTY_BLOWS 获得状态增加 combat_dam，失去时对应 less menacing；更具威胁符合状态变化语境。'),
'e827':('advisory',False,'GameOptions.lua:150–166 此说明附于 HUD 选择列表，界面风格在界面中仍明确标识选择内容；补选择可提升完整措辞，但不改变选项功能，不据孤立动词遗漏强制修复。'),
'e82c':('refuted',False,'zemekkys.lua:120–146 备齐材料后 prepare portal 的实际后续为 create_portal 任务；准备制造传送门符合具体动作，无额外能力或条件。'),
'e82dab':('confirmed',True,'world-artifacts.lua:2770–2776 Gravitational Staff 的实物外观明确 massive tip；译文仅尖端，遗漏粗大这一独立形态信息。'),
'e83a':('confirmed',True,'timeline-threading.lua:do_instakill 在抹除后日志 this never happened，紧接死亡处理；过去从未发生被译成也不会发生，改变时间方向。见 HOST-SOURCE-ADDITIONAL。'),
'e840':('advisory',False,'cursed/gloom.lua:95–139 Weakness 为 gloom 分支技能，弱化敌人伤害；黑暗衰竭为专名意译，无绑定术语正文要求 Weakness 必须虚弱。更名涉及命名偏好，不自动全局改名。'),
'e843':('refuted',False,'Object.lua:425–430 power 的实际格式参数是武器 c.dam 与 c.dam*c.damrange 的伤害区间，因此译成伤害正确。'),
'e859824':('advisory',False,'原文 tome 的典籍语气比册子厚重，但当前语境无页数、体积或机制约束；册子仍指书册，词体优化保留建议，不强制判为小册子实体错误。'),
'e85e4d':('refuted',False,'冻结术语 combat.tsv daze 明确眩晕，stun 为震慑；agility.lua 施加 EFF_DAZED。审核将普通英语推断覆盖游戏状态术语，撤销该意见。'),
'e862':('refuted',False,'cunning/cunning.lua tools 为 artifice 配套工具；artifice.lua:25–62、216–245 为潜行者暗刃等诡计工具及 Master Artificer 掌握关系，非通用工匠锻造分类。当前相关技能名诡计大师支持该语境称呼，不能据脱离角色的词典义判错。'),
'e873':('advisory',False,'generic save spell 为内部通用物品标签，中文额外词间空格不改变语义，无运行或规定空白不变量被破坏；可作排版建议，不自动改动。'),
'e882':('confirmed',True,'discharge.lua:54–81 发射 MIND 弹体并扣除 Feedback；灵能值球误引入资源值含义。原文3LF/6TAB、译文4LF/8TAB，额外一段及缩进违反格式不变量。修复同时恢复客观格式，见 HOST-FORMAT-COMPARISON。'),
'e8959a':('confirmed',True,'dirge.lua:175 现有护盾 power 累加、dur=max(existing,eff.dur)，可增加护盾持续时间；译文仅强化，遗漏延长持续时间及适用条件。'),
'e895fea':('confirmed',True,'elixir-ingredients.lua:153–162 明确 spinneret，带吐丝孔的巨蛛摘取部位。Australian Museum 将 spinnerets 与 silk glands 区分；丝腺误指产丝腺体，应恢复吐丝器官语义。主来源及固定源码见 HOST-SPINNERET-REFERENCE、HOST-SOURCE-SUPPLEMENTAL；不在本裁决授权全局替换相关名称。'),
'e8a956':('refuted',False,'冻结 terminology/talents.tsv 的 Probability Travel 明确 preferred 次元移动，notes 要求技能/状态/异常名称统一；本条符合已授权术语。'),
'e8b5':('refuted',False,'magical.lua:3355–3398 LIGHT_BURST 为作用于持有者的有益状态，邻接速度效果明确 The target；英文 The is 缺词，中文补目标由状态主体支持。'),
'e8b90':('refuted',False,'GameOptions.lua:397–405 开关 fullscreen_confusion，Player.lua:497–501 据混乱/睡眠启用 blur shader；实际为全屏画面效果，非通知消息流，全屏混乱效果准确。'),
'e8bc936':('confirmed',True,'damage_types.lua:778 将 eviscerated 列为物理死亡描述；词义指取出内脏/剖腹，不限定心脏。译文被掏心错误缩窄受创器官，应恢复剖腹/内脏意象。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260922/review253-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   match=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(match)==1
   d,repair,why=match[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=repair,conclusion=why))
assert len(rows)==19
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations will be adjudicated separately',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory')})
