40 条已全部复核完毕：**14 条存在问题、5 条待确认、2 条仅建议、19 条未发现问题**。以下是审核观察，不是真值，也不代表 DONE_VERIFIED。entry-03304 不在冻结集内，entries.json 实际 40 条，与冻结顺序一致。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03292 | 未发现问题 | 与 GetQuantity 标题语义一致 |
| entry-03293 | 未发现问题 | 权重默认值为 1（Talents.lua:108），0 表示关闭 |
| entry-03294 | 存在问题 | C01；C02 为建议 |
| entry-03295 | 未发现问题 | 对话框标题 |
| entry-03296 | 仅建议 | C03 |
| entry-03297 | 未发现问题 | 与 Talents 树末尾「随机法术」节点的 desc 一致 |
| entry-03298 | 未发现问题 | 与 allow_for_arcane_combat 加 knowTalent 的筛选一致 |
| entry-03299 | 存在问题 | C04、C05、C06、C07；C08 待确认；C09 为建议 |
| entry-03300 | 未发现问题 | 忠实于原文 |
| entry-03301 | 未发现问题 | — |
| entry-03302 | 未发现问题 | — |
| entry-03303 | 未发现问题 | 「炼金术士」与术语库的 existing 条目不同，但 source_tag 不同，不强制 |
| entry-03305 | 未发现问题 | 问句改为陈述，属于合法重排 |
| entry-03306 | 存在问题 | C10 |
| entry-03307 | 未发现问题 | — |
| entry-03308 | 未发现问题 | Dreadfell 译作「恐惧王座」，与术语一致 |
| entry-03309 | 存在问题 | C11 |
| entry-03310 | 未发现问题 | — |
| entry-03311 | 未发现问题 | — |
| entry-03312 | 未发现问题 | — |
| entry-03313 | 未发现问题 | — |
| entry-03314 | 未发现问题 | — |
| entry-03315 | 未发现问题 | 叙事 tip 中用「雷电」，不适用伤害类型术语 |
| entry-03316 | 未发现问题 | — |
| entry-03317 | 仅建议 | C12 |
| entry-03318 | 未发现问题 | 箭袋（QUIVER）栏说明（load.lua:133） |
| entry-03319 | 未发现问题 | 「X 键」是常规写法，load.lua:135 |
| entry-03320 | 未发现问题 | load.lua:136 |
| entry-03321 | 未发现问题 | load.lua:137 |
| entry-03322 | 待确认 | C13 |
| entry-03323 | 存在问题 | C14、C15；C16 为建议 |
| entry-03324 | 存在问题 | C17–C25 |
| entry-03325 | 存在问题 | C26、C27、C28、C29；C30 为建议 |
| entry-03326 | 未发现问题 | 信息完整，[i] 标记保留 |
| entry-03327 | 待确认 | C31 |
| entry-03328 | 待确认 | C32 |
| entry-03329 | 未发现问题 | 代码示例原样保留 |
| entry-03330 | 未发现问题 | — |
| entry-03331 | 未发现问题 | 补「Steam」与同文件上下文一致 |
| entry-03332 | 未发现问题 | — |

---

### C01 | entry-03294 | 存在问题
- **原文**：「After turning them on here, you need to unsustain and resustain them manually.」
- **译文**：「在你在这里调整之后，需要手动先关闭再重新启用这些持续技能。」
- **问题**：条件范围被扩大。原文只在「在此处重新开启光环」这个方向上要求手动关再开；「调整」把关闭方向也包括了进去。
- **源码**：`ShimmerRemoveSustains.lua:94-110` `toggleAura`
  - 隐藏方向只调用 `removeAura`，不需要任何手动操作。
  - 只有重新开启方向（`shimmer_sustains_hide[tid]=false`）才在 `not t.no_sustain_autoreset` 时，连续两次 `forceUseTalent` 自动重置。
  - 黄色名称来自 `generateList`（:155），对应 `no_sustain_autoreset`。所以手动关再开只在「黄色光环、重新开启后」才需要。
- **结论**：玩家会误以为隐藏光环之后也要手动操作。

