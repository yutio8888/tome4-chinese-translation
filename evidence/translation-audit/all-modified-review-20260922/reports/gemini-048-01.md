### batch-048 译文只读复核报告

#### 1. 前置信息与校验
- **复核批次**：batch-048（条目范围：`entry-01325` 至 `entry-01344`，共 20 条）
- **批次文件哈希核对**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-048.md` 的 SHA-256 值为 `d9a810879dd2227b59bc2137661bc51e940c59e17e5e48680a751e41f1a08967`，核验一致。
- **源码比对基准**：依据 `evidence/translation-audit/all-modified-review-20260922/source-access.json`，本批全部 20 条条目均位于 `mod-tome` 模块下的 Lore 文本，对应 `t-engine4` 公开源码仓库固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/data/lore/` 目录。
- **译文工作树比对终点**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua` 当前工作树与该 commit 一致）。

---

#### 2. 逐条复核记录（共 20 条）

- **entry-01325** (`mod-tome.lua:18914` / `mod-tome/data/lore/orc-prides.lua`)
  - **判定**：未发现问题
  - **依据**：格式标签 `#{bold}#`、`#{italic}#`、`#{normal}#` 完整对称闭合；段落结构与换行与原文 8 个自然段完全对应；专有名词（Eldoral/艾德瑞尔人、Nargols/纳格尔人、Thaloren/自然精灵、Shaloren/永恒精灵、Daikara Mountains/岱卡拉山脉、Reknor/瑞库纳、Sher'Tul farportal/夏·图尔远行传送门、Atamathon/阿塔玛森）均准确规范；对 Prides 双关语（兽人部落与自豪）处理恰当；叙事完整准确，无漏译错译。

- **entry-01326** (`mod-tome.lua:19079` / `mod-tome/data/lore/orc-prides.lua`)
  - **判定**：细微观察
  - **依据**：正文内容忠实生动，专有名词（Sher'Tul/夏·图尔、Derth/德斯镇、Dreadfell/恐惧王座）及术语均符合规范。但在排版空行上存在细微不一致：英文原文中每段日志分隔处的省略号（`...`）后均为 1 个空行（2 个换行符），而译文在第 1 处和第 2 处 `……` 后均出现了连续 2 个空行（3 个换行符，见 `mod-tome.lua:19104-19105` 与 `19111-19112`），第 3 处省略号后则为 1 个空行，空行排版格式略有微瑕。

- **entry-01327** (`mod-tome.lua:19139` / `mod-tome/data/lore/rhaloren.lua`)
  - **判定**：未发现问题
  - **依据**：专有名词（Scintillating Caverns/闪光洞穴、Spellblaze/魔法大爆炸、Council/长老会、The Inquisitor/审判者）符合术语库 preferred 规范；4 个自然段的段落换行与标点完全匹配；语义忠实原意，无增删误译。

- **entry-01328** (`mod-tome.lua:19211` / `mod-tome/data/lore/sandworm.lua`)
  - **判定**：存在疑点
  - **依据**：诗歌第二节首句 `"In the trail of giant worms I walk"` 译为 `"我循着巨型沙龙的踪迹"`。
    1. 原文为 `"giant worms"`（蠕虫/沙虫），此处译为“沙龙”疑似将 worm 混淆为 wyrm 或拼写输入笔误。
    2. 同 section（`sandworm.lua`）内其他各篇诗歌中，`"sandworms"` 均统译为“沙虫”（如 `mod-tome.lua:19254`），`"legendary worm"` 译为“传奇巨虫”（`mod-tome.lua:19262`）。
    3. 诗歌第一节专门以首句 `"crimson wyrms"`（赤红巨龙）和 `"drakes"`（幼龙）与沙漠深处追寻的物种形成对比，强调诗人身为龙战士却在沙漠中追踪 giant worms；译作“巨型沙龙”破坏了龙（wyrm）与虫（worm）的物种设定区别与文本对照逻辑。

- **entry-01329** (`mod-tome.lua:19276` / `mod-tome/data/lore/scintillating-caves.lua`)
  - **判定**：未发现问题
  - **依据**：专有名词（scintillating caves/闪光洞穴、council/长老会、Spellblaze/魔法大爆炸、Sher'Tul farportal/夏·图尔时代遗留的远行传送门、Shaloren mages/永恒精灵法师）均准确规范；4 个自然段结构及末尾换行对应一致；省略号与问号标点完备，语意流畅。

- **entry-01330** (`mod-tome.lua:19334` / `mod-tome/data/lore/scintillating-caves.lua`)
  - **判定**：未发现问题
  - **依据**：3 篇日志的日期斜体标签 `#{italic}#...#{normal}#` 闭合完整；历法与月份纪年（Age of Ascendancy/卓越纪、Mirth/狂欢月、Summertide/炎华）译名规范统一；专有名词（Rhaloren/罗兰精灵、scintillating caverns/闪光洞穴）准确；段落换行与标点无误，叙事生动完整。

