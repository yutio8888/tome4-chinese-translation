import pathlib,json
P=pathlib.Path('.ai/task/batch-f740e6898e8b430ca79f')
D={
'12ff2c09':('refuted',False,'discharge.lua:69–81 超额飞弹循环 for i=1,min(p.overcharge,getTargetCount) 每次 rng.table(tgts_oc) 后 table.remove，同一目标本回合至多一枚，总数受目标数上限约束。译文“每个目标至多 1 枚、总数不超过 %d”与实现一致，并非新增限制。'),
'e00b2a8b':('refuted',False,'dirge.lua:165 callbackOnTemporaryEffectAdd 仅在 e_def.status=="detrimental" and e_def.type~="other" and eff.src~=self 时触发。译文的“非自身施加、且不属于其他类型”与固定源码实现一致，属窗口7修复后贴合实现的表述。'),
'e8fc5b0a':('confirmed',True,'cursed.lua:22 endless-hunt 技能树描述：Each day, you lift your weary body and begin the unending hunt。译文“你不知疲倦无时无刻狩猎你的下一个目标”把疲惫的身体反转为不知疲倦，并丢失每天起身开始无尽狩猎的意象，意义相反，需修复。'),
'e90949f9':('advisory',False,'quests.lua:337–340 ALL_DREAMS 成就为完成 Dogroth Caldera 全部梦境；Dreaming my dreams 为歌名式标题。译文我的梦就是你的梦属标题意译，不影响成就条件或机制，保留命名建议，不强制修复。'),
'e92433bc':('refuted',False,'所附 observation（资源被缩窄为能量）与本条 unlock-yeek 文本无关，是同 lane 上一条 e923d2b8 的错位。本条 cunning 译灵巧与术语库 combat.tsv Cunning=灵巧（stat name）一致，不构成错误。错位目标另见 HOST additional observation。'),
'e9253668':('confirmed',True,'所附 observation（cunning 译灵巧）属上一条 yeek 的错位；但本条 misc.lua:530–545 Thalore 诗句自身有独立缺陷：Once flowers rose to reach the sky 被译为曾经炽热的复仇火焰染红天空，把花朵高耸误写成复仇火焰，改变诗意与意象（与下句 blossoms、thrush and owl 同为昔日繁盛），经宿主独立核验确认需修复。'),
'e928ce2c':('refuted',False,'所附 observation 描述 Thalore 诗句，与本条 blighted-ruins objects.lua:67 A paper scrap, left by the Necromancer 无关，为错位；本条译文一张死灵法师留下的纸片准确。'),
'e9517394':('refuted',False,'damage_types.lua:4012–4040 BLIGHT_POISON 按 dam.poison 取 rng.range(1,n)，在基础毒与已解锁的阴险/麻痹/致残毒素中等概率选一施加。译文中毒几率在可能的毒素效果中平分，表达各效果机会均等，与实现一致。'),
'e9884825':('advisory',False,'misc.lua:505–509 races-10 为 Loremaster Greynot 的种族分析第11章，作者以第一人称撰写分类（同系列 Demons 章 I feel the need to describe）。译文补我把龙列为智慧种族在该语境可成立；单独列出为轻微增译，只记建议。'),
'e992e871':('refuted',False,'daikara/npcs.lua:34–37 RANTHA_THE_WORM type="dragon" subtype="ice"，desc 称 Dragons are not all extinct；Worm 即 wyrm 龙称，巨龙兰莎符合实体身份。'),
'e99aa6d6':('advisory',False,'lore/fun.lua:37 rogue-poem 随机传说物品名，为双关玩笑标题。译文盗贼在你身后传达背后偷袭意象，未译出 do it 的双关，属标题风格建议，不影响机制。'),
'e9a9aef2':('advisory',False,'magical.lua:2172–2185 SPELLSHOCKED 为有持续时间的 detrimental 状态，addTemporaryValue 全抗性 -power。译文省略 temporarily，但状态本身带时限显示，不构成永久化误导；可补暂时，记建议。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review254-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==12
extra=[dict(revision_key='e923d2b8d0b9da723ca5a9accc6bdaec2314e3b10deeea0fd4d8dd258ff711fe',source='The target is using talents without consuming resources.',target='目标使用技能时不再消耗能量。',disposition='advisory',note='surface lane-000-1 的 observation 错位挂到下一条；本条 surface 判 OK、无 accepted observation，不能加裁决键。resources 被译为能量略窄（能量非资源通称术语），记为宿主补充建议，本批按 done，后续批次或维护者可重新覆盖。')]
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=dict(lane='lane-000-1',entries=['e92433bc','e9253668','e928ce2c'],fact='observations for lane indexes 14,15,16 were attached to 15,16,17 (off by one), verified by native tool call 3 of lane-000-1 which built the output from an index dict'),rows=rows,additional_host_observations=extra),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory')})
