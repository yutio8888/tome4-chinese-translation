# batch-057 译文复核报告

本批次文件哈希核对：
- 文件路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-057.md`
- 冻结 SHA-256：`b574a338da8fe0ab9433ef63afdeed2c493280b184ac3e7b8bdcd183b08c4edf`
- 核验结果：**匹配一致**
- 条目范围：`entry-01666` 至 `entry-01705`，共 40 条
- 源码核验基准：公开源码 `engine/boot/tome` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取）

---

### entry-01666
- **位置**：`mod-tome.lua:22969`（`mod-tome/data/talents/corruptions/scourge.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `100%%` 与 `%d%%` 数量及类型完全一致。核对源码 `scourge.lua` 中 `Corrupting Strike` 技能（line 210-222），目标被附加 `EFF_CORRUPTING_STRIKE` 降低 100% 疾病免疫 2 回合，移除最多 2 个自然持续效果（`removeSustainsFilter` 自然属性），并进行双武器攻击造成伤害。译文对机制、数值与持续时间还原准确。

---

### entry-01667
- **位置**：`mod-tome.lua:22982`（`mod-tome/data/talents/corruptions/shadowflame.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%0.2f`（火焰伤害）、`%0.2f`（暗影伤害）、`%d`（半径）顺序与数量一致，换行及制表符对应。核对源码 `shadowflame.lua`（line 74-81），暗影与火焰伤害各占一半受法术强度加成，译文完全符合。

---

### entry-01668
- **位置**：`mod-tome.lua:22986`（`mod-tome/data/talents/corruptions/shadowflame.lua`）
- **结论**：未发现问题
- **核验依据**：3 个 `%d%%` 占位符按序对应火焰抗性、暗影抗性与全局速度加成。核对源码 `shadowflame.lua` 中 `Flame of Urh'Rok`（line 116-121），术语 `global speed` 译为“全局速度”、`Fearscape` 译为“恶魔空间”均符合术语规范，行首缩进与换行完全对应。

---

### entry-01669
- **位置**：`mod-tome.lua:22996`（`mod-tome/data/talents/corruptions/shadowflame.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `shadowflame.lua` line 199（`game.logPlayer(self, "The spell fizzles...")`），无占位符，译文“法术失败了……”标点使用中文省略号，语义与游戏常规日志一致。

---

### entry-01670
- **位置**：`mod-tome.lua:23021`（`mod-tome/data/talents/corruptions/torment.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d` 回合匹配。核对源码 `torment.lua` 中 `Blood Lock`（line 58-69），在 2 码范围（radius 2 ball）施加 `EFF_BLOOD_LOCK`，使目标生命值无法回复至施法时刻之上。译文引入技能名“鲜血禁锢”补充主语（`caught in the radius 2 ball` 译作“在 2 码范围内，任何被鲜血禁锢攻击到的敌人的治疗或回复…”），机制表达准确无歧义。

---

### entry-01671
- **位置**：`mod-tome.lua:23028`（`mod-tome/data/talents/corruptions/torment.lua`）
- **结论**：未发现问题
- **核验依据**：颜色代码 `#RED#` 与 `#LAST#` 配对完整，占位符 `%s` 匹配。核对源码 `torment.lua` line 150（`game.logSeen(self, "#RED#The powerful blow energizes %s reducing their cooldowns!#LAST#", self:getName())`），译文“强大的攻击使 %s 获得能量，技能冷却时间缩短了！”与上下文逻辑一致。

---

### entry-01672
- **位置**：`mod-tome.lua:23068`（`mod-tome/data/talents/corruptions/vile-life.lua`）
- **结论**：未发现问题
- **核验依据**：颜色标记 `#CRIMSON#`、实体宏 `#Source#` 和 `#Target#` 及效果名占位符 `(%s)` 完整保留。核对源码 `vile-life.lua` line 199（`Vile Transplant` 转移负面效果日志），格式与语义完全吻合。

---

### entry-01673
- **位置**：`mod-tome.lua:23108`（`mod-tome/data/talents/cunning/ambush.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%s` 保留，感叹号全角化。核对源码 `ambush.lua` line 95（`Shadow Leash` 缴械判定失败分支 `game.logSeen(target, "%s resists the disarm!", ...)`），术语 `disarm` 译为“缴械”，准确无误。

---