- **entry-01331** (`mod-tome.lua:19358` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：细微观察
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合完好；夏·图尔语文本未作破坏。细微处在于原文夏·图尔语外层使用英文直单引号 `'...'`，此处译文转为了中文全角双引号 `“...”`，而同 section 内多数同类壁画未识文字条目（如 19364、19376、19382、19388、19394）均保持直单引号 `'...'`，标点风格略有不一致，但无功能性缺陷。

- **entry-01332** (`mod-tome.lua:19359` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 完整闭合；核心设定术语 `"petty gods"` 准确译为 `"伪神们"`（符合术语快照 `petty gods 伪神 T.NARRATIVE.LORE preferred`）；语义准确，标点匹配完备。

- **entry-01333** (`mod-tome.lua:19365` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：存在疑点
  - **依据**：
    1. `"And he made the Sun from his breath"` 原文指阿马克泰尔“以其气息创造了太阳”的神话创世行为，译文误译为 `"他深呼吸后把太阳高举到了世界之上"`，完全遗漏并歪曲了“创造/制造太阳”（made the Sun）的核心叙事，且将 `"from his breath"` 误读为“深呼吸后”。
    2. `"and the petty gods fled before his glory"` 原文中 `"fled"` 为 flee（逃跑、奔逃）之过去式，壁画画面描述亦为 `"The other gods are running from him"`（其他神明从他身边逃跑），译文却译为 `"伪神们慑服于他的荣耀"`，将诸神“畏光逃跑”反向曲解为“顺从/臣服”，与前后剧情事实矛盾。
    3. `"All that this light touches shall be mine"` 原文为“凡此光照及之处皆归我所有”，译文过度意译为 `"阳光所至，即我所至"`，改变了原句对主权占有的宣称。
    4. `"his might surpassed all else"` 原文指其神力超越/凌驾于万物之上，译文被窄化且增添为 `"他的勇武震慑了众人"`。

- **entry-01334** (`mod-tome.lua:19370` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：细微观察
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合完整，夏·图尔语字符原样保留。细微观察在于原文外层为单引号 `'...'`、内层为转义双引号 `"..."`，译文将外层改为中文全角双引号 `“...”`，而内层保留半角双引号 `"..."`，导致出现双引号嵌套双引号（`“... "..." ”`）的标点层级微瑕。

- **entry-01335** (`mod-tome.lua:19371` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合正确；专有名词（AMAKTHEL/阿马克泰尔、SHER'TUL/夏·图尔）对应准确；叙述与对话层级清晰，语义传达忠实无误。

- **entry-01336** (`mod-tome.lua:19377` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合正确；直单引号与省略号保留完整；准确传达了夏·图尔人征服世界、建造水晶之城与天际堡垒但仍不满足的叙事。

- **entry-01337** (`mod-tome.lua:19379` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：双行换行排版结构完全一致；专有名词（Sher'Tul/夏·图尔人、runed staff/符文法杖）准确；提示语 `"There is some text beneath "` 译为 `"下面有一行文字"` 规范统一。

- **entry-01338** (`mod-tome.lua:19385` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：双行换行排版对应完好；`"Sher'Tul warriors fighting and slaying god-like figures over ten times their size"` 译为 `"夏·图尔的战士们正与十倍于自身的神明般的存在厮杀，并将其斩灭"`，准确生动；提示语完整无误。

- **entry-01339** (`mod-tome.lua:19388` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合正确；夏·图尔语字符完整无损；单引号闭合完好；提示词 `"which you do not understand:"` 译为 `"不明意义的文字："` 统一得当。

- **entry-01340** (`mod-tome.lua:19395` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 闭合正确；专有名词（AMAKTHEL/阿马克泰尔、golden throne/黄金王座）准确；`"was assaulted"`、`"he was finally felled"` 翻译贴切，单引号保留完整。

- **entry-01341** (`mod-tome.lua:19402` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：单句壁画损毁描述翻译忠实完整，准确传达了深深的刻痕、划痕与残存火焰图案的意象，标点规范。

- **entry-01342** (`mod-tome.lua:19405` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：短标题翻译准确，专有名词（Sher'Tul/夏·图尔人）规范，标点 `?!` 转换为中文全角 `？！`，符合中文排版习惯。

- **entry-01343** (`mod-tome.lua:19406` / `mod-tome/data/lore/shertul.lua`)
  - **判定**：未发现问题
  - **依据**：专有名词（Sher'Tul Fortress/夏·图尔要塞、Sher'Tul/夏·图尔人）规范统一；叙述准确流畅，无漏译错译。

- **entry-01344** (`mod-tome.lua:19454` / `mod-tome/data/lore/slazish.lua`)
  - **判定**：未发现问题
  - **依据**：标签 `#{italic}#...#{normal}#` 正确闭合；段落结构、换行与双引号对应无误；专有名词与角色称谓（Waverider Tiamel/踏浪者塔米尔、Zoisla/佐西拉、Saviour/救世主、farportal/远行传送门、Slasul/萨拉苏尔、the Devourer/吞噬者）均符合设定与术语规范；娜迦语境下的 `"arms and tails"`（手臂和尾巴）及军事语境下的 `"strengths"`（兵力）处理自然贴切。

---

#### 3. 统计汇总
- **覆盖条目**：20 / 20 条（全部逐条核验完成）
- **未发现问题**：15 条（`entry-01325`, `entry-01327`, `entry-01329`, `entry-01330`, `entry-01332`, `entry-01335`, `entry-01336`, `entry-01337`, `entry-01338`, `entry-01339`, `entry-01340`, `entry-01341`, `entry-01342`, `entry-01343`, `entry-01344`）
- **存在疑点**：2 条（`entry-01328` 龙/虫混淆、`entry-01333` 创世造日遗漏与伪神逃跑反向误译）
- **细微观察**：3 条（`entry-01326` 日志多余空行、`entry-01331` 引号风格不一、`entry-01334` 双引号嵌套微瑕）