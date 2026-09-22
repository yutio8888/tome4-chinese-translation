本批次为 **batch-090**（条目范围：`entry-02972` 至 `entry-03011`，共 40 条）。已完成文件哈希核对（SHA-256：`4a842aa56467043966f2a88091f53bab8521b1e8c93a8bdae933f1c5306cd2e9` 匹配无误）。
涉及公开源码均通过固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 核验，译文语境基准已对齐至 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

以下为逐条复核报告：

---

### entry-02972
- **位置**：`mod-tome.lua:38566`（section: `mod-tome/data/zones/golem-graveyard/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应 `ATAMATHON_RUBY_EYE` 的 `subtype = "red"`，在宝石子类别语境下译为“红色”，准确规范。

---

### entry-02973
- **位置**：`mod-tome.lua:38568`（section: `mod-tome/data/zones/golem-graveyard/objects.lua`）
- **状态**：细微观察
- **可核验依据**：源码对应阿塔玛森红宝石眼球描述。专名术语均准确（`Atamathon` -> 阿塔玛森，`halflings` -> 半身人，`Age of Pyre` -> 烈火纪，`orcs` -> 兽人，`Garkul the Devourer` -> 吞噬者加库尔）。段落换行与原文一致。细微观察点在于后半句：“managed to deal a crippling blow by killing their leader”译为“成功地使对方的首领……走向死亡”，略微弱化了“给予沉重打击 / 予以重创”的语义色彩，但整体剧情与核心事实传达完整。

---

### entry-02974
- **位置**：`mod-tome.lua:38642`（section: `mod-tome/data/zones/grushnak-pride/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应格鲁希纳克部落的加库尔传说底本文档描述（`desc = _t[[The Legend of Garkul the Devourer, mightiest of all orcs.]]`）。加库尔与吞噬者称号规范，语序流畅，大意准确。

---

### entry-02975
- **位置**：`mod-tome.lua:38659`（section: `mod-tome/data/zones/halfling-ruins/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应半身人废墟中遭遇试验品 Z 时向夺心魔玩家发出的心灵警告弹窗。样式与颜色标签 `#{italic}##UMBER#...#{normal}#` 完整对称闭合，换行对齐，术语 `Wayist` 准确译为“维网信徒”。

---

### entry-02976
- **位置**：`mod-tome.lua:38663`（section: `mod-tome/data/zones/halfling-ruins/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应触发紧急回归时的玩家日志输出。语义准确，中文省略号规范。

---

### entry-02977
- **位置**：`mod-tome.lua:38671`（section: `mod-tome/data/zones/halfling-ruins/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应 `YEEK_WAYIST` 的外貌描述。半身人对照、白毛大头及灵能悬浮武器特征传达地道贴切，标点准确。

---

### entry-02978
- **位置**：`mod-tome.lua:38684`（section: `mod-tome/data/zones/halfling-ruins/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应半身人穿戴夺心魔皮毛长袍（`Yeek-fur Robe`）时的特殊增益日志。颜色码 `#LIGHT_BLUE#` 保留完整，感叹号对齐，语义准确。

---

### entry-02979
- **位置**：`mod-tome.lua:38724`（section: `mod-tome/data/zones/high-peak/grids.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应巅峰高塔内的远行传送门实体 `FAR_EAST_PORTAL` 的名字。与全库同名传送门实体（如 `charred-scar`）保持一致，统一译为“远行传送门：至远东大陆”。

---

### entry-02980
- **位置**：`mod-tome.lua:38729`（section: `mod-tome/data/zones/high-peak/grids.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应通往西方的远行传送门实体 `WEST_PORTAL` 的名字。`Iron Throne` 严格对应术语库标准“钢铁王座”。

---