### entry-01674
- **位置**：`mod-tome.lua:23116`（`mod-tome/data/talents/cunning/ambush.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（命中）、`%d`（闪避）、`%d%%`（暗影伤害抗性穿透）顺序及格式一致。核对源码 `ambush.lua` line 121-129（`Dark Tidings` 被动效果增加 Accuracy、Defense 及 resists_pen.DARKNESS），换行与制表符对应良好。

---

### entry-01675
- **位置**：`mod-tome.lua:23139`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：颜色代码 `#YELLOW#` 与 `#LAST#` 配对完整，占位符 `%s`（工具名）与 `%s`（等级）匹配，末尾换行符一致。核对源码 `artifice.lua` line 74（`artifice_tools_get_descs` 中已准备工具描述行），准确无误。

---

### entry-01676
- **位置**：`mod-tome.lua:23142`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：颜色代码 `#GREY#` 与 `#LAST#` 配对完整，末尾换行符保留。核对源码 `artifice.lua` line 81（无短描述工具的占位说明），译文“（查看技能介绍）”准确。

---

### entry-01677
- **位置**：`mod-tome.lua:23156`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 151（技能名 `Cunning Tools`），为机巧系第 2 个槽位技能，译为“机巧工具”，与前后文统一。

---

### entry-01678
- **位置**：`mod-tome.lua:23168`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 185（技能名 `Intricate Tools`），为机巧系第 3 个槽位技能，译为“精密工具”，准确无误。

---

### entry-01679
- **位置**：`mod-tome.lua:23180`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 217（技能名 `Master Artificer`），机巧系大招，译为“诡计大师”（沿用既有成熟译名）。

---

### entry-01680
- **位置**：`mod-tome.lua:23182`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%s`（当前选择工具）与 `%s`（工具增强描述列表）顺序与数量匹配，颜色代码 `#YELLOW#` 与 `#LAST#` 配对完整，段落分行一致。核对源码 `artifice.lua` line 237-245，效果描述与机制一致。

---

### entry-01681
- **位置**：`mod-tome.lua:23192`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Source#` 与 `#target#` 保留完整。核对源码 `artifice.lua` line 313（袖剑近战暴击触发日志 `self:logCombat(target, "#Source# strikes #target# with hidden blades!")`），译文“#Source#使用隐藏的刀片击中了#target#！”准确。

---

### entry-01682
- **位置**：`mod-tome.lua:23193`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d%%` 匹配。核对源码 `artifice.lua` line 328（`Hidden Blades` 的 `short_info`），近战暴击触发额外徒手攻击造成 `%d%%` 伤害，冷却 4 回合，译文简明准确。

---

### entry-01683
- **位置**：`mod-tome.lua:23194`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 333（`local slot = _t"not prepared"`），用于在技能详细描述中未装配于槽位时显示，译为“未装备”符合工具槽位使用语境。

---

### entry-01684
- **位置**：`mod-tome.lua:23195`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d%%` 与 `%s` 匹配，颜色代码 `#YELLOW#` 与 `#LAST#` 完整，换行格式一致。核对源码 `artifice.lua` line 337-340（`Hidden Blades` 的 `info`），暴击触发弹出徒手攻击并标明准备槽位，机制表达准确。

---

### entry-01685
- **位置**：`mod-tome.lua:23202`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Source#` 与 `#target#` 保留。核对源码 `artifice.lua` line 378（`Assassinate` 攻击日志 `self:logCombat(target, "#Source# strikes at a vital spot on #target#!")`），译文“#Source#攻向#target#的要害！”准确。

---

### entry-01686
- **位置**：`mod-tome.lua:23209`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（生命）、`%d`（体力）、`%d`（负面效果数）顺序与数量一致。核对源码 `artifice.lua` line 470（`Rogue's Brew` 的 `short_info`），回复生命、体力并清除负面物理状态，冷却 20 回合，译文完全一致。

---

### entry-01687
- **位置**：`mod-tome.lua:23210`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`、`%d`、`%d`、`%s` 顺序与格式一致，第二行前置制表符与 `#YELLOW#`、`#LAST#` 对应。核对源码 `artifice.lua` line 480-485（`Rogue's Brew` 的 `info`），术语 `Cunning` 译为“灵巧”，准确表达了受灵巧属性加成。

---

