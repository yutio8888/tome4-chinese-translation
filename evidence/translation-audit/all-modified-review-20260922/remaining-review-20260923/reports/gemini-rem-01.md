# 译文审核报告：rem-01 批次（共 40 条）

根据审核规则，本报告采用只读旁路模式对 `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-01.md` 中的全部 40 条冻结译文条目进行逐条核验。比对依据包括公开冻结源码（SHA256 校验一致，注明来源未固定）、`snapshots/tome-orcs.lua` 同 section 上下文以及 `terms.json` 术语规范。

---

## 一、逐条判定表（按输入顺序排列）

| 序号 | 条目 ID | 判定状态 | Claim 编号 / 依据简要说明 |
| :--- | :--- | :--- | :--- |
| 1 | entry-03733 | 未发现问题 | 格式标签与大写警示语义完整，蒸汽巨人名词一致 |
| 2 | entry-03735 | 存在问题 | C01：漏译“on the scrying panel”，双重视角交错被混淆为窗外远眺 |
| 3 | entry-03736 | 未发现问题 | 召唤物战斗呐喊情绪与语境匹配 |
| 4 | entry-03737 | 未发现问题 | 格式标签完整，顺从语境传达准确 |
| 5 | entry-03738 | 存在问题 | C02：漏译“and broken”，缺失反派残酷折磨的关键心理与状态刻画 |
| 6 | entry-03739 | 未发现问题 | 标签完好，名词人名统一，语义忠实 |
| 7 | entry-03741 | 仅建议 | C03：“Give it back!”译为“拿出来”弱化了物归原主的索要语气，建议润色 |
| 8 | entry-03742 | 未发现问题 | 强调格式标签完整，主客体与语义准确 |
| 9 | entry-03743 | 未发现问题 | 简短疑问对白忠实准确 |
| 10 | entry-03745 | 未发现问题 | 务实商人情境传达清晰 |
| 11 | entry-03747 | 存在问题 | C04：“So, what'll it be?”商铺招呼习语误译为盘问行动意图的“你要做什么呢？” |
| 12 | entry-03748 | 存在问题 | C05：“front-row seat”习语望文生义硬译为“坐在椅子上”，破坏修辞对比 |
| 13 | entry-03749 | 未发现问题 | 战斗宣言对白忠实准确 |
| 14 | entry-03750 | 未发现问题 | 叙事完整，“软蹄者”称谓与同 section 白蹄人设保持一致 |
| 15 | entry-03751 | 未发现问题 | 问候语及玩家占位符保留完整 |
| 16 | entry-03752 | 未发现问题 | 克服英文原文缺词瑕疵，准确传达部族自由与暴君伏诛含义 |
| 17 | entry-03753 | 未发现问题 | 阵营专名“气之部族”“克鲁克部落”与术语规范完全一致 |
| 18 | entry-03754 | 未发现问题 | 白蹄、兽人名词及占位符准确，情节因果逻辑完整 |
| 19 | entry-03755 | 未发现问题 | 疑问对白简洁准确 |
| 20 | entry-03756 | 未发现问题 | 口语化对白，原意传达清晰 |
| 21 | entry-03757 | 未发现问题 | 任务道具交付文本忠实准确 |
| 22 | entry-03758 | 未发现问题 | 承接对白准确 |
| 23 | entry-03759 | 未发现问题 | 准确传达对机械怪物的讽刺口吻 |
| 24 | entry-03760 | 未发现问题 | 提问对白忠实准确 |
| 25 | entry-03761 | 未发现问题 | 动态占位符 `%s` 完好，反魔机制与魔瘾设定准确 |
| 26 | entry-03762 | 未发现问题 | 占位符 `%s` 完好，击退战斗日志标准规范 |
| 27 | entry-03764 | 未发现问题 | 占位符 `%s` 完好，牵引/拖动抗性判定日志准确 |
| 28 | entry-03765 | 未发现问题 | 地形遗迹交互描述忠实准确 |
| 29 | entry-03767 | 未发现问题 | 颜色格式标签完整，管道破裂事件传达准确 |
| 30 | entry-03768 | 未发现问题 | 机械门交互提示文本准确 |
| 31 | entry-03769 | 未发现问题 | 机械墙门交互提示文本准确 |
| 32 | entry-03772 | 仅建议 | C06：正统星辰施法者译为“魔术师”有马戏杂耍联想，建议“唤术师/咒术师” |
| 33 | entry-03773 | 未发现问题 | 金属材质“斯莱特”符合 preferred 术语规范，场面描写生动 |
| 34 | entry-03776 | 未发现问题 | 材质“斯莱特”规范，法杖描述忠实准确 |
| 35 | entry-03777 | 未发现问题 | 双占位符 `%s` 保留完整，动作日志准确 |
| 36 | entry-03779 | 未发现问题 | 植入体交互操作文本准确 |
| 37 | entry-03780 | 未发现问题 | 实体名称“斯莱特蒸汽枪”符合术语规范 |
| 38 | entry-03782 | 未发现问题 | 实体名称“斯莱特蒸汽链锯”符合术语规范 |
| 39 | entry-03783 | 未发现问题 | 材质短名“斯莱特”符合术语规范 |
| 40 | entry-03784 | 未发现问题 | 蒸汽科技药剂体系描述准确规范 |

