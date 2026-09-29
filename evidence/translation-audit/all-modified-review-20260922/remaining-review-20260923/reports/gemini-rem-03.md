## rem-03 审核报告

### 逐条审核结论表格

| 条目 ID | 判定 | 依据 / 疑点编号（40字内） |
| :--- | :--- | :--- |
| entry-03829 | 未发现问题 | 原料实体与括注蛇草译名准确，全角括号规范无偏差 |
| entry-03831 | 未发现问题 | 原料实体与括注越桔译名准确，表达清晰规范 |
| entry-03832 | 未发现问题 | 原料实体与括注牛蒡译名准确，符合语境规范 |
| entry-03833 | 未发现问题 | 原料实体与括注金叶译名准确，符合语境规范 |
| entry-03834 | 未发现问题 | 矿物名称准确，完全符合术语库 global preferred 条目“斯莱特” |
| entry-03835 | 未发现问题 | 句子完整规范，矿物材料名称匹配术语库规范 |
| entry-03836 | 未发现问题 | 实体名称与括注蛇草对应正确，格式与标点规范 |
| entry-03837 | 未发现问题 | 实体名称与括注延龄草对应正确，表达准确 |
| entry-03838 | 未发现问题 | 实体名称与括注越桔对应正确，格式规范 |
| entry-03839 | 未发现问题 | 实体名称与括注牛蒡对应正确，格式规范 |
| entry-03840 | 未发现问题 | 实体名称与括注金叶对应正确，格式规范 |
| entry-03845 | 仅建议 | C01：well-being译全身心偏泛，If nothing else意译略宽 |
| entry-03849 | 存在问题 | C02：逃跑习语误为首个传送门，tinies蔑称与人称偏离 |
| entry-03850 | 未发现问题 | 叙事口吻传神，主客体与钻地避险语境准确无误 |
| entry-03851 | 存在问题 | C03：动词成语 join forces with 误译为名词“合作部队” |
| entry-03852 | 存在问题 | C04：施害者实体 Anomaly 误转为环境状语“在那场异常中” |
| entry-03853 | 存在问题 | C05：第三人称买家误转为第二人称“你想”，主客体错误 |
| entry-03854 | 存在问题 | C06：祈使习语误译为字面爱意，accommodations偏离 |
| entry-03856 | 存在问题 | C07：intervention看错词形误作发明，排气孔代词指代错误 |
| entry-03859 | 未发现问题 | 选民公告口吻严谨，初选与竞技规则表达准确无误 |

---

### 原子疑点详情

