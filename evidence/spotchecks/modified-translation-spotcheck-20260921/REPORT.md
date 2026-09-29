# 已修改译文只读抽查结果

本轮完成 11 条有界样本复核：10 条未报疑点，spot-06 提出机制与术语疑点。宿主独立核验后，**确认的实质问题 0 条，待确认问题 0 条，可选人工一致性复核 1 条**。未修改译文、术语或主工作区，不推进生产队列，也不宣称全库通过。

## 可选人工复核清单

| 条目 | 位置 | 状态 | 人工可考虑的事项 |
| --- | --- | --- | --- |
| spot-06 / Indiscernible Anatomy | mod-tome.lua:25321 | advisory，非阻断 | 是否在后续已授权统一工作中把「目盲免疫」统一为「致盲免疫」。两者语义一致；此措辞并非本次修复新引入，不自动修改或扩大范围。 |

依据：terminology/combat.tsv:52 的 blind=致盲 是 effect subtype 的 existing 记录。当前 mod-tome.lua:853 使用「致盲免疫」，:21487、:25321、:26804 使用「目盲免疫」。这证明用词差异存在，不能单凭该术语行判定本句机制错误。

## 已撤销的意见

1. **暴击机制**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 tome 组件 `game/modules/tome/data/talents/gifts/ooze.lua:256–269` 把同一个 critResist 数值用于 ignore_direct_crits 与第一个占位符。`game/modules/tome/data/damage_types.lua:130–154` 将暴击倍率超出 1 的部分按该百分比降低，没有以该属性作概率掷骰。现译「额外伤害降低 %d%%」正确。可复算例：基础伤害 100、暴击倍率 1.5、该属性 50 时，结果为 125，而不是 50% 几率在 100 与 150 间二选一。
2. **wounds 应译创伤**：同一技能 `ooze.lua:262` 实际授予 cut_immune；`terminology/combat.tsv:54` 的 cut 对应「流血」。wound 的 effect subtype 条目不能覆盖此处固定源码行为；现译「流血」有依据。

原始意见保留在 [reviewer-full-02.md](reviewer-full-02.md)，不把模型严重程度标签当作事实。

## 范围、方法与限制

- 独立分支 `audit/modified-translations-20260921`，冻结提交 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`；选择规则及基线见 [workset.json](workset.json)，实际差异见 [selection.patch](selection.patch)。近期修复窗口间共有 11 条 target 变更，包括同期名称修正。这是有界定向样本，不是全库随机抽样。
- 通过 Paseo 派发 Antigravity / Gemini 3.8 Flash / High，实时身份与 lineage 均核验。首轮 JSON 末尾有非法字符，原样保留；用户随后明确要求自然语言输出，第二轮按该要求交付，由宿主核验全部 11 个编号并整理记录。不再因格式重跑；不把转换后的记录冒充模型原生严格 JSON。
- 冻结输入附技能及 Combat/Actor 等固定源码，但未附 damage_types.lua 的最终消费逻辑；宿主另行读取该固定文件进行裁决，证据见 [host-damage-types-excerpt.txt](host-damage-types-excerpt.txt)。后续机制抽查应在派发前补齐此类属性的最终消费位置，减少仅凭属性名猜测机制的误报。
- reviewer 期间 HEAD、译文 diff、冻结文件哈希及关键 STATE 哈希均核验通过；两个 child 已确认归档。
- 按用户输出格式例外完成手工验收，不宣称未修改的严格 JSON checker 已返回 DONE_VERIFIED。没有译文变更，依只读验证矩阵核验事实、引用、报告空白及只读守卫，不运行译文构建或生产全量门禁。