### C02 | entry-03294 | 仅建议
- 「It may explode!」译为「它随时可能出现问题！」，把原文的夸张玩笑弱化成了普通说法。警告的实际含义保留了，属于风格偏好。
- 格式标记 `#{bold}#`、`#CRIMSON#`、`#LAST#`、`#YELLOW#` 以及换行都完整保留。

### C03 | entry-03296 | 仅建议
- 原文用 `'Random spells'` 引号标出界面选项，译文「如果你选择随机法术」去掉了引号。选项文本「随机法术」（context.lua:55）仍能对应上，信息没有丢失。
- 「with each attack」译为「每次攻击时会随机施放」，这是沿袭上游的表述。该选项自己的说明是「Each time Arcane Combat is triggered」（MagicalCombatArcaneCombat.lua:139），上游措辞本身就不严谨，不算翻译新增的错误。

### C04 | entry-03299 | 存在问题
- **原文**：「This is the Age of Ascendancy.」
- **译文**：「现在的埃亚尔大陆是卓越纪。」
- **问题**：新增了「埃亚尔大陆」，把 Eyal 说成了大陆。同包上下文（context.lua:153）明确写着「Maj'Eyal is the biggest continent in the world of Eyal」，Eyal 是世界，不是大陆。这是翻译新增的地理事实错误。

### C05 | entry-03299 | 存在问题
- **原文**：「After over ten thousand years of strife」
- **译文**：「在长达一万年的冲突痛苦和混乱之后」
- **问题**：丢掉了「over」（超过）这个数量限定，「长达一万年」读起来像是恰好一万年。

### C06 | entry-03299 | 存在问题
- **原文**：「The last effects of the Spellblaze have been tamed.」
- **译文**：「所造成的影响已经渐渐减轻」
- **问题**：原文是「最后残余的影响已被平息」，表示已经完成。译文变成了「正在逐渐减轻」的进行态，「last」（最后残余的）也丢了。时序和完成状态都被改变。

### C07 | entry-03299 | 存在问题
- **原文**：「Together they ruled the kingdoms with fairness」
- **译文**：「在他们的统治下，王国天下太平」
- **问题**：「公正地统治」被换成了「天下太平」，统治者「公正」这一信息丢失。

### C08 | entry-03299 | 待确认
- 「under the leadership of Aranion Gayaeil」译为「在精灵王艾伦尼恩·加威尔的统治下」，新增了「精灵王」这个头衔。
- 本包允许读取的材料里没有证据证明该人物的头衔。缺少 lore 或 NPC 定义源码作证据。

### C09 | entry-03299 | 仅建议
- 「healing the wounds of thousands of years of conflict」译为「所有的文明在过去数千年中经历的不幸正在好转」，是意译：「冲突」泛化为「不幸」，并加了「所有的」。主旨没变，属于措辞偏好。
- 「冲突痛苦和混乱」之间缺少顿号，属于排版问题。
- 颜色码 `#FF0000#…#WHITE#`、`#14fffc#…#ffffff#` 完整保留。

### C10 | entry-03306 | 存在问题
- **原文**：「The Spellblaze tore Eyal apart」
- **译文**：「撕裂了埃亚尔大陆」
- **问题**：同 C04，把 Eyal（世界）说成了大陆，证据同样是 context.lua:153。
- 原文开头有一个不成对的 `"`，译文去掉了。这是上游残留，不计为缺陷。

### C11 | entry-03309 | 存在问题
- **原文**：「Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.」
- **译文**：「虽然有人说还能在某些隐秘之地找到……但据说不可轻慢它们。」
- **问题**：前半句在原文里是直接断言，译文加了「有人说」，改成了传闻。只有后半句才是原文的「it is said」，前半句的确定程度被改变。

### C12 | entry-03317 | 仅建议
- 「Sandals or boots」泛化为「鞋子」。这是 FEET 栏说明（load.lua:131），「脚部装备栏」这个作用对象没错，只是例举丢了，属于措辞偏好。