### entry-01688
- **位置**：`mod-tome.lua:23217`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d`（持续回合）与 `%d`（视野削减）格式一致（原文中 `radius 2` 为字面值常量 2）。核对源码 `artifice.lua` line 575（`Smokebomb` 的 `short_info`），机制与数值传递准确。

---

### entry-01689
- **位置**：`mod-tome.lua:23218`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：细微观察
- **核验依据**：占位符 `%d`、`%d`、`%d`、`%s` 顺序一致，制表符与颜色代码完整。核对源码 `artifice.lua` line 582-585，原文第 2 句后半句包含状语 `even if their proximity would normally forbid it`（说明为何在近距离生物通常会阻止进入潜行），译文处理为“被烟雾影响的生物不能阻止你潜行”，虽然核心机制（烟雾内生物不阻止潜行）完全表达无误，但省略了该让步解释从句，语意略有简缩。

---

### entry-01690
- **位置**：`mod-tome.lua:23223`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 590（技能名 `Smokescreen Mastery`），译为“烟雾弹精通”，准确且与前置技能统一。

---

### entry-01691
- **位置**：`mod-tome.lua:23227`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%s` 匹配，感叹号全角化。核对源码 `artifice.lua` line 643 及 `physical.lua` line 3482，此处的镇静麻醉效果 `EFF_SEDATED` 其 subtype 设定包含 `{ sleep=true, poison=true }`，抵抗判定为目标免疫睡眠/中毒，译为“%s抵抗了睡眠！”契合底层状态类型。

---

### entry-01692
- **位置**：`mod-tome.lua:23229`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%0.2f`（物理伤害）、`%d`（唤醒伤害阈值）、`%s`（装配槽位）顺序与格式完全一致，分行与 `#YELLOW#`、`#LAST#` 对应。核对源码 `artifice.lua` line 660-664（`Dart Launcher` 的 `info`），机制（活物沉睡 4 回合、伤害降低持续时间、不破隐）翻译精准。

---

### entry-01693
- **位置**：`mod-tome.lua:23235`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d%%` 匹配。核对源码 `artifice.lua` line 674（`Dart Launcher Mastery` 的 `short_info`），飞镖无视中毒与睡眠免疫，苏醒后减速 `%d%%` 持续 4 回合，译文准确。

---

### entry-01694
- **位置**：`mod-tome.lua:23236`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d%%` 匹配。核对源码 `artifice.lua` line 677-678（`Dart Launcher Mastery` 的 `info`），译文表达与机制一致。

---

### entry-01695
- **位置**：`mod-tome.lua:23239`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 713、762（钩爪无法移动提示 `if self:attr("never_move") then game.logPlayer(self, "You cannot move!")`），无占位符，译为“你无法移动！”准确。

---

### entry-01696
- **位置**：`mod-tome.lua:23240`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Source#` 与 `#target#` 匹配。核对源码 `artifice.lua` line 726（`self:logCombat(target, "#Source# throws a grappling hook at #target#!")`），译为“#Source#朝#target#扔出钩爪！”准确。

---

### entry-01697
- **位置**：`mod-tome.lua:23241`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Source#` 与 `#target#` 匹配。核对源码 `artifice.lua` line 735（`self:logCombat(target, "#Source#'s grappling hook latches onto #target#!")`），“latches onto”译为“命中了”，符合战斗日志习惯。

---

### entry-01698
- **位置**：`mod-tome.lua:23242`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Source#` 与 `#target#` 匹配。核对源码 `artifice.lua` line 740（目标体型大于自身或无法击退时拖拽施法者 `self:logCombat(target, "#Source# is dragged towards #target#!")`），译文“#Source#被拉向#target#！”准确。

---

### entry-01699
- **位置**：`mod-tome.lua:23243`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：实体宏 `#Target#` 与 `#source#` 匹配。核对源码 `artifice.lua` line 748（目标被拖拽至施法者身边 `self:logCombat(target, "#Target# is dragged towards #source#!")`），译文“#Target#被拉向#source#！”准确。

---

### entry-01700
- **位置**：`mod-tome.lua:23246`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：细微观察
- **核验依据**：3 个 `%s` 占位符数量与顺序匹配。核对源码 `artifice.lua` line 776：`game.logSeen(self, "%s uses a grappling hook to pull %s %s!", self:getName():capitalize(), self:his_her_self(), game.level.map:compassDirection(tx - self.x, ty - self.y))`。传参依次为：角色名、反身代词（自己）、罗盘方位（例如 north / 北）。译文“%s使用钩爪来拉动%s向%s！”保留了顺序，运行时不会报错，但中文语序呈现为直译结构（如“玩家使用钩爪来拉动自己向北！”），相比“%s使用钩爪将%s拉向%s方向！”略带翻译腔。

