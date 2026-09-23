# 匿名源码核验与归并：40 条 / 69 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方69项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好69行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03413

### C01 | entry-03413 | 存在问题

原文为“chance for the seed to take hold … creatures rank”，译文为“种子的存活几率基于宿主的级别”。这里把**寄生成功几率**写成了存活几率，并把生物的 **rank** 写成等级。`tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua:647–665` 按 `target.rank` 设定几率；`tome-ashes-urhrok/data/timed_effects.lua:515–518` 在宿主死亡时用该几率决定是否生成种子。两项均为译文新增的信息偏差。状态：**已证实，限所给 DLC 快照**。



## O002 | entry-03413

### C01 | entry-03413 | 存在问题

原文：“Implanting a seed into **unique demons**”；译文：“植入**史诗生物（Unique）**的体内”。

译文保留了 Unique，却遗漏“恶魔”这一生物类型限定，将特殊种子规则的适用对象扩大为史诗生物。后面的“有对应的恶魔种子”不能替代原文明示的宿主类型条件。

证据：`D/data/talents/corruptions/demonic-pact.lua:364–369`，`createSeed` 仅在 `host.type == "demon"` 时优先按宿主名称选择种类；其他宿主走随机种类分支。文本遗漏已证实，快照对目标版本的适用性未固定。



## O003 | entry-03413

### C01 | entry-03413 | 存在问题
- **原文与译文：** 原文「Implanting a seed into unique demons … grant a seed of that type」，译文为「成功将种子植入史诗生物（Unique）的体内…必定会获得该恶魔种子」。
- **问题：** 原文的作用对象是 demons（恶魔），译文丢掉了这个限定，范围扩大成任何史诗生物。
- **源码依据：** `talents/corruptions/demonic-pact.lua:364`（createSeed）。只有 `host.type == "demon"` 时，种子类型才取宿主名；非恶魔宿主一律从 `seeds[lvl]` 随机抽取。因此，非恶魔的史诗宿主不会给出同类种子。



## O004 | entry-03413

