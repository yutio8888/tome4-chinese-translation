import pathlib,json
P=pathlib.Path('.ai/task/batch-6b8acfddd3cc0c11f471')
D={
'ef213285':('refuted',False,'成就说明：本库 birth descriptor 译名 Roguelike=永久死亡模式、Adventure=冒险模式（mod-tome.lua:3260/3265），二者即两种 permadeath 设置；“永久死亡或冒险模式”与原文一致，不存在遗漏限定。'),
'ef3dcead':('advisory',False,'birth/races/human.lua:134 Higher 种族描述：other Humans 字面为“其他人类”，“普通人类”带出高等人自视高人一等的语气但所指相同（高等人以外的人类），不误导；可选改“其他人类”。'),
'ef608e1d':('advisory',False,'talents/gifts/mucus.lua Oozewalk：在黏液上移动并清除负面效果；“粘液探戈”为既有技能名意译（全库 1 处），风格取舍，不影响机制；可选改“黏液行走”一类，属技能名族级决定，本批不改。'),
'ef7d5a43':('refuted',False,'chats/jewelry-store.lua:168 珠宝师对话：本库 amulet 物品类别统一译“项链”（mod-tome.lua:11310 entity subtype amulet=项链），与装备栏一致；改“护身符”反而与物品类型不一致。'),
'ef88e6a8':('advisory',False,'talents/chronomancy/anomalies.lua:1638 异常 message：随机目标获得加速、再生与痛苦抑制，odds have tilted 为“形势/胜算发生了倾斜”，“几率发生了倾斜”偏字面，但战斗日志风味文本，不误导；可选改“形势发生了倾斜”。'),
'ef9f97a2':('confirmed',True,'talents/psionic/psi-archery.lua:50 Guided Shot（psionic/psi-archery）：with precise telekinetic nudges 是念力微调导引箭矢的心灵异能方式，译文“射出一支导引箭精确的飞向敌人”删去念力、改写成箭自带导引，且“精确的”应作“精确地”。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（完整性）；数值部分（atk 与 crit_chance 同加 shot_boost）无误。整句修复。'),
'efe21d07':('confirmed',True,'general/npcs/canine.lua:62 巨狼描述：snaps at you 是朝你猛咬、扑咬，译文“咆哮”把动作误译为吼叫；prowls 为潜行逡巡。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（动作误译）。整句修复。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review260-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==7,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 7 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
