import pathlib,json
P=pathlib.Path('.ai/task/batch-73136994056fb59bf591')
D={
'ee26d955':('refuted',False,'zones/town-last-hope/traps.lua:111–115：Rich merchant 是 BASE_STORE 地图入口实体（MELINDA_FATHER，chatfeature last-hope-melinda-father，门图 shop_door_barred），与同文件 "Home of Ungrol the Alchemist" 同类，指富商宅邸门；“富商的家”贴合地图实体语境。'),
'ee27cabc':('refuted',False,'damage_types.lua:2202–2230 ITEM_ACID_CORRODE：tdesc “chance to reduce armor by %d%%”，projector 施加 EFF_ITEM_ACID_CORRODE 降低护甲；“物品腐蚀护甲”与机制一致。'),
'ee32b186':('advisory',False,'talents/psionic/psionic.lua:44 psionic/dream-smith 技能树描述；梦境锻造树召唤的锤即“梦之巨锤”，未体现 forge 属风格取舍，不误导；可选改“召唤梦境熔铸的巨锤”。'),
'ee3d073a':('confirmed',True,'timed_effects/other.lua:4184 Self-Judgement 流血致死的 special_death_msg：well-deserved death 意为“罪有应得的死”，译文“死得其所”（死得有价值）语义评价相反。改“因失血过多而死，罪有应得”一类；不涉及死亡描述词表的增添意象问题。'),
'ee4b54c6':('advisory',False,'lore/misc.lua:156 Rolf 致 Weisman 信：do not go after that... that thing 为“别去追/找那东西”，译文“不要回去和那东西战斗”加了“回去”、略去吞吐语气；主旨（劝其别去对付那东西）未误导。'),
'ee646924':('confirmed',True,'talents/spells/stone.lua:79–132 Body of Stone：transform your flesh into stone 译成“融入石头”偏义；“Reduces the cooldown … by %d%%” 译为“冷却时间回合数：%d%%”把百分比缩减写成回合数（getCooldownReduction 为百分比，cd_recution=cdr*cooldown/100）。移动打断部分：never_move 下仅可能被强制移动，Actor.lua:1486 任一 moved 即关闭，译文“任何移动会打断”功能等价，但宜随整句修回“任何强制移动都会终止此效果”。整句修复。'),
'ee6fdad7':('advisory',False,'lore/misc.lua:682 召唤凤凰卷轴：A few fireballs at the vial 为“朝瓶子放几个火球（加热）”，译文“往瓶子里放几个小火球”方向偏差、“小”为增添；风味文本，不影响玩法。'),
'ee7affcb':('confirmed',True,'general/objects/wands.lua:30 魔杖类型描述：made by powerful Alchemists and Archmagi to store spells，译文“被炼金术师和大法师用来储存法术”漏 made（制造者）与 powerful，改写为使用者，信息错位。改“魔杖由强大的炼金术师和大法师制造，用来储存法术。任何人都可以用它释放其中的法术。”一类。'),
'eea3b16d':('confirmed',True,'techniques/grappling.lua:120–147 Crushing Hold：slow 经 startGrapple 合并为抓取附加效果，GRAPPLED 效果以 global_speed_add -eff.slow 实现（physical.lua:1475）；“Reduces global action speed” 译为“目标减速”丢失机制名，冻结术语 combat.tsv:137 global action speed=全局速度（preferred，tformat）。与 contextual 同向，宿主由 advisory 改判 confirmed 一级术语缺陷；随整句补“每次抓取”，并修 #RED# 后多余空格。'),
'eeb95697':('advisory',False,'timed_effects/magical.lua:2105–2106 ABYSSAL_SHROUD on_gain/on_lose：feels closer to the abyss 为“感到更接近深渊”，“堕入了深渊”稍过，但与 on_lose “逃离了深渊”（mod-tome.lua:35276）成对，战斗日志风味，不误导。'),
'eecb4b05':('refuted',False,'class/Object.lua:1859 compare_fields 标签：中文标签以全角冒号结尾不带空格是本库惯例（同形 "…: "→"…：" 共 251 条），全角冒号自带视觉间隔，显示无问题。'),
'eef71452':('refuted',False,'load.lua:135–136 第二武器套装 inventory 描述：键名写作大写 X 是中文键位惯例，指同一按键，不暗示 Shift；不改变操作。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review259-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==12,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 12 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
