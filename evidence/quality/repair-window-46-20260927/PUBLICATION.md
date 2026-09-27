# 修复窗口 46 发布记录

- 范围：来源批次 353、354、355 共 15 条确认问题（353 批 6、354 批 4、355 批 5），加宿主补充 5 条（工匠制造技能 info 同族治疗学/化学/爆炸学/铁匠/机械“X道具”→“X蒸汽工具”，与窗口 45 的“电子蒸汽工具”一致，待审第 41 项，用户可否决），合计 20 条，均为 tome-orcs.lua，已全部修复；无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
- 预检：开窗前宿主对口袋时间 lore 全文逐段预检（f466031dbb：自然精灵段全角逗号、孔克雷夫宝库、沙虫女皇之心、相位之门、“双手仍空着时”），写入 SOURCE-CLAIMS 并入首轮修复。
- 复审路径（各轮裁决见 [publication/](publication/) 下的 `ADJUDICATION-*.json`）：execute-01 修复 20 条 → REVIEW(0) r0a1（GPT-6 Sol）1 条确认（沉睡洞穴忏悔书“凯尔帝勒和他的背教者们”）→ execute-02 → RE_REVIEW(1) r1a1 1 条确认（收容营欢迎信“第一步”句）→ execute-03 → RE_REVIEW(2) r2a1：Weirdling Beast“异形触手”为本库既定名 refuted，conjuration wands（of conjuration 词缀）advisory → FINAL(2) f2a2（Opus 5.5）1 条确认（治疗学/爆炸学配方两行与同族对齐）→ execute-04 → RE_REVIEW(3) r3a1 1 条确认（bone armour 骨盾→骨甲）→ execute-05 → RE_REVIEW(4) r4a1“奥术法力燃烧”为游戏内伤害类型名 advisory → FINAL(4) f4a2 1 条确认（七彩龙→多彩巨龙，按 preferred 术语“多彩”）→ execute-06 → RE_REVIEW(5) r5a1 2 条 advisory（conjuration 同前；埃尔瓦拉外交官措辞，二级 cycle≥3）→ FINAL(5) f5a2 20/20 OK，cycle 5 收敛（max_cycles 5）。
- 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
- 标识：译文提交 `11e26bd86411afc9933aef21e49d161fb485806c`；新 catalog `a579d2d431de461ef2533cb4f102033abff721c86d24d5697a5eb4761d611883`；migration `5c379350bcc72d8f444532921fc9b08056103ef8885bcc14101e71417df91d7c`。
- 后续：20 个 successor 必须重新审核，不继承旧 done。新增待审第 42 项（Destructicus 译名）与第 43 项（multi-hued：术语 preferred“多彩”与生物名“七彩龙”系分裂）。
- 本 publication child 待宿主归档。