---

## 二、原子疑点台账（Claim C01 - C06）

### C01
- **条目 ID**：`entry-03735`
- **原译短引**：“你从窗户里看见导弹朝目标飞去，飞向你视线远处，拥挤的飞船里惊恐的乘客那边。”
- **具体意义差异**：
  原文为：“you see its missile flying away from you through the window, as you see it racing towards your view, and the terrified passengers, on the scrying panel.”
  原文呈现了电影分镜式的双重观察视角对比：
  1. 透过操作室窗户（through the window），肉眼看到导弹从自身面前呼啸飞远（flying away from you）；
  2. 在探知面板的魔法画面中（on the scrying panel，前文设定为锁定在飞船内部客舱的探知视角），看到导弹正急速迎面冲向玩家的探知视点（racing towards your view）以及客舱中惊恐绝望的乘客。
  原译完全遗漏了“on the scrying panel”（在探知/显象面板上），并将“racing towards your view, and the terrified passengers”误译为“飞向你视线远处，拥挤的飞船里惊恐的乘客那边”，使得玩家肉眼仿佛能直接从窗户看清远方密闭飞船里的乘客，破坏了原文精妙的魔法监控设备双重视角叙事机制。
- **最强等价读法与处理**：
  若辩称“视线远处”是泛指画面呈现的景况，但前文已明确写道隔窗只能看到飞船外形，飞船客舱内的妇孺惊恐状况完全是通过探知面板（scrying panel）转播呈现的；漏译“on the scrying panel”属于客观语义缺失与叙事机制失真。
- **判定状态**：`confirmed`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/destructicus.lua:74-76`（SHA256: `ecf3e77e...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:358-360`
- **缺失证据**：无

---

### C02
- **条目 ID**：`entry-03738`
- **原译短引**：“不，你活着对我更有用！”
- **具体意义差异**：
  原文为：“No, you are more useful alive and broken to me!”
  原译遗漏了修饰约翰身心状态的关键并列形容词“and broken”（残破/崩溃/被折服）。对话语境中，约翰濒死哀求速死解脱（“let me have some rest”），玩家残忍地拒绝给予其安息，声明将其彻底摧毁崩溃并维持存活以供奴役利用（后续将其灵魂强行拘禁并奴役至戒指中，召唤台词皆为折磨痛楚的悲鸣）。遗漏“and broken”使冷酷的反派征服者形象与惩戒意图大幅弱化。
- **最强等价读法与处理**：
  若辩称“活着”已包含利用价值，但原文强调的是“alive and broken”双重状态（既要你活命，又要你身心崩溃、沦为废人奴隶），属于明确的形容词修饰缺失。应补全为“不，让你身心崩溃地活着对我才更有用！”或“你残破地活着对我更有用！”。
- **判定状态**：`confirmed`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-surrender.lua:96`（SHA256: `06d44429...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:410`
- **缺失证据**：无

---

### C03
- **条目 ID**：`entry-03741`
- **原译短引**：“拿出来，受死吧！！”
- **具体意义差异**：
  原文为：“Give it back! DIE!”
  原译为：“拿出来，受死吧！！”
  此处约翰因爱人艾琳被杀、戒指被玩家戴在身上炫耀而怒火中烧，“Give it back!”的明确诉求是“还给我！（物归原主）”。译为“拿出来”偏向“掏出来出示”，丢失了要求归还挚爱遗物的强烈悲愤色彩。
- **最强等价读法与处理**：
  结合后续立即触发死战的语境，“拿出来”可引申理解为逼迫玩家交出戒指，未完全脱离情境，但语气与内涵有所偏移。按规则作为表达风格澄清，不计为确认错译。
- **判定状态**：`advisory`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/john-worldmap.lua:26`（SHA256: `b645caec...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:426`
- **缺失证据**：无

---

### C04
- **条目 ID**：`entry-03747`
- **原译短引**：“那么，你要做什么呢？”
- **具体意义差异**：
  原文为：“So, what'll it be?”
  原译为：“那么，你要做什么呢？”
  在英语商业服务语境（尤其是酒馆、商店柜台）中，“What'll it be?”是极其固定、高度地道的掌柜招揽客套话，意为“那么，您想来点什么？/ 想买点什么？”。此处巨人商人卡托尔刚刚热情地向顾客玩家展示了满是珍奇武器护甲的陈列柜（“a glass display case loaded with exotic weaponry and armor”）与宣传海报，随即询问玩家的购买意向。译文生硬直译为“那么，你要做什么呢？”，脱离了商铺买卖语境，误将热情的商品推销变成对玩家行动企图的质询。
- **最强等价读法与处理**：
  即便店主在初次见面时对玩家怀有防备，但该分支（`id="back"`）是玩家再次光临选购商品时的标准台词，紧接的交互就是进入商品选购列表，因此该句语义必然是招揽选购“想买点什么？”，直译为“你要做什么”属于确凿的习语误译。
- **判定状态**：`confirmed`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:51`（SHA256: `1012ca4c...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:467`
- **缺失证据**：无

