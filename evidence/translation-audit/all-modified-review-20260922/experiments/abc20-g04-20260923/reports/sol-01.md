| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03292 | 未发现问题 | 权重乘数含义相符 |
| entry-03293 | 未发现问题 | 0 与 1 的说明相符 |
| entry-03294 | 存在问题 | C01：手动重启的时机 |
| entry-03295 | 未发现问题 | 名称相符 |
| entry-03296 | 未发现问题 | 选择法术与随机选项相符 |
| entry-03297 | 未发现问题 | 随机法术说明相符 |
| entry-03298 | 未发现问题 | 已学会法术的范围相符 |
| entry-03299 | 存在问题 | C02–C05：地点、时长、施政与事件 |
| entry-03300 | 仅建议 | C06：站位措辞 |
| entry-03301 | 未发现问题 | 叙事信息相符 |
| entry-03302 | 未发现问题 | 灭绝传闻的并置保留 |
| entry-03303 | 未发现问题 | 炼金术士说明相符 |
| entry-03305 | 存在问题 | C07：死灵术缩为职业 |
| entry-03306 | 未发现问题 | 灾难及后续影响相符 |
| entry-03307 | 未发现问题 | 诅咒与仇恨关系相符 |
| entry-03308 | 未发现问题 | 地点与传闻相符 |
| entry-03309 | 存在问题 | C08：传闻修饰对象改变 |
| entry-03310 | 未发现问题 | 职业说明相符 |
| entry-03311 | 未发现问题 | 巨魔变化相符 |
| entry-03312 | 未发现问题 | 双关叙述保留 |
| entry-03313 | 未发现问题 | 宝石用途相符 |
| entry-03314 | 未发现问题 | 格斗家说明相符 |
| entry-03315 | 未发现问题 | 雷电叙述相符 |
| entry-03316 | 未发现问题 | 斗篷用途相符 |
| entry-03317 | 存在问题 | C09：两类鞋具被概括 |
| entry-03318 | 未发现问题 | 弹药栏说明相符 |
| entry-03319 | 未发现问题 | 主手与切换说明相符 |
| entry-03320 | 未发现问题 | 副手条件与切换说明相符 |
| entry-03321 | 未发现问题 | 念动力栏说明相符 |
| entry-03322 | 未发现问题 | 即时使用含义相符 |
| entry-03323 | 存在问题 | C10–C11：灾变名称与占有关系 |
| entry-03324 | 存在问题 | C12–C21：多处叙事信息偏移 |
| entry-03325 | 存在问题 | C22–C28：条件、身份与范围偏移 |
| entry-03326 | 存在问题 | C29：图书管理员身份遗漏 |
| entry-03327 | 待确认 | C30：`%s` 是否为目录 |
| entry-03328 | 待确认 | C31：`%s` 是否为目录 |
| entry-03329 | 未发现问题 | `tags` 表要求相符 |
| entry-03330 | 未发现问题 | 上传错误说明相符 |
| entry-03331 | 未发现问题 | 更新与预览上传相符 |
| entry-03332 | 未发现问题 | 更新上传相符 |

### C01 | entry-03294 | 存在问题

原文要求黄色名称的光环“**After turning them on here**”再手动关闭、启用；译文说“在这里调整之后”，把操作条件扩成任何调整。`ShimmerRemoveSustains.lua:94–106,150–157` 显示黄色对应 `no_sustain_autoreset`，在界面重新开启时不会执行自动重置。状态：已证实。

### C02 | entry-03299 | 存在问题

原文在欢迎来到 *Maj’Eyal* 后称“**This is the Age of Ascendancy**”；译文称“现在的**埃亚尔大陆**是卓越纪”。`init.lua:131` 明确区分 Eyal 世界与 Maj’Eyal 大陆，“埃亚尔大陆”混淆两者。状态：已证实。

### C03 | entry-03299 | 存在问题

“**over ten thousand years**”译为“长达一万年”，丢失“超过”的数量界限。依据：`init.lua:30`。状态：已证实。

