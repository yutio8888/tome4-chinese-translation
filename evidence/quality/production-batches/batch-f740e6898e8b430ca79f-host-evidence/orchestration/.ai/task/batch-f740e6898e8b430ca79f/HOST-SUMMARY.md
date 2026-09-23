第254批：80条，全部固定ToME源码，65文件逐字节核验，80条原文字面命中。含窗口7的8个successor（均判OK或所附观察被驳回）。

审核模型按用户2026-09-23指示改为surface codex/gpt-6-sol、contextual claude/claude-opus-5-5。四组surface：68 OK / 12 ISSUE（lane-000-1有3条observation错位一格，已逐条比对）；一组full contextual：6 OK / 6 ISSUE。5个独立reviewer已严格校验并归档，原生读取边界已人工审计。Codex 0.156.0/Claude Code 2.1.280 高于仓库原生parser固定版本，原文bytes以仅替换版本字面量的同一parser提取并走严格--raw收取，仓库工具未改。

宿主对18个观察裁决{"refuted": 6, "confirmed": 9, "advisory": 3}，合并为6条修复、74条完成。修复范围：诅咒无尽狩猎技能树描述（疲惫被反转）、ALL_DREAMS成就名、unlock-yeek多余换行、自然精灵诗句花朵/逃散两行、麻痹毒素伤害方向、龙族传说四处限定词与地名。Overcharge飞弹每目标一枚、挽歌触发条件、毒素风暴等概率均与实现一致而驳回；e923d2b8 资源→能量为错位漏报，记宿主补充建议。

批次提交、finalize和推送闭合后提前进入窗口8，仅处理这6条。
