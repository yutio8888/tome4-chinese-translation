# 修复窗口 38 发布记录

## 范围

来源批次 315、316、317、318、319 共 24 条确认问题已修（tome-cults.lua 2 条、tome-orcs.lua 22 条；全仓库同 source 检查无跨组件同键）。Cults 与 Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 预检

开窗前一个只读助手逐段比对 2 条最长条目（2d9e3f67 心灵传讯《马基埃亚尔的传说》、281445cd 艾琳日记），宿主逐字核验引文 14/14 后并入修复（ADJUDICATION-HOST-PRECHECK-C0）。

## 复审路径

- execute-01 修复 24 条，宿主精确 diff 核验。
- REVIEW(0) r0a1 确认 1 条：2d9e3f67 None can say what our champion did（做了什么，非去向）。
- execute-02 → RE_REVIEW(1) r1a1 24/24 OK → FINAL(1) f1a2 确认 2 条：21c042dd 维序者广告引语补「」（对齐同文件同类广告引语）；2d9e3f67 “出于”→“处于”。
- execute-03 → RE_REVIEW(2) r2a1 24/24 OK → FINAL(2) f2a2、f2a3 输出截断（24 条只回 3 条与 2 条、末个 key 残缺）被契约拒收（INVALID-F2A2、INVALID-F2A3），重派 f2a4 确认 1 条：1bc7d052 涌血末行斜体引语 The marvels of technology, now at the service of true butchery!
- execute-04 → RE_REVIEW(3) r3a1 确认 1 条：2d9e3f67 格鲁希纳克部落“力量与钢铁的蛮攻并不够强大”（原译增“精英部队”“最强大”），宿主同段并入加伯特部落同位语。
- execute-05 → RE_REVIEW(4) r4a1：2485f3aa/354df698 tinker 术语（existing“蒸汽工具”）refuted，六条同族技能一致用“…道具”，属跨条决定，记 advisory；宿主对 2d9e3f67 全文逐句复核 26 项（22 组精确替换）确认。
- execute-06（结果与宿主预构 target 逐字相同）→ RE_REVIEW(5) r5a1 24/24 OK → FINAL(5) f5a2 24/24 OK。max_cycles=5 用满后收敛。

## 门禁

17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`e34291e7ae890b3f4af1bc0a62b823732d018e2a`
- 新 catalog：`d2b34cb7355c28f94293a3c5665fc46c0d61d3e06251d83b6f01dc42aef39441`
- migration：`c67c525de5411f674069c31420a67d1c370a3f820cb84f90aeb755ecbec7d57b`

## 后续

24 个 successor 必须重新审核，不继承旧 done。窗口外宿主补充项待下个窗口按 revision 核实后纳入：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖。待用户审阅第32项（Thunder Grenade）、第33项（Voltaic Bolt）不变。

本 publication child 待宿主归档。