### C01 | entry-03413 | 存在问题
- **原文短引**：`Implanting a seed into unique demons, if successful, will always try to grant a seed of that type, if available.`
- **译文短引**：`如果成功将种子植入史诗生物（Unique）的体内，且它有对应的恶魔种子的话，你必定会获得该恶魔种子。`
- **问题具体内容**：对象与范围扩大错误。原文明确限定为 `unique demons`（史诗/独特恶魔），译文错译为泛指的“史诗生物（Unique）”，漏掉了“恶魔”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua:364-369`（`createSeed` 函数内）：
  ```lua
  if host.type == "demon" then
      kind = host.name
      if not demon_seeds_effects[kind] then kind = rng.table(seeds[lvl]) end
  else
      kind = rng.table(seeds[lvl])
  end
  ```
  代码明确检查宿主实体类型是否为 `demon`；只有恶魔宿主才会匹配自身名字并给予对应的恶魔种子。非恶魔的史诗生物（如人形怪、亡灵等 Unique）进入 `else` 分支，只能随机获取通用种子池中的种子，绝不会获得对应生物的专属种子。译文遗漏“恶魔”导致机制描述失真，误导玩家对任何史诗生物植入种子。

---



## O005 | entry-03413

### C02 | entry-03413 | 仅建议
- **原文短引**：`If the attack hits a demonic seed tries to take hold inside your foe...`
- **译文短引**：`如果攻击命中，你会将恶魔种子植入目标体内...`；`造成 %d%% 盾牌伤害并眩晕 敌人 %d 回合。`
- **建议简述**：偏好与轻度润色。原文为“tries to take hold”，植入本身受后续几率（5%–100%）限制，“你会将恶魔种子植入”语气稍显绝对，但下文已明确说明存活几率，未构成不可逆信息断裂；另“眩晕 敌人”之间存在一处多余空格。两者均不属于阻断性事实缺陷，列为建议。
- **状态**：仅建议

---



## O006 | entry-03413

### C02 | entry-03413 | 存在问题

原文及译文都把几率概括为依生物阶级而定，但 `demonic-pact.lua:654–655` 将首次使用的几率强制设为 100%。这是**英文原文已有、译文沿袭**的例外遗漏，不归因于译者。状态：**已证实，限所给 DLC 快照**。



## O007 | entry-03413

### C02 | entry-03413 | 存在问题
- **原文与译文：** 原文「it will instead increase its level if the host was of higher level … and the demon inside will regenerate … and resurrect」，译文为「如果…已有同类种子，且宿主等级高于恶魔的等级，它会提升种子的等级。此外，里面的恶魔会恢复…复活」。
- **问题：** 译文把「宿主等级更高」提成整句的前提，回复与复活于是也像要满足这个等级条件才会发生。另外，「instead」（不再生成新种子）这层信息丢失了。
- **源码依据：** `demonic-pact.lua:536` 在找到同类种子时就调用 updateSeed。其中 `:440` 取 `hlevel = math.max(hlevel, demon.level)`，`:451` 清除死亡状态，`:467` 执行治疗，三者都不依赖等级条件。



## O008 | entry-03413

### C03 | entry-03413 | 上游误述（不计为译文缺陷）
- **内容：** 原文称恶魔「regenerate %d%% health」，源码 `:467` 实际是 `demon:heal(t:_getHeal(self))`，getHeal 为 10–30 点固定值，不是百分比。
- **结论：** 译文照搬原文，问题来自上游。



## O009 | entry-03413

### C04 | entry-03413 | 仅建议
- **内容：** 「眩晕 敌人」中间多了一个空格。
- **为何只是建议：** 属于排版问题，不影响参数和信息。



## O010 | entry-03416

### C02 | entry-03416 | 存在问题

原文：“within … **up to %d grids**”；译文：“传到 **%d 码外**的一个位置”。

“至多”的距离上限被表达成指定距离之外，改变了传送范围信息。“误差 %d”描述落点散布，不能补回最大距离的含义。

证据：`D/data/talents/corruptions/demonic-pact.lua:855–875`，第一个显示参数用于目标选择的 `range`，第二个用于 `teleportRandom` 的散布半径；`:891–895` 给出对应格式参数。



## O011 | entry-03416

### C03 | entry-03416 | 仅建议
- **原文短引**：`Teleports you randomly within a small range of up to %d grids with %d precision.`
- **译文短引**：`传到 %d 码外的一个位置，误差 %d。`
- **建议简述**：措辞偏好。原文“within a small range of up to %d grids”指最大射程为 %d 码范围，“传到 %d 码外”易被误读为传送至固定的 %d 码距离。但由于玩家在实际操作中需要选取目标格，且属于 ToME 空间传送类技能的通用表述，未导致参数或机制严重偏离，仅属润色偏好。
- **状态**：仅建议

---



## O012 | entry-03416

### C03 | entry-03416 | 存在问题

原文“up to %d grids with %d precision”，译文“传到 %d 码外的一个位置，误差 %d”。“%d 码外”把**最大可选距离**写成了确定距离。`demonic-pact.lua:855–864、888–895` 将第一参数用作选点范围，将第二参数用作目标附近的随机传送范围。状态：**已证实，限所给 DLC 快照**。



## O013 | entry-03416

### C03 | entry-03416 | 存在问题

原文：“a random demon **from your seeds**”；译文：“随机召唤一个恶魔”。

译文遗漏随机选择的来源集合。末段说明施法需要装备种子，但没有说明召唤对象来自这些种子；“存在种子才能施法”与“从种子中的恶魔随机选择”是不同的信息。

证据：`D/data/talents/corruptions/demonic-pact.lua:326–343` 的 `availableDemonSeed` 构造可用种子列表；`:851` 获取该列表，`:879–882` 从列表随机取出恶魔并召唤。



## O014 | entry-03416

### C04 | entry-03416 | 存在问题

译文说视线外目标“有一定几率失败”；英文的 “fizzle” 也有此歧义。`demonic-pact.lua:866–875` 显示触发该分支时，法术改为从施法者位置进行随机传送，并非没有传送效果。此项主要是**英文原文沿袭的机制误述**，译文的“失败”未说明实际后果。状态：**已证实，限所给 DLC 快照**。



## O015 | entry-03416

### C04 | entry-03416 | 待确认

原文：“there is a chance the spell will fizzle”；译文：“有一定几率失败”。

快照中，视线外触发该分支后会退回以自身为中心的随机传送，随后仍继续尝试召唤，并非直接终止技能。

证据：`D/data/talents/corruptions/demonic-pact.lua:867–882`，失败分支重设 `x, y, rad`，然后继续执行 `teleportRandom`；该分支的日志也明确包含“works randomly”。

这是英文与译文共同存在的描述缺口。快照行为可证，但尚缺目标 DLC 版本与该快照一致的证明，不能确认为目标版本的翻译新增错误。



## O016 | entry-03416

### C05 | entry-03416 | 存在问题
- **原文与译文：** 原文「within a small range of up to %d grids」，译文为「传到 %d 码外的一个位置」。
- **问题：** 「up to」（最多）是距离上限，译文读起来像固定距离。
- **源码依据：** `demonic-pact.lua:862-875`。目标的 range 为 getRange，属于上限；随后在所选点周围 radius 范围内 teleportRandom。



## O017 | entry-03416

### C06 | entry-03416 | 存在问题
- **原文与译文：** 原文「summon a random demon from your seeds」，译文为「随机召唤一个恶魔」。
- **问题：** 「from your seeds」丢失，召唤来源的限定没了，读者会以为召唤的是任意随机恶魔。
- **源码依据：** `demonic-pact.lua:879` 为 `rng.table(list).demon`，list 来自已穿戴的种子（availableDemonSeed）。



## O018 | entry-03416

### C07 | entry-03416 | 上游误述（不计为译文缺陷）
- **内容：** 原文「fizzle」被译为「失败」。
- **源码依据：** `demonic-pact.lua:867-871` 显示，不在视线内时有 35%（外加地图属性修正）的几率改为以自身为中心、按全射程随机传送，并不是施法失败。
- **结论：** 误述来自英文原文。



## O019 | entry-03419

### C04 | entry-03419 | 存在问题
- **原文短引**：`This effect stacks multiplicatively up to %d times.`
- **译文短引**：`这个效果能叠加至最多 %d 层。`
- **问题具体内容**：关键数学/机制修饰语遗漏。原文明确声明“stacks multiplicatively”（以乘算方式叠加），译文完全漏译了“乘算/以乘算方式”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:805, 817`（`DARK_REIGN` 效果）：
  ```lua
  local p = 1 for i = 1, old_eff.stacks do p = p * 0.92 end p = 100 * (1 - p)
  ```
  亲和计算逻辑是经典的乘算法则（每层吸收剩余伤害的 8%，实际亲和为 $100\% \times (1 - 0.92^n)$）：1 层为 8%，2 层为 15.36%（而非加算的 16%），3 层为 22.13%（而非 24%）。缺少“乘算”，玩家会按照线性加算预期效果，丢失了核心数值机制信息。

---



## O020 | entry-03419

### C05 | entry-03419 | 存在问题