### entry-02981
- **位置**：`mod-tome.lua:38734`（section: `mod-tome/data/zones/high-peak/grids.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应通往虚空的远行传送门实体 `VOID_PORTAL` 的名字。`the Void` 严格对应术语库标准“虚空”。

---

### entry-02982
- **位置**：`mod-tome.lua:38735`（section: `mod-tome/data/zones/high-peak/grids.lua`）
- **状态**：细微观察
- **可核验依据**：源码对应 `VOID_PORTAL` 的地形描述。段落换行与原文对应。细微观察有两点：其一，句首 `A farportal` 在此简译为“传送门”（与本 section 内另两座传送门说明保持了同模板一致，实体名则为“远行传送门”）；其二，第二段“seems to go to an unknown place, seemingly out of this world”译为“似乎通向未知之地，似乎为世外之地”，连续出现两个“似乎”，语感略有重叠，但不影响整体语义传达。

---

### entry-02983
- **位置**：`mod-tome.lua:38739`（section: `mod-tome/data/zones/high-peak/grids.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应玩家使用多元水晶球关闭召唤传送门后的地形名称格式化（`g.name = ("%s (disabled)"):tformat(_t(g.name))`）。占位符 `%s` 保持一致，括号规范转换为全角括号。

---

### entry-02984
- **位置**：`mod-tome.lua:38762`（section: `mod-tome/data/zones/high-peak/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应堕落/高阶太阳骑士艾琳（Aeryn）的描述文本。板甲（`plate armour`）与整体句意翻译准确通顺。

---

### entry-02985
- **位置**：`mod-tome.lua:38771`（section: `mod-tome/data/zones/high-peak/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应浸血钻石（`bloodsoaked diamond`）的物品描述。语义简洁准确。

---

### entry-02986
- **位置**：`mod-tome.lua:38775`（section: `mod-tome/data/zones/high-peak/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应埃兰达日记（`ELANDAR_JOURNAL1` / `2`）的物品描述。语义简洁准确。

---

### entry-02987
- **位置**：`mod-tome.lua:38787`（section: `mod-tome/data/zones/high-peak/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应觉醒吸能法杖（`STAFF_ABSORPTION_AWAKENED`）的主动吸收生命技能战斗日志。两个 `%s` 占位符、战斗日志标签 `#Source#` 和 `#target#!` 完整保留，语义准确。

---

### entry-02988
- **位置**：`mod-tome.lua:38790`（section: `mod-tome/data/zones/high-peak/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应剧情宝石生死珍珠（`PEARL_LIFE_DEATH`）的 `subtype = "white"`，作为宝石子类型译为“白色”，准确无误。

---

### entry-02989
- **位置**：`mod-tome.lua:38849`（section: `mod-tome/data/zones/infinite-dungeon/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应药水使用可见日志（`game.logSeen(who, "%s quaffs the %s!", ...)`）。两个 `%s` 占位符、叹号均对应，动词 `quaff` 译为“大口喝下”生动准确。

---

### entry-02990
- **位置**：`mod-tome.lua:38850`（section: `mod-tome/data/zones/infinite-dungeon/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应喝下武艺药水后解锁技能系 `technique/combat-training` 的提示日志。颜色标签 `#VIOLET#` 完整，括号完备，`Combat Training` 正确对应“战斗训练系”。

---

### entry-02991
- **位置**：`mod-tome.lua:38851`（section: `mod-tome/data/zones/infinite-dungeon/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应药水学会射击技能（`T_SHOOT`）的提示日志。颜色标签 `#VIOLET#` 完整，弓与投石索语义准确。

---

### entry-02992
- **位置**：`mod-tome.lua:38854`（section: `mod-tome/data/zones/infinite-dungeon/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应药水包含技能均已学会时的日志分支。颜色标签 `#VIOLET#` 完整，语义准确。

---

### entry-02993
- **位置**：`mod-tome.lua:38860`（section: `mod-tome/data/zones/infinite-dungeon/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应走反魔路线时自动卸下奥术装备的提示日志。占位符 `%s` 准确，语义忠实。

---

### entry-02994
- **位置**：`mod-tome.lua:38891`（section: `mod-tome/data/zones/infinite-dungeon/zone.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应无尽地下城下层出口提示（拼接 `grids.desc` 与 `layout.desc`）。前置换行排版严格对齐，占位符 `%s%s` 数量与顺序准确无误。

---

