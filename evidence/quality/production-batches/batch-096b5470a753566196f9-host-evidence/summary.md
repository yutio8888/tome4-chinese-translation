第256批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：63 OK / 17 ISSUE，逐条比对无错位（lane-000-0 一条 OK 结果回显 identity 错 17 位，经原生日志核实后宿主 hand-attribution 恢复）；一组full contextual（claude/claude-opus-5-5）：10 OK / 7 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计（lane-000-2 因 sandbox 失败经 Paseo 终端只读读取，终端已关闭）、全部归档确认。

宿主对23个观察裁决{"refuted": 6, "confirmed": 10, "pending": 4, "advisory": 3}，结果72条完成、5条修复、3条pending（blocked）。修复范围：Plate of the Blackened Mind 描述、魔法大爆炸区域效果传送警告、时空特工入职信（几十年/fair game/彩票/quite literally）、刀刃风暴构造体 short_info、碾压擒抱解除提示。驳回：Shadow Mages 暗影之火、潜行“能看见你的敌人”、两个前缀尾空格、两处冒号尾空格。pending：技能名 Blunt Thrust（钝器挥击）、传说标题 If I Should Die Before I Wake、神器名 Crystal Shard（水晶之杖）。

按1:1节奏，推送后进入修复窗口10，仅处理这5条。
