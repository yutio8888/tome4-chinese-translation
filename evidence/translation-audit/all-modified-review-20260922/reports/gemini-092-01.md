本批次（batch-092，条目 entry-03052 至 entry-03091，共 40 条）已完成只读核验。所有条目均来自 `mod-tome`，已按照固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 读取公开源码，并对照当前译文终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00` 及相关术语规范进行了逐条核对。

以下为逐条复核报告：

---

### entry-03052
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39647`（`mod-tome/data/zones/sandworm-lair/objects.lua`）
- **核验依据**：源码对应物品“巨龙胆汁”（`PUTRESCENT_POTION`）的简易使用动作名 `use_simple = { name=_t"drink the vile fluid", ... }`。译文“喝下这瓶恶臭液体”符合语境与道具特性，无占位符或格式问题。

---

### entry-03053
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39650`（`mod-tome/data/zones/sandworm-lair/objects.lua`）
- **核验依据**：源码为 `game.log("You have %d category point(s) to spend. Press p to use them.", who.unused_talents_types)`。译文“你有%d点技能树解锁点。请按 P 键使用。”中占位符 `%d` 准确对应，术语 `category point` 统一译为“技能树解锁点”，快捷键指引准确。

---

### entry-03054
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39652`（`mod-tome/data/zones/sandworm-lair/objects.lua`）
- **核验依据**：源码为红宝石眼睛（`ATAMATHON_ACTIVATE`）的宝石子类型 `subtype = "red"`。标签 `entity subtype`，译文“红色”准确无误。

---

### entry-03055
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39687`（`mod-tome/data/zones/scintillating-caves/zone.lua`）
- **核验依据**：源码为交错洞穴（Scintillating Caves）扭曲变体进入时的弹窗说明 `simplePopup(_t"Caves...", _t"As you enter the caves you notice the magic here has distorted the land, making sharp angles and turns.")`。译文“当你走进洞穴时，你发现这里已经被魔法力量扭曲了，使地形形成尖锐的棱角和弯折。”忠实通顺，语义完全吻合。

---

### entry-03056
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39709`（`mod-tome/data/zones/shadow-crypt/zone.lua`）
- **核验依据**：源码为区域定义 `name = _t"Shadow Crypt"`。译文“阴影地宫”符合通用地名规范。

---

### entry-03057
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39719`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为实体命名 `name = "Exploratory Farportal"`。译文“探索用远行传送门”严格遵循术语库 preferred 规范，用以区分普通远行传送门。

---

### entry-03058
- **状态**：细微观察
- **位置**：`mod-tome.lua:39725`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为触发特殊远行目的地卡尔迪扎尔太空堡垒（`caldizar-space-fortress`）时的日志：`game.log("#VIOLET#You enter the swirling portal and in the blink of an eye you set foot in a strangely familiar zone, right next to a farportal...")`。颜色代码 `#VIOLET#` 对应完整，省略号一致。观察到原文中的修饰副词 `strangely`（奇怪地/莫名熟悉）在译文“到了一个熟悉的地方”中被略去，略微淡化了主角传送到未知外太空堡垒时“既熟悉又异样”的叙事反差；但基本句意与机制功能传达正常。

---

### entry-03059
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39727`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为交互弹窗标题 `Dialog:simplePopup(_t"Exploratory Farportal", ...)`。译文“探索用远行传送门”符合术语标准。

---

### entry-03060
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39728`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为玩家未激活堡垒任务时的提示 `Dialog:simplePopup(_t"Exploratory Farportal", _t"The farportal seems to be inactive")`。译文“这个远行传送门关闭着”意译准确，符合游戏实际交互状态。

---

### entry-03061
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39729`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为远行传送门故障损坏分支提示 `Dialog:simplePopup(_t"Exploratory Farportal", _t"The farportal is broken and will not be usable anymore.")`。译文“远行传送门损坏了，已经无法使用。”忠实准确。

---

### entry-03062
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39730`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为堡垒能量不足分支提示 `Dialog:simplePopup(_t"Exploratory Farportal", _t"The fortress does not have enough energy to power a trip through the portal.")`。译文“堡垒能量不足，无法驱动远行传送门进行旅行。”准确且表意清晰。

---

### entry-03063
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39731`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为启动确认弹窗 `Dialog:yesnoPopup(_t"Exploratory Farportal", _t"Do you want to travel in the farportal? You cannot know where you will end up.", ...)`。译文“你想穿过远行传送门么？你可不知道它会把你送到哪里。”通顺自然，标点与句意无误。

---

### entry-03064
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39732`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为随机探索副本中的返程实体命名 `g.name = _t"Exploratory Farportal exit"`。译文“探索用远行传送门出口”符合术语规范。

---

### entry-03065
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39735`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为传送到达随机探索地带后的日志 `game.log("#VIOLET#You enter the swirling portal and in the blink of an eye you set foot in an unfamiliar zone, with no trace of the portal...")`。颜色代码 `#VIOLET#` 匹配，省略号一致，译文“你进入了传送漩涡，一眨眼功夫你发现你到了一个陌生的地方，传送门不见了……”准确通俗。

