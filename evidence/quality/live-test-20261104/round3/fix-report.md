# r3fix 执行报告

完成规范 7 项问题，共修改 13 个 Lua 译文条目；未提交 git。
用户追加授权同步 tome-possessors.lua:475–476 及本次同 source 译文重复项。历史 evidence、.ai 冻结快照不改。工具、文档、术语库未修改。

| 文件:行 | 旧 target | 新 target | 代入后的通读句 |
| --- | --- | --- | --- |
| engine.lua:1318 | `在 %s` | `到达%s` | 奔跑了10回合（中断原因：到达出口）。 |
| mod-tome.lua:5 | ` %s 在 %s！` | `%s在%s！` | 救命！森林巨魔在东面！ |
| mod-tome.lua:152 | `#FFD700#命中值　#FFFFFF#：` | `#FFD700#命中值#FFFFFF#：` | 命中值：35 |
| mod-tome.lua:153 | `#0080FF#闪避值　#FFFFFF#：` | `#0080FF#闪避值#FFFFFF#：` | 闪避值：20 |
| mod-tome.lua:418 | `提升 %s +%d` | `的%s提升了 %d 点` | 作为奖励，你的魔力提升了 5 点。 |
| mod-tome.lua:420 | `提升 %s豁免 +%d` | `的%s豁免提升了 %d 点` | 作为奖励，你的物理豁免提升了 5 点。 |
| mod-tome.lua:790 | ` ; 材质等级 ` | `，材质等级 ` | 类型：护甲/板甲，材质等级 1 |
| mod-tome.lua:1104 | `在 %s` | `到达%s` | 奔跑了10回合（中断原因：到达出口）。 |
| mod-tome.lua:1447 | `在 %s` | `到达%s` | 奔跑了10回合（中断原因：到达出口）。 |
| mod-tome.lua:6864 | `被冷藏` | `被冻僵` | 玩家在地牢第1层被冻僵而死。 |
| mod-tome.lua:41395 | `#LIGHT_BLUE#伤害抗性   ：基础/上限：` | `#LIGHT_BLUE#伤害抗性（基础/上限）：` | 伤害抗性（基础/上限）： |
| tome-possessors.lua:475 | `#FFD700#命中值　#FFFFFF#：` | `#FFD700#命中值#FFFFFF#：` | 命中值：35 |
| tome-possessors.lua:476 | `#0080FF#闪避值　#FFFFFF#：` | `#0080FF#闪避值#FFFFFF#：` | 闪避值：20 |

材质等级新 target 为 `，材质等级 `，保留末尾一个 ASCII 空格。每条修改时已代入示例值通读；停止原因三处使用同一完整嵌入句核验。

## 语境与源码核验

固定 engine commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`。固定版本全组件源码 grep 确认，两条奖励描述的有效调用仅位于 `game/modules/tome/class/EscortRewards.lua:497、515`；其他命中为 locale 定义。`game/modules/tome/data/chats/escort-quest.lua:35–36` 的 on_chose 将 log 保存为 reward_message，`game/modules/tome/data/quests/escort-duty.lua:64` 嵌入奖励说明。两条 `[Improve …]` 按钮 target 未改。仓库其他命中包含历史冻结译文及 DLC 源码快照中的注释，不构成额外有效使用场景。
冰冷死亡词相邻列表保持 `frozen`→“被冰冻”、`chilled`→“被冷冻”、`iced`→“被冻结”；新“被冻僵”与这三项均不重复。
全仓 grep 已完成；所有现行根目录 Lua 同 source 条目均已同步，历史证据快照保留原样。

## 验证

按有界译文维护矩阵验证。所有修改均仅替换第二参数；已逐行比较 HEAD 验证 source、source_tag、占位符数量与顺序、颜色码、换行不变。

- doctor：通过，LuaJIT / Lua 5.1、LPeg 0.10.2；DLC 来源未固定警告与本次修复无关。
- `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict`：退出码 0，30308 translations，**0 errors、0 warnings**。
- lint 报告：`.artifacts/i18n/runs/20261104T133919.424418Z-2083970-lint/lint.json`。
- 运行键扫描：0 collisions；重复运行键分类通过，1711 个重复键均为同 target。
- 严格核心 addon 构建通过：complete，7816 runtime keys。构建后仅追加了未纳入该核心 profile 的 possessors 闪避条目，追加后严格 lint、同键扫描、分类及不变量检查均通过。
- `git diff --check`：通过。
