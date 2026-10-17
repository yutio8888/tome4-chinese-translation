# 议题：ToME4 简体中文本地化 —— 两个待裁定专名

你是本地化专名顾问。下面是**冻结的客观证据**（游戏版本 1.7.6，commit 624a6732）。
只依据这些证据作答，不要臆测未列出的内容。两个议题彼此独立，请分别作答。

---

# 议题 A：`Zemekkys`（人名）

## A1. 现行译名
「**伊莫克斯**」，全库 19 处一致（mod-tome.lua 18、tome-orcs.lua 1）。

## A2. 该角色是谁（取自游戏文本）
- `Zemekkys, Grand Keeper of Reality` → 现译「伊莫克斯，现实至高守护者」
- `High Chronomancer Zemekkys` → 现译「高阶时空法师伊莫克斯」
- `Zemekkys' Broken Hourglass`（物品）→ 现译「伊莫克斯的破沙漏」
- `Zemekkys Home`（地点）→ 现译「伊莫克斯的家」
- 剧情：他在晨曦之门（Gates of Morning）研究 farportal（远行传送门），
  早期实验有志愿者失踪；玩家需带「共鸣钻石」与「仪式匕首」找他；
  他能为玩家建造返回故乡的传送门；文本里另一角色形容他
  "even lazier than I am, but he has status to maintain"。
- 是时空法师（Chronomancer）阵营的核心 NPC，掌管「现实」。

## A3. 其他语言
- 日文 `ja_JP`：「**ゼメッキス**」（Ze-me-kki-su）
- 繁体中文 `zh_hant`：「伊莫克斯」（与简体相同）
- 韩文 `ko_KR`：未单独列出该专名条目

## A4. 已提出的问题
两轮独立审核均指出：`Zemekkys` 首音为 /z/，「伊」无对应；整体读音与原文不匹配。

## A5. 约束
- 19 处一致沿用，改名须一次性全部同步，否则触发跨组件 runtime-collision 门禁。
- 玩家社群、攻略中已有惯性。
- 需能自然嵌入既有句式：「____，现实至高守护者」「高阶时空法师____」
  「____的破沙漏」「____的家」「____潦草的笔记」「____说道：“…”」。

---

# 议题 B：`Animated Sword` / `Distorted Animated Sword`（实体名）

## B1. 现行译名
| 英文 | 现行中文 | 出现处 |
|---|---|---|
| `Animated Sword` | 次元之刃 | mod-tome.lua:8311 |
| `Distorted Animated Sword` | 极·次元之刃 | mod-tome.lua:8315 |
| `Open a hole in space, summoning an animated blade for 10 turns.` | 在空间中打开一个孔洞，召唤一个次元之刃 10 回合。 | 25929 |
| 同上（15 turns 版） | 同上 | 25945 |

「次元之刃」共 4 处；「极·」作为 `Distorted` 前缀全库**仅此 1 例**，未形成惯例。

## B2. 该实体在游戏里是什么（取自游戏文本）
- 描述：`Time seems to warp and bend around this floating weapon.`
  → 现译「时空在其周围扭曲。」
- 出场日志：`#AQUAMARINE#A rift opens and a free floating blade emerges!`
  → 现译「时空裂缝打开了，里面出现了一把浮空的刀刃!」
- 消失日志：`The %s no longer seems to be controlled and clatters to the ground
  before vanishing into a rift.` → 现译「%s 似乎失去了控制，坠落在地面，消失在时空裂隙中。」
- `Distorted` 变体描述：`This floating weapon shifts and shimmers, time and space
  warping and bending as it moves. It appears to vibrate, as if it may explode at
  any moment.` → 现译「时空在其周围崩塌。」
- 由「在空间中打开一个孔洞」的技能召唤。
- 实体分类：`type = construct`（现译「机关」）、`subtype = weapon`（现译「武器」）。

## B3. 其他语言
| 英文 | 日文 ja_JP | 韩文 ko_KR | 繁中 zh_hant |
|---|---|---|---|
| `Animated Sword` | リビングソード（Living Sword） | 살아 움직이는 칼（活动的刀） | 次元之刃 |
| `Distorted Animated Sword` | リビングタイムソード（Living Time Sword） | 왜곡된 살아 움직이는 칼（扭曲的活动的刀） | 極·次元之刃 |

## B4. 已提出的问题
两轮独立审核均指出：`Animated`（活化的）与 `Distorted`（扭曲的）在译名中都没有对应；
「极·」是无据添加。

反方证据（供你权衡）：该实体确实由时空裂缝生成、周身时空扭曲，故「次元」并非无据，
只是没有译出 animated；日文同样没有直译 distorted，而是改用「タイム」。

## B5. 约束
- 若改，须整族同步：实体名 2 条 + 技能描述 2 条，共 4 处。
- 需能嵌入句式：「召唤一个____ 10 回合」「%s 似乎失去了控制…」。
- 本库对 `animated` 已有既定译法：`Animated %s` → 「活化的 %s」。
- 本库无其他 `Distorted` 实体可供参照（全库仅此 1 条）。

---

# 请回答

对 A、B **分别**回答：

1. **是否应当改名**？给出明确立场，并说明理由中最有分量的一条。
2. 若改，**推荐译名**：1 个首选 + 至多 2 个备选，各自说明取舍。
3. 把你的首选代入该议题「约束」一节列出的句式，逐条写出实际效果，检查是否通顺。
4. 若你的立场是「不改」，说明已提出的问题该如何交代。

请直接输出结论与论证，不要复述证据。用中文回答。
