### batch-028 译文复核报告

#### 基础核验信息
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-028.md`
- **文件 SHA-256 校验**：`16e0c1ccde7c7b713108708349b546d672da47d8814c23e388760945513a2aba`（经核对完全一致）
- **复核范围**：`entry-01084` 至 `entry-01124`，共 40 条（注：本批中无 `entry-01115`，总计 40 条）
- **核验源码依据**：ToME 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/general/objects/world-artifacts.lua`）及同 section 译文终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua`）。

---

### 逐条复核详情

#### entry-01084
- **位置**：`mod-tome.lua:12878`
- **结论**：未发现问题
- **可核验依据**：源码对应 `world-artifacts.lua:3850`（沃瑞钽臂铠 Spellhunt Remnants 5阶描述）。术语 voratun 译为“沃瑞钽”，spellhunt 译为“魔法狩猎”，arcane artifacts 译为“奥术类装备”，均符合术语表；无占位符，文本语义与句式完整通顺。

#### entry-01085
- **位置**：`mod-tome.lua:12879`
- **结论**：存在疑点
- **可核验依据**：
  1. 形状术语疑点：原文 `radius %d cone` 中的 `cone` 被译为“弧形区域”，而游戏常规标准术语为“锥形”/“锥形区域”（同文件 entry-01097 即译为“锥形范围”，技能通用亦为锥形）；
  2. 原文与机制差异：原文表述为 `attempt to destroy all magic effects and sustains`，译文加入了括号注释 `（至多两项；`。经查固定源码 `world-artifacts.lua:3923`，底层实现确实为循环两次 `for i = 1, 2 do ... target:dispel(...)`，即机制上限确为 2 项，译者系依据机制补充说明，但与英文表面字面“all”存在差异并改变了原句结构；
  3. 占位符 `%d` 与 `%0.2f` 格式与顺序均保留正确。

#### entry-01086
- **位置**：`mod-tome.lua:12880`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:3918` 调用 `game.logSeen(who, "%s unleashes antimagic forces from %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。译文保留 3 个 `%s`（释放者、his/her、装备名），语序 `%s从%s%s中放出反魔法力量！` 完全对应，标点感叹号一致。

#### entry-01087
- **位置**：`mod-tome.lua:12881`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:3946` 调用 `game.logSeen(target, "%s's animating magic is disrupted by the burst of power!", ...)`。占位符 `%s` 对应目标名称；“animating magic”译为“活化魔法”（作用于不死族与傀儡 construct），表达准确贴切。

#### entry-01088
- **位置**：`mod-tome.lua:12884`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:3968` 中背包物品选择标题 `Destroy which item?`，译文“摧毁哪一件物品？”准确，问号完整。

#### entry-01089
- **位置**：`mod-tome.lua:12885`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:3971` 调用 `game.logPlayer(who, "You crush the %s, and the gloves take on an illustrious shine!", o:getName{do_color=true})`。占位符 `%s` 保留；动作与日志意思明确（“take on an illustrious shine”简译为“开始发光”，传达清晰）。

#### entry-01090
- **位置**：`mod-tome.lua:12889`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4004` 盾牌名称 `Summertide`。与埃亚尔月份、卫星以及关联神器“炎华之瓶”（Summertide Phial）保持严格一致，统一译为“炎华”。

#### entry-01091
- **位置**：`mod-tome.lua:12893`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4063` 中 `tformat(self.use_power.range, 0.8*dam, dam)`。占位符 `%d`、`%0.2f`、`%0.2f` 顺序与数量完全对应；属性 Willpower（意志）、Cunning（灵巧）、light damage（光系伤害）均符合标准术语。

#### entry-01092
- **位置**：`mod-tome.lua:12894`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4074` 调用 `game.logSeen(who, "%s's %s flashes!", who:getName():capitalize(), self:getName(...))`。两个 `%s` 占位符完整保留（后带空格为排版微瑕，不影响运行）。

#### entry-01093
- **位置**：`mod-tome.lua:12899`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4116` Silk Current 未鉴定名称 `flowing robe`，译为“飘逸的法袍”，准确无误。

#### entry-01094
- **位置**：`mod-tome.lua:12902`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4148` Skeletal Claw 未鉴定名称 `bone-link chain`，译为“骨节锁链”，对应正确。

#### entry-01095
- **位置**：`mod-tome.lua:12926`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4402` Umbraphage（噬暗之灯）描述。文本对应完整，文笔契合原作意境。