---

### entry-01701
- **位置**：`mod-tome.lua:23247`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：核对源码 `artifice.lua` line 785（未钩住地形障碍物时的提示 `game.logPlayer(self, "You must anchor the hook to something solid.")`），译文“你需要将钩爪固定在某个坚固的物体上。”准确。

---

### entry-01702
- **位置**：`mod-tome.lua:23249`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%d` 与 `%s` 匹配，颜色代码 `#YELLOW#` 与 `#LAST#` 完整，换行与缩进对应。核对源码 `artifice.lua` line 801-804（`Grappling Hook` 的 `info`），包含判定（墙壁/不可移动/大体型则拉自己过去，否则拉敌人过来，命中生物定身 2 回合，至少距离 2 格），译文与代码机制一致。

---

### entry-01703
- **位置**：`mod-tome.lua:23255`（`mod-tome/data/talents/cunning/artifice.lua`）
- **结论**：存在疑点
- **核验依据**：占位符 `%d%%`、`%0.2f`、`%0.2f` 数量及类型完全一致。核对源码 `artifice.lua` line 816（`Grappling Hook Mastery` 的 `short_info`）：
  ```lua
  ([[Your grappling hook deals %d%% unarmed damage when it hits, plus a further %0.2f physical and %0.2f nature damage over 4 turns.]])
  :tformat(t.getDamage(self, t)*100, damDesc(self, DamageType.PHYSICAL, t.getSecondaryDamage(self,t)), damDesc(self, DamageType.NATURE, t.getSecondaryDamage(self,t)))
  ```
  底层代码（line 756-758）对目标附加 `EFF_CUT`（造成物理伤害）和 `EFF_POISONED`（造成自然伤害），且完整版 `info`（line 820）中表述为 `bleed for %0.2f physical damage and be poisoned for %0.2f nature damage`。
  当前条目译文为：“被钩爪击中的生物受到 %d%% 徒手伤害，在 4 回合内受到 %0.2f 流血伤害和 %0.2f 自然毒素伤害。”
  此处将原文中明确的伤害类型 `physical`（物理伤害）和 `nature`（自然伤害）意译为了“流血伤害”和“自然毒素伤害”。虽然在叙事上解释了效果来源，但在 ToME4 伤害机制中，“物理伤害”与“自然伤害”对应特定的抗性体系，不存在独立的“流血伤害/自然毒素伤害”类型，容易对玩家产生机制误导。

---

### entry-01704
- **位置**：`mod-tome.lua:23280`（`mod-tome/data/talents/cunning/called-shots.lua`）
- **结论**：未发现问题
- **核验依据**：4 个占位符 `%d%%`（基础远程伤害）、`%d%%`（零距离惩罚）、`%d`（最大射程）、`%d%%`（最大射程加成）顺序与类型完全吻合，分行与制表符一致。核对源码 `called-shots.lua` line 179-183（`Skirmisher: Sniping Shot` 的 `info`），子弹穿透中间敌人并随距离递增伤害，译文忠实还原。

---

### entry-01705
- **位置**：`mod-tome.lua:23288`（`mod-tome/data/talents/cunning/called-shots.lua`）
- **结论**：未发现问题
- **核验依据**：占位符 `%s` 匹配，感叹号全角化。核对源码 `called-shots.lua` line 210（`Noggin Knocker` 命中时若目标未能触发震慑加深：`game.logSeen(target, "%s resists the stunning shot!", target:getName():capitalize())`），术语 `stun` 译为“震慑”，符合术语表。

---

### 复核小结
- 覆盖条目：`entry-01666` 至 `entry-01705` 全部 40 条。
- **未发现问题**：37 条。
- **细微观察**：2 条（`entry-01689` 省略让步解释从句；`entry-01700` 三参数直译结构略带翻译腔，但参数顺序正确无报错）。
- **存在疑点**：1 条（`entry-01703` 将 `physical` 与 `nature` 伤害类型意译为“流血伤害”与“自然毒素伤害”，脱离了游戏底层标准的物理/自然抗性机制定义）。