原文明确为“stacks multiplicatively”，译文仅说“能叠加至最多 %d 层”，丢失了**乘法叠加方式**。`tome-ashes-urhrok/data/timed_effects.lua:805、813–820` 以每层乘以 `0.92` 计算总亲和。状态：**已证实，限所给 DLC 快照**。



## O021 | entry-03419

### C05 | entry-03419 | 存在问题

原文：“stacks **multiplicatively**”；译文：“能叠加至最多 %d 层”。

译文仅保留层数上限，遗漏叠加算法。这会影响玩家对多层亲和数值的理解，不属于措辞偏好。

证据：`D/data/timed_effects.lua:805、813–820`，每层将剩余比例乘以 `0.92`，再计算 `100 × (1 − 剩余比例)`。例如快照中两层为 15.36%，并非直接相加的 16%。乘法限定在冻结英文中也明确存在。



## O022 | entry-03419

### C08 | entry-03419 | 存在问题
- **原文与译文：** 原文「This effect stacks multiplicatively up to %d times」，译文为「能叠加至最多 %d 层」。
- **问题：** 译文漏掉「乘算叠加」，玩家会按每层 8% 线性累加去理解。
- **源码依据：** `timed_effects.lua:805/817`（DARK_REIGN）的计算是 `p = 1 - 0.92^stacks`。



## O023 | entry-03420

### C05 | entry-03420 | 存在问题
- **原文短引**：`Pay %d%% of your current life and gain 100%% darkness damage conversion for 1 turns.`
- **译文短引**：`支付 %d%% 当前生命值，1 回合内你造成的所有伤害转化为黑暗伤害。`
- **问题具体内容**：伤害类型术语错误。将伤害类型 `darkness damage` 误译为“黑暗伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  按术语表（`INPUT.md:691`）明确规则：`darkness` 在伤害类型语境（`T.GAME.DAMAGE`，combat）下标准译名为“暗影”；`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/doom-covenant.lua:32` 亦为 `DamageType.DARKNESS`。同树前一天赋 entry-03419 均译为“暗影伤害”，同效果 Buff 描述 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:845`（`context.lua:112`）亦为“你的所有伤害转化为暗影伤害”。译为“黑暗伤害”造成系统伤害类型概念混乱。

---



## O024 | entry-03420

### C09 | entry-03420 | 仅建议
- **内容：** 本条用「黑暗伤害」，同组 03419、03438 用「暗影伤害」（术语库 darkness 为 existing「暗影」）。另外，「黑暗支配开启」对一个被动天赋的效果来说稍显别扭。
- **为何只是建议：** 语义没有错，只是用词一致性问题。



## O025 | entry-03422

### C06 | entry-03422 | 存在问题

原文和译文均称诅咒持续 **5 回合**，而 `tome-ashes-urhrok/data/talents/corruptions/doom-shield.lua:177–185` 调用 `setEffect(...EFF_CURSE_IMPOTENCE, 10, ...)`，传入时长为 **10**。这是**原文已有、译文沿袭**的数值差异；本包未提供该效果定义及目标版本源码，最终显示时长的适用性仍需核对。状态：**快照内调用参数已证实；目标版本适用性待确认**。



## O026 | entry-03422

### C06 | entry-03422 | 待确认

原文：“for **5 turns**”；译文：“**5 回合**内”。

快照的格挡反击回调传给诅咒效果的基础持续时间为 10。

证据：`D/data/talents/corruptions/doom-shield.lua:177–185`，`on_cs` 调用 `setEffect(...EFF_CURSE_IMPOTENCE, 10, ...)`；`E/game/modules/tome/data/timed_effects/magical.lua:949–964` 确认该效果降低所有伤害。持续时间还会进入 `Actor:on_set_temporary_effect` 的豁免处理，不能把基础赋值 10 简化为所有目标必定持续 10 回合。

这是沿袭英文的数值差异。尚缺固定目标 DLC 版本证明。



## O027 | entry-03422

### C10 | entry-03422 | 上游误述（不计为译文缺陷）
- **内容：** 原文和译文都写「5 回合」，源码 `doom-shield.lua:185` 设置 CURSE_IMPOTENCE 的持续时间为 10。
- **结论：** 译文忠实于原文，误述来自上游。



## O028 | entry-03424

### C06 | entry-03424 | 待确认
- **原文短引**：`...allowing you to see all enemies within %d spaces for the next 3 turns.`
- **译文短引**：`...让你能够在 4 回合内觉察到 %d 码内的所有敌对生物。`
- **问题具体内容**：数值与英文原文不一致（原文 3 turns vs 译文 4 回合）。经核对公开快照源码，代码实际行为与译文一致，但与原文字面冲突；因 DLC 源码未固定 commit，目标版本适用性保留待确认。
- **状态**：待确认
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/fearfire.lua:75`：
  ```lua
  self:setEffect(self.EFF_SENSE, 4, {
      range = rad,
      actor = 1,
  })
  ```
  公开快照源码中实际施加的持续时间确实是硬编码的 4 回合（`EFF_SENSE, 4`），而英文字符串硬编码写着 `3 turns`，属于上游代码与技能文本脱节。译文虽然反映了快照源码行为，但由于 ashes-urhrok DLC 来源未固定 commit（`source-access.json:23` 为 unpinned），无法完全排除目标正式版本是否向上游文本统一为 3，目标版本适用性缺口保留为待确认。

---



## O029 | entry-03424

### C07 | entry-03424 | 待确认

原文：“for the next **3 turns**”；译文：“在 **4 回合**内觉察”。

