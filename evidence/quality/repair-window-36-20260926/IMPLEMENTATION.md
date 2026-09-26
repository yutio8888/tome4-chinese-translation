# 修复窗口 36 实施记录

本次仅修改 `tome-cults.lua` 中 `WORKSET.json` 冻结的 21 个 target，并在本目录保存实现验证结果。source、section、source_tag、args_order、special、运行键及其他记录均未改变；未修改术语库、任务记录、规则或工具，也未 stage、commit、push 或创建 agent。

## 逐条修复

- `428381f995…`：按原文恢复克罗格“一手拿锤、一手拿剑”的次序，并明确一手传播讯息、另一手将其贯彻到底。
- `ce25dcc579…`：把 `darkness damage` 统一为“暗影伤害”，并删除 target 多出的物理换行，使整句与单行原文一致。
- `ce4ea9ba02…`：将 `global speed` 译为“全局速度”，修正“维度之门”标点并补足句末标点。
- `cfaafbdaed…`：把踢击选项改为“踢出一条路逃出去”，恢复脱身目的。
- `d0e2bafe76…`：恢复法杖“依然平静”以及对“愚蠢、无用、可悲的冒牌死灵法师”的辱骂原义。
- `d5f14597d4…`：纠正城堡守卫段的生命、墙壁、防御触发与鬼魂安息等语义，删除“玻璃幕墙”等增译。
- `d67b9da42c…`：将职业特色改为“撕裂时空，创造裂隙”。
- `dc519faa34…`：把状态文本改为“进入禁忌之书《家，可怕的家》%d 回合。”，修正书名格式与多余空格。
- `df6ed2f1bd…`：整段校正采购、火势逐渐平息、搜寻可能未逃出者、纳格尔城与叙述者自我怀疑等语义。
- `e487193fbf…`：恢复单数魔法畸兽、死灵法师住处及触手间幼龙等含义，不再误译为龙或肉块。
- `e68028787a…`：补回开头斜体闭合标记，校正名字无意义、思索、弓、方位、文火及身体开始复原等语义。
- `e9e0b787b1…`：恢复通常会作为祭品的转折、蜿蜒长度，以及亲眼见过吞噬者分解巨物的叙述。
- `ea6c288db2…`：整段校正对食人魔的仇恨、战斗声、杀戮冲动、半身人罪不至死、意识崩断、面具变化及复仇偿还等语义。
- `ead23fb891…`：将实体名 `The Divine Writhing Mass` 改为“神性蠕动肉团”。
- `efa7badd9b…`：逐行重译诗体，恢复祈使/陈述关系、Pain 与 Focus 的分行及非人称指代；保持原文 17 个物理行与相同空行下标。
- `f067c87f47…`：恢复虚空之星的触发条件、40%% 熵能反冲与“最多叠加 4 颗”，并压回与原文一致的三行及 TAB 层级。
- `f30b472bd0…`：恢复“合上两本束缚之书”、城堡稳定及能够进入最后一章的含义。
- `f4db736957…`：整段校正灵能奴役结果、被迷住后的服从、帐篷场景、攻击动作、怒火克制、冒牌者与使者主语等语义。
- `f5569f0456…`：恢复“他们看不见”“凡人的舌头”，并将口号校正为“思想是财富。珍惜思想。”
- `f6030742f5…`：删除 `paranoia` 之外新增的“狂热”，把导师保持为未知存在而非“大师”，并恢复幸存者乞求可作武器之知识的句法。
- `f7b0d66ac9…`：明确目标会“浪费该回合”并尝试攻击邻近单位，修正数值空格而不改变占位符。

## 来源与结构核验

仅按 `SOURCE-ANCHORS.json` 指定路径读取 `/workspace/tome4-dlcs/cults` 下的公开源码。21 条查询涉及的 14 个文件 SHA-256 均与冻结锚点一致；逐条整句对照了原文及给定的相关机制行。Cults 源码仓库与 commit 仍未固定，不能把本地 checkout 当作版本 pin。

使用 manifest 配置的 LuaJIT 同时加载 HEAD baseline 与当前 `tome-cults.lua`，共比较 2199 条记录：恰有 21 个 target 改变，且与 `BASELINE-records.json` 的冻结 preimage 和 `WORKSET.json` 的条目集合完全一致；其他字段和记录均不变。21 条 source/target 的 LF 数、空行下标、逐行行首 TAB 数、行尾空白、markup、`@` token、适用格式占位符和 `<?=...?>` 模板表达式序列均通过直接断言；文件保持纯 LF，并保留末尾换行。

## 验证结果

- `python3 -B tools/i18n doctor`：退出 0；LuaJIT 2.1.0-beta3、Lua 5.1、LPeg 0.10.2-1 与 manifest 正常；三个公开 DLC 均按预期报告 source-unpinned 警告。
- `sha256sum <14 个 SOURCE-ANCHORS 指定的 Cults 文件>`：退出 0；14/14 文件哈希匹配全部 21 条查询。
- manifest-compatible LuaJIT HEAD/current 全记录比较：退出 0；`records_compared=2199`、`changed_targets=21`、`non_target_changes=0`，冻结 workset/preimage 与结构不变量全部通过。
- `python3 -B tools/i18n lint --strict`：退出 0；30308 条译文，0 errors、0 warnings；报告为 `.artifacts/i18n/runs/20260926T100958.976986Z-390833-lint/lint.json`。
- `git diff --check`：退出 0，无空白错误。

## 风险与宿主后续

唯一已知来源风险是 Cults 源码仓库与 commit 未固定；本轮以冻结文件 SHA 和逐条公开源码锚点约束实际输入。独立 REVIEW、FINAL_REVIEW、完整门禁、`DONE_VERIFIED`、提交与推送仍由宿主负责，本执行不作这些完成声明。
