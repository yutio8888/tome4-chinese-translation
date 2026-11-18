独立代码复审（只读）。审阅 ToME4 中文插件 chn-mod 的一处未提交改动，判断它是否正确、安全、只在约定边界内生效。

冻结输入（只读这些及其引用的源码）：
- /tmp/r6/review/addon.diff：插件改动（hooks/load.lua 接线、新增 hooks/dynamic_desc_fixes.lua、新增 tests/test_dynamic_desc_fixes.lua）。插件工作树 /workspace/tome4-chn-mod。
- /tmp/r6/review/translation.diff：配套中文译文改动（/workspace/tome4-chinese-translation/tome-orcs.lua）。
- 上游源码：Embers of Rage DLC 公开检出 /workspace/tome4-dlcs/orcs/tome-orcs（data/talents/steam/sawmaiming.lua 的 Bloodstream；data/timed_effects/other.lua 的 AUTOMATED_REPAIR_SYSTEM；hooks/load.lua 的 ToME:load）；ToME 核心固定提交用 `git -C /workspace/t-engine4 show 624a67329fe2:<path>` 读取（如 game/engines/default/engine/Entity.lua 的 addTemporaryValue/removeTemporaryValue、game/modules/tome/data/talents.lua 的 damDesc、game/modules/tome/load.lua 的定义与钩子加载顺序）；插件现有 superload/engine/interface/ActorTalents.lua、ActorTemporaryEffects.lua、overload/engine/i18nhelper.lua。

改动意图（需由你独立核实是否成立）：两处中文说明中的动态数值与实际作用值不一致——Bloodstream 的说明显示 getDamageInc 而 action 用 getDamage/100 作倍率；AUTOMATED_REPAIR_SYSTEM 的 activate 把 eff.heal/resist/life 改写为临时值 id，long_desc 却显示这些字段。改动只想在中文下改显示，不改游戏机制。

请核对：
1. 机制事实与改动所用的实参/读取方式是否与上游代码一致（含 compute_vals 中存的值是否就是本效果的增量、resists 与 die_at 的存储形态、移除后的状态）。
2. 只在 zh_hans 下生效、英文输出逐字节不变；DLC 未安装或定义缺失时不报错；与插件现有 replaceFormat 包装及加载顺序（插件权重高于 DLC）的交互；幂等性。
3. 是否可能写入或污染 eff、actor、临时值登记、存档数据；异常回退是否会改变状态或掩盖问题。
4. 测试是否真实覆盖上述行为（而非自证），有无遗漏的重要情形。
5. 译文措辞与机制条件是否准确（命中、攻击前已有 EFF_CUT、命中后仍存在、只强化一次、倍率可低于 100%）。

只读：不要修改任何仓库或文件，不要运行游戏。可以运行只读命令和 LuaJIT 测试（测试需环境变量 CHN_TEST_ENTITY=<固定提交 Entity.lua 导出到 /tmp 的路径>、CHN_TEST_ORCS_ROOT=/workspace/tome4-dlcs/orcs/tome-orcs、CHN_TEST_LOCALE=/workspace/tome4-chinese-translation/tome-orcs.lua，在 /workspace/tome4-chn-mod 下运行 luajit tests/test_dynamic_desc_fixes.lua）。临时文件只写 /tmp。

把结论写到 /tmp/r6/review/result.md：开头一行 `VERDICT: READY` 或 `VERDICT: CHANGES`，然后逐条列出发现（每条标 blocking 或 advisory，附文件:行号证据）。最终回复只写一行摘要。
