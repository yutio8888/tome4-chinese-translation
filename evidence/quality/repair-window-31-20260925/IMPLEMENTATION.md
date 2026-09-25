# 修复窗口 31 实施记录

本次仅修改 `tome-ashes-urhrok.lua` 与 `tome-cults.lua` 中 `WORKSET.json` 冻结的 23 个 target，并在本目录保存实现验证结果。source、section、source_tag、args_order、special、运行键及其他记录均未改变；未修改术语库、任务记录、规则或工具，也未 stage、commit、push 或创建 agent。

## 逐条修复

- `00b0f993a3…`：Cults 描述恢复首句后的换行，并补回 `partly insane` 的“神志也有些失常”。
- `01bdde5133…`：将恐魔堡垒增益提示改为目标目睹恐魔后士气大振，纠正观看者方向。
- `0545d03281…`：补回 `towering`，将 `manifestation` 译为“熵之化身”，删除原文没有的观察视角。
- `055d79222e…`：将 `rend the very essence` 改为“撕裂目标的本质”，并依冻结术语将伤害类型 darkness 统一为“暗影”。
- `0576002f95…`：补回触手存在“有时从天而降看你”，删除“整天”增译，并按单数 `it/its` 修正解释者与警告来源。
- `08ed9231fa…`：只恢复 `Additionally` 段前的空行。
- `0deeb818e5…`：修正“愚蠢的野心”“控制不了外面的东西”，并将 `Something` 保持为不定指。
- `0f226fd7a2…`：恢复三段之间的两处空行、移除多余 TAB，并将伤害类型 darkness 统一为“暗影”。
- `11d347416e…`：恢复两个段前空行，移除颜色标签附近的多余空格；保留“麻痹”。
- `11ef5bb25d…`：逐段修复魔法大爆炸时间范围、解救/囚禁施受关系、庆祝会引语与叙述、附魔师事件、话音渐弱、离开而非待在家里、心理独白、庆典地点与时间比较、十来个食人魔/其中几人、两个永恒精灵及“自己的心声”等确认问题。
- `1260e07b9e…`：补回食物足够部落吃几天。
- `12c7900b7b…`：逐段保留 `may/likely/possibly`，修正矮人保密反事实、`blasted` 咒骂义、城门没收物品问句、平民携带物品的危险说明、两个半身人、对付永恒精灵的计划、矮人守密语义，并统一“马基·埃亚尔”。
- `12c97a3b71…`：修正“无法与之讲理”“或许最不寻常”、德瑞姆毛发、如何进食、thinking Drem 限定、野生德瑞姆及“德瑞姆”专名一致性。
- `1594e62acd…`：修正复数领袖、过河石块增译、十来个人/另一名守卫、被迫离开的定居点与 `likely`、酒馆客人指代，以及“反正本来也打算这么干”。
- `192a8688c5…`：将 `ever being, ever ceasing` 恢复为“永在存续，永在消逝”的对举。
- `1a5b7fe508…`：仅移除 `[[ ]]` 长串前两处续行的多余 TAB，使四行均与原文无缩进结构一致。
- `1cba11e4fd…`：将 thinking Drem 改为最近才“出现”，而非最近才“被发现”。
- `f6eee01b5c…`：恶魔之角合回原文四行；补回所造成伤害的 50%%、暗影伤害、流血期间与近战命中条件。
- `f746ce383c…`：战术简报逐段修正狡猾难缠、再次接触启蒙石板、标准改造与反应性魔法协同、内脏主动避让、代词模板、专注干扰、韧性改造、毒素/火焰、打到不能动、熟悉度及“不太可能出现伤亡”，并恢复末尾空行。
- `f985ec15c0…`：补回“至多消耗 %s 层”的上限语义。
- `f9e45b5a07…`：只将燃烧献祭两条续行恢复为两个行首 TAB。
- `fc65680ae7…`：修正秘密行动、本土危险实验、海底斥候与仆从、致敬，以及远方基地等整段语义。
- `fc8cdfb222…`：只将炙炎之牢两条续行恢复为两个行首 TAB。

## 来源与结构核验

仅按 `SOURCE-ANCHORS.json` 中的 18 个明确源码文件取证。18 个文件的 SHA-256 全部与冻结锚点一致；DLC 源码仓库与 commit 仍未固定，不能把本地 checkout 当作版本 pin。

使用 manifest 配置的 LuaJIT 同时加载两个 baseline 文件与两个当前文件，共比较 2892 条记录：恰有 23 个 target 改变，其他字段和记录均不变。23 条 source/target 的行数、空行下标、逐行行首 TAB 数及 `<?=...?>` 模板表达式序列全部一致。strict lint 同时验证 printf 占位符、`%%` 与 markup。

## 验证结果

- `python3 -B tools/i18n doctor`：退出 0；LuaJIT 2.1.0-beta3、Lua 5.1、LPeg 0.10.2-1 与 manifest 正常；三个公开 DLC 均如预期报告 source-unpinned 警告。
- 有界 LuaJIT baseline/current 全记录比较：退出 0；`total=2892`、`changed_targets=23`、`non_target_changes=0`、行结构 `23/23`、模板结构 `23/23`。
- `python3 -B tools/i18n lint --strict`：退出 0；30308 条译文，0 errors、0 warnings。
- `python3 -B tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict`：退出 0。
- `python3 -B tools/scan_runtime_collisions.py`：退出 0；runtime collisions 0。
- `python3 -B tools/classify_runtime_keys.py`：退出 0；1711 个既有重复键全部属于不同 section，桶 B/C 均为 0。
- `git diff --check`：退出 0。
- 对两份新证据分别运行 `git diff --no-index --check -- /dev/null <path>`：均无空白诊断；退出 1 仅表示文件相对 `/dev/null` 存在差异。

## 风险与宿主后续

唯一已知来源风险是 Ashes/Cults 仓库与 commit 未固定；本轮以冻结文件 SHA 与逐条公开源码锚点约束实际输入。独立 REVIEW、FINAL_REVIEW、完整 17 项门禁、严格构建、`DONE_VERIFIED`、提交与推送仍由宿主负责，本执行不作这些完成声明。
