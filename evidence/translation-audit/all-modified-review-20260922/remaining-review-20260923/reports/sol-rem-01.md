---

已按指定入口只读交叉核验 **Flash C01–C06**，包括两项 advisory。六项均有足够的冻结文本与源码证据；其中 C04 的“确认错译”判断需要下调。

### C01 | entry-03735 | confirmed

原译短引：“你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。”

原文把**窗外导弹远去**与**探知面板上导弹迎面冲向画面和乘客**并列呈现。前文已写明面板显示飞船内部。译文漏掉“on the scrying panel”，把两个视角合成了窗外远眺；“飞向你视线远处”也没有传达面板画面中的迎面而来。即使将“视线”宽泛理解为画面视线，译文仍未交代画面的载体，因此疑点成立。证据：[源码 destructicus.lua 第44–50、73–76行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/destructicus.lua:73)、[冻结译文第350行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:350)。

### C02 | entry-03738 | confirmed

原译短引：“不，你活着对我更有用！”

原文是“alive **and broken**”：约翰活着且被摧垮，两种状态共同限定“更有用”。译文只保留“活着”。前一句约翰请求死亡和安息，随后该选项将其绑定到戒指；语境不能替代选项台词中漏掉的“broken”。疑点成立，但不必把它限定为某一种具体的肉体折磨。证据：[源码 john-surrender.lua 第97–103行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-surrender.lua:97)、[冻结译文第410行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:410)。

### C03 | entry-03741 | advisory

原译短引：“拿出来，受死吧！！”

“Give it back!”明说归还戒指；“拿出来”没有明说归还，削弱了约翰索回艾琳遗物的诉求。不过，约翰紧接着说感觉戒指在玩家身上，并要求玩家拿出它；在这一对峙中，“拿出来”仍可理解为交出戒指。保留表达澄清建议，不判确认错译。证据：[源码 john-worldmap.lua 第25–33行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-worldmap.lua:25)、[冻结译文第426–428行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:426)。

### C04 | entry-03747 | advisory

原译短引：“那么，你要做什么呢？”

商店回访语境下，“So, what'll it be?”自然可译为“想买点什么？”，现译不够像店主招呼顾客。但 Flash 所称“必然是在问选购商品，误译成盘问行动意图”证据不足：该对白接入的选项同时包括**看货、攻击和不购物**。“你要做什么呢？”可以概括这些选择，未造成明确的选项意义错误。将原 confirmed 判断下调为措辞建议。证据：[源码 kaltor-shop.lua 第24–31、40–45、66–69行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:24)、[冻结译文第467–470行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:467)。

### C05 | entry-03748 | confirmed

原译短引：“我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。”

“bird’s-eye view”与“front-row seat”对比的是**从飞船上远观**和**留在现场近距离目睹**。译文把后者写成单纯“坐在椅子上”，丢失“前排、近在事发处”的位置关系，令对比变成站与坐。即使将 *seat* 作字面座位理解，*front-row* 仍未译出。疑点成立；源码足以支持远近对比，无须推断飞船高度或具体灾害。证据：[源码 kaltor-shop.lua 第48–51行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:48)、[冻结译文第474–475行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:474)。

### C06 | entry-03772 | advisory

原译短引：“星空魔术师”。

源码将 *astral conjurer* 定义为持杖、施展星辰法术的法师实体；“魔术师”在现代汉语中容易让人想到舞台表演，“星界唤术师”等称呼可能更贴近角色。然而“魔术师”也能在奇幻语境中泛指施法者，现译未把实体误指成确定的另一种职业或机制。保留命名风格建议。证据：[源码 sunwall-mage.lua 第114–131行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/npcs/sunwall-mage.lua:114)、[冻结译文第957行](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:957)。

| 原 Claim | entry-ID | 交叉结论 |
|---|---|---|
| C01 | entry-03735 | confirmed：探知面板与双视角漏失 |
| C02 | entry-03738 | confirmed：“and broken”漏译 |
| C03 | entry-03741 | advisory：归还语气可更明确 |
| C04 | entry-03747 | advisory：购物措辞可改进；原 confirmed 判断不成立 |
| C05 | entry-03748 | confirmed：“front-row”远近对比漏失 |
| C06 | entry-03772 | advisory：实体命名风格建议 |

**读取范围与版本限制：**实际读取了指定批次入口、`RULES.md`、`batches/rem-01.md`、`reports/gemini-rem-01.md`、`source-access.json`、`terms.json`、`snapshots/tome-orcs.lua`，以及上列五份冻结 orcs 源码；未读取其他审核报告。五份源码的 SHA256 均与 `source-access.json` 登记值一致。orcs DLC 的来源仓库 commit 和目标版本未固定，以上结论针对该冻结文本与源码，不宣称已核验目标 1.7.4。未修改文件、创建代理或发现需另列的 N 项。