#### entry-01096
- **位置**：`mod-tome.lua:12927`
- **结论**：细微观察
- **可核验依据**：源码 `world-artifacts.lua:4404` 为 `special_desc` 格式化字符串。
  1. 占位符 `%d`、`%d` 顺序正确；
  2. 格式与标点：译文使用了半角括号 `(强度 %d...` 与 `(当前增幅：%d)`，且前后无空格，存在中英文全半角混用现象；
  3. 机制术语：“current charge %d”中的 `charge` 在代码中为该神器的实际累积充能值（`self.charge`，上限 300，且在 entry-01097 中直接作为伤害计算因子 `math.floor(self.charge/4)`），译文译作“当前增幅”略带歧义，容易让玩家误以为是亮度增幅或百分比，直译为“当前充能：%d”或“当前蓄能：%d”更符合机制本意。

#### entry-01097
- **位置**：`mod-tome.lua:12929`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4447` 为 `tformat(radius, blindchance, dam)`。占位符 `%d`、`%d%%`、`%0.2f` 全部保留且转义无误；Mindpower 译为“精神强度”，darkness damage 译为“暗影伤害”，均符合术语表。

#### entry-01098
- **位置**：`mod-tome.lua:12930`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4481` 调用 `game.logSeen(who, "%s unshutters %s %s, unleashing a torrent of shadows!", who:getName():capitalize(), who:his_her(), self:getName(...))`。保留 3 个 `%s`，语序匹配，动作“unshutters”（打开遮光罩）译为“打开了”准确明了。

#### entry-01099
- **位置**：`mod-tome.lua:12932`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4501` Spectral Cage 未鉴定名称 `ethereal blue lantern`，译为“飘渺的蓝色灯笼”，准确对应。

#### entry-01100
- **位置**：`mod-tome.lua:12935`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4536` 调用 `game.logPlayer(self, "Not enough space to summon!")`。译文“没有足够的空间召唤！”准确，感叹号完整保留。

#### entry-01101
- **位置**：`mod-tome.lua:12938`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4580` 调用 `who:logCombat(..., "#Source# releases an icy whisp from %s %s!", who:his_her(), self:getName(...))`。`#Source#` 实体标签保留，2 个 `%s` 占位符完整对应，“寒冷鬼火”贴合召唤实体（will o' the wisp）。

#### entry-01102
- **位置**：`mod-tome.lua:12949`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4710` 调用 `who:logCombat(m, "#Source# uses %s to summon a natural guardian!", self:getName(...))`。`#Source#` 实体标签与单占位符 `%s` 均保留，语义完全对应。

#### entry-01103
- **位置**：`mod-tome.lua:12950`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4734` 披风装备名称 `Cloth of Dreams`，译为“梦幻披风”，符合标准物品命名惯例。

#### entry-01104
- **位置**：`mod-tome.lua:12956`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4764` 中 `tformat(radius, range, dam_temporal, dam_darkness)`。占位符 `%d`、`%d`、`%0.2f`、`%0.2f` 共 4 个完全对应且顺序正确；temporal（时空）、darkness（暗影）符合伤害类型术语。