---

### entry-03066
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39743`（`mod-tome/data/zones/shertul-fortress/grids.lua`）
- **核验依据**：源码为训练木桩控制球的全局伤害统计回调 `("Turns: %d\nTotal Damage: %d\nDamage/turns: %d"):tformat(turns, data.total, data.total / turns)`。3 个 `%d` 占位符和 2 个换行符严格对应，译文“回合数：%d\n总伤害：%d\n每回合伤害：%d”完全匹配。

---

### entry-03067
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39755`（`mod-tome/data/zones/shertul-fortress/npcs.lua`）
- **核验依据**：源码为异形触手首领（`WEIRDLING_BEAST`）的描述文本。译文“一只大致呈人形的生物，四肢的位置长着触须般的附肢。当你发现它没有头时，倒吸了一口凉气。腐臭的肉疣在它皮肤上迅速鼓起，又迅速炸开。”逐句对照完整，措辞生动且忠实于原文。

---

### entry-03068
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39778`（`mod-tome/data/zones/shertul-fortress/zone.lua`）
- **核验依据**：源码为堡垒子区域的动态显示名模板 `("%s (Yiilkgur, the Sher'Tul Fortress)"):tformat(_t(zn))`。占位符 `%s` 匹配，中文全角括号规范替换半角括号，专名“夏·图尔”与“伊克格”均符合术语表，译文“%s（夏·图尔堡垒，伊克格）”与同 section 前一条一致。

---

### entry-03069
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39792`（`mod-tome/data/zones/shertul-fortress-caldizar/grids.lua`）
- **核验依据**：源码为外太空堡垒实体命名 `name = "Exploratory Farportal"`。译文“探索用远行传送门”符合术语标准。

---

### entry-03070
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39798`（`mod-tome/data/zones/shertul-fortress-caldizar/grids.lua`）
- **核验依据**：源码为外太空堡垒中传送门弹窗标题 `Dialog:simplePopup(_t"Farportal", ...)`。译文“远行传送门”符合术语标准。

---

### entry-03071
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39799`（`mod-tome/data/zones/shertul-fortress-caldizar/grids.lua`）
- **核验依据**：源码为外太空堡垒传送门未激活提示 `Dialog:simplePopup(_t"Farportal", _t"The farportal seems to be inactive")`。译文“这个远行传送门关闭着”与 entry-03060 保持统一。

---

### entry-03072
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39813`（`mod-tome/data/zones/shertul-fortress-caldizar/zone.lua`）
- **核验依据**：源码为进入太空堡垒时的弹窗剧情文本。译文“随着突然的震动，你发现自己身处某个熟悉的地方。那光滑的墙壁和柔和的灯光让你想起自己的堡垒。不过它仍然有所不同。背景中传来轻柔的嗡嗡声，你感觉整个身体轻飘飘的，几乎像羽毛一样，似乎你轻轻的移动都能跃至半空。你有着一种奇异的感觉——你似乎不在马基·埃亚尔了……在你的前方你感到了某种既可怕又美妙的东西，恐惧充满了你身心的每个角落。”中专名“马基·埃亚尔”遵循 preferred 规范，零重力机制描述贴切，文风与原典一致。

---

### entry-03073
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39826`（`mod-tome/data/zones/slazish-fen/grids.lua`）
- **核验依据**：源码为破坏沼泽传送门完成任务时的日志 `game.log("#VIOLET#The portal starts to break down, run!")`。颜色代码 `#VIOLET#` 与标点感叹号完全一致，译文“#VIOLET#传送门开始崩塌了，快跑！”准确无误。

---

### entry-03074
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39834`（`mod-tome/data/zones/slazish-fen/npcs.lua`）
- **核验依据**：源码为娜迦潮汐守卫（`NAGA_TIDEWARDEN`）描述。译文“在你面前站着一个高大的身影，本该是双腿的位置由一条蛇尾高高撑起。他的躯干纤细而精悍，面容有着精灵般的俊美，两侧垂落着一缕缕金色长发。但这个生物也透着一股凶悍之气，明亮的双眼背后藏着燃烧的怒火。”逐句对应完全吻合，文笔流畅。

---

### entry-03075
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39838`（`mod-tome/data/zones/slazish-fen/npcs.lua`）
- **核验依据**：源码为娜迦海仙女（`naga nereid`）描述。译文“一双绿色的眼睛从缕缕金色长发后凝视着你，那长发如波浪般垂落在光洁苍白的肌肤上。你的目光被裸露的肌肤吸引，但再往下看，就会见到黑色的鳞片一路延伸，化作长长的蛇尾。她一动，发丝分开，露出一张清瘦而美丽的脸庞，颧骨高耸，双唇丰润。然而，纵使这奇异生灵如此诱人，那蛇一般的尾巴带来的恐惧仍让你脊背发凉。”翻译极佳，语意精准。

---

