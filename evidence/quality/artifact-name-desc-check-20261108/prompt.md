# 固定神器名称与描述匹配审核（只读）

你在审核《马基埃亚尔的传说》(ToME4 1.7.6) 简体中文汉化里的固定神器（unique 物品）。**只读**：不得修改任何仓库文件，不 git add/commit；草稿可写 /tmp/artchk/scratch-LANE/。

输入：`/tmp/artchk/chunkLANE.jsonl`，每行一件神器：`name_en/name_zh`（名称）、`unided_en/unided_zh`（未鉴定名）、`desc_en/desc_zh`（描述）、`use_power_en/use_power_zh`（主动效果名），`file` 是源码路径（`src/game/...` 对应 `git -C /workspace/t-engine4 show 624a67329fe2:game/...`；`dlc:...` 对应 `/workspace/tome4-dlcs/...`，来源未固定）。zh 字段是数组（同一原文可能有多个译法），null 表示库里没有找到译文。
译文库：`/workspace/tome4-chinese-translation/` 的 `mod-tome.lua`、`tome-orcs.lua`、`tome-cults.lua`、`tome-ashes-urhrok.lua`（格式 `t("英文", "中文", "tag")`），可 grep 查同一专名在别处的译法。

**逐件**检查以下「名称与描述不匹配」问题：
1. **物品类型不符**：中文名、未鉴定名、描述三者对物品种类的说法互相矛盾，或与英文/源码的实际类型不符（如英文是戒指，中文名写项链；描述说「这把剑」而物品是斧）。需要时到源码看该物品的 base/type/subtype。
2. **专名不一致**：名称里的人名、地名、种族、组织、典故，在中文名与中文描述里译法不同；或与库里该专名的通行译法不同（用 grep 查证，列出其他出处的行号）。
3. **名称含义与描述矛盾**：描述解释了名字由来或特征，而中文名的译法与之矛盾或丢失关键含义（如描述强调「冰霜」，名字却译成「火焰」；英文名是双关、描述点明了含义，中文名译偏）。
4. **描述张冠李戴**：中文描述讲的明显是另一件物品，或与英文描述内容对不上。
5. **主动效果名/未鉴定名** 与名称、描述矛盾。
6. 缺失译文（zh 为 null）只在确实应翻译时报告。

不要报：纯文风偏好、可接受的意译、标点空格、与匹配无关的一般翻译瑕疵（除非是明显误译导致名称与描述对不上）。每条必须给出具体证据。

## 产出
写 `/tmp/artchk/findingsLANE.json`：数组，每条
`{"id":<行id>,"name_en":"…","name_zh":"…","type":"item_type|proper_noun|name_meaning|wrong_desc|power_or_unided|missing","issue":"具体说明","evidence":"源码路径:行号 或 库内其他出处 文件:行号 与原文","suggestion":"建议改法或null","confidence":"high|medium|low"}`。
没有问题写 `[]`。必须读完全部行（文件约 128 行）再交付；最终回复只写一行：`REVIEW artchk-LANE DONE findings=<n>`。
