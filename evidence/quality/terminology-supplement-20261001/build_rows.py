import json,csv,collections
E=json.load(open('.artifacts/i18n/term-completeness/entries.json'))
C=json.load(open('.artifacts/i18n/term-completeness/candidates.json'))
cand={(c['source'],c['tag']):c for c in C}
D={'ashes-urhrok','cults','items-vault','orcs','possessors'}
def scope(src,tag):
    cs={x['c'] for x in E if x['s']==src and x['tag']==tag}
    if not cs: return None
    return 'dlc' if cs<=D else ('core' if not cs&D else 'multi')
def tgt(src,tag):
    ts={x['t'] for x in E if x['s']==src and x['tag']==tag}; assert len(ts)==1,(src,tag,ts); return ts.pop()
rows=[]  # file, source,target,category,domain,tag,status,scope,notes
def add(f,src,tag,cat,dom,status,notes,target=None,sc=None):
    t=target or tgt(src,tag); s=sc or scope(src,tag)
    rows.append([f,src,t,cat,dom,tag,status,s,notes])
# --- talent names cited in other texts
REVIEW_T={
 'Antimagic Shield':'技能说明引用中另有“反魔盾”（1/2 处）；待统一',
 'Mana Gale':'游戏提示与越层效果说明中写作“法力风暴”（4/4 处引用）；待统一',
 'Telekinetic Punt':'学习提示中写作“念力推送”（2/2 处引用）；待统一',
 'Hidden Blades':'技能使用提示中写作“隐藏刀片”（1/3 处）；待统一',
 'Saw Wheels':'技能说明引用中写作“链锯轮”（1/2 处）；待统一',
 'Aether Avatar':'技能说明引用中写作“以太形态”（1/4 处）；待统一',
 'Deeprock Form':'技能说明引用中写作“深岩元素形态”（1/3 处）；待统一',
 'Hideous Visions':'虚空之声说明中写作“失智冲击”（1/2 处）；待统一',
 'Burning Wake':'放电柱类技能说明中写作“无尽之炎”（2/5 处）；待统一',
 'Called Shots':'标记说明中写作“精巧射击”（1/3 处）；待统一',
 'Steamgun Mastery':'炮台说明中写作“蒸汽枪精通”（1/3 处）；待统一',
 'Avatar of a Distant Sun':'职业进阶提示中写作“遥远太阳的化身”（1/4 处）；待统一',
}
NOTE_T={
 'Fire Drake':'召唤技能名；说明中指代召唤生物本身时写作“火龙”，不带“召唤：”',
 'Ritch Flamespitter':'召唤技能名；说明中指代召唤生物本身时写作“喷火里奇”',
 'Stone Golem':'召唤技能名；说明中指代召唤生物本身时写作“岩石傀儡”',
 'War Hound':'召唤技能名；说明中指代召唤生物本身时写作“战争猎犬”',
 'Night Terror':'技能名；被召唤的生物“暗夜恐魔”是另一实体，不混用',
 'Sand Shredder':'技能名；物品 Stralite Sand Shredder 译“斯莱特掘沙者”，不混用',
 'Kinetic Shield':'Spiked Kinetic Shield 是另一技能，不按本行要求',
 'Charged Shield':'Spiked Charged Shield 是另一技能，不按本行要求',
 'Healing Nexus':'状态名 Healing Nexus Redirection 另译“治疗被转移”',
}
for c in C:
    if c['kind']!='talent': continue
    s=c['source']
    if s in REVIEW_T: add('talents','%s'%s,'talent name','T.GAME.TALENT','talents','review',REVIEW_T[s])
    else: add('talents',s,'talent name','T.GAME.TALENT','talents','existing',NOTE_T.get(s,''))