不能仅按英文数字判译文错误。快照明确调用 `setEffect(self.EFF_SENSE, 4, ...)`。

证据：`D/data/talents/corruptions/fearfire.lua:74–78`；`E/game/modules/tome/data/timed_effects/physical.lua:952–972` 的 `SENSE` 将参数用于生物感知；`E/game/engines/default/engine/interface/ActorTemporaryEffects.lua:117–131` 将传入持续时间写入效果。

译文与快照赋值一致，英文与快照不一致。尚缺目标 DLC 版本对应关系，故保留待确认，不计作已证实错误。



## O030 | entry-03424

### C11 | entry-03424 | 未发现问题（偏离英文，但与源码一致）
- **内容：** 原文写「next 3 turns」，译文写「4 回合」。
- **源码依据：** `fearfire.lua:75` 为 `setEffect(EFF_SENSE, 4, …)`。引擎 `ActorTemporaryEffects.lua` 的 timedEffects（第 78–109 行）先检查 `dur<=0` 再递减，所以实际约持续 4 回合。
- **结论：** 译文与实现一致，不算缺陷。



## O031 | entry-03425

### C07 | entry-03425 | 存在问题

原文与译文都称移除“所有”负面效果。`tome-ashes-urhrok/data/talents/corruptions/fearfire.lua:104–117` 实际只移除 `status == "detrimental"`、`type ~= "other"` 且非 `cross tier` 的效果。“所有”遗漏了这些排除条件，属于**原文已有、译文沿袭**的范围误述。状态：**已证实，限所给 DLC 快照**。



## O032 | entry-03425

### C08 | entry-03425 | 待确认

原文：“Removes **all detrimental effects**”；译文：“移除**所有负面状态**”。

快照有明确排除条件：仅清除 `status == "detrimental"`、`type ~= "other"` 且不是 `"cross tier"` 的效果。

证据：`D/data/talents/corruptions/fearfire.lua:104–117`，清除过滤函数决定哪些效果计入 `cleansed`，之后再按清除数量计算自灼伤害。译文的总伤害、7 回合及瞬发部分未发现差异。

范围过宽沿袭英文。目标版本是否采用这一过滤实现仍待确认。



## O033 | entry-03429

### C12 | entry-03429 | 仅建议
- **内容：** 选择目标的提示用「受害者」，技能描述 03430 和效果描述用「牺牲生物」，同一流程里称呼不一致。
- **为何只是建议：** 不导致错误信息。



## O034 | entry-03430

### C08 | entry-03430 | 存在问题

原文“victim takes %d%% of the damage”，译文“%d%% 伤害由牺牲生物承受”容易表示伤害从源生物**转移**给受害者。`tome-ashes-urhrok/data/timed_effects.lua:715–724` 在源生物受击后，另对受害者调用 `takeHit`；源生物原伤害并未由此转移。状态：**已证实，限所给 DLC 快照**。



## O035 | entry-03430

### C09 | entry-03430 | 存在问题

原文：“the source creature takes damage **the victim takes %d%% of the damage**”；译文：“**%d%% 伤害由牺牲生物承受**”。

“由……承受”把另一生物描述成原伤害的承担者，容易形成分担或转移关系；原文及冻结邻近状态说明描述的是原目标受伤后，另一目标也受到额外伤害。两者对源生物是否减伤的含义不同。

证据：`D/data/timed_effects.lua:708` 明写 “will **also** be done”；`:715–731` 计算 `cb.value × eff.power / 100` 后对受害者调用 `takeHit`，没有扣减源生物的 `cb.value`。固定本体 `E/game/modules/tome/class/Actor.lua:3013–3014` 消费该回调值。



## O036 | entry-03430

### C13 | entry-03430 | 存在问题
- **原文与译文：** 原文「the victim takes %d%% of the damage」，译文为「%d%% 伤害由牺牲生物承受」。
- **问题：** 「由…承受」暗示这部分伤害从源生物转嫁出去，源生物因此少受伤害。
- **源码依据：** `timed_effects.lua:715-722`（LINK_OF_PAIN 的 callbackOnHit）没有修改 cb.value，只是另外对 victim 执行 `takeHit(cb.value*power/100)`。源生物仍承受全额伤害。



## O037 | entry-03431

### C07 | entry-03431 | 存在问题
- **原文短引**：`Any time you damage this foe in melee while it bleeds you get healed for %d (this can only happen once per turn).`
- **译文短引**：`每次你攻击被恶魔角刺穿的目标时，你回复 %d 生命（每回合至多 1 次）。`
- **问题具体内容**：关键机制与操作条件遗漏。原文严格限定“in melee”（近战）且“damage”（造成伤害），译文简略翻译为“每次你攻击...”，遗漏了“近战”和“造成伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:683-686`（`EFF_DEMONIC_CUT` 效果）：
  ```lua
  callbackOnMeleeHit = function(self, eff, src, dam)
      if not dam or dam <= 0 or src ~= eff.src then return end
      src:heal(eff.heal)
  ...
  ```
  该效果的生命回复回调挂在 `callbackOnMeleeHit` 上，明确要求必须是近战命中且造成有效伤害（`dam > 0`）。若玩家使用远程法术、弓箭或未造成有效伤害的攻击，均无法触发治疗。遗漏“近战”使玩家无法知晓真实的技能触发生效范围。

---



## O038 | entry-03431

### C08 | entry-03431 | 存在问题
- **原文短引**：`...causing it to bleed black blood for 50%% of the damage done as darkness over 5 turns.`
- **译文短引**：`...流血 5 回合，合计受到额外 50%% 黑暗伤害。`
- **问题具体内容**：伤害类型术语错误。将 `as darkness` 伤害类型错译为“黑暗伤害”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/infernal-combat.lua:153`：
  ```lua
  DamageType:get(DamageType.DARKNESS).projector(self, tgt.x, tgt.y, DamageType.DARKNESS, dam)
  ```
  代码明确使用 `DamageType.DARKNESS`。依据术语表（`INPUT.md:691`），`darkness` 在伤害类型分类（`T.GAME.DAMAGE`）下统一确立为“暗影”，不得译为“黑暗”。

