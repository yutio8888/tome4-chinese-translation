### batch-062 译文复核报告

#### 基础核验信息
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-062.md`
- **文件 SHA-256**：`22aea48884ff79d1ab3004c40a2d359b7ae93c79c1427308b9d08e1fa1a9d0a3`（核验一致）
- **覆盖范围**：`entry-01866` 至 `entry-01905`，共 40 条
- **公开源码参照**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均位于 engine/mod-tome 路径下，不涉及 DLC 未固定源码或缺失源码的 addon）
- **译文语境基准**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

#### 逐条复核详情

- **entry-01866**（`mod-tome.lua:24937` / `mod-tome/data/talents/gifts/fire-drake.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `fire-drake.lua:115-120` 中 `tformat(damDesc(self, DamageType.FIRE, dam), radius, duration)` 传入 3 个参数。译文占位符 `%0.2f`（伤害）、`%d`（半径）、`%d`（持续回合）按序对应；`10%%` 与 `1%%` 转义百分号匹配；“吸收 10%% 伤害治疗自身”准确反映 `DamageType.FIRE_DRAIN`（`healfactor=0.1`）机制；术语“精神强度”、“火焰抗性”规范。

- **entry-01867**（`mod-tome.lua:24945` / `mod-tome/data/talents/gifts/fire-drake.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `fire-drake.lua:130` 中 `message = _t"@Source@ breathes fire!"`。占位标识符 `@Source@` 保持完整，译文“@Source@喷出火焰！”自然准确，感叹号标点与原文一致。

- **entry-01868**（`mod-tome.lua:24956` / `mod-tome/data/talents/gifts/fungus.lua`）
  - **判定**：细微观察
  - **可核验依据**：源码 `fungus.lua:36-39` 参数为 `tformat(t.getLife(self, t), t.getRegen(self, t))`，两个 `%d` 依次对应最大生命与生命回复，数值加成与意志（Willpower）对应无误。细微观察为原文 `reinforcing fungi`（强固/起强化作用的真菌）被意译为“有治疗作用的孢子”，既将真菌改为孢子，又将 reinforcing 偏向理解为治疗，但鉴于技能实际提供生命与回复加成，未造成实质机制误导。

- **entry-01869**（`mod-tome.lua:24962` / `mod-tome/data/talents/gifts/fungus.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `fungus.lua:53-56` 对应公式 `dur + math.ceil(dur * t.getDurationBonus(self, t)) + 1`，译文“增加 %d%% +1，向上取整”精准传达了 `+ 1 rounded up` 的计算逻辑；占位符 `%d%%` 匹配；“回复类的增益效果”与“精神强度”术语规范。

- **entry-01870**（`mod-tome.lua:24969` / `mod-tome/data/talents/gifts/fungus.lua`）
  - **判定**：存在疑点
  - **可核验依据**：
    1. **机制限制漏译**：源码 `fungus.lua:67-73` 计算获得能量时为 `local heal = (self.life + value) < self.max_life and value or self.max_life - self.life`，仅计入未溢出的实际治疗量。原文明确写有 `This effect can't add energy past 2 stored turns and overhealing is not counted.`，译文仅翻译了“这一效果最多获得 2 个回合”，完全漏译了关键限制句 `and overhealing is not counted`（过量/溢出治疗不计入）。
    2. **行结构变动**：原文为 4 行，译文将第 2 行断开并新增缩进行拆成了 5 行。
    3. （附带观察：首句 `Your fungus` 被译为“你的孢子”，与本系真菌主体名称存在差异）。

- **entry-01871**（`mod-tome.lua:24977` / `mod-tome/data/talents/gifts/fungus.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `fungus.lua:92` 技能名 `Sudden Growth` 译为“骤然生长”，命名契合自然/真菌类技能风格，无格式错误。

- **entry-01872**（`mod-tome.lua:24987` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:22` 自然协调（harmony）系描述 `Nature heals and cleans you.`，译为“利用大自然的力量治疗你受到的创伤、清洁你的身体。”，语意通顺契合。

- **entry-01873**（`mod-tome.lua:24989` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:23` 反魔法（antimagic）系描述 `The way to combat magic, or even nullify it.`，译文“对抗乃至使魔法失效的手段。”准确精炼。

- **entry-01874**（`mod-tome.lua:24990` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:24` 技能类别名 `summoning (melee)`，译为“召唤（近战）”，括号及类别术语规范。

- **entry-01875**（`mod-tome.lua:24991` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:24` 近战召唤系描述，译文“召唤近战生物来协助你战斗的艺术。”忠实原文。

- **entry-01876**（`mod-tome.lua:24992` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:25` 技能类别名 `summoning (distance)`，译为“召唤（远程）”，分类术语规范。