---

### C05
- **条目 ID**：`entry-03748`
- **原译短引**：“我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。”
- **具体意义差异**：
  原文为：“and I'd rather have a bird's-eye view of what you're about to do than a front-row seat.”
  原译为：“我更想站在上面鸟瞰你要做的事情，而不是坐在椅子上。”
  原文运用了鲜明的修辞反差：`bird's-eye view`（在私人飞船上的高空鸟瞰视角）与 `front-row seat`（前排座席，英语常用习语，比喻身处风暴中心、第一线直面冲击与危险）。卡托尔的意思是“大难临头之际，我宁可坐上飞船在万米高空安全地观赏你造成的浩劫，也不想留在地面第一排近距离遭殃”。译文将 `front-row seat` 望文生义生搬硬套成“坐在椅子上”，把富有戏剧感的生死避险修辞变成了荒诞无稽的“站着看还是坐椅子看”，造成核心语义扭曲与逻辑断裂。
- **最强等价读法与处理**：
  “坐在椅子上”在中文语境中无法建立起任何与“近距离直面危险”相关的联想，系典型翻译腔与习语硬译。应改为“而不是留在第一排近距离遭殃 / 而不是坐在前排近观危险”。
- **判定状态**：`confirmed`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua:57`（SHA256: `1012ca4c...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:474`
- **缺失证据**：无

---

### C06
- **条目 ID**：`entry-03772`
- **原译短引**：“星空魔术师”
- **具体意义差异**：
  原文为：“astral conjurer”
  原译为：“星空魔术师”
  该条目是晨曦之墙敌对精英施法者的实体名称（`sunwall-mage.lua`），其战斗配置掌握日光球、银河脉冲、超新星等强大天体魔法，外形描述为“身着绘有光明与黑暗图案华美长袍的法师”。“conjurer”在奇幻设定中为正统法师分支（咒法师/唤术师/具现师），译为“魔术师”带有浓厚的现代马戏杂耍、障眼戏法联想（stage magician），与严肃奇幻背景及高阶施法者身份严重不符。
- **最强等价读法与处理**：
  在早期古汉语和少数语境中“魔术”亦可指代奇法异术，且该词条作为怪物名称不影响战斗机制结算，故定性为风格与风味层面的优化建议（advisory），建议调整为“星空唤术师”或“星界咒法师”。
- **判定状态**：`advisory`
- **来源路径行号**：
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/npcs/sunwall-mage.lua:115`（SHA256: `e2c2dcc9...`，来源未固定）
  - 冻结原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:957`
- **缺失证据**：无

---

## 三、报告汇总统计

- **审核条目总数**：40 条
- **未发现问题**：34 条
- **存在问题（confirmed）**：4 条（C01, C02, C04, C05）
- **仅建议（advisory）**：2 条（C03, C06）
- **待确认（pending）**：0 条

---

## 四、实际读取路径与限制声明

1. **实际读取文件清单**：
   - 审核规则：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - 源码访问映射：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - 术语库：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
   - 输入批次清单：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-01.md`
   - 同 section 原译快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
   - 冻结公开源码（`.artifacts/i18n/all-modified-review-20260922/sources/orcs/`）：
     - `tome-orcs/data/chats/destructicus.lua`
     - `tome-orcs/data/chats/john-surrender.lua`
     - `tome-orcs/data/chats/john-worldmap.lua`
     - `tome-orcs/data/chats/kaltor-shop.lua`
     - `tome-orcs/data/chats/metash.lua`
     - `tome-orcs/data/chats/weissi-machine.lua`
     - `tome-orcs/data/damage_types.lua`
     - `tome-orcs/data/general/events/merchant-stall.lua`
     - `tome-orcs/data/general/events/sewer-alligator-nest.lua`
     - `tome-orcs/data/general/grids/mechstone.lua`
     - `tome-orcs/data/general/grids/mechwall.lua`
     - `tome-orcs/data/general/npcs/sunwall-mage.lua`
     - `tome-orcs/data/general/npcs/titan.lua`
     - `tome-orcs/data/general/objects/boss-artifacts.lua`
     - `tome-orcs/data/general/objects/generic-world-artifacts.lua`
     - `tome-orcs/data/general/objects/inscriptions.lua`
     - `tome-orcs/data/general/objects/steamgun.lua`
     - `tome-orcs/data/general/objects/steamsaw.lua`
     - `tome-orcs/data/general/objects/tinker.lua`

2. **限制与合规声明**：
   - 本次审核严格遵循只读 Reviewer 规范，未修改或写入任何工作区文件，未调用已归档 Skill，未创建任何子代理，亦未查阅任何历史审核报告。
   - 所有引用的 Embers of Rage（`orcs`）DLC 源码均已核对 SHA256 哈希值，其实际来源仓库 commit 及目标版本未固定，不宣称已核验 1.7.4 版本机制。
   - 本审核报告沿用用户明确授权的自然语言审核旁路，不附带正式 JSON contract，不宣称 `DONE_VERIFIED`。
