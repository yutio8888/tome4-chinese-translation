import pathlib,json
P=pathlib.Path('.ai/task/batch-b1809d747f471912638d')
D={
'f009c2b1':('pending',False,'damage_types.lua:1006 时间伤害 death_message 列表中的 grandfathered（祖父悖论梗）；现译“因弹指间度过了无数美好的青葱岁月，转瞬间你已白发苍苍”为大幅改写。死亡描述词表整族已由用户 2026-09-16 裁定继续 pending；contextual 另证 PartyDeath.lua:71 将其代入第三人称死讯模板（mod-tome.lua:1412“玩家%s……%s而死”），现译含“你”致人称错位，作为该族新证据补充登记待用户审阅，本批不单独修改。'),
'f09f7b5b':('pending',False,'talents/corruptions/scourge.lua:25 技能 Virulent Strike（short_name REND，双持两击并延长目标疾病持续时间）；现译“撕裂”沿用旧名 Rend，未体现 virulent（致病/剧毒）。改技能名需同步日志 You cannot use Virulent Strike without two weapons!（mod-tome.lua:22961），且“撕裂”族另有 Lacerating Strikes=撕裂挥击 等；属技能名命名决定，列入待用户审阅。'),
'f0ba5e1e':('advisory',False,'quests/shertul-fortress.lua:114 gain_energy：能量由玩家（经转化箱）送往堡垒，sent 为“送来/输送”；“收集了”方向略偏且增“尽快”，但门槛与后续动作（回堡垒升级回归之杖）无误，不误导；可选改“已经送来了足够的能量”。'),
'f0d4b3e8':('confirmed',True,'lore/misc.lua:230 半身人创世论：No, clearly other gods were responsible, lesser gods than our own which copied his grand design 意为“显然是其他神明造了他们，那些次于我们之神、模仿其宏伟设计的次等神明”；现译“其他创造者也很负责，但比起我们的创造者来差了一些”把 responsible（为之负责/造成）误作“尽职负责”，并漏掉模仿其宏伟设计。整句（含 fudging fingers and inelegant touches 下一句）对照修复。'),
'f0fdd62c':('confirmed',True,'zones/halfling-ruins/npcs.lua:91 紧急召回：对方 Wayist 刚传讯“我已经完了，你还能自救”，玩家启动回归之杖 vowing to come back later；现译增“救他”，与“我已经完了”的语境相悖且无原文依据，“答应”也弱于 vowing。改为“发誓日后再回来”一类。'),
'f1117764':('advisory',False,'zones/ruined-dungeon/grids.lua:111 Strange Orb 血之传送门提示：orb 全族（39547–39578）统一译“水晶球”，属既有族内一致译法；thick（浓稠）被省略为轻微风味损失，不误导；可选改“水晶球上淌着浓稠的鲜血”。'),
'f11d3485':('advisory',False,'talents/corruptions/vile-life.lua 转移负面状态：实现筛选 e.type=="physical" or e.type=="magical" 且 detrimental；“物理与魔法负面状态”为类别并列，中文读作两类状态均可，不误导机制；可选改“物理或魔法负面状态”。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review261-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==7,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 7 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