### entry-03076
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39878`（`mod-tome/data/zones/slime-tunnels/grids.lua`）
- **核验依据**：源码为巅峰入口确认弹窗 `_t'As you stand on the stairs you can feel this is a "do or die" one way trip. If you enter there will be no coming back.\nEnter?'`。单换行符准确匹配，译文“当你站在楼梯上时，你能感觉到这是一次不能回头的战斗，非生即死，一旦进去就不能回来。\n现在进去么？”符合决战单程旅途的语境。

---

### entry-03077
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39906`（`mod-tome/data/zones/sludgenest/grids.lua`）
- **核验依据**：源码共用巅峰入口阶梯的进入确认文本。与 entry-03076 完全一致，换行和语义均准确无误。

---

### entry-03078
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39925`（`mod-tome/data/zones/sludgenest/zone.lua`）
- **核验依据**：源码为泥泞巢穴中地形变怪物的动态日志 `game.logSeen(m, "#YELLOW_GREEN#One of the wall shakes for a moment and then turns into %s!", m.name:capitalize())`。颜色代码 `#YELLOW_GREEN#`、占位符 `%s` 及感叹号完全一致，译文“#YELLOW_GREEN#一面墙壁颤抖了一会，变成了 %s！”准确无误。

---

### entry-03079
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39936`（`mod-tome/data/zones/south-beach/grids.lua`）
- **核验依据**：源码为约会任务未完成时阻拦离开的日志 `game.log("You have not finished your romantic time at the beach.")`。译文“你还没享受完在海滩的浪漫时光。”通顺准确。

---

### entry-03080
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39946`（`mod-tome/data/zones/south-beach/npcs.lua`）
- **核验依据**：源码为梅琳达濒死触发枯萎爆发的大字广播 `game.bignews:say(120, "#DARK_GREEN#As Melinda is about to die a powerful wave of blight emanates from her!")`。颜色代码 `#DARK_GREEN#` 匹配，专名“梅琳达”与伤害类型“枯萎”准确，感叹号一致。

---

### entry-03081
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39958`（`mod-tome/data/zones/south-beach/zone.lua`）
- **核验依据**：源码为战斗中梅琳达异变光环提示 `game.bignews:say(120, "#DARK_GREEN#Melinda begins to glow with an eerie aura!")`。颜色代码 `#DARK_GREEN#` 匹配，感叹号匹配，译文“#DARK_GREEN#梅琳达身边散发出诡异的光环！”准确。

---

### entry-03082
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39963`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为天体实体命名 `name = "Shandral (Sun)"`。中文括号规范，译文“珊德拉（恒星）”准确对应星系中心恒星。

---

### entry-03083
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39965`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为天体实体命名 `name = "Eyal (Planet)"`。译文“埃亚尔（星球）”括号规范，名称准确。

---

### entry-03084
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39966`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为埃亚尔行星描述 `desc=_t[[One of the main planets of the Shandral system.]]`。译文“珊德拉星系的主要行星之一。”通顺准确。

---

### entry-03085
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39967`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为卫星实体命名 `name = "Summertide (Moon of Eyal)"`。专名 Summertide 统一译作“炎华”，中文括号规范，译文“炎华（埃亚尔的卫星）”准确无误。

---

### entry-03086
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39969`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为卫星实体命名 `name = "Wintertide (Moon of Eyal)"`。专名 Wintertide 统一译作“霜华”，中文括号规范，译文“霜华（埃亚尔的卫星）”准确无误。

---

### entry-03087
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39970`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为天体实体命名 `name = "Kolal (Planet)"`。译文“克拉尔（星球）”括号规范，音译准确。

---

### entry-03088
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39971`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为天体实体命名 `name = "Luxam (Planet)"`。译文“卢克萨姆（星球）”括号规范，音译准确。

---

### entry-03089
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39972`（`mod-tome/data/zones/stellar-system-shandral/grids.lua`）
- **核验依据**：源码为天体实体命名 `name = "Ponx (Gaz Planet)"`。作者拼写为 Gaz Planet（气态行星），译文“波尼克斯（气态巨星）”准确达意，括号规范。

---

### entry-03090
- **状态**：未发现问题
- **位置**：`mod-tome.lua:39984`（`mod-tome/data/zones/tannen-tower/grids.lua`）
- **核验依据**：源码为泰恩之塔传送门弹窗标题 `require("engine.ui.Dialog"):yesnoPopup(_t"Back and there again", ...)`。文本严格匹配术语快照中的倒装任务/成就标题 preferred 规范“归而复往”（用以区分普通 There and back again）。

---

### entry-03091
- **状态**：未发现问题
- **位置**：`mod-tome.lua:40000`（`mod-tome/data/zones/tannen-tower/npcs.lua`）
- **核验依据**：源码为巨型龙形傀儡（`DROLEM`）的描述。实体定义中包含机制属性 `block_sight = true`。译文“这是泰恩的构装体，一只巨大的龙形傀儡。\n它如此庞大，遮蔽了它身后的视线。”中术语“泰恩”、“构装体”、“傀儡”完全规范，换行符一致，且机制描述与底层 `block_sight` 逻辑严格对应。