### C04 | entry-03299 | 存在问题

“**ruled … with fairness**”译为“王国天下太平”：和平不等于公正施政，后者的信息未保留。依据：`init.lua:33–34`。状态：已证实。

### C05 | entry-03299 | 存在问题

法师帮助结束的是“**the terrors of the Spellblaze**”，译文却说他们“终止了……魔法大爆炸”，将灾难造成的恐怖后果改成事件本身。依据：`init.lua:42`。状态：已证实。

### C06 | entry-03300 | 仅建议

“tactically reposition”译作“重新占位”仍能传达调整位置，但搭配略生硬；这是表达偏好，没有可证的信息错误。依据：`init.lua:87`。

### C07 | entry-03305 | 存在问题

“**drive people to necromancy**”指驱使人研习或施行死灵术；“使一个人成为死灵法师”缩窄为取得某种职业身份。依据：`init.lua:96`。状态：已证实。

### C08 | entry-03309 | 存在问题

原文肯定仍可找到某些夏·图尔神器，传闻所修饰的是“**they are not to be trifled with**”；译文“虽然有人说还能……找到”把可找到一事也改为传闻。依据：`init.lua:102`。状态：已证实。

### C09 | entry-03317 | 存在问题

原文明确列出“**Sandals or boots**”，译文仅称“鞋子”，抹去了脚部栏说明中的两类物品。依据：`load.lua:131` 的 `FEET` 栏定义。状态：已证实。

### C10 | entry-03323 | 存在问题

“**the Cataclysm**”译为“大爆炸”，与同批文本中 *Spellblaze* 的“魔法大爆炸”混淆。`misc.lua:376` 指灾变使肖尔塔土地沉海；`init.lua:131–132` 也分别提到 Spellblaze 与 Cataclysm。状态：已证实。

### C11 | entry-03323 | 存在问题

少数马卓普人据传仍“**possess citadels and towers**”，译文改为“仍住在……城堡或高塔里”。拥有与居住不是同一关系。依据：`misc.lua:378`。状态：已证实。

### C12 | entry-03324 | 存在问题

“**No text would be complete without at least a brief note**”是说文章应简述这些种族；“没有任何文字可以诠释”变成文字无法描述，开篇论点反转。依据：`misc.lua:497`。状态：已证实。

### C13 | entry-03324 | 存在问题

“**do not hold any civilised society of note**”谈的是没有值得一提的文明社会；“没有任何文化遗留”改成没有文化遗存。依据：`misc.lua:497`。状态：已证实。

### C14 | entry-03324 | 存在问题

岩石巨魔有“**a thick, solid hide**”，其外观像煤或花岗岩；译文只说“厚厚的……外观”，漏掉厚实外皮这一身体特征。依据：`misc.lua:499`。状态：已证实。

### C15 | entry-03324 | 存在问题

森林巨魔有更成熟的“**form of speech**”，译文对应位置说“更为敏捷的速度”，把语言能力误作速度；原文随后才另说它们移动更快。依据：`misc.lua:499`。状态：已证实。

### C16 | entry-03324 | 存在问题

兽人训练巨魔发生在“**towards the end of the Age of Pyre**”；译文仅称“在烈火纪时”，丢失接近纪元末期的时点。依据：`misc.lua:499`。状态：已证实。

### C17 | entry-03324 | 存在问题

娜迦记载始于“**the last few hundred years**”，译文称“近一百年”，时间跨度由数百年缩为约一百年。依据：`misc.lua:503`。状态：已证实。

### C18 | entry-03324 | 存在问题

原文说这些记载“**only more recently have … been interpreted**”为真实记录；译文说“越来越多的证据表明”，把解释方式的变化改成证据数量增长。依据：`misc.lua:503`。状态：已证实。

### C19 | entry-03324 | 存在问题

恶魔“**can be summoned by certain magical rites**”说的是可被某些仪式召唤；“他们是由某种魔法仪式召唤而来”将召唤能力写成其来源。依据：`misc.lua:505`。状态：已证实。