---



## O039 | entry-03431

### C09 | entry-03431 | 存在问题

原文限定“damage this foe **in melee while it bleeds**”，译文写成“每次你**攻击**被恶魔角刺穿的目标”。它遗漏近战、造成伤害及流血仍有效三个触发条件。`tome-ashes-urhrok/data/timed_effects.lua:673–686` 的 `DEMONIC_CUT.callbackOnMeleeHit` 只在该效果存在、来源相同且伤害大于零时治疗。状态：**已证实，限所给 DLC 快照**。



## O040 | entry-03431

### C10 | entry-03431 | 存在问题

原文：“damage this foe **in melee while it bleeds**”；译文：“每次你**攻击被恶魔角刺穿的目标**时”。

译文遗漏近战、实际造成伤害，以及仍处于流血效果期间这些触发限定，将回血条件扩大为对曾被刺穿目标的攻击。

证据：`D/data/timed_effects.lua:683–686` 的 `callbackOnMeleeHit` 检查伤害为正且攻击来源等于效果来源后才治疗；效果存在期间才有该回调。`E/game/modules/tome/class/interface/Combat.lua:643` 在近战命中流程中调用它。



## O041 | entry-03431

### C11 | entry-03431 | 待确认

原文：“only happen **once per turn**”；译文：“**每回合至多 1 次**”。

已读快照的治疗回调没有每回合次数检查；每次符合条件的近战命中都会调用治疗。

证据：`D/data/timed_effects.lua:683–692`；固定本体 `E/game/modules/tome/class/interface/Combat.lua:643` 的调用点，以及 `E/game/modules/tome/class/Actor.lua:6049–6075` 的回调登记关系。

这是译文沿袭英文的限制，与所读实现不一致。尚缺目标 DLC 版本及对应加载组合的证明，保留待确认。



## O042 | entry-03431

### C14 | entry-03431 | 存在问题
- **原文与译文：** 原文「bleed … for 50%% of the damage done as darkness over 5 turns」，译文为「合计受到额外 50%% 黑暗伤害」。
- **问题：** 百分比的基数「of the damage done」（本次命中的伤害）丢失，「额外 50%」可以读成其他基数的加成。
- **源码依据：** `infernal-combat.lua:168`，`dam = dam * 0.5 / 5`，每回合一跳。



## O043 | entry-03431

### C15 | entry-03431 | 存在问题
- **原文与译文：** 原文「Any time you damage this foe in melee」，译文为「每次你攻击…目标时」。
- **问题：** 「近战」这个条件丢失，远程攻击和法术看起来也能触发回复。
- **源码依据：** `timed_effects.lua:683`，DEMONIC_CUT 只挂在 callbackOnMeleeHit 上，并要求 `dam > 0` 且 `src == eff.src`。



## O044 | entry-03431

### C16 | entry-03431 | 上游误述（不计为译文缺陷）
- **内容：** 原文和译文都有「每回合至多 1 次」，但 `timed_effects.lua:683-686` 没有 turn_procs 之类的限制。
- **结论：** 误述来自上游。



## O045 | entry-03433

### C09 | entry-03433 | 存在问题
- **原文短引**：`Your successful melee hits apply a stacking effect that decreases damage done by %d%%.`
- **译文短引**：`你的攻击能够惊吓目标，降低目标 %d%% 的伤害。`
- **问题具体内容**：触发条件关键限定词遗漏。原文明确为“successful melee hits”（近战攻击命中），译文直接泛化为“你的攻击”，遗漏了“近战”与“命中”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/oppression.lua:72-75`：
  ```lua
  callbackOnMeleeAttack = function(self, t, target, hitted)
      local tt = self:isTalentActive(t.id)
      if not tt then return end
      if not hitted then return end
  ...
  ```
  代码通过 `callbackOnMeleeAttack` 回调监听，并且严格检验 `if not hitted then return end`。该技能树的核心设计即“通过近战贴身并命中敌人提供防御”（见该文件行 22 设计注释），法术与远程攻击均不触发。译文直接写“你的攻击”，丢失了关键的作用方式和门槛。

---



## O046 | entry-03433

### C10 | entry-03433 | 存在问题

原文“successful melee hits”，译文“你的攻击能够惊吓目标”，遗漏**近战命中**条件。`tome-ashes-urhrok/data/talents/corruptions/oppression.lua:72–81` 的 `callbackOnMeleeAttack` 在 `hitted` 为假时直接返回。状态：**已证实，限所给 DLC 快照**。



## O047 | entry-03433

### C12 | entry-03433 | 存在问题

原文：“Your **successful melee hits**”；译文：“你的**攻击**能够惊吓目标”，并称“每次攻击会刷新”。

译文遗漏“近战”和“成功命中”，扩大了叠加及刷新的触发条件。法术攻击、远程攻击或未命中的攻击不能从原文获得同样承诺。

证据：`D/data/talents/corruptions/oppression.lua:72–81`，仅通过 `callbackOnMeleeAttack` 进入，随后明确以 `if not hitted then return end` 排除未命中。



## O048 | entry-03433

### C17 | entry-03433 | 存在问题
- **原文与译文：** 原文「Your successful melee hits」，译文为「你的攻击」。
- **问题：** 「命中」和「近战」两个触发条件都丢了。
- **源码依据：** `oppression.lua:72-75`，callbackOnMeleeAttack，且 `if not hitted then return end`。



## O049 | entry-03436

### C18 | entry-03436 | 仅建议
- **内容：** 「乌鲁洛克之口：角度增加 %d」缺少单位「度」；原文为「by %d degrees」，数值为 `dest*10`，作用于 `fearfire.lua:186` 的 cone_angle。
- **为何只是建议：** 上下文能看出是角度。



## O050 | entry-03437

### C10 | entry-03437 | 存在问题
- **原文短引**：`Hasten yourself out of phase, teleporting you to a specific location up to %d spaces away.`
- **译文短引**：`加速自身，以至于脱离空间，传送半径 %d。`
- **问题具体内容**：范围机制与玩家操作信息丢失且失真。原文为“teleporting you to a specific location up to %d spaces away”（将你传送至最远 %d 码内的一个指定位置），译文篡改为“传送半径 %d”。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/misc/races.lua:40, 47, 56-68`：
  ```lua
  range = function(self, t) return self:attr("control_haste_doom") and 5 or 4 end,
  ...
  target = function(self, t) return {type="beam", range=self:getTalentRange(t), nolock=true, talent=t} end,
  ...
  self:teleportRandom(x, y, 0)
  ```
  该技能为精准定向位移技能，瞄准类型为 `beam`，目标范围参数是最大施法距离 `range`（4 或 5 码），落点精度为 0（即精确传送至玩家点击的目标空地 `x, y`）。译文写成“传送半径 %d”，完全丢失了“指定位置”的操作属性，且将“最远距离/射程”误导为“以自身为中心的随机传送半径”，严重误导机制理解。

