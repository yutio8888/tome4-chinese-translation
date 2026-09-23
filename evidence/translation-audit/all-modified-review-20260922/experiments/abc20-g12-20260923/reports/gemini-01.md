### 译文复核判定表（entry-03613 至 entry-03652）

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03613 | 未发现问题 | 护甲与护盾数值/回合占位符完全匹配，机制描述准确 |
| entry-03614 | 未发现问题 | 虚无巨石译名与同文件实体一致，四处数值占位符与机制一致 |
| entry-03615 | 未发现问题 | 源码实际增加虚空之星(T_VOID_STARS)，译文符合核验源码机制 |
| entry-03616 | 存在问题 | C01 |
| entry-03617 | 未发现问题 | 参数重排[2, 1]与源码入参严格对应，数值与机制正确 |
| entry-03618 | 未发现问题 | 地名与技能名专名准确，标点规范 |
| entry-03619 | 未发现问题 | 惯用施法失败日志，省略号标点规范 |
| entry-03620 | 存在问题 | C02, C03 |
| entry-03621 | 未发现问题 | 日志占位符保留完整，抵抗碎玻璃效果语义准确 |
| entry-03622 | 存在问题 | C04 |
| entry-03623 | 未发现问题 | 黑血伤害、抗性加成与可见生物上限核验证实，数值准确 |
| entry-03624 | 仅建议 | C05 |
| entry-03625 | 未发现问题 | 召唤受阻日志，感叹号标点与原文一致 |
| entry-03626 | 未发现问题 | 等价重排句子顺序，额外生命与持续回合参数消费正确 |
| entry-03627 | 未发现问题 | 荒野之怒震慑几率、首击必中与豁免判定描述与源码一致 |
| entry-03628 | 未发现问题 | 样式标记与高亮完整，括号符合中文排版习惯 |
| entry-03629 | 未发现问题 | 参数重排[1, 3, 2, 4, 5, 6]与源码入参对应无误，教团专名准确 |
| entry-03630 | 存在问题 | C06 |
| entry-03631 | 未发现问题 | 战斗日志占位符完整，动作语义准确 |
| entry-03632 | 未发现问题 | 斩杀线、秒杀几率与体质恢复加成数值占位符准确 |
| entry-03633 | 存在问题 | C07 |
| entry-03634 | 未发现问题 | 传送撤离机制与堡垒描述准确 |
| entry-03635 | 未发现问题 | 获得状态日志占位符与标点准确 |
| entry-03636 | 未发现问题 | 失去状态日志占位符与标点准确 |
| entry-03637 | 未发现问题 | 黏稠触须束缚日志占位符与标点准确 |
| entry-03638 | 未发现问题 | 摆脱触须日志占位符与标点准确 |
| entry-03639 | 未发现问题 | 触手缠绕状态日志准确，符合 preferred 术语规范 |
| entry-03640 | 存在问题 | C08 |
| entry-03641 | 未发现问题 | 状态获得日志占位符与恐惧因果语义准确 |
| entry-03642 | 未发现问题 | 混沌法球层数与全伤害增益数值格式化无误 |
| entry-03643 | 未发现问题 | 获得受害者痛苦增益日志占位符与语义准确 |
| entry-03644 | 未发现问题 | 变身恐魔颜色标记、占位符与术语准确 |
| entry-03645 | 仅建议 | C09 |
| entry-03646 | 存在问题 | C10 |
| entry-03647 | 未发现问题 | 毁灭预言血量阈值与暗影伤害数值占位符完整准确 |
| entry-03648 | 未发现问题 | 痛苦连接创伤日志高亮标记与占位符无误 |
| entry-03649 | 未发现问题 | 虚空歼灭者现身日志高亮与占位符无误 |
| entry-03650 | 未发现问题 | 好运状态三项增益数值占位符与原文忠实对应 |
| entry-03651 | 未发现问题 | 译文修正上游歧义并准确反映源码中厄运覆盖治疗机制 |
| entry-03652 | 未发现问题 | 状态描述与传送地名规范一致 |

---

### 复核观察与 Claim 详情