- **entry-01877**（`mod-tome.lua:24993` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:25` 远程召唤系描述 `adept in elemental destruction`，译文“召唤远程元素攻击类生物来协助你战斗的艺术。”符合该系召唤物均为火龙、小狗等元素/远程生物的实际语境。

- **entry-01878**（`mod-tome.lua:24994` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:26` 技能类别名 `summoning (utility)`，译为“召唤（通用）”，术语规范统一。

- **entry-01879**（`mod-tome.lua:24996` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:27` 技能类别名 `summoning (augmentation)`，译为“召唤（增益）”，类别术语规范。

- **entry-01880**（`mod-tome.lua:24997` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:27` 增益召唤系描述 `manipulating the lifespan and location of your summons`，译文“操纵召唤物寿命和位置的战斗艺术。”精准传达机制。

- **entry-01881**（`mod-tome.lua:24999` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:28` 高级召唤系（summoning (advanced)）描述，译文“增强召唤物的战斗艺术。”准确精炼。

- **entry-01882**（`mod-tome.lua:25001` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:29` 史莱姆（slime）系描述，slime mold juice（黏菌汁液）与 affinity（亲和力）翻译准确。

- **entry-01883**（`mod-tome.lua:25003` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:30` 真菌（fungus）系描述，译文“利用真菌环绕周身，增强你的治疗能力。”忠实流畅。

- **entry-01884**（`mod-tome.lua:25005` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:31` 土龙形态（sand drake aspect）描述，译文“化身成为土龙形态使你能使用土龙技能。”符合该系列技能树形态描述的一贯表达。

- **entry-01885**（`mod-tome.lua:25007` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:32` 火龙形态（fire drake aspect）描述，译文“化身成为火龙形态使你能使用火龙技能。”与同组风格保持一致。

- **entry-01886**（`mod-tome.lua:25009` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:33` 冰龙形态（cold drake aspect）描述，译文“化身成为冰龙形态使你能使用冰龙技能。”与同组风格一致。

- **entry-01887**（`mod-tome.lua:25011` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:34` 雷龙形态（storm drake aspect）描述，译文“化身成为雷龙形态使你能使用雷龙技能。”与同组风格一致。

- **entry-01888**（`mod-tome.lua:25013` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:35` 毒龙形态（venom drake aspect）描述，译文“化身成为毒龙形态使你能使用毒龙技能。”与同组风格一致。

- **entry-01889**（`mod-tome.lua:25015` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:36` 高等龙族（higher draconic abilities）描述，译文“继承远古真龙的力量使你能使用强大的龙族技能。”翻译得体，契合设定。

- **entry-01890**（`mod-tome.lua:25017` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:37` 灵晶掌握（mindstar mastery）描述，mindstars（灵晶）与 psionic blades（心灵利刃）术语完全规范。

- **entry-01891**（`mod-tome.lua:25019` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：细微观察
  - **可核验依据**：源码 `gifts.lua:38` 粘液（mucus）系描述 `Cover the floor with natural mucus.`。译文“用粘液覆盖地面。”省略了修饰词 natural（自然），但作为技能系概述含义清晰，无误解。

- **entry-01892**（`mod-tome.lua:25023` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:40` 苔藓（moss）系描述，译文“你学会控制苔藓生长，帮助战斗。”简明概括了原文。

- **entry-01893**（`mod-tome.lua:25027` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:42` 软泥利刃（oozing blades）描述，译文“你向心灵利刃里灌注软泥能量。”术语精准。

- **entry-01894**（`mod-tome.lua:25029` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:43` 腐蚀利刃（corrosive blades）描述，译文“你向心灵利刃里灌注酸性能量。”术语精准。

- **entry-01895**（`mod-tome.lua:25031` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：细微观察
  - **可核验依据**：源码 `gifts.lua:44` 埃亚尔之怒（eyal's fury）描述 `Unleash nature's fury against foes around you.`。译文“向敌人释放自然的愤怒。”略去了“around you”（你周围的）这一方位限定，但技能系描述语意仍属自洽。

- **entry-01896**（`mod-tome.lua:25035` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:46` 岩石藤蔓（earthen vines）描述，译文“掌握岩石并赋予其生命，形成恐怖的藤蔓。”文笔流畅，意境贴切。

- **entry-01897**（`mod-tome.lua:25037` / `mod-tome/data/talents/gifts/gifts.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `gifts.lua:47` 矮人之自然力量（dwarven nature）描述，译文“学会驾驭自身与生俱来的种族力量。”准确通顺。

