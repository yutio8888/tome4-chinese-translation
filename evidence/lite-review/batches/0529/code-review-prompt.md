独立代码复审（只读）。审阅 ToME4 中文插件 chn-mod 工作分支 code/dynamic-desc-fixes 的追加提交 3580885（父提交 6303b33；分支基于 c05bb96 = 已发布 v0.3.13），判断 Bloodstream 中文说明的“文案—实参”契约在各种代码/译文组合下是否都成立，且改动安全、只在约定边界内生效。

冻结输入（只读这些及其引用的源码）：
- /tmp/r7/review/addon-increment.diff：3580885 相对 6303b33 的改动（hooks/dynamic_desc_fixes.lua、data/chn_supplement.lua、tests/test_dynamic_desc_fixes.lua）。
- /tmp/r7/review/addon-full.diff：分支相对 c05bb96 的完整改动（含 hooks/load.lua 接线与 Automated Repair 部分，供上下文）。
- /tmp/r7/review/translation.diff：配套译文提交（/workspace/tome4-chinese-translation/tome-orcs.lua 的 Bloodstream 上游键译文）。
- /tmp/r7/review/zh_hans-0.3.13.lua：已发布 0.3.13 的生成 locale（旧 locale）。
- 插件文件可用 `git -C /workspace/tome4-chn-mod show 3580885:<path>` 读取（含 superload/engine/interface/ActorTalents.lua、overload/engine/i18nhelper.lua、hooks/load.lua）。
- 上游：Embers of Rage DLC 公开检出 /workspace/tome4-dlcs/orcs/tome-orcs（data/talents/steam/sawmaiming.lua 的 Bloodstream）；ToME 核心固定提交用 `git -C /workspace/t-engine4 show 624a67329fe2:<path>`（如 game/engines/default/engine/I18N.lua 的 _t/get/tformat/loadLocale，game/modules/tome/data/talents.lua 的 damDesc）。

改动意图（需由你独立核实）：上游 info 把 getDamageInc 作为第三实参，而 action 以 getDamage/100 为现有流血效果倍率。插件中文路径改用一个插件专用的英文显示键（只作内部键）及其在 data/chn_supplement.lua 中的中文，代入 getDamage；只有当前 locale 中该专用键确有译文时才走新路径，否则或出错时返回原 info。上游键译文恢复为与 getDamageInc 一致的原措辞。目标是以下组合都不出现“新实参配旧措辞”或“旧实参配新倍率措辞”：新代码+旧 locale、旧代码（c05bb96，无此钩子）+新 locale、新代码+新 locale、新代码但专用键缺译文、新路径异常回退；英文输出逐字节等于上游 info。

请核对：
1. 能力检查（_t 返回值与键比较）在固定引擎 I18N 语义下是否可靠：tag、"nil" 回退表、补充 locale 的加载时机与 locale 名、专用键是否可能与上游或其他键冲突、"##" 后缀对查找/格式化有无影响；tformat 对该键的 args_order/special 处理。
2. 专用键中文与 action 实际行为、实参顺序是否一致；占位符与上游一致；上游键中文与 getDamageInc 一致。
3. 上述各组合与回退路径的实际显示；英文不变；DLC 缺失/定义缺失无错；与 replaceFormat 包装和加载顺序的交互；幂等；不写 actor/eff/存档。
4. 测试是否真实覆盖上述矩阵（而非自证），有无重要遗漏。
5. CRLF 文件中长字符串的行尾是否会使补充 locale 的键与代码中的键不一致。

只读：不要修改任何仓库或文件，不要运行游戏。可以运行只读命令和 LuaJIT 测试：在 /workspace/tome4-chn-mod（当前检出即 3580885）下运行
CHN_TEST_ENTITY=/tmp/r7/review/Entity.lua CHN_TEST_ORCS_ROOT=/workspace/tome4-dlcs/orcs/tome-orcs CHN_TEST_LOCALE=/workspace/tome4-chinese-translation/tome-orcs.lua CHN_TEST_OLD_LOCALE=/tmp/r7/review/zh_hans-0.3.13.lua luajit tests/test_dynamic_desc_fixes.lua
临时文件只写 /tmp。

把结论写到 /tmp/r7/review/result.md：开头一行 `VERDICT: READY` 或 `VERDICT: CHANGES`，然后逐条列出发现（每条标 blocking 或 advisory，附文件:行号证据）。最终回复只写一行摘要。