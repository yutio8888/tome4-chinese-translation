# rem-11 译文审查报告

**审查角色**：只读 REVIEWER（purpose: `translation_contextual_v1`）  
**审查模式**：自然语言审核旁路（依据原 campaign 授权，不要求正式 JSON）  
**审查输入**：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-11.md`（共 20 条，全部归属于 DLC `orcs`）

---

## 逐条审核汇总表（20条）

| 序号 | entry-ID | 判定 | 关联 Claim | 简要依据 |
| :--- | :--- | :--- | :--- | :--- |
| 01 | entry-03872 | 未发现问题 | - | 托拉克国王长文书信；主客体、语气、人名地名及排版标记完全一致，叙事与机制无偏差 |
| 02 | entry-03875 | 存在问题 | C01 | 维斯石板剧情；`lift them up` 误译为“连根拔起”，将正向共存选择反转为毁灭动作 |
| 03 | entry-03878 | 未发现问题 | - | 任务目标与人物头衔准确，`High Sun Paladin Aeryn` 符合 preferred 术语规范 |
| 04 | entry-03879 | 未发现问题 | - | 炸弹引爆提示意译准确流畅，时序与逃生指引无误 |
| 05 | entry-03881 | 未发现问题 | - | `The Tribe` 准确对应前置任务的 Atmos 气之部族，跨任务指代一致 |
| 06 | entry-03882 | 未发现问题 | - | 道具名 `Stralite` 准确对齐 terms.json preferred 术语“斯莱特” |
| 07 | entry-03883 | 仅建议 | C02 | 道具描述省略 `trained`（受训过的），建议补全以契合任务驯化设定与野雪人区分 |
| 08 | entry-03887 | 未发现问题 | - | 螺旋暗影能量技能描述数值、伤害类型与负能量回复机制均准确无误 |
| 09 | entry-03888 | 未发现问题 | - | 技能名称 `Twilit Echoes` 译为“暮光回响”准确自然 |
| 10 | entry-03890 | 仅建议 | C03 | `Sustained energy` 译为“持续能量”易混淆为回能，建议优化为“维持技能占用的能量” |
| 11 | entry-03892 | 存在问题 | C04 | `Create a distortion` 严重误译为“创造一个地块”（实为击退投射物的空间力场） |
| 12 | entry-03896 | 未发现问题 | - | 抛射物增速与减速效果机制、数值及法强联动描述准确 |
| 13 | entry-03897 | 未发现问题 | - | 技能名称同源副本，译为“暮光回响”一致无误 |
| 14 | entry-03898 | 未发现问题 | - | 光暗回响 DoT 与减速机制、持续时间重置与分摊计算描述精准 |
| 15 | entry-03900 | 未发现问题 | - | NPC 状态技能名“沉睡中…”简洁准确，省略号规范 |
| 16 | entry-03901 | 未发现问题 | - | 触手召唤空间不足日志提示准确无误 |
| 17 | entry-03902 | 未发现问题 | - | 战斗日志占位符 `%s` 顺序与色彩标记 `#ORCHID#` 完整保留 |
| 18 | entry-03903 | 未发现问题 | - | 喊话文本与日志一致，格式与占位符完全匹配 |
| 19 | entry-03904 | 未发现问题 | - | 诅咒之地半径、持续时间及负面效果翻倍机制准确无误 |
| 20 | entry-03905 | 未发现问题 | - | 锯刃风暴伤害、流血及持续回合描述清晰，参数重构合理 |

---

## 疑点详细判定

### C01 | entry-03875 | confirmed
- **短引**：`让现实不得不要么将他们连根拔起，要不被他们一道拖进深渊。`
- **具体差异**：原文为 `will sink their hooks so deep into reality that it must either lift them up or be dragged into the depths with them`。主语“it”指代现实（reality），“them”指代维斯一族（Weissi）。原文意为：维斯将钩子深深扎入现实，迫使现实要么将其一同托起（容纳其存在上升），要么被其拖入深渊共毁。译文将 `lift them up` 误译为“将他们连根拔起”，把原本作为生存诉求的正向对立项反转为毁灭动作，严重扭曲了维斯一族誓死在现实中确立自身存在的叙事主旨。
- **最强合理等价解释与处置**：最强辩解认为译者受“扎入钩子”意象影响，将 lift 误读为现实把钩子“连根拔除”；但语法上 lift 的宾语是 them，且与后半句“拖进深渊”构成经典的“托起存续 vs 坠入深渊”二选一对照。判定为 **confirmed**。处置建议更正为：“……将钩子深深扎入现实，迫使现实要么将他们一同托举而起，要么与他们一道坠入深渊。”此外句首“在你过来时前刚刚”建议顺带修正为“在你到来前刚刚”。
- **来源证据**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua:83`

---

### C02 | entry-03883 | advisory
- **短引**：`召唤雪人来协助你。`
- **具体差异**：原文道具说明为 `Call a trained yeti to your side.`。译文省略了修饰词 `trained`（受训过的/训练有素的），并将 `to your side` 略译为“来协助你”。
- **最强合理等价解释与处置**：最强辩解认为该任务核心即为捕获野雪人送回克鲁克部落训练，玩家使用传送信标时当然知晓召唤的是训练好的盟友，且其使用效果就是召唤随从助战，略译并未影响机制理解，不属于硬性语义错误。判定为 **advisory**。处置建议后续润色微调为：“召唤一只受训雪人到你身边。”
- **来源证据**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua:47`

