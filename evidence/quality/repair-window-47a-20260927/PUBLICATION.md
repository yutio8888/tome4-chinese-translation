# 修复窗口 47a 发布记录

## 范围

A 组（用户 2026-09-27 对待审清单的裁决中涉及术语库改动与全局改名的部分），77 条＝第356批确认项 `3724ff9284` 1 条＋宿主补充 76 条：Eyal“埃亚尔大陆”→“埃亚尔”24（含 Orcs 一处瓦·埃亚尔）、Numbing 族→“麻木”25、Sunwall→“太阳堡垒”5、Ureslak→“乌瑞斯拉克”9、Crimson Templar→“血色圣殿骑士”6、DESTRUCTICUS 6、Gardanion 1；第356批条目为口袋时间 lore（巨魔 tossed around 与七彩巨龙）；涉及 `mod-tome.lua`、`tome-ashes-urhrok.lua`、`tome-cults.lua`、`tome-orcs.lua` 四个文件。

术语库 6 个 TSV 先于译文修改：新增/调整 Eyal、numbing、paralyzed、Ureslak、Crimson Templar、两个物品名、sunwall 升 preferred、manaburn 与 multi-hued 注释、Fire Imp＝火焰小鬼（用户 2026-09-28 裁决），并把 affinity 行更正为游戏界面用语“伤害亲和”。领域映射 `tools/annotate_domains.py` 登记三个新实体名。Ashes/Cults/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 范围扩展

首轮 FINAL 后按 [`publication/HOST-NOTE-scope-widening.md`](publication/HOST-NOTE-scope-widening.md)，把 workset 内经源码确认的旧缺陷一并修复（长 lore 条目的漏译、所属关系颠倒、“黑暗麻木”→“暗影麻木”、“伤害吸收”→“伤害亲和”等），不扩大条目集合；workset 外同类问题转入窗口 47b（见 [`publication/CARRY-FORWARD-47B.md`](publication/CARRY-FORWARD-47B.md)）。

## 轮次与复审

用户为本窗口单独授权放宽 `max_cycles`（先至 6、再至 7，最终至多 10），其他窗口仍为 5。

复审路径（各轮裁决见 `publication/ADJUDICATION-*.json`）：REVIEW(0)、RE_REVIEW(1)–(10)（GPT-6 Sol）与 FINAL(0)(6)(7)(9)(10)（Opus 5.5）；共十一次修复（execute-01…11）；r5a1 因输出顺序无效、f9a2 因原生日志并行 `tool_use` 侧枝被 parser 拒收（宿主登记其发现），均不计轮次。已驳回：Weirdling Beast、Ureslak 套装加成、Aeryn 已死、workset 内“莎西·凯希”写法；advisory：`f5f092ac5d` 歌词 ogre/over 双关、Destructicus 瞄准措辞。cycle 10 FINAL f10a2 77/77 OK。

## 工具与门禁

`tools/orchestration/review_lifecycle.py` 放行两种良性原生日志形状（Codex 跨零点 `environment_context` 注入、Claude 并行 `tool_use` 侧枝），各附单测；见 [`publication/HOST-NOTE-execute-01-date-rollover.md`](publication/HOST-NOTE-execute-01-date-rollover.md) 与 [`publication/HOST-NOTE-f9a2-parallel-branch.md`](publication/HOST-NOTE-f9a2-parallel-branch.md)。

门禁 17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 工具提交：`94e5a35cf5c1333e8801ba43c0f8ea91baec4c41`
- 译文提交：`78123847745c86c76033048b0b07b63cb89cc4f1`
- 新 catalog：`c7abbba1362d6924552bd273e7d7e5466876f9a7921185fa6aacf6cd86790481`
- migration：`ac10dc6364c2c5edafce574d5b15610cb800a2d4551f61f5f76db4ddd056b7c2`

## 后续

77 个 successor 必须重新审核，不继承旧 done。下一步窗口 47b（B 组单条措辞与名称，并纳入 [`publication/CARRY-FORWARD-47B.md`](publication/CARRY-FORWARD-47B.md) 转入项）。

本 publication child 待宿主归档。
