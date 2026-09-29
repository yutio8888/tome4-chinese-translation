---

# rem-20 只读交叉核验报告

本报告仅代表本次 REVIEWER 对 **4 条译文、6 个既有疑点**的核验；未修改文件，也不代表其他模型完成复核。下表按冻结批次顺序列出结论。

| 完整 entry-ID | 结论 | 依据 |
|---|---|---|
| entry-04109 | 仅建议 | C01；“创造”可表达制成，工匠语境用“制作”更自然。 |
| entry-04110 | 仅建议 | C02；“配方”正确，省略了 `tinker` 限定，但上下文可补足。 |
| entry-04114 | 未发现中文新增问题 | `%s`、被动语态及“击退”均对应原文；源码另有一处英文日志调用疑点，见下文。 |
| entry-04115 | 存在问题 | C03、C04、C05 已确认；C06 仅建议。另见 N01、N02。 |

### C01 | entry-04109 | advisory

原译“**创造插件：%s**”表达了制成物品的结果。最强等价读法成立；“制作插件”更贴合操作语境，但不足以判为错译。冻结源码在 `PartyTinker.lua:135-145` 创建物品后发出该日志；快照见 `snapshots/tome-orcs.lua:8177`。`terms.json:1521` 的 `tinker→蒸汽工具` 是 *existing* 实体类型记录，不据此强制改掉此处已有的“插件”。

### C02 | entry-04110 | advisory

原译“**已学习新的配方**”省去 `tinker`。`PartyTinker.lua:168-174` 表明这里学习的是工匠配方，补作“插件配方”会更明确；但在该系统中，“配方”及随后显示的名称足以让原译成立。`schematic→配方` 符合 `terms.json:1587`；快照见 `snapshots/tome-orcs.lua:8178`。

### C03 | entry-04115 | confirmed

原译“**我保证，真的无关紧要**”与 `This IS relevant` 正好相反。前文称议程 *irrelevant*，此处坦塔洛斯强调自己转谈的方案**确实相关**；不存在能保留反义词的等价读法。建议改为“我保证，这确实切题”。证据：`palace-fumes.lua:90-100`、`snapshots/tome-orcs.lua:8375`。

### C04 | entry-04115 | confirmed

原译“**不论是哪种，我们都没法直接介入**”把 `Neither` 所指的两派人变成说话者一方。最强等价读法是“我们”泛指参与讨论的人，但前句的“有些人……也有人……”及后句向他们争取支援，均支持“**两方都无力直接介入**”。证据：`palace-fumes.lua:98-102`、`snapshots/tome-orcs.lua:8377`。

### C05 | entry-04115 | confirmed

原译“**狡猾的小绿人**”将 `filthy` 的“肮脏、污秽”换成了“狡猾”，改变了辱骂的具体含义；两词在此没有足够的等价读法。建议按原文的蔑称处理。证据：`palace-fumes.lua:110`、`snapshots/tome-orcs.lua:8387`。

### C06 | entry-04115 | advisory

原译“**这决定了我们从这方案里获益良多**”弱化了 `It's resolved that...` 连续三次作出议会决议的口吻。结合会议及散会语境，读者仍可将“决定了”理解为议会已定下结论，故暂列文体澄清建议；“决议认定……”更准确。证据：`palace-fumes.lua:88-110`、`snapshots/tome-orcs.lua:8387`。

## 新发现

### N01 | entry-04115 | confirmed

原译“**过分的亵渎**”把 `excessively profane` 指向亵渎神圣事物；此处描述的是卡西罗斯发言**粗俗、满口脏话**，随后被投票从记录中删去。“亵渎”缺乏该段的宗教对象作等价支撑。证据：`palace-fumes.lua:108`、`snapshots/tome-orcs.lua:8385`。

### N02 | entry-04115 | advisory

末句原文是卡西罗斯在**正式辞职前**作了长篇演说，译文“**在从议会正式辞职时**”模糊了先后。它也可宽泛指辞职过程，故建议明确为“正式辞职前”。证据：`palace-fumes.lua:112`、`snapshots/tome-orcs.lua:8389`。

## 来源与版本限制

实际读取了入口 `batches/sol-rem-20.md`、同目录 `RULES.md`、当前 `batches/rem-20.md`、`reports/gemini-rem-20.md`、`source-access.json`、`terms.json`，以及 `snapshots/tome-orcs.lua` 中本批对应段落；源码只读取了登记的 `PartyTinker.lua`、`Archery.lua`、`DebugMain.lua`、`palace-fumes.lua`。四份 DLC 源码的 SHA256 均与 `source-access.json:486,806,815,820` 相符。上述相对路径的冻结源码根为 `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/`。

来源登记将 **orcs DLC 标为 unpinned**（`source-access.json:376-377`）：哈希固定了本次所读文件，仓库 commit 与目标游戏版本未固定，故本报告不声称核验了 1.7.4。`entry-04115` 的快照 section 标为 `DebugMain.lua`，而所引英文长文实际见冻结的 `data/lore/palace-fumes.lua:88-112`；`DebugMain.lua:29-31` 仅见“Learn all schematics”菜单项。此处的提取归属与实际消费路径仍待核实，不影响以上逐句文本对照。`Archery.lua:76-80` 在施加眩晕的分支也调用了英文“is knocked back!”日志；这是冻结英文源码自身的调用疑点，译文“被击退”忠实对应所给英文，未计为中文新增问题。