---

### C03 | entry-03890 | advisory
- **短引**：`持续能量仍然算向最大值。`
- **具体差异**：原文为 `Sustained energy still counts toward the maximum.`。译文将 `Sustained energy` 直译为“持续能量”，并将 `counts toward the maximum` 译为生硬的“算向最大值”。
- **最强合理等价解释与处置**：最强辩解认为译者以“持续”对应 sustain，在天体系语境下玩家可推测其指被技能维持所锁定的能量池；但 TOME4 统称此类为“维持技能”（sustains），“持续能量”极易被误解为每回合持续恢复的能量（regen），“算向最大值”亦属不通顺的翻译腔。判定为 **advisory**。处置建议优化为：“维持技能占用的能量仍计入加成上限。”
- **来源证据**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/energies.lua:38`

---

### C04 | entry-03892 | confirmed
- **短引**：`在目标所在地创造一个地块，击退所有的飞行物如果可能的话还会改变他们的方向。`
- **具体差异**：原文为 `Create a distortion at the target tile, knocking back all projectiles and changing their direction to face away if possible.`。译文将核心机制动作 `Create a distortion at the target tile` 严重错译为“在目标所在地创造一个地块”，把名词 `distortion`（空间扭曲/力场扭曲）错译为“地块”，把地点状语 `at the target tile` 误译为“在目标所在地”；且后半句漏译了 `face away`（背向/向外偏转），缺乏连接标点。
- **最强合理等价解释与处置**：最强辩解可能认为译者误将 tile 与 distortion 混淆，或类比同系造墙技能（Mirror Wall）；但源码表明本技能 `Diffraction Pulse` 纯属弹道偏转力场，仅产生光效与坐标推移，绝对不会创造任何地形、地块或实体障碍物。译为“创造一个地块”会严重误导玩家以为具有阻挡地形功能。判定为 **confirmed**。处置建议更正为：“在目标地块制造一处空间扭曲，击退所有投射物，并尽可能使其背向偏转。”
- **来源证据**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/reflection.lua:140`

---

## 实际读取路径与来源限制说明

### 实际读取路径
1. **规则与配置**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
2. **待审条目入口**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-11.md`
3. **同 section 译文上下文快照**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
4. **许可公开源码（全部核验 SHA256 哈希一致）**：
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/sunwall.lua` (`e80b0cf8...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/weissi.lua` (`b486ccb6...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/destroy-sunwall.lua` (`b40919ef...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/kill-dominion.lua` (`be5363c2...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/palace.lua` (`5b2a7be9...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/quarry.lua` (`00549119...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/ritch-hive.lua` (`5aa19207...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua` (`1deae3b1...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/cosmic.lua` (`58e81b71...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/crepescula.lua` (`1cd8e04c...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/energies.lua` (`2439377d...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/reflection.lua` (`972f949d...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/sol.lua` (`8e073404...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/celestial/void.lua` (`b6c361de...`)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/misc/npcs.lua` (`0e62db4f...`)

### 来源限制与核验规范
1. **DLC 来源未固定声明**：上述 `orcs` DLC 源码仅通过 `source-access.json` 中给出的快照 SHA256 哈希进行内容固定；仓库 commit 及目标版本（如 1.7.4）在清单中属于 unpinned，本报告不宣称已核验固定 commit 或目标发行版本，所有机制判断严格基于当前冻结快照源码事实。
2. **归因与判定边界**：代码差异归因与文本差异严格分开；未修改任何文件，未创建任何子代理，未读取历史审核报告，遵守只读 REVIEWER 约束。