### entry-02995
- **位置**：`mod-tome.lua:38923`（section: `mod-tome/data/zones/keepsake-meadow/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应遗物草原商队商人（`CARAVAN_MERCHANT`）描述。语义准确。

---

### entry-02996
- **位置**：`mod-tome.lua:38925`（section: `mod-tome/data/zones/keepsake-meadow/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应商队守卫（`CARAVAN_GUARD`）描述。语义准确。

---

### entry-02997
- **位置**：`mod-tome.lua:38927`（section: `mod-tome/data/zones/keepsake-meadow/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应商队搬运工（`CARAVAN_PORTER`）描述。语义准确。

---

### entry-02998
- **位置**：`mod-tome.lua:38944`（section: `mod-tome/data/zones/keepsake-meadow/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应首领 NPC 实体名 `Kyless`。严格遵循术语快照 preferred 标准译为“凯勒斯”。

---

### entry-02999
- **位置**：`mod-tome.lua:38945`（section: `mod-tome/data/zones/keepsake-meadow/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应凯勒斯的 NPC 描述。专名凯勒斯一致，人物状态描写传神贴切。

---

### entry-03000
- **位置**：`mod-tome.lua:38965`（section: `mod-tome/data/zones/keepsake-meadow/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应凯勒斯日记残页（`KYLESS_JOURNAL`）描述。专名一致，语义准确。

---

### entry-03001
- **位置**：`mod-tome.lua:38966`（section: `mod-tome/data/zones/keepsake-meadow/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应任务物品实体名 `Kyless' Book`。专名与通用物品名准确对齐。

---

### entry-03002
- **位置**：`mod-tome.lua:38967`（section: `mod-tome/data/zones/keepsake-meadow/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应凯勒斯之书的描述。专名凯勒斯准确，文字润色生动自然，语义忠实。

---

### entry-03003
- **位置**：`mod-tome.lua:39028`（section: `mod-tome/data/zones/last-hope-graveyard/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应死灵法师赛利亚（Celia）的外貌描述。长袍、病容皮肤与怀孕体态细节刻画精准，文学色彩优美。

---

### entry-03004
- **位置**：`mod-tome.lua:39029`（section: `mod-tome/data/zones/last-hope-graveyard/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应击杀 Celia 后获得心脏的任务日志输出。占位符 `%s` 及中英文标点一致。

---

### entry-03005
- **位置**：`mod-tome.lua:39031`（section: `mod-tome/data/zones/last-hope-graveyard/npcs.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应巫妖形态任务挖取心脏的弹窗说明。专名赛利亚与巫妖仪式准确，换行结构一致。

---

### entry-03006
- **位置**：`mod-tome.lua:39039`（section: `mod-tome/data/zones/last-hope-graveyard/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应赛利亚的信件描述。译文简洁准确。

---

### entry-03007
- **位置**：`mod-tome.lua:39044`（section: `mod-tome/data/zones/last-hope-graveyard/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应赛利亚仍在跳动的心脏（`CELIA_HEART`）描述。术语“死灵法师”与专名“赛利亚”准确，与物品名上下文高度吻合。

---

### entry-03008
- **位置**：`mod-tome.lua:39053`（section: `mod-tome/data/zones/last-hope-graveyard/zone.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应开棺生成亡灵时的日志提示。`undead` 准确译为术语库规范“亡灵”，语义清晰。

---

### entry-03009
- **位置**：`mod-tome.lua:39059`（section: `mod-tome/data/zones/last-hope-graveyard/zone.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应踏入最后的希望地下陵墓二层时的氛围描写弹窗。三段式结构与空行严格对应，破折号与省略号对齐；`dread`（心理恐惧感，非召唤物实体名）与 `unholy horror`（不洁的恐怖）区分得当，行文压迫感十足，翻译质量极高。

---

### entry-03010
- **位置**：`mod-tome.lua:39074`（section: `mod-tome/data/zones/mark-spellblaze/grids.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应大爆炸印记祭坛上腐化沙虫女王心脏的日志。颜色代码 `#GREEN#` 完好保留，动词与意象准确。

---

### entry-03011
- **位置**：`mod-tome.lua:39088`（section: `mod-tome/data/zones/mark-spellblaze/objects.lua`）
- **状态**：未发现问题
- **可核验依据**：源码对应大腐化者草稿信件描述。译文简洁准确。