### C01 | entry-03845 | advisory
- **短引与差异**：“用他们的全身心信任守卫们”/“如果你愿意伸出援手的话”。原文“trust the Guard with their well-being”意为“将安危托付给守卫”，原译“全身心”泛化且偏离 well-being 本义；“If nothing else”意为“退一步说/至少”，非条件假设。
- **最强等价与处理**：表达虽通顺但偏离原意，建议微调为“将自身安危托付给守卫们”、“退一步说，你至少可以让一个……”。
- **出处**：[`tome-orcs/data/lore/emporium.lua:52,54`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/emporium.lua#L52-L54)

### C02 | entry-03849 | confirmed
- **短引与差异**：“我们要使用这个大陆上的第一个远行传送门，不管你们这些家伙喜不喜欢”。“taking the first [portal] off this continent”是“搭乘最早/最近离开这片大陆的传送门”逃命，误译为基数“第一个传送门”；“those tinies”是巨人对矮小种族的第三人称蔑称（小矮子们），误译为第二人称。
- **最强等价与处理**：属习语误读与人称偏离；改译为“随便找个最早离开这片大陆的远行传送门逃走，不管那些小矮子答不答应”。
- **出处**：[`tome-orcs/data/lore/gem.lua:65`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/gem.lua#L65)

### C03 | entry-03851 | confirmed
- **短引与差异**：“与联合王国的合作部队的良好的第一步”。原文“joining forces with the Allied Kingdoms”中“join forces with”为动词成语（携手合作/联合结盟），主语是“your kind”，原译误将 forces 当作名词“部队”，导致整句结构错乱。
- **最强等价与处理**：动词短语不可拆解为名词部队；改译为“你们一族……与联合王国携手联合的良好的第一步”。
- **出处**：[`tome-orcs/data/lore/internment-camp.lua:31`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/internment-camp.lua#L31)

### C04 | entry-03852 | confirmed
- **短引与差异**：“我们众多精英卫兵在那场异常中的牺牲”。原文“the deaths of Khulmanar ... at the hands of the Anomaly”中“the Anomaly”（特异点/异象实体）为施害者宾语（死于异象之手），原译误将主体实体理解为情境状语“在那场异常中”，丢失加害施动关系。
- **最强等价与处理**：不可将个体宾语转为抽象事件；改译为“死在特异点/异常者手中”。
- **出处**：[`tome-orcs/data/lore/misc.lua:45`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua#L45)

### C05 | entry-03853 | confirmed
- **短引与差异**：“要是你想把他们带回西部去的话”。原文“when I get a customer who wants them taken right back to the West”，承接前句“你不是唯一买家”，指遇到“其他客户”要求带回西方大陆时，原译误改为主语“你想”，发生人称混淆与主客体错误移位。
- **最强等价与处理**：前文已明确指出其他客户，改译为“每当有买家想把他们直接带回西部时”。
- **出处**：[`tome-orcs/data/lore/misc.lua:76`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua#L76)

### C06 | entry-03854 | confirmed
- **短引与差异**：“为了莱娜尼尔的爱，别再把远行传送门叫做远行传送门了”。“for the love of [Linaniil]”为祈使感叹口头习语（看在……的份上），误译为获得情爱“为了莱娜尼尔的爱”，属典型翻译腔错译。另“accommodations”误译为“安全设施”（实为食宿安置）。
- **最强等价与处理**：感叹祈使习语不可字面直译；改译为“看在莱娜尼尔的份上”。
- **出处**：[`tome-orcs/data/lore/misc.lua:91`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua#L91)

### C07 | entry-03856 | confirmed
- **短引与差异**：“害怕他们不谨慎的发明”/“排气行为通常是不可见的”。原文“careless intervention”系将“介入/干涉”看错词形误译为“发明（invention）”；代词“they”指代前句排气孔（pores and vents），非“排气行为”。另专名“IMMOLATUS”被臆译为成语“撼天动地”。
- **最强等价与处理**：硬伤错译无等价读法；改译为“鲁莽介入/轻率干涉”；“排气孔近乎隐形”；专名保留或音译“伊莫拉图斯/焚灭者”。
- **出处**：[`tome-orcs/data/lore/misc.lua:139,143,147`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua#L139-L147)

---

### 读取文件与版本限制说明

1. **实际读取文件**：
   - 规则与配置：[`evidence/.../RULES.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md)、[`source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json)、[`terms.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json)
   - 批次与快照：[`batches/rem-03.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-03.md)、[`snapshots/tome-orcs.lua:1830-1865`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua#L1830-L1865)
   - 冻结源码（SHA256核验通过）：
     - [`tome-orcs/data/ingredients.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/ingredients.lua) (`45a12c6837...`)
     - [`tome-orcs/data/lore/emporium.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/emporium.lua) (`0d5842ad1f...`)
     - [`tome-orcs/data/lore/gem.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/gem.lua) (`556355e204...`)
     - [`tome-orcs/data/lore/internment-camp.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/internment-camp.lua) (`11fb9bc3a1...`)
     - [`tome-orcs/data/lore/misc.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/misc.lua) (`0f33aa795e...`)
     - [`tome-orcs/data/lore/palace-fumes.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua) (`b57c1122b5...`)
2. **源码版本限制**：
   - 本次审核仅依据 `source-access.json` 中哈希固定的 DLC 快照源码文本进行核对；DLC 源码仓库 commit 及 1.7.4 目标版本未固定，未宣称核验 1.7.4 实际运行机制。未写入任何文件、未创建子代理、未读取任何历史报告。