### C13 | entry-03322 | 待确认
- 「instantly used by swift hands」译为「可即时使用（不消耗回合）」，括号里新增了一条机制说明。
- 已读源码只有 `load.lua:139` 定义 SWIFT_HANDS 栏位，看不到消费该栏位的技能怎么处理行动耗时。
- 本包允许的调用链里没有可追的文件，所以「不消耗回合」是否准确待确认。

### C14 | entry-03323 | 存在问题
- **原文**：「few in number since the Cataclysm tore much of their land into the sea」
- **译文**：「自从大爆炸将他们大部分土地沉入海洋后」
- **问题**：Cataclysm（大灾变）被译成「大爆炸」，和 Spellblaze（魔法大爆炸）混淆了。同包 context.lua:153-154 把 Cataclysm 译作「大灾变」，并写明它发生在魔法大爆炸「数个世纪之后」，是两次不同的事件。

### C15 | entry-03323 | 存在问题
- **原文**：「A few are rumoured to still possess citadels and towers in remote locations.」
- **译文**：「有部分传言说他们仍住在……」
- **问题**：
  - 原文的主体是「少数马卓普人」，译文变成了「部分传言」，并说「他们」全体，数量范围被改变。
  - 「possess」（拥有）变成了「住在」。

### C16 | entry-03323 | 仅建议
- 末段「勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子……手中」主语衔接不通顺，但意思能还原。
- 「arcane experiments」只译成「实验」。
- Conclave 这里译作「秘法会」，而同包 context.lua:136 用的是「孔克雷夫」。术语快照未收录该词，不构成术语缺陷。
- 以上都只记为建议。

### C17 | entry-03324 | 存在问题
- **原文**：「No text would be complete without at least a brief note of some of the more brutish races which infest our world.」
- **译文**：「没有任何文字可以诠释那些影响我们世界的野蛮种族。」
- **问题**：句义被颠倒。原文说「任何著述都少不了简述这些种族」，译文说成了「无法诠释它们」。

### C18 | entry-03324 | 存在问题
- 同段还有三处偏差：
  - 「do not hold any civilised society of note」译为「没有任何文化遗留」，把「文明社会」换成了「文化遗留」。
  - 「nor … seem capable」中的「seem」没译，推测被说成了定论。
  - 「of interest to study for any who take delight in analysing…」译为「仍能激起大家研究……的兴趣」，把特定读者群扩大成了「大家」。

### C19 | entry-03324 | 存在问题
- **原文**：「They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster」
- **译文**：「他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速……闻名」
- **问题**：「更发达的语言能力」被错译成「速度」。语言信息丢失，速度信息重复出现。

### C20 | entry-03324 | 存在问题
- **原文**：「a thick, solid hide which bears the appearance of coal or granite」
- **译文**：「厚厚的煤黑色或花岗岩状的外观」
- **问题**：「hide」（外皮）这个主体丢了，变成了「厚厚的外观」。
- 同句前面还有两处小偏差：「生存与东北部」错把「于」写成「与」；「many mountain chains」中的「many」丢失。

### C21 | entry-03324 | 存在问题
- **原文**：「towards the end of the Age of Pyre many were trained as fighters by the orcs」
- **译文**：「然而在烈火纪时，他们被兽人当做战士般训练」
- **问题**：「烈火纪末期」这个时间点丢了；「many」（许多）变成了泛指全体。
- 另外「as they are colloquially known」被误解成「因为这更加通俗地为人所知」，多出了一个原文没有的因果关系。

### C22 | entry-03324 | 存在问题
- **原文**：「Records of them exist only from the last few hundred years」
- **译文**：「有关他们的记载只有近一百年的」
- **问题**：数量错误，「几百年」被译成了「近一百年」。

### C23 | entry-03324 | 存在问题
- **原文**：「though their tails extend several feet further」
- **译文**：「尽管他们的尾巴可能更长」
- **问题**：「再长出几英尺」的具体数量丢了，还新增了原文没有的「可能」。

### C24 | entry-03324 | 存在问题
- **原文**：「which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness」
- **译文**：「可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中」
- **问题**：
  - 「与我们的大气发生异常反应」这一因果丢失。
  - 「释放酸液、喷出黑暗云雾」这个主动行为被改成「藏在里面」，行为方向错了。