---



## O051 | entry-03437

### C11 | entry-03437 | 存在问题

原文说传送到距离内的“specific location”，译文仅说“传送半径 %d”，丢失了**由玩家指定落点**的信息。`tome-ashes-urhrok/data/talents/misc/races.lua:58–69` 先获取并检查目标坐标，再以随机半径 `0` 传送至该坐标。状态：**已证实，限所给 DLC 快照**。



## O052 | entry-03437

### C13 | entry-03437 | 存在问题

原文：“teleporting you to a **specific location** up to %d spaces away”；译文：“**传送半径 %d**”。

译文只留下距离，没有表达可指定落点这一玩家操作信息。它没有让读者区分定点传送与范围内随机传送。

证据：`D/data/talents/misc/races.lua:55–68`，技能读取玩家选择的坐标，检查距离和空位后，调用 `teleportRandom(x, y, 0)`；散布半径为零。遗漏在冻结文本中直接可证。



## O053 | entry-03437

### C19 | entry-03437 | 存在问题
- **原文与译文：** 原文「teleporting you to a specific location up to %d spaces away」，译文为「传送半径 %d」。
- **问题：** 「指定的精确落点」这层信息丢失，「传送半径」容易让人理解成在半径内随机落点。
- **源码依据：** `talents/misc/races.lua:68`，`teleportRandom(x, y, 0)`，落点半径为 0，是精确传送。



## O054 | entry-03437

### C20 | entry-03437 | 存在问题（术语）
- **原文与译文：** 原文「out of phase」，译文为「脱离空间」「停留在相位外」。
- **问题：** 这里描述的是 EFF_OUT_OF_PHASE 状态（`races.lua:73`）。引擎固定 commit 下，`game/modules/tome/data/timed_effects/magical.lua:2583` 的状态名为「Out of Phase」。术语库 preferred 为「脱离现实」，备注写明「统一沿用效果定义」。译文没有沿用这个名字，玩家难以把描述和状态栏里的效果对上。



## O055 | entry-03437

### C21 | entry-03437 | 仅建议
- **内容：** 「全体抗性」与术语库 preferred「全部抗性」不同。
- **为何只是建议：** 该术语行针对面板标签（_t），语义也不受影响。



## O056 | entry-03438

### C11 | entry-03438 | 仅建议
- **原文短引**：
  - `...triggers a darkness explosion of radius 1 for half the damage...`
  - `...when you transform the cooldowns of Haste of the Doomed and Pitiless are reset`
- **译文短引**：
  - `...在半径 1 的范围内产生一次暗影爆炸，造成额外 50%% 伤害...`
  - `...变形时重置种族技能“末日加速”与种族技能“无情”`
- **建议简述**：措辞偏好。爆炸伤害在代码中为 `DamageType.DARKNESS, val / 2`，译文表达为“额外 50% 伤害”在数学上等价，但表述为“造成相当于该次伤害 50% 的暗影伤害”在 AoE 语境下更严谨；重置技能处遗漏了“冷却时间”，但在汉语游戏语境中“重置技能”通常理解为重置冷却。两者均属建议。
- **状态**：仅建议

---



## O057 | entry-03438

### C14 | entry-03438 | 存在问题

原文：“the **cooldowns** of Haste of the Doomed and Pitiless are reset”；译文：“重置种族**技能**‘末日加速’与种族技能‘无情’”。

译文遗漏被重置的是冷却时间，改变了动作对象。“技能重置”需要读者自行补出冷却含义，未完整表达原文明确说明的信息。

证据：`D/data/talents/misc/races.lua:133–134`，分别对两个技能调用 `alterTalentCoolingdown(..., -1000)`。两个技能的名称与冻结语境一致，问题不在专名。



## O058 | entry-03438

### C15 | entry-03438 | 待确认