#### entry-01105
- **位置**：`mod-tome.lua:12957`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4776` 调用 `game.logSeen(who, "%s siphons space and time into %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。3 个 `%s` 占位符保留，语序与语义准确。

#### entry-01106
- **位置**：`mod-tome.lua:12968`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:4866` Pouch of the Subconscious（潜意识之袋）描述。译文“你发现自己在不断抵抗摆弄这袋奇异弹丸的冲动。”准确流畅。

#### entry-01107
- **位置**：`mod-tome.lua:12994`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5126` Prothotipe's Prismatic Eye 宝石 `special_desc`。源码机制为佩戴（wielder）或镶嵌（imbue）时法术触发激光（GOLEM_BEAM），译文“当装备或镶嵌时，施放法术时附加激光。”机制完全吻合。

#### entry-01108
- **位置**：`mod-tome.lua:13004`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5229` 调用 `game.logSeen(who, "%s merges with %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。3 个 `%s` 占位符对应角色、代词和装备名称，语义表达清晰。

#### entry-01109
- **位置**：`mod-tome.lua:13006`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5239` Ring of Growth（生命之戒）描述。译文“这枚小巧的木戒上缠绕着一根绿色的茎，纤薄的叶片似乎仍在从中生长。”准确生动。

#### entry-01110
- **位置**：`mod-tome.lua:13010`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5260` Wrap of Stone（石化风衣）描述。译文“这件厚重的斗篷坚韧异常，却依然能轻松地弯折垂流。”通顺准确。

#### entry-01111
- **位置**：`mod-tome.lua:13022`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5378` Eternity's Counter（永恒沙漏）描述。文本翻译完整对应。

#### entry-01112
- **位置**：`mod-tome.lua:13028`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5434` 调用 `game.logPlayer(who, "#GOLD#The sands slowly begin falling towards %s.", ...)`。颜色代码 `#GOLD#` 与占位符 `%s` 均严格保留，句尾标点正确。

#### entry-01113
- **位置**：`mod-tome.lua:13045`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5588` Eyal's Will（埃亚尔之意志）描述。译文通顺流畅，符合意境。

#### entry-01114
- **位置**：`mod-tome.lua:13079`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:5895` The Untouchable（不可触及）三行背景故事描述。术语 Spellblaze 对应“魔法大爆炸”，rogue 对应“盗贼”，3 行换行结构严格对应。

#### entry-01116
- **位置**：`mod-tome.lua:13089`
- **结论**：存在疑点
- **可核验依据**：源码 `world-artifacts.lua:5962` The Calm（宁静长袍）描述：
  `...Its original owner, a powerful mage named Proccala, was often revered for both his great benevolence and his intense power when it proved necessary.`
  译文：“这件绿色长袍上刻有云朵和旋风的图案。它最初的主人，大法师普偌卡拉，因其善行和力量被人们敬畏。”
  **疑点证据**：译文漏译了关键条件从句 `when it proved necessary`（“在必要之时”/“在必要时展现出的”）。该法袍名称为 The Calm（宁静/暴风雨前的平静），背景叙事强调其平时行善仁慈，但当必要之时才显现雷霆手段与强大力量。漏译此从句使背景叙事设定出现信息残缺。

#### entry-01117
- **位置**：`mod-tome.lua:13105`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6090` Guise of the Hated（被憎恨者的伪装）4行诗歌描述。4行换行格式严格一致，文学翻译典雅契合。

#### entry-01118
- **位置**：`mod-tome.lua:13120`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6168` Frost Lord's Chain（冰霜领主之链）描述。语义表达完整贴切。

#### entry-01119
- **位置**：`mod-tome.lua:13124`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6201` Twilight's Edge（晨昏之刃）描述。材质名称 voratun 对应“沃瑞钽”，stralite 对应“斯莱特”，均严格匹配术语表规范；叙事光暗交织表达完整。

#### entry-01120
- **位置**：`mod-tome.lua:13125`
- **结论**：存在疑点
- **可核验依据**：源码 `world-artifacts.lua:6206` 为暴击特效描述 `desc=_t"release a burst of light and dark damage (scales with Magic)"`。
  底层代码实际造成伤害为：
  `who:project(tg, target.x, target.y, engine.DamageType.LIGHT, ...)`
  `who:project(tg, target.x, target.y, engine.DamageType.DARKNESS, ...)`
  **疑点证据**：
  1. 伤害类型术语偏离：在 ToME4 伤害类型术语中，DamageType.LIGHT 标准译名为“光系伤害”，DamageType.DARKNESS 标准译名为“暗影伤害”（同批 entry-01091 即为“光系伤害”，entry-01097/01104 均为“暗影伤害”）。译文译为“光明和黑暗伤害”，使用了非标准伤害类型词汇；
  2. 属性术语偏离：角色核心属性 Magic 的标准术语为“魔力”（Magic -> 魔力），此处译为了“魔法”。建议规范为：“释放光系和暗影伤害爆发（受魔力加成）”。

#### entry-01121
- **位置**：`mod-tome.lua:13136`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6308` 击中特效描述 `25% chance to strike the target again.`。译文“25%几率再次攻击。”精炼准确，数字与百分号完好。

#### entry-01122
- **位置**：`mod-tome.lua:13143`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6360` 击杀特效描述 `Enter a Rampage (Shared cooldown).`。技能 Rampage 对应“暴走”，括号与句号标点完全一致。

#### entry-01123
- **位置**：`mod-tome.lua:13150`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6437` Boots of the Hunter（猎人之靴）描述。文本对应完整，语意自然。

#### entry-01124
- **位置**：`mod-tome.lua:13151`
- **结论**：未发现问题
- **可核验依据**：源码 `world-artifacts.lua:6477` Boots of the Hunter 主动技能名。查阅底层代码（触发 EFF_HUNTER_SPEED，`nobreakStepUp = true`），玩家执行非移动行为时加速效果打断，译文“增加移动速度300%，最多持续五回合。（任何非移动行动会打断这个效果）”完全准确体现机制（括号前句号为排版微瑕，不影响理解与机制）。

---

### 复核结果统计与汇总

1. **总条目数**：40 条（逐条覆盖 entry-01084 至 entry-01124 全部编号，无遗漏）。
2. **未发现问题**：36 条。
3. **存在疑点**：3 条
   - `entry-01085`：cone 译为“弧形区域”不符合通用“锥形”术语；译文补充“至多两项；”系参考代码循环机制的额外说明，与英文字面有别。
   - `entry-01116`：漏译关键条件从句 `when it proved necessary`（“在必要时/必要之时”）。
   - `entry-01120`：伤害类型未使用标准术语“光系和暗影伤害”（译作“光明和黑暗伤害”）；属性 Magic 未使用标准属性名“魔力”（译作“魔法”）。
4. **细微观察**：1 条
   - `entry-01096`：半角括号中英文混排；`charge`（累积充能数）译为“增幅”对机制表述略有歧义。