### C25 | entry-03324 | 存在问题
- **第一处**：「they can be summoned by certain magical rites」译为「他们是由某种魔法仪式召唤而来」。原文是「可以被召唤」（可能性），译文成了对来源的断言。
- **第二处**：「The main theory, which is supported by certain studies by Shaloren archmages」译为「由永恒精灵魔导师们得出的」。原文说研究「支持」这个理论，译文改成理论由他们「得出」，归属关系变了。
- 以下只记为建议，不计缺陷：
  - Naga 段「craft weapons and armour from materials found on the sea-bed」的层次被合并。
  - 「communication… impossible」加了「几乎」。
  - 巨人段「seem」没译，「Daikara Pass」只写作「岱卡拉」。
  - 「臭名卓著」应为「臭名昭著」，是错字。

### C26 | entry-03325 | 存在问题
- **原文**：「speaking with several of their guild leaders」
- **译文**：「并有幸与他们的主要领导人对话」
- **问题**：「几位公会首领」被改成「主要领导人」。这与本文第三段「谁实际担任名义领袖，外人不得而知」以及 03299「not even their leader's name」直接矛盾，属于事实错误。

### C27 | entry-03325 | 存在问题
- **原文**：「unless hefty bribes are paid」
- **译文**：「除非你给他们点好处」
- **问题**：程度被弱化。「重金贿赂」变成了「给点好处」。

### C28 | entry-03325 | 存在问题
- **原文**：「They trade heavily in their crafts from their capital the Iron Throne, but allow no outsiders in」
- **译文**：「他们在首都——钢铁王座中进行大量的交易，但是从不欢迎外来者」
- **问题**：
  - 原文是「以首都为基地向外输出货物」，译文变成「在首都里交易」，与「不许外人进入」自相矛盾。
  - 「不允许进入」被弱化成了「不欢迎」。

### C29 | entry-03325 | 存在问题
- **原文**：「Their skill with metal is renowned above all else.」
- **译文**：「他们对金属的加工技艺也是举世闻名的。」
- **问题**：「最负盛名、居于其他一切之上」这个比较级丢了，变成了并列的「也」。

### C30 | entry-03325 | 仅建议
- 「for no known reason」译为「无缘无故」，原意是「原因不明」，语气略有偏移。
- 「a great deal of young dwarves」译为「越来越多的年轻矮人」，加入了原文没有的增长趋势。
- 两处都影响不大，记为建议。

### C31 | entry-03327 | 待确认
- 「Logs written to %s」译为「日志目录：%s」，把 `%s` 断定为目录。
- addon-dev 组件在 unavailable_components 中，没有源码，无法核实 `%s` 实际是日志文件路径还是目录，因此待确认。
- 占位符数量和 tformat 标签都保留了，没有运行时格式问题。

### C32 | entry-03328 | 待确认
- 同 C31，「日志目录：%s」的参数类型因 addon-dev 源码不可用而待确认。

---

**读取范围与越界说明**
- 读取的路径：
  - `experiments/abc20-g04-20260923/` 下的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。
  - `sources/game/modules/tome/` 下的 `dialogs/orders/Talents.lua`、`dialogs/shimmer/ShimmerRemoveSustains.lua`、`dialogs/talents/MagicalCombatArcaneCombat.lua`、`init.lua`、`load.lua`。这 5 个文件的 sha256 都与 source-access.json 核对一致，对应本体 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63。
- 没有额外读取源码，没有执行 `git show`，也没有读取 DLC 快照。
- addon-dev 组件没有源码：C31、C32 待确认；03329–03332 只按文本判断。
- 03323–03326 这几条叙事文本来自 lore 定义（load.lua:111 `PartyLore:loadDefinition`），但没有继续追读 lore 文件。这几条只按语义和同包上下文判断，C08 因此待确认。
- 没有创建临时文件或子 agent，没有修改仓库，没有读取其他报告、SPEC、STATE 或生产结论，没有越界。
