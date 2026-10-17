# `crypt` 译名三方咨询结果与裁定（2026-09-11）

> **这份文件是主编排者的归纳，不是三个模型答复的逐字原文。**
> 三份答复的完整文本只存在于各自 agent 的会话记录里，未落盘——这是本次流程的一个缺口，
> 其它几次咨询（`projection-trust-model-20260911` 等）都有 `ANSWER-*.md`。
> 下面的结论与论据经过主编排者逐条核对，核对手段一并写明。

## 裁定

维护者裁定：**全部 `crypt` 统一译作「地宫」**。
已落地 25 处（`mod-tome.lua` 24 + `tome-ashes-urhrok.lua` 1），提交 `41b819f`。

## 三方结论

| 模型 | 结论 | 技能名 `Call of the Crypt` |
|---|---|---|
| GPT-6-Astra (xhigh) | 统一为「墓室」 | 墓室之唤 |
| Grok 4.6 | 统一为「墓室」 | 墓室召唤 |
| Gemini 3.8 Flash (high) | 统一为**「地宫」** | 地宫召唤 |

**三家一致：必须统一、不分派；「地窖」必须废弃。**

## 三家独立给出的同一条论证

同一处地点会在区名、遭遇弹窗、任务、对话、成就里反复出现：玩家遭遇
`Enter the crypt` → 进入 `Dark crypt` → 任务写 `out of the crypt` → 梅琳达父亲说
`that crypt` → 成就记 `Crypt of Kryl-Feijan`。分派会让同一事件链出现三个不同词。
且 `Dark crypt`、`that crypt` 都是小写却指专名，**大小写不能当分派判据**。

## 三家一致否决的候选及其占用者

| 候选 | 已绑给 |
|---|---|
| 墓穴 | `grave` / `tombs` |
| 地穴 | `breeding pits` / `Intimidating Cave` |
| 洞穴 | `cave` |
| 墓园 | `graveyard` |
| 陵墓 | `mausoleum` |
| 地下室 | `basement` |

## 分歧：空间尺度 vs 建筑属性

- **「墓室」**（GPT-6、Grok）：准确对应 `crypt` 的「地下墓葬建筑」本义。
  **两家都主动承认**其弱点——「室」是单间尺度，而 `crypt-kryl-feijan/zone.lua:24`
  是 `max_level = 5`、`shadow-crypt/zone.lua:24` 是 `max_level = 3`——仍选它，
  理由是宁可尺度感弱也要保住墓葬义。Grok 另明确考虑并否决了「地宫」，
  理由是帝陵语域过高、且会模糊「地宫召唤／陵墓召唤」的分工。
- **「地宫」**（Gemini）：尺度与建筑感都对，四字区名工整（黑暗地宫／阴影地宫／
  废弃地宫）。弱点是偏帝王陵寝，而 Kryl-Feijan 是邪教巢穴、Forsaken Crypt 是
  鼠巫妖随机事件。

## 主编排者独立核实的事实（核实手段一并列出）

| 主张 | 核实结果 | 手段 |
|---|---|---|
| `cellar` 已绑「地窖」 | **属实**，`tome-cults.lua:1667/1669`（活板门、酒、蔬菜干果） | `grep -rn '地窖'` |
| 「地宫」全库 0 处 | 属实，无一词两指 | `grep -rn '地宫'` |
| 「墓室」全库 0 处 | 属实 | 同上 |
| Kryl-Feijan 5 层 / Shadow Crypt 3 层 | 属实 | `zone.lua:24` 的 `max_level` |
| `Call of the Crypt` 与 `Call of the Mausoleum` 成对 | 属实，`master-of-bones.lua:21` 与 `master-of-flesh.lua:21`（死灵系姊妹技能） | 引擎源码 |
| `Call of the Mausoleum` 现译「陵墓召唤」 | 属实，`mod-tome.lua:29251` | grep |
| `basement` → 「地下室」 | 属实 | grep |

## 裁定时谁都不知道的那条事实

**`cellar` 早已绑给「地窖」。** 第 85 批把 `crypt` 也定为「地窖」时，
我列出了洞穴／地穴／墓穴／墓园四个已绑定词并逐一排除，报告写得像做过完整冲突检查——
**但没有查「地窖」自己是不是已经被别的英文词占了**。

这一条独立于任何审美判断，**它本身就足以推翻原裁定**。
由此立的规矩：**候选译名要双向查冲突**（记忆 `candidate-term-needs-two-way-conflict-check`）。

## 落地范围

25 处编辑 = 24 个 catalog 条目（`lore/fun.lua` 的尸妖段与幽灵段同属一个
`t([[…]])` 块）。分类见 `handoff.md` §17，其中包含三处 `crypt` **整词漏译的补回**，
以及一处**明知不忠实而保留**的取舍（`Entrance to a dark crypt` 保留「阴影」而非
字面的「黑暗」，因为该入口实际通向 `Shadow Crypt`，照字面改会与 Kryl-Feijan 的
`Dark crypt`「黑暗地宫」在界面上同名）。