### C20 | entry-03324 | 存在问题

金属化血肉会与“**our atmosphere**”异常反应，部分恶魔会释放酸或黑暗云雾；译文改成“超乎我们想象的形态”“藏在酸雾里”，遗漏大气反应，并将主动释放改为置身其中。依据：`misc.lua:505`。状态：已证实。

### C21 | entry-03324 | 存在问题

“**magic has fallen out of use**”指魔法较少被使用；“魔法淡出人们的视野”说的是较少被看见，改变恶魔减少所关联的条件。依据：`misc.lua:505`。状态：已证实。

### C22 | entry-03325 | 存在问题

“**unless hefty bribes are paid**”要求数额可观的贿赂；“除非你给他们点好处”既弱化数额，也不再明确是贿赂。依据：`misc.lua:403`。状态：已证实。

### C23 | entry-03325 | 存在问题

“**for no known reason**”是外人不知道原因；“无缘无故”断言没有原因。依据：`misc.lua:403`。状态：已证实。

### C24 | entry-03325 | 存在问题

作者获准与数位“**guild leaders**”交谈；“主要领导人”遗漏其公会领袖身份。依据：`misc.lua:403`。状态：已证实。

### C25 | entry-03325 | 存在问题

“**resistant to any physical suffering**”描述能承受身体痛苦；“超强的物理抵抗能力”将其表述成抵抗物理伤害的能力。依据：`misc.lua:405`。状态：已证实。

### C26 | entry-03325 | 存在问题

原文明确说可凭胡须上的珠饰识别**女性矮人**；“他们的性别……可以通过……珠饰来辨认”未说明珠饰识别的是女性。依据：`misc.lua:405`。状态：已证实。

### C27 | entry-03325 | 存在问题

“**allow no outsiders in**”是通常不准外人入城；“从不欢迎外来者”只表示态度，不再表达准入限制。前文作者获特准入城是原文写出的例外。依据：`misc.lua:403,409`。状态：已证实。

### C28 | entry-03325 | 存在问题

原文说有“大量年轻矮人”外出，没有增长趋势；译文“**越来越多**的年轻矮人”增加了趋势判断。依据：`misc.lua:411`。状态：已证实。

### C29 | entry-03326 | 存在问题

奎科加任命的是自己的“**librarians**”，译文只称“记录者”，丢失图书管理员身份；紧接着的“这个图书馆”因此也少了对应依据。依据：冻结 `INPUT.md` 的 entry-03326 原文、译文。此项是文本语义判断，不据此断言游戏机制。状态：已证实。

### C30 | entry-03327 | 待确认

“**Logs written to %s**”未指明 `%s` 是目录还是文件路径；“日志目录：%s”断言它是目录。`source-access.json` 将 addon-dev 列为源码不可用；缺少调用处传入 `%s` 的路径构造证据，不能确认错误。状态：待确认。

### C31 | entry-03328 | 待确认

同 C30，这条“**Logs written to %s**”也译成“日志目录：%s”。缺少本条调用处的参数来源，不能确定 `%s` 的路径类型。状态：待确认。

**读取范围与核验边界：**读取了指定实验目录中的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/` 下获准的 `dialogs/orders/Talents.lua`、`dialogs/shimmer/ShimmerRemoveSustains.lua`、`dialogs/talents/MagicalCombatArcaneCombat.lua`、`init.lua`、`load.lua`；五份源码的 SHA-256 均与清单相符，本体版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。沿 `load.lua:111` → `data/lore/lore.lua` 的明确加载关系，在该固定提交只读检查了 `data/lore/lore.lua`、其中列出的 `data/lore/misc.lua`，以及为定位奎科加文本检查的 `data/lore/angolwen.lua`、`data/lore/shertul.lua`；后两文件未定位到该段，C29 只据冻结文本判断。addon-dev 源码不可用，C30–C31 保留待确认。未创建临时文件，未读取其他报告或模型输出，未修改仓库；无已知越界。本结果是独立审核观察，不代表生产 `DONE_VERIFIED`。
