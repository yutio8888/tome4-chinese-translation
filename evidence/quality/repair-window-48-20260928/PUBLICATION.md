# 修复窗口 48 发布记录

## 范围

- 第357、358批遗留待修复 9 条：`175effe253`、`196ce36308`（Ashes 开场与起始任务的陨石句及控制水晶）；`3626a66415`（莎西·凯希雕像 lore 三处限定词）；`5e73a63007`（毁灭号“致命得离谱”）；`6a71689b25`（水小鬼雕像 lore 代词）；`ae4cc0af7a`（米诺陶雕像 lore）；`ba5e371016`（艾伦尼恩回忆录）；`dc3200b76d`（元素法师起始任务“抛入星辰之间的虚空”）；`d0aff018a9`（夸塞魔雕像 lore）。
- 全局改名宿主补充 13 条：water imp“小水怪”→“水小鬼”、wretchling“酸液树魔”→主游戏既有“小劣魔”，均为用户指示的 Gemini 3.8 Flash 咨询结论。
- 共 22 条，涉及 `mod-tome.lua`、`tome-orcs.lua`、`tome-ashes-urhrok.lua`；术语库 `terminology/creatures.tsv` 新增 water imp、wretchling 两行，`tools/annotate_domains.py` 与静态审计测试行数随译文提交；无跨组件同键兄弟（`check_siblings` 0）。
- 范围外 Archmage `8b977dd836` 未纳入，仍为 `pending_repair`。Ashes/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-*.json`](publication/)：

1. execute-01 修改 22 条并加术语行。
2. REVIEW(0) r0a1（GPT-6 Sol）确认 2 条：开场“当你逐渐恢复意识”的同时关系；主要恶魔台词补 gnashing 与“那些只是幼体”。
3. execute-02 修复上述问题。
4. RE_REVIEW(1) r1a1 确认 2 条：纳格尔摄政们已提供研究成果；“饲养”改为“繁育”米诺陶。
5. execute-03 因模型容量错误未回报即终止；改动正确，但输出无效，见 [`HOST-NOTE-execute-03-capacity.md`](publication/HOST-NOTE-execute-03-capacity.md)。
6. fresh retry execute-04 核验并记录。
7. RE_REVIEW(2) r2a1 确认 2 条：小劣魔雕像结句“作出了巨大贡献”；caloric energy 译“身体所需的能量”，与同文件第 97 行对应条目一致。
8. execute-05 修复上述问题。
9. RE_REVIEW(3) r3a1：22/22 通过。
10. FINAL(3) f3a2（Opus 5.5）：22/22 OK，cycle 3 收敛（`max_cycles` 5）。

## 结果

- advisory：无。
- 门禁：17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。
- 译文提交：`6d56a09f6dda8fe203eb44f9e08b23c97813ed72`。
- 新 catalog：`f1f3f7a2ef1022ced9224f77b7f3462c147878f10c9f587608d273c97560bb7d`。
- migration：`70a471df192f0fc3db0a9e72c96ae12195ede2360d397d0b68e596f39cf30ee2`。
- 后续：22 个 successor 必须重新审核，不继承旧 done。
- 本 publication child 待宿主归档。