### C01 | entry-03616 | 存在问题
- **原文短引**：`, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#`
- **译文短引**：`，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#`
- **问题具体内容**：作用对象与事实错误。技能 `Mutated Hand`（`T_MUTATED_HAND`）本身为被动技能（mode="passive"），其提供的物理强度加成与触手武器伤害增益并不受副手装备限制；只有在副手非空时，触手副手武器攻击无法触发（`canTentacleCombat` 为 false，`getTentacleCombat` 返回 nil）。原文主句为 `Your tentacle hand currently has those stats%s:`，谓语动词 `is currently disabled` 的逻辑主语是“你的副手触手”（tentacle hand），而非技能本身。译文将其译为“该技能暂时被禁用”，错误地扩大了禁用对象，误导玩家以为整个被动技能失效。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/demented/writhing-body.lua:62`（未固定快照）。该段文本在 `info` 函数中作为 `%s` 拼接至 `Your tentacle hand currently has those stats%s:\n%s`，判断条件为 `allow_tcombat and "" or _t", #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#"`。

### C02 | entry-03620 | 存在问题
- **原文短引**：`#ORCHID#Speed:#LAST# Increases global speed by %d%%.`
- **译文短引**：`#ORCHID#速度：#LAST# 增加 %d%% 整体速度。`
- **问题具体内容**：明确适用的 preferred 术语违规。快照术语表中明确规定：`global speed` 的 preferred 译名为“全局速度”，且在备注中特别强调“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文使用了明确被禁止的“整体速度”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:263`（未固定快照）。技能 `Twisted Evolution` 的 `info` 函数格式化输出，直接面向玩家展示全局速度增益数值。

### C03 | entry-03620 | 存在问题
- **原文短引**：`#ORCHID#Power:#LAST# Increases all damage by %d%%.`
- **译文短引**：`#ORCHID#力量：#LAST# 增加 %d%% 伤害。`
- **问题具体内容**：语义与机制混淆，且存在信息遗漏。该技能的三项进化分支分别为 Speed（全局速度）、Form（全属性加成 `all stats by %d`）与 Power（全部伤害提升 `all damage by %d%%`）。在紧接上一行“全属性”的语境下，将“Power”直译为“力量”，极易让玩家将其误解为主属性“力量”（Strength）；同时，“all damage”漏译了“全部/所有”，弱化了其对全系伤害加成的机制覆盖表述。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:247-264`（未固定快照）。分支 3 施加效果 `EFF_TWISTED_POWER`，对应逻辑为提升全伤害比例，与主属性 Strength 无关。

### C04 | entry-03622 | 存在问题
- **原文短引**：`#Source# expertly hurls a pebble at #target#!`
- **译文短引**：`#Source#朝#target#投掷鹅卵石！`
- **问题具体内容**：语义修饰信息遗漏。原文包含副词 `expertly`（熟练地/娴熟地/巧妙地），用以刻画该技能虽然只是投掷鹅卵石但动作极其熟练的动作特征。译文将 `expertly` 完全略去未译。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:325`（未固定快照）。技能 `Throw Pebble` 动作执行时的战斗日志输出 `self:logCombat(target, "#Source# expertly hurls a pebble at #target#!")`。

### C05 | entry-03624 | 仅建议
- **原文短引**：`Your faceless visage is puzzling and emotionless, allowing you to more easily resist mind tricks.`
- **译文短引**：`你无面孔的脸没有情感，令人困惑。这让你更容易抵抗精神冲击。`
- **问题具体内容**：措辞修饰与个人偏好。首句“你无面孔的脸”略显直译和同义反复（faceless visage 表达无面之容）；后半句“mind tricks”指心智诡计/惑控伎俩（对应后文的精神豁免与混乱免疫），译为“精神冲击”略有偏离，但鉴于整句纯属背景叙述（flavour text），不影响后文属性与百分比豁免机制的理解与参数消费，故仅属表达层面的润色建议，不计作事实缺陷。
- **状态**：仅建议
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:100`（未固定快照）。技能 `Faceless` 的背景说明。

### C06 | entry-03630 | 存在问题
- **原文短引**：`You were created by ziguranth for one purpose only, to wage war on magic!`
- **译文短引**：`你被伊格制造的唯一理由：对魔法作战！`
- **问题具体内容**：专名术语混淆。术语快照关于 `Zigur` 与 `Ziguranth` 有极其明确的严格区分：“教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换”。Krog 是由反魔教团（Ziguranth）通过龙血融合改造制造的战士，动作的施动者是教团而非据点地名。译文将其译为“被伊格制造”，将教团专名误套为据点地名，违反了术语快照的强制区分规则。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:369`（未固定快照）。Krog 种族大招 `Drakeblood Strike` 的技能说明首句背景描述。

### C07 | entry-03633 | 存在问题
- **原文短引**：`Increases global speed by %d%%.`
- **译文短引**：`整体速度增加 %d%%。`
- **问题具体内容**：明确适用的 preferred 术语违规。快照术语表中明确规定：`global speed` 的 preferred 译名为“全局速度”，且备注严格限定“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文使用了被明确禁止的“整体速度”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:422`（未固定快照）。寄生项圈被动技能 `Ultra Instinct`（`T_ULTRA_INSTINCT`）为角色提供 `global_speed_add`，其 `info` 显示全局速度加成。