原文：“any … damage … triggers a darkness explosion”；译文：“每当你造成……伤害时……产生一次暗影爆炸”。

快照另有“该次伤害没有杀死目标”的条件：目标死亡时直接返回，不触发爆炸。

证据：`D/data/timed_effects.lua:1050–1058`，首个条件包含 `dead`；只有通过该检查才执行暗影范围伤害。

这个条件在英文与译文中均未说明，属于共同遗漏的机制疑点；尚缺目标 DLC 版本证明。



## O059 | entry-03438

### C16 | entry-03438 | 待确认

原文：“damage … **above %d**”；译文：“造成**超过 %d 点**……伤害”。

快照仅在 `val < eff.threshold` 时排除，因此恰好等于阈值、且满足其他条件的伤害也可继续触发。英文与译文均表达严格大于。

证据：`D/data/timed_effects.lua:1051–1058`；显示阈值由 `D/data/talents/misc/races.lua:127、156` 提供。

这是边界条件疑点，沿袭英文；目标 DLC 版本适用性仍待确认。



## O060 | entry-03440

### C12 | entry-03440 | 存在问题

原文“#Target#’s **weapon** looks less threatening”，译文“#Target#的危险度看起来降低了”，把变化对象从**武器**换成了角色。`tome-ashes-urhrok/data/timed_effects.lua:43–56` 将此句用作 `DEMON_BLADE` 消失日志，前一句获得日志也明确指向武器。状态：**已证实，限所给 DLC 快照**。



## O061 | entry-03440

### C12 | entry-03440 | 存在问题
- **原文短引**：`#Target#'s weapon looks less threatening.`
- **译文短引**：`#Target#的危险度看起来降低了。`
- **问题具体内容**：实体主语严重遗漏与语义错置。原文主语为 `#Target#'s weapon`（目标的武器），译文漏译了 `weapon`，将受词错置为 `#Target#` 本身。
- **状态**：存在问题
- **源码依据与消费逻辑**：
  `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:51-52`（`DEMON_BLADE` 状态）：
  ```lua
  on_gain = function(self, err) return _t"#Target# imbues its weapon with demonic fire.", _t"+Demon Blade" end,
  on_lose = function(self, err) return _t"#Target#'s weapon looks less threatening.", _t"-Demon Blade" end,
  ```
  该状态为恶魔之刃状态，获得时为“给武器附魔”，结束时自然是“武器看起来不再那么危险”。译文丢弃“武器”，变成描述目标本身的危险度降低，导致游戏状态提示日志主客体严重失真。

---



## O062 | entry-03440

### C17 | entry-03440 | 存在问题

原文：“#Target#'s **weapon** looks less threatening”；译文：“#Target#的**危险度**看起来降低了”。

武器这一所属对象被遗漏，武器威胁减弱变成角色整体危险度降低。

证据：`D/data/timed_effects.lua:44–56`，该句是 `DEMON_BLADE` 的失去效果日志；对应获得效果日志明确描述给武器附加恶魔之火。属于文本与语境直接可证的对象变化。



## O063 | entry-03440

### C22 | entry-03440 | 存在问题
- **原文与译文：** 原文「#Target#'s weapon looks less threatening.」，译文为「#Target#的危险度看起来降低了」。
- **问题：** 所属关系错了：原文说的是目标的武器，译文变成了目标本身。
- **源码依据：** `timed_effects.lua` 中 DEMON_BLADE 的 on_lose（约第 52 行），对应武器附魔结束。



## O064 | entry-03441

### C13 | entry-03441 | 存在问题

译文“#Target#不再闪耀”没有说明熄灭的是**武器的火光**。英文消失日志本身有缺词（“#Target#’s is no longer blazing”），但同一效果的获得日志写明“weapon surges with fire”；`tome-ashes-urhrok/data/timed_effects.lua:148–163` 也显示这是武器攻击相关效果。此项包含**上游缺词**与译文未恢复可由同一语境确认的对象。状态：**已证实，限所给 DLC 快照**。

**读取范围与来源：**读取了指定目录的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `source-access.json.sections` 列出的 13 个 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/` 下的 Lua 单文件：`talents/corruptions/` 中的 `demonic-pact.lua`、`demonic-strength.lua`、`doom-covenant.lua`、`doom-shield.lua`、`fearfire.lua`、`heart-of-fire.lua`、`infernal-combat.lua`、`npcs.lua`、`oppression.lua`、`torture.lua`、`wrath.lua`，以及 `talents/misc/races.lua`、`timed_effects.lua`。13 个文件的 SHA-256 均与 `source-access.json` 相符。未读取额外源码，故无额外调用链路径；未读取引擎仓库、其他报告或实验输出，未创建临时文件，未发现越界。DLC 快照的仓库和 commit 未固定；上述机制结论只证明该哈希快照内的行为，**目标版本适用性待确认**。这份结果是只读审核观察，不是生产 `DONE_VERIFIED`。


## O065 | entry-03441

### C18 | entry-03441 | 存在问题

原文：“no longer **blazing**”；译文：“不再**闪耀**”。

语境中的 blazing 指火焰燃烧，译文只表达光亮消失，丢失燃烧信息。英文存在多余的 `'s`，但这不改变火焰语境。

证据：`D/data/timed_effects.lua:156–178`，同一字符串分别用于 `RAGING_FLAMES` 和 `CURSED_FLAMES` 的结束日志；相邻获得效果日志分别说明武器涌出火焰和目标被吞噬性火焰包围。不能统一解释为普通闪光效果。



## O066 | entry-03441

