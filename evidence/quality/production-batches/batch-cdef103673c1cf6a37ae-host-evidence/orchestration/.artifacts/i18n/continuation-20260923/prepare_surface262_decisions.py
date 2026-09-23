import pathlib,json
P=pathlib.Path('.ai/task/batch-cdef103673c1cf6a37ae')
D={
'f1403b3e':('pending',False,'objects/world-artifacts.lua:6833 独特戒指神器 Exiler（时空术士 Solith 的戒指，unided_name insignia ring）；现译“放逐”把施事名词译成动作。神器专名改名属命名决定（先例：Crystal Shard 列 pending），列入待用户审阅；建议“放逐者”。'),
'f14a476f':('confirmed',True,'50 级祝贺提示：原文首句与第二段之间有空行（\\n\\n），译文只保留一个换行，丢失段间空行；按换行不变量整句修复，其余内容一致。'),
'f1598310':('refuted',False,'lore/shertul.lua:50 壁画 There is some text beneath 后以 .. 拼接 which you do not understand:…（mod-tome.lua:19361 起“不明意义的文字：…”）；中文“下方写着”+“不明意义的文字”无需空格，末尾空格不是缺陷。'),
'f15aa79a':('refuted',False,'objects/egos/amulets.lua:196 前缀 ego starlit （prefix=true）与物品名拼接；中文前缀直接连写（“星光的项链”），不需保留英文分词空格。'),
'f15f5593':('confirmed',True,'星辰契约说明（tformat）：The strength of your bond is so strong 指与恒星化身的羁绊之强使你能同持双手武器与盾，现译“你的力量如此强大”丢失 bond 且改变因由；另多行前导 \\t\\t 被改成 8 个空格而其余行保留 \\t\\t，缩进不一致。整条对照修复，恢复与原文一致的 \\t\\t。'),
'f181f499':('pending',False,'talents/cursed/cursed.lua:46 技能系 Crimson Templar（堕落圣骑士，由 Guardian=守卫 转化而来，wil.lua:399 / unlock-paladin_fallen.lua:36）；现译“赤红守卫”未体现 Templar（圣殿骑士）。技能系改名需同步引用处，属命名决定，列入待用户审阅。'),
'f18f9a4e':('refuted',False,'lore/fun.lua:227 wild infusion 为物品/纹身名，术语表 items.tsv:20 preferred “野性纹身”，与 Wild infusion 技能名统一；现译正确。'),
'f19cec26':('confirmed',True,'chats/alchemist-last-hope.lua:405–406 矮人送药对话：I put a bit of the good stuff in this one, though it won’t do you any favors tomorrow morning 意为“我往这瓶里加了点好料（烈酒），不过明早可有你受的（宿醉）”；现译“这里面我给你带来个好东西，尽管也许明天早上对你没什么用”把“往里加料”误为“带来好东西”、把“会让你难受”误为“没用”并增“也许”。与 contextual 独立复核同向，宿主由 advisory 改判 confirmed（语义）。整条对照修复。'),
'f1a593de':('advisory',False,'events/cultists.lua:105 邪教徒随机喊话 My soul for her!（献身黑暗女王）；“我的灵魂属于她”与原意（以灵魂献给她）相近，属喊话风味；可选改“我的灵魂献给她！”。'),
'f1e389df':('confirmed',True,'成就说明 Won ToME by closing the Void portal using yourself as a sacrifice：closing 为“关闭”，现译“阻止虚空传送门”误述动作（本库 closing the void farportal=关闭虚空传送门，mod-tome.lua:16039）。'),
'f20e44ef':('confirmed',True,'chats/sorcerer-end.lua:146/161 special_death_msg ("sacrificing %s to bring the Way to all"):tformat(string.his_her_self(player))，%s 运行时为“他自己/她自己”（mod-tome.lua:1403–1404）；现译“%s牺牲自己，将维网带给众生”渲染为“他自己牺牲自己…”，%s 语义角色错置。同族 fiery wrath 句译“牺牲了%s，引来…”（mod-tome.lua:6142），按同式修复。'),
'f2230567':('confirmed',True,'talents/techniques/munitions.lua:414 强化弹药 Venomous：leeching poison 造成 nature damage，本库伤害类型统一译“自然伤害”；现译“毒素伤害”误述伤害类型（机制术语）。整条对照修复。'),
'f22e755a':('advisory',False,'timed_effects/other.lua:857 SHADOW_VEIL on_gain 浮动提示 +Assail（配 -Assail）；“+暗影笼罩”为描述性译名，与效果一致，不误导；可选改“+暗影突袭”一类，需与 -Assail 同步。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review262-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==13,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 7 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