# single-word talent names used as mechanics in text
add('talents','Stealth','talent name','T.GAME.TALENT','talents','existing','技能名；说明中的潜行状态与潜行强度同用“潜行”')
add('talents','Gloom','talent name','T.GAME.TALENT','talents','existing','黑暗光环持续技能；地名 Heart of the Gloom 为“黑暗之心”，不按本行')
add('talents','Radiance','talent name','T.GAME.TALENT','talents','existing','光辉光环技能；叙事中的普通 radiance 不按本行')
add('talents','Invisibility','talent name','T.GAME.TALENT','talents','existing','技能名；说明中 invisibility power 另有“隐身强度”写法，待一致性复核')
# --- mechanic words in text
add('combat','Accuracy','tformat','T.GAME.STAT','combat','existing','技能与物品说明中的命中属性（93/93 处一致）；面板标签 Accuracy: 另行记录',target='命中',sc='global')
add('combat','Defense','tformat','T.GAME.STAT','combat','existing','技能与状态说明中的闪避属性（50/53）；专名 Automated Defense System“自动防御系统”不按本行',target='闪避',sc='global')
add('combat','critical','tformat','T.GAME.STAT','combat','existing','暴击机制（169/175）；critical chance“暴击率／暴击几率”；“go critical”“critical point”等普通用法不按本行；现有 1 处“爆击”为错字待修',target='暴击',sc='global')
add('combat','talent level','tformat','T.GAME.STAT','combat','existing','技能说明中的技能等级；句式中可写作“等级 N 时”“技能 N 级时”',target='技能等级',sc='global')
add('combat','Physical save','_t','T.GAME.STAT','combat','existing','物理豁免；并列“physical, spell and mental save”可合写“物理、法术、精神豁免”')
add('combat','Spell save','_t','T.GAME.STAT','combat','existing','法术豁免；并列时可合写')
add('combat','Mental save','_t','T.GAME.STAT','combat','existing','精神豁免；并列时可合写')
add('combat','Melee','_t','T.GAME.STAT','combat','existing','近战（208/232 处）；界面术语说明中有“近身”写法')
add('combat','Armour Hardiness','_t','T.GAME.STAT','combat','existing','护甲强度（20/20 处一致）；与 Armour“护甲值”区分')
add('combat','Feedback','_t','T.GAME.RESOURCE','combat','existing','灵能反馈资源（说明中 32/32 处含“反馈”）')
# --- proper names
P=[('society','Archmage Tarelion','T.PN.PERSON','existing',''),
 ('society','Berethh','T.PN.PERSON','existing',''),('society','Caldizar','T.PN.PERSON','existing',''),
 ('society','Celia','T.PN.PERSON','review','墓地任务对话中写作“塞莉娅”（1/10 处）；待统一'),
 ('society','Elandar','T.PN.PERSON','existing',''),('society','Kryl-Feijan','T.PN.PERSON','existing',''),
 ('society','Norgan','T.PN.PERSON','existing',''),('society','Protector Myssil','T.PN.PERSON','existing',''),
 ('society','Slasul','T.PN.PERSON','existing',''),('society','Walrog','T.PN.PERSON','existing','主游戏与 Ashes 同名水中恶魔'),
 ('society','Harkor\'Zun','T.PN.PERSON','review','物品描述中写作“哈克祖”（1/4 处）；待统一'),
 ('society','Outpost Leader John','T.PN.PERSON','review','引用中有“前哨站首领约翰”“前哨站领袖约翰”（2/4 处）；待统一'),
 ('society','Subject Z','T.PN.PERSON','existing','实体名；红帕兰日志中“Test subject Z”语境写作“试验品 Z”'),
 ('society','The Master','T.PN.PERSON','preferred','恐惧王座之主；2026-09-16 维护者裁决保持“领主”；Master of the Arena 是另一人物'),
 ('society','The Teacher','T.PN.PERSON','existing',''),('society','The Eidolon','T.PN.PERSON','existing',''),
 ('society','Grand Corruptor','T.PN.PERSON','existing',''),('society','Fortress Shadow','T.PN.PERSON','existing',''),
 ('creatures','Rat Lich','T.GAME.ENTITY','existing',''),('creatures','Sandworm Queen','T.GAME.ENTITY','existing',''),
 ('creatures','Weirdling Beast','T.GAME.ENTITY','existing',''),('creatures','Yeek Wayist','T.GAME.ENTITY','existing',''),
 ('creatures','Mindwall','T.GAME.ENTITY','existing',''),('creatures','Planar Controller','T.GAME.ENTITY','existing',''),
 ('creatures','Godfeaster','T.GAME.ENTITY','existing',''),
 ('creatures','Drolem','T.GAME.ENTITY','review','实体名为“卓勒姆”，职业解锁与说明中均写作“龙傀儡”（4/4 处）；待统一'),
 ('creatures','losgoroth','T.GAME.ENTITY','review','状态与日志中写作“罗斯戈洛斯”（5 处），实体名为“洛斯格罗斯”（7 处）；待统一'),
 ('creatures','Phoenix','T.GAME.ENTITY','review','实体名“不死鸟”；传说标题 How to Summon a Phoenix 与状态 Reviving Phoenix 用“凤凰”；待确定是否同一所指'),
 ('items','Blood of Life','T.GAME.ENTITY','existing',''),('items','Blood of Undeath','T.GAME.ENTITY','existing',''),
 ('items','Orb of Many Ways','T.GAME.ENTITY','existing',''),('items','Resonating Diamond','T.GAME.ENTITY','existing',''),
 ('items','Staff of Absorption','T.GAME.ENTITY','existing',''),('items','Transmogrification Chest','T.GAME.ENTITY','existing',''),
 ('items','Summertide','T.GAME.ENTITY','existing',''),('items','Wintertide','T.GAME.ENTITY','existing',''),
 ('items','Automated Portable Extractor','T.GAME.ENTITY','review','任务对话中写作“便携式自动提取仪”（1/3 处）；待统一'),
 ('items','Shoes of Moving Quickly','T.GAME.ENTITY','review','物品名为“疾行之鞋”，合成提示均写作“疾行之靴”（3/3 处）；待统一'),
 ('places','Charred Scar','T.PN.PLACE','existing',''),
 ('narrative','The Hunter and the Hunted','T.NARRATIVE.LORE','existing',''),
 ('narrative','Records of Lorekeeper Hadak','T.NARRATIVE.LORE','existing',''),
 ('narrative','Iron Throne Profits History','T.NARRATIVE.LORE','review','实体名无“的”，各篇传说标题均写作“钢铁王座的盈利历史”；待统一'),
 ('narrative',"Clinician Korbek's experimental notes",'T.NARRATIVE.LORE','review','实体名为“实验笔记”，各篇传说标题与正文均写作“实验报告”（8/8 处）；待统一'),
]
DOM={'society':'society','creatures':'creatures','items':'items','places':'places','narrative':'narrative'}
for f,s,cat,st,n in P: add(f,s,'entity name',cat,DOM[f],st,n)
w=csv.writer(open('.artifacts/i18n/term-completeness/new_rows.tsv','w',newline=''),delimiter='\t',lineterminator='\n')
for r in rows: w.writerow(r)
print(len(rows),collections.Counter(r[0] for r in rows),collections.Counter(r[6] for r in rows))