### C08 | entry-03640 | 存在问题
- **原文短引**：`Terrified of the horror duo attacking them reducing defense and spell save by %d.`
- **译文短引**：`因两只恐魔的现身而惊恐，闪避和法术豁免降低 %d。`
- **问题具体内容**：语义与事实错误。原文明确指出恐慌的原因是遭受两只恐魔的围攻（`attacking them`），译文将其错误地翻译为“因两只恐魔的现身而惊恐”。将持续攻击动作（attacking）篡改为出现/现身（appearing），扭曲了状态的因果描述与动作事实。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:276`（未固定快照）。效果 `WTW_TERRIBLE_SIGHT` 的 `long_desc`，由步行蠕虫同伴机制在近身触发。

### C09 | entry-03645 | 仅建议
- **原文短引**：`Target briefly saw what True Horror means, deeply scaring it. %d%% chances to fail using a talent.`
- **译文短引**：`目标被真正的恐惧吓倒，%d%% 几率使用技能失败。`
- **问题具体内容**：叙述细节压缩与偏好建议。原文 `Target briefly saw what True Horror means, deeply scaring it.` 中，“briefly saw”（短暂瞥见）、“what True Horror means”（真正的恐怖意味着什么）及“deeply scaring it”（深受惊吓）具有较强的克苏鲁风格叙事色彩；译文过度精简为“目标被真正的恐惧吓倒”。由于该句为纯背景叙述，其后关键机制 `%d%% chances to fail using a talent.` 对应正确，未造成机制理解偏差，故判定为偏好建议。
- **状态**：仅建议
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:557`（未固定快照）。状态 `GLIMPSE_OF_TRUE_HORROR` 的 `long_desc`。

### C10 | entry-03646 | 存在问题
- **原文短引**：`...and causing them to take an additional %d%% temporal damage from Dark Whispers and Hideous Visions.`
- **译文短引**：`...并使他们从黑暗低语和失智冲击中受到额外 %d%% 时空伤害。`
- **问题具体内容**：状态/机制专名误译与内部不一致。原文提及的状态 `Hideous Visions` 在同文件上方第 761 行（对应本组 context.lua 第 398 行）已有唯一定名且翻译为“惊骇幻象”。译文在此处将其误译为一个完全无关的名称“失智冲击”，导致前后译名冲突，玩家在游戏界面中寻找对应联动状态时无法辨识。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:779`（未固定快照）。状态 `CACOPHONY` 的 `long_desc`，联动强化 `Dark Whispers`（黑暗低语）与 `Hideous Visions`（惊骇幻象）的时空伤害。

---

### 读取路径、版本核验与合规声明

1. **实际读取的文件路径与哈希/版本**：
   - 冻结输入：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/INPUT.md`
   - 条目与语境数据：
     - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/entries.json`
     - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/context.lua`
     - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/source-access.json`
   - DLC 公开源码快照单文件（来源未固定，哈希经验证匹配 source-access.json）：
     - `sources/dlc/cults/tome-cults/data/talents/demented/void.lua`（SHA256: `19cb982e3487d52626f46c5e0623f5f75b4ad2e126c7580e000672c74ce934b1`）
     - `sources/dlc/cults/tome-cults/data/talents/demented/writhing-body.lua`（SHA256: `37c7c1f3ebe52ca6e8b339ac909de51c0aeaa5b3b79d61ada37ce4499a1d833c`）
     - `sources/dlc/cults/tome-cults/data/talents/misc/misc.lua`（SHA256: `3b37fe925ecba44b1931c740c085a00425eeeeaae2ff47c0b646cf7fe4d1976b`）
     - `sources/dlc/cults/tome-cults/data/talents/misc/races.lua`（SHA256: `59b9b67cb0a3752d9e66dc28f587dcaa40a6ffd16bfdc85bdd17ab803c80b05f`）
     - `sources/dlc/cults/tome-cults/data/timed_effects.lua`（SHA256: `0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c`）
2. **额外源码路径调用链**：无。本组条目均在上述 5 个指定的 section 单文件内闭环核验，未读取任何额外源码文件。
3. **临时文件目录**：根据用户授权创建临时目录 `/tmp/abc20-g12-20260923-kdxfc2vo`，核验完毕后已清理移除。
4. **越界与无法核验情况**：未读取任何未授权文件，未读取其他实验报告，未创建子 agent，未修改仓库任何文件。Cults DLC 组件源码仓库与 commit 未固定，已显式标注快照内已证事实，目标版本机制适用性保留待主流程裁决。
5. **合规性说明**：本输出为独立 REVIEWER 观察报告，非事实真值，不宣称生产 DONE_VERIFIED。
