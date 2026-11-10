# ToME4 汉化公开插件译文反向检查（只读）

你在检查《马基埃亚尔的传说》(ToME4 1.7.6) 简体中文汉化**近期修订过**的译文是否合理（这些条目最近被修改过，修改后的文字尚未做过这种通读检查）。**只读**：不得修改任何仓库文件，不 git add/commit；草稿可写 /tmp/revchk/scratch-LANE/。

## 方法：先读中文，再对英文（反向检查）
1. **先只读中文**：`/tmp/revchk/lanes3/LANE-zh.jsonl`，每行 `{"i":编号,"sec":源文件段,"comp":组件,"tag":用途标签,"zh":译文}`。以玩家的身份逐条通读，**全部读完**。标出读起来有问题的条目：
   - 语义不通、自相矛盾、逻辑或因果颠倒、读不懂；
   - 病句、语序错误、成分残缺、搭配不当、明显翻译腔；
   - 同一段内同一事物（技能、物品、人物、地名、状态、属性）译名前后不一致；
   - 数值/条件读起来不合理（例如「降低」与「增加」矛盾、持续时间与冷却混淆、百分比对象不明）；
   - 占位符（%s、%d、#Target# 等）放在中文里语义不通（例如主语宾语错位）；
   - 颜色码、标记泄露或残缺，残留英文。
2. **再对英文核实**：只对标出的条目，到 `/tmp/revchk/lanes3/LANE-en.jsonl` 按编号 i 查英文原文。确认是误译、漏译、错译，还是只是中文表达问题；必要时查固定版本源码确认机制：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/<路径>`（sec 字段 `mod-tome/...` 对应 `game/modules/tome/...`，`engine/...` 对应 `game/engines/default/engine/...`）；DLC（comp 为 tome-orcs／tome-cults／tome-ashes-urhrok）源码在 `/workspace/tome4-dlcs/<orcs|cults|ashes-urhrok>/`（来源未固定，引用时注明）。
3. 专名/术语可查 `/workspace/tome4-chinese-translation/terminology/*.tsv`（preferred 为定稿译名）与译文库 `mod-tome.lua`、`tome-*.lua` 的其他出处，确认库内通行译法。

## 不要报告
- 数值占位符与全角标点/汉字之间的 ASCII 空格（如「%d 点」「伤害， %d」「%d （」）：这是升级预览比对所需的规则，**故意保留**。
- 以下是维护者已确定的译法：Archmage＝元素法师、Parry＝招架（格挡专指 Block）、Summon 队伍头衔＝召唤、Exhaustion＝力竭、Fatigue＝疲劳值、regain Equilibrium＝降低失衡值、致命一击！（保留感叹号）、_t"her" 统一「她的」、护盾吸收类日志短格式「(%d 护盾吸收)」、徒手伤害也称「武器伤害」、yeek＝夺心魔、The Master＝领主。
- 中英文都通顺且意思一致的意译、纯文风偏好。
- 原文本身与游戏实现不符时，译文按实现写是有意的，不算错（先查源码再判）。

## 产出
写 `/tmp/revchk/findings-LANE.json`：数组，每条
`{"i":编号,"sec":"…","zh":"当前译文（可截取相关部分）","en":"英文原文（相关部分）","type":"mistranslation|omission|grammar|awkward|inconsistent|logic|placeholder|markup|untranslated","severity":"major|minor","issue":"问题说明（中文）","evidence":"英文/源码路径:行号/库内其他出处","suggestion":"建议译文（只改有问题的部分，保留占位符、颜色码与换行）"}`。
- 每条必须先在中文通读中被你标出，再经英文核实；英文核实后发现译文没问题的不要写入。
- 没有问题写 `[]`。
- 写 `/tmp/revchk/scratch-LANE/coverage.txt`：一行 `read=<读完的条目数>/<总条目数>`。
- 最终回复只写一行：`REVCHK LANE DONE findings=<n> read=<读完数>/<总数>`。