- **entry-01898**（`mod-tome.lua:25090` / `mod-tome/data/talents/gifts/higher-draconic.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `higher-draconic.lua:45` 吐息消息 `message = _t"@Source@ breathes venom!"`。占位符 `@Source@` 保留无误，译文“@Source@呼出毒液！”与冰息、流沙等系列呼出消息统一。

- **entry-01899**（`mod-tome.lua:25114` / `mod-tome/data/talents/gifts/malleable-body.lua`）
  - **判定**：细微观察
  - **可核验依据**：源码 `malleable-body.lua:35-43` 占位符 `%d`（回合）与 `%d%%`（全抗性）位置对应无误。存在两处细微观察：
    1. 技能树名称不一致：前文 `gifts.lua:42, 43` 将 oozing blades 译为“软泥利刃”、corrosive blades 译为“腐蚀利刃”，此处译为“软泥之刃系技能树”与“腐蚀之刃技能树”（“之刃” vs “利刃”）；
    2. “all resistances”与“Resistances”译为“所有抵抗”与“抵抗”，而角色面板常规官方术语习惯为“所有抗性”/“抗性”。

- **entry-01900**（`mod-tome.lua:25136` / `mod-tome/data/talents/gifts/malleable-body.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `malleable-body.lua:85-88` 参数为 `tformat(self:getTalentLevelRaw(t) * 15)`。占位符 `%d%%` 正确对应；“改按普通伤害结算”准确反映 `ignore_direct_crits` 将暴击伤害还原为直接普通伤害的底层机制。

- **entry-01901**（`mod-tome.lua:25151` / `mod-tome/data/talents/gifts/mindstar-mastery.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `mindstar-mastery.lua:67-72` 传参顺序为 `tformat(t.getStatmult, t.getAPRmult, t.getPowermult, 100 * inc)`。译文中 3 处 `%0.2f`（伤害加成、护甲穿透、精神/意志/灵巧属性倍率）及 1 处 `%d%%`（武器伤害增加）位置严格按序匹配，字面常数 `30 点物理强度` 准确；各项属性名词完全规范。

- **entry-01902**（`mod-tome.lua:25157` / `mod-tome/data/talents/gifts/mindstar-mastery.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `mindstar-mastery.lua:83` 前置条件检测 `You require a psiblade in your mainhand to use this talent.`。译文“你需要主手的心灵利刃来使用该技能。”表达清晰准确。

- **entry-01903**（`mod-tome.lua:25158` / `mod-tome/data/talents/gifts/mindstar-mastery.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `mindstar-mastery.lua:93-97` 格式化传参为 `tformat(100*t.speedPenalty, damDesc, get_mindstar_power_mult)`。源码中第 3 个占位符为 `%2.f`，译文中的 `%d%%`、`%0.2f` 与 `%2.f` 逐字按序严格对应；机制与属性加成说明准确。

- **entry-01904**（`mod-tome.lua:25164` / `mod-tome/data/talents/gifts/mindstar-mastery.lua`）
  - **判定**：未发现问题
  - **可核验依据**：源码 `mindstar-mastery.lua:119` 前置条件检测 `You require two psiblades in your hands to use this talent.`。译文“你需要双手的心灵利刃来使用该技能。”准确传达了必须双持心灵利刃的判定要求。

- **entry-01905**（`mod-tome.lua:25165` / `mod-tome/data/talents/gifts/mindstar-mastery.lua`）
  - **判定**：细微观察
  - **可核验依据**：源码 `mindstar-mastery.lua:140-145` 传参为 `tformat(dam, c, get_mindstar_power_mult)`，占位符 `%0.2f`、`%d%%`、`%0.2f` 匹配一致。存在细微观察：
    1. 机制词选择：原文 `completely avoid any damaging attack` 与 `avoidance` 在底层实现为 `cancel_damage_chance`（免除/取消受到伤害的机会），译文作“完全免疫任何伤害”与“免疫几率”，虽然在玩家理解上均指受击不掉血，但用“免疫”较原文的“回避/免受”略有泛化；
    2. 原文“bleeding for %0.2f per turn”在译文中为“每回合受到 %0.2f 点伤害”，伤害类型（流血伤害）未在数值后重复注明，但前句已提“会开始流血”，语意清楚。

---

#### 总结汇总表
- **全部 40 条已逐一核验完成**，无省略跳过。
- **存在疑点（1 条）**：
  - `entry-01870`：核心机制限制漏译（漏译 `and overhealing is not counted`，即过量/溢出治疗不计入），且译文拆行导致行数由 4 行增至 5 行。
- **细微观察（4 条）**：
  - `entry-01868`：`reinforcing fungi` 意译为“有治疗作用的孢子”。
  - `entry-01891`：`natural mucus` 略译为“粘液”（未译 natural）。
  - `entry-01895`：`foes around you` 略译为“敌人”（未体现周围范围）。
  - `entry-01899`：技能树名称（“之刃” vs 前文“利刃”）与属性术语（“抵抗” vs “抗性”）存在不一致。
  - `entry-01905`：`avoid/avoidance` 译为“免疫/免疫几率”较“规避/免除”略泛化。
- **其余 35 条**：均「未发现问题」，占位符、参数顺序、控制符及机制译名均严格准确。