### C23 | entry-03441 | 仅建议
- **内容：** 「blazing」被译为「闪耀」，失去了「燃烧」的意味。这条文本由 Revel 与 Devoured 共用（`timed_effects.lua:157/178`）。
- **为何只是建议：** 它与邻近的「武器闪耀着火花」成对出现，并伴随「-Revel」「-Devoured」提示，机制信息没有丢失。



## O067 | entry-03445

### C24 | entry-03445 | 仅建议
- **内容：** 「获得%d%% 酸性抗性与 %d%%酸性伤害亲和」前后空格不对称。
- **为何只是建议：** 纯排版问题。



## O068 | entry-03447

### C19 | entry-03447 | 待确认

原文：“Will not die **until %d life**”；译文：“生命值**不低于 %d** 时不会死亡”。

译文明确把等于阈值包括在安全范围中，而固定本体的受伤结算在 `life <= die_at` 时进入死亡处理。

证据：`D/data/timed_effects.lua:805、822、830–831` 将显示的负生命值与 `die_at` 加值联系起来；`E/game/modules/tome/class/interface/ActorLife.lua:49–56` 使用 `<=` 判定。

固定本体的比较符已核验。由于显示参数及效果设置来自未固定版本的 DLC 快照，对目标运行组合的结论仍待确认；不能把“不低于”当作已经得到机制支持。

实际读取范围与版本：

设包路径 `P` 为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g07-20260923`

读取了以下冻结输入：

- `P/INPUT.md`
- `P/entries.json`
- `P/context.lua`
- `P/source-access.json`

读取并核对了以下 13 个包内源码文件，SHA-256 全部与 `source-access.json` 一致。共同前缀为 `P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/`：

```text
data/talents/corruptions/demonic-pact.lua
data/talents/corruptions/demonic-strength.lua
data/talents/corruptions/doom-covenant.lua
data/talents/corruptions/doom-shield.lua
data/talents/corruptions/fearfire.lua
data/talents/corruptions/heart-of-fire.lua
data/talents/corruptions/infernal-combat.lua
data/talents/corruptions/npcs.lua
data/talents/corruptions/oppression.lua
data/talents/corruptions/torture.lua
data/talents/corruptions/wrath.lua
data/talents/misc/races.lua
data/timed_effects.lua
```

额外读取了白名单中的以下 DLC 文件，哈希均匹配。共同前缀为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok/`

| 额外路径 | 已读调用或符号来源 |
|---|---|
| `tome-ashes-urhrok/superload/mod/class/Actor.lua` | `demonic-strength.lua` 设置的 `demonblood_def` 等属性，核查 Actor 消费扩展；该文件内未找到对应消费点 |
| `tome-ashes-urhrok/superload/mod/class/interface/Combat.lua` | `doom-shield.lua` 的 `Hardened Core.armor` 与 `spellpower`，核查属性计算调用 |
| `tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua` | 已读 `DEMON_SEED_BLACKICE` 与 `EFF_BLACKICE`，核查充能生成及消耗 |
| `tome-ashes-urhrok/hooks/load.lua` | 已读 `demonblood_def`、`DEMONFIRE`、`fiery_torment`，核查加载钩子是否补充消费逻辑；未找到这些符号 |

本体仅通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取以下单文件：

| 固定提交内路径 | 调用链来源 |
|---|---|
| `game/modules/tome/class/Actor.lua` | Actor 扩展的 `loadPrevious`、伤害回调及效果设置 |
| `game/modules/tome/class/interface/ActorLife.lua` | Actor 明确 require 的生命结算接口 |
| `game/engines/default/engine/interface/ActorLife.lua` | 上述接口 require 的基类 |
| `game/engines/default/engine/interface/ActorTemporaryEffects.lua` | Actor require、`setEffect` 与 `timedEffects` |
| `game/modules/tome/class/interface/Combat.lua` | Combat 扩展及 `callbackOnMeleeHit`、`on_melee_hit` |
| `game/modules/tome/data/damage_types.lua` | 已读 `DEMONFIRE`、`demonblood_dam`、`demonblood_def` |
| `game/modules/tome/data/timed_effects/magical.lua` | `EFF_CURSE_IMPOTENCE`，并查找 `EFF_SENSE` |
| `game/modules/tome/data/timed_effects/mental.lua` | 查找已读调用中的 `EFF_SENSE`，未找到定义 |
| `game/modules/tome/data/timed_effects/other.lua` | 查找已读调用中的 `EFF_SENSE`，未找到定义 |
| `game/modules/tome/data/timed_effects/physical.lua` | 找到并核验 `EFF_SENSE` 定义 |

曾尝试读取该固定提交中的 `engine/interface/ActorLife.lua`，路径不存在，未取得内容；随后按实际引擎目录读取上述基类文件。

共覆盖 **40 条：存在问题 10 条、待确认 4 条、仅建议 0 条、未发现问题 26 条**。部分“存在问题”条目另含已单列的待确认 claim。40 条原译文与 `entries.json` 一致；消费占位符顺序、命名标记及空的 `args_order`／`special` 未发现异常，百分号的等价表达和合法换行未计作缺陷。

未发现读取越界；未读取其他报告、当前译文文件、其他语言答案或生产结论，未创建子 agent，未修改仓库，未创建临时文件。未核验的目标 DLC 版本适用性已保留在待确认项中。本输出仅为独立审核观察，不作生产完成声明。


## O069 | entry-03448

### C25 | entry-03448 | 仅建议
- **内容：** 「charges」被译为「叠加次数」，与邻近的「%d charges.」→「%d层充能」译法不一致。
- **为何只是建议：** 源码显示的就是 eff.stacks（`timed_effects.lua:861`），语义没有错。


