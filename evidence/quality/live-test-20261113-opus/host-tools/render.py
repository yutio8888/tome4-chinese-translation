import re
EXTRA = """
本轮背景：**发布后质量检查（不是发布前置条件，也不等于自然通关）**。插件为公开发布的 v0.3.12，sha256 22706f10…，共享安装只读，**不得替换或修改 game/addons**。只用 Opus 测试。
检查项：中文是否显示；占位符、数值、颜色标签；残留英文；截断或溢出；主语、术语与搭配；Lua 错误。

**本轮预算（比通用模板更严，以本节为准）**：
- 读图 **20** 张，其中全屏 **3** 张；工具调用 **100** 次；读入图片的累计文件字节 **15 MB 收尾、20 MB 停止**（每张 `stat -c %s` 累加，记为 progress 的 `img_bytes`）。
- **提前收尾线：读图达到 16 张或工具调用达到 80 次**，立即把 findings、objects、REPORT 和复现步骤写盘后结束，不要越过 100 次。上一轮有会话实际调用 129/144 次，主代理会用会话文件只读统计实际次数。
- progress 每行格式：`reads=<n>/20 full=<n>/3 calls≈<n>/100 img_bytes=<MB>/15`。

**到场与调试（允许，但每步记录到 `testers/{NAME}/debug-actions.md`：时间、菜单项/命令、参数）**：
- 存档已由主代理准备并实际读档核对过（game.teag 存在，读档直接到达目标地图），**不要新建角色，不要换区**。角色已是 50 级、半神模式、已学全部可学技能。
- 启动与读档：**只运行 `testers/{NAME}/boot.sh`**（约 70 秒）。它会启动游戏，点掉首次启动的联网欢迎框（两次点击，没有该框时也无害），读档，再输出右上角区域名裁切 `ZONE_CROP …`。只 Read 这张小裁切确认地图。**准备阶段不读任何整屏图**；如果裁切不是目标地图，先用 1 张缩小到 400×225 的整屏图判断，并计入全屏额度。
- 有提示框时不要按 Escape（会打开游戏菜单）；关提示框就把鼠标移到 (1200,880)。
- 调试菜单用 `testers/{NAME}/dbgopen.sh`（像素校验重试）。控制台用 `testers/{NAME}/con.sh '命令1' '命令2'`：它会先聚焦游戏窗口、松开 ctrl，已打开就不再按 ctrl+l，输完自动按 Escape 关闭；加 `-k` 则保持打开。按键（i、l 等）没反应时先运行 `testers/{NAME}/focus.sh`。
- 上一批验证过的界面打开方式（键盘入口不稳时用；属于调试打开的真实界面，记入 debug-actions）：
  - 物品栏（triggerVirtual 不一定生效，优先用这条）：`con.sh -k 'D=require("mod.dialogs.ShowEquipInven")' 'game:unregisterDialog(game.dialogs[#game.dialogs]) game:registerDialog(D.new("x",game.player))'`
  - 角色面板/观察详情（M 为目标实体）：`con.sh -k 'CS=require("mod.dialogs.CharacterSheet")' 'game:unregisterDialog(game.dialogs[#game.dialogs]) game:registerDialog(CS.new(M))'`
  - 按 Escape 关面板；不要在提示框存在时按 Escape（会打开游戏菜单），先把鼠标移到 (1200,880)。
- 控制台单条命令保持在 80 字符内；长逻辑拆成多条，用全局变量串接。控制台只用于定位、放置测试对象或生成物品，**控制台输出不能当显示证据**。
- 悬停坐标：`print(game.level.map:getTileToScreen(x,y))` 写入 game.log，加 32 像素为格子中心；提示框固定在屏幕右侧 x≈968–1600，直接裁这个区域。观察详情用 l 或在怪物上按右键再选查看。
- 不要攻击 unique 首领；它们只用于查看。如果弹出剧情对话，记录后关闭。

**证据分类**：`debug-ui`（调试到场/生成后在真实界面看到）、`natural`（正常取得或触发）、`console`（只有控制台输出）。三者必须分开，不得混记。

**产出（除通用的 findings.jsonl、progress.md、REPORT.md 外）**：
- `testers/{NAME}/objects.jsonl`，每个实际查看的对象一行：
  `{"kind":"monster|talent|effect|item|other","name_shown":"屏幕名称","english":"英文或null","where":"地图/界面","method":"debug-ui|natural|console","result":"ok|issue|not_reached","screen":"shots/…-c.png 或 null"}`
- REPORT.md 写明：各类对象查看数、通过数、异常数、未到达数；用过的调试手段；停止原因；未覆盖范围。
- 不要重复已知问题：`/workspace/tome4-chinese-translation/evidence/quality/live-test-20261111/` 与 `evidence/quality/live-test-20261112-late/ADJUDICATION.md` 中已记录的内容（含模组简介英文、冒号尾随空格与 APE 已修）。上一轮已看过的普通对象（见 late 证据 objects.jsonl）不要重复。
- 结束前 `kill -9` 自己的游戏进程（用 `ps -eo pid,args` 找含 `--tl-{NAME}` 的 t-engine 进程，**不要用 pkill -f**，也不要碰别人的进程或显示）。
"""
SCOPES_ALL = {
"o7a": ("191", """**场景组 o7a：沃尔部落（Vor Pride）1 层——兽人怪物、技能与装备**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，已在沃尔部落 1 层，本层有 82 个怪物：orc warrior、orc soldier、orc cryomancer / high cryomancer、orc high pyromancer、orc assassin、orc grand master assassin、icy orc wyrmic，以及多个带随机名的兽人稀有怪（如「高阶兽人冰霜术士 …」「兽人烈焰术士 …」）。
本会话只做：
1. 兽人怪物 4–5 种（优先 grand master assassin、wyrmic、high pyromancer、一个兽人稀有怪、soldier）：悬停提示，并对其中 2 个打开观察详情查看技能列表与 1–2 条技能说明。定位方法：控制台把对应怪物 `move` 到玩家附近空格，或把玩家传送到它旁边（`game.player:move(x,y,true)`）。
2. 用「h) 制造物品」生成 2 件兽人相关或高等级随机词缀装备（记下列表项名称），悬停并按 Ctrl 与已装备物品比较。
3. 预算允许：怪物施放到你身上的 1 个效果提示（左上效果图标悬停）。"""),
"o7b": ("192", """**场景组 o7b：Forbidden Cults——天灾之穴（Scourged Pits）1 层：怪物观察详情、Cults 物品、疯狂值**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，已在天灾之穴 1 层，本层有 93 个怪物：scourge drake hatchling、scourge drake、scourge wyrm、void horror、netherworm mass 等。上一轮只悬停看过天谴龙幼仔，本轮不要重复它。
注意：Cults DLC 包自带 zh_hans.lua，界面文本可能来自 DLC 包而不是插件。每条问题先在 `tome-cults.lua` 中 grep 中文片段；查不到的写「未在本库找到（可能来自 DLC 自带译文）」。
本会话只做：
1. 怪物观察详情：scourge wyrm、void horror、netherworm mass 各打开观察详情（不只是悬停），查看技能列表与 1–2 条技能说明。
2. Cults 物品：用「h) 制造物品」生成 2–3 件 Cults 神器，候选英文名 Spinal Cage、Staff of Bones、Fanged Collar、Perseverance、Rod of Entropy（列表按名称排序，找到后记录序号），悬停并按 Ctrl 比较。
3. 疯狂值：控制台依次执行 `P=game.player`、`P:learnTalentType("demented/madness",true)`、`P:learnTalent(P.T_INSANITY_POOL,true)`，再用调试菜单「k) 玩家升级」勾选「学习技能」接受。然后查看左侧资源栏的疯狂值显示、技能界面中 madness 树的 1–2 条技能说明（含疯狂值消耗行）。每条命令记入 debug-actions。"""),
"o7c": ("193", """**场景组 o7c：巅峰（High Peak）1 层——被动技能、武器/护甲 Ctrl 比较、首领**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，已在巅峰 1 层，本层有兽人法师猎手、熔炉巨人、女妖、雪巨人雷霆使者、恶魔 uruivellas / onilug、带随机名的稀有怪等。上一轮在巅峰看过：符文骨巨人、稀有怪半身人 Lbol、4 个主动技能、阿塞拉、巨兽皮甲、黑火之盾，本轮不要重复。
本会话只做：
1. 被动技能 2–3 条：在技能界面（或升级界面）悬停被动技能，看说明数值与条件。
2. 武器与护甲 Ctrl 比较：用「h) 制造物品」生成 1 件高等级武器、1 件身甲（不是上一轮那几件），先装备一件同部位物品，再悬停另一件并按 Ctrl 比较。
3. 首领：控制台依次执行 `M=game.zone:makeEntityByName(game.level,"actor","ELANDAR")`、`A=engine.Map.ACTOR`、`X,Y=util.findFreeGrid(game.player.x,game.player.y,5,true,{[A]=true})`、`game.zone:addEntity(game.level,M,"actor",X,Y)`，然后悬停并打开观察详情，查看 1–2 条技能说明。不要攻击它。若放置失败，改为查看 uruivellas（恶魔，已在本层）。"""),
"o7c2": ("195", """**场景组 o7c2：巅峰（High Peak）1 层接续——武器/护甲 Ctrl 比较、首领、1 条被动**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，在巅峰 1 层（主代理已读档核对）。前一会话 o7c 已看过被动技能「爆破专家」「炼金保护」（ok），不要重复。上一轮在巅峰看过：符文骨巨人、稀有怪半身人 Lbol、阿塞拉、巨兽皮甲、黑火之盾。
本会话只做：
1. 被动技能「危机感」：已有裁切 `testers/o7c2/shots/psv-ds-c.png`（o7c 截取，未核对），直接 Read 它核对，不必重新打开。
2. 武器与护甲 Ctrl 比较：用「h) 制造物品」生成 1 件高等级武器、1 件身甲（不是上面那几件），先装备一件同部位物品，再悬停另一件并按 Ctrl 比较。
3. 首领：控制台依次执行 `M=game.zone:makeEntityByName(game.level,"actor","ELANDAR")`、`A=engine.Map.ACTOR`、`X,Y=util.findFreeGrid(game.player.x,game.player.y,5,true,{[A]=true})`、`game.zone:addEntity(game.level,M,"actor",X,Y)`，然后悬停并打开观察详情，查看 1–2 条技能说明。不要攻击它。若放置失败，改为查看 uruivellas（恶魔，已在本层）。"""),
"o7a2": ("197", """**场景组 o7a2：沃尔部落（Vor Pride）1 层接续——装备 Ctrl 比较、效果提示、第 2 只兽人观察详情**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，在沃尔部落 1 层（主代理已读档核对；前一会话没有存档，怪物在原位）。o7a 已看过 5 个兽人悬停（高阶兽人刺客大师、兽人士兵、稀有兽人烈焰术士、冰霜兽人龙战士、高阶兽人烈焰术士）和刺客大师的角色面板与 2 条技能，不要重复。
本会话只做：
1. 装备：用「h) 制造物品」或控制台 `makeEntity` 生成 2 件高等级装备（一件武器、一件护甲，兽人主题或随机词缀），鉴定后放入物品栏；用上面的方法打开物品栏，悬停并按住 Ctrl 与已装备物品比较。
2. 观察详情：再选 1 只兽人（orc grand master assassin 以外，例如 orc high cryomancer 或 icy orc wyrmic），用控制台定位后打开角色面板，查看技能页与 1–2 条技能说明。
3. 效果：让 1 只兽人法师对你施放法术（站在其旁边等待几回合，半神模式不会死），然后悬停左上效果图标查看 1 个负面效果提示；若几回合内没有效果，记录后跳过。"""),
"o7b2": ("198", """**场景组 o7b2：天灾之穴（Scourged Pits）1 层接续——Cults 物品、madness 技能**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，在天灾之穴 1 层（主代理已读档核对；前一会话没有存档，之前生成的物品不在背包）。o7b 已看过虚空恐魔、天谴巨龙、虚空蠕虫团的角色面板和 4 条怪物技能，以及疯狂值资源栏，不要重复。上一轮看过天谴龙幼仔。
注意：Cults DLC 包自带 zh_hans.lua，界面文本可能来自 DLC 包而不是插件。每条问题先在 `tome-cults.lua` 中 grep 中文片段；查不到的写「未在本库找到（可能来自 DLC 自带译文）」。
本会话只做：
1. Cults 物品：控制台 `O=game.zone:makeEntityByName(game.level,"object","SPINAL_CAGE")`、`O:identify(true) game.player:addObject(game.player.INVEN_INVEN,O)`；同样生成 ROD_ENTROPY、FANGED_COLLAR（若返回 nil，改用「h) 制造物品」按英文名 Spinal Cage / Rod of Entropy / Fanged Collar 查找）。用上面的方法打开物品栏，悬停 2–3 件，并对其中 1 件按住 Ctrl 比较。
2. madness 技能：控制台依次 `P=game.player`、`P:learnTalentType("demented/madness",true)`、`P:learnTalent(P.T_INSANITY_POOL,true)`，再用调试菜单「k) 玩家升级」勾选「学习技能」(496,506) 后「接受」(440,602)。然后打开技能界面（m 或升级窗口 p），查看 madness 树 1–2 条技能说明，确认疯狂值消耗行。"""),
"o7d2": ("196", """**场景组 o7d2：烟雾宫殿（Palace of Fumes）1 层接续——配件附着行、首领观察详情、工匠技能**（只做这一张地图）
存档：50 级半神兽人快枪手 player，在烟雾宫殿 1 层。o7d 已看过 3 件配件提示（惊人的第二皮肤、沃瑞钽火箭靴、沃瑞钽电力反击装置）和议员托马克的地图提示，不要重复。
**先运行 `testers/o7d2/setup.sh`**（主代理实测过，约 1 分钟）：它会用控制台重新生成这 3 件配件，生成并穿上一件沃瑞钽锁甲，把「惊人的第二皮肤」附着到锁甲上，并把议员托马克放到玩家附近；最后打印 game.log 中的 O7D2 行（O7D2T 为附着结果，O7D2M/O7D2S 为托马克的格子与屏幕坐标，屏幕坐标加 32 为格子中心）。M 是托马克，A 是锁甲。
本会话只做：
1. 配件附着行：打开物品栏，悬停身体栏的沃瑞钽锁甲，查看提示中的配件行（裁切右侧提示框）。
2. 首领观察详情：用上面的角色面板命令打开托马克（M）的面板，查看技能页与 1–2 条技能说明。不要攻击它。
3. 工匠技能：技能界面中 1–2 条配件/工匠类技能说明（角色已学全部可学技能）。"""),
"o7d3": ("199", """**场景组 o7d3：烟雾宫殿（Palace of Fumes）1 层接续——首领观察详情、工匠技能**（只做这一张地图）
存档：50 级半神兽人快枪手 player，在烟雾宫殿 1 层。o7d/o7d2 已看过 3 件配件提示、锁甲上的配件附着行和议员托马克的地图提示，不要重复。
**先运行 `testers/o7d3/setup.sh`**（约 1 分钟；它会生成配件和锁甲，并把议员托马克放到玩家附近，打印 O7D3 行）。M 是托马克。
本会话只做：
1. 首领观察详情：用上面的角色面板命令打开托马克（M）的面板，查看技能页（裁切技能列表）与 1–2 条技能说明（悬停技能名后裁切提示框）。不要攻击它。
2. 工匠技能：按 `p` 打开升级窗口（若无反应先运行 focus.sh），悬停 1–2 条配件/工匠类或蒸汽类技能，裁切提示框查看说明。
**全屏额度只有 3 张，前两批都因准备阶段读整屏图而停止。** 找坐标时优先用前后两张截图的差分 bbox 自动裁切（PIL ImageChops.difference(...).getbbox()），不要读整屏图。"""),
"o7d": ("194", """**场景组 o7d：Embers of Rage——烟雾宫殿（Palace of Fumes）1 层：配件（tinker）与首领**（只做这一张地图）
存档：50 级半神兽人快枪手 player（o6b4 留下、o6b5 已成功读档的存档），在烟雾宫殿 1 层。物品栏已有金枪、飞行背包（上一轮已看，不要重复），以及配件「便携式自动材料提取仪」「洞穴炸弹」（已看过）。上一轮还看过 9 个怪物和 5 个技能。
本会话只做：
1. 配件（tinker）：用「h) 制造物品」生成 2–3 件不同类别的配件（治疗类、机械类、电力类，例如 Life Support Suit、Steam Powered Armour、Stormcutter 或列表中其他配件），悬停查看；再把一件配件附着到已装备物品上（物品栏中对配件使用「附着」），查看装备提示中的配件行。
2. 工匠技能：技能界面中查看 1–2 条配件/工匠类技能说明（如果角色已学）。
3. 首领：本层不是首领层。控制台依次执行 `M=game.zone:makeEntityByName(game.level,"actor","COUNCIL2")`、`A=engine.Map.ACTOR`、`X,Y=util.findFreeGrid(game.player.x,game.player.y,5,true,{[A]=true})`、`game.zone:addEntity(game.level,M,"actor",X,Y)`，放出议员 Tormak，悬停并打开观察详情，查看 1–2 条技能说明。不要攻击它。放置失败就记录原因，改看本层精英。"""),
}
SCOPES = {k:v for k,v in SCOPES_ALL.items() if k in __import__('sys').argv[1:]}
tmpl = open('/home/paseo/tome-live/prompts/common.md', encoding='utf-8').read()
for name,(disp,scope) in SCOPES.items():
    s = tmpl.replace('{BUILD}','0.3.12 公开发布版，sha256 22706f10…').replace('{SCOPE}', (scope+"\n"+EXTRA).strip())
    s = s.replace('{NAME}',name).replace('{DISP}',disp)
    assert not re.findall(r'\{[A-Z]+\}', s), name
    open(f'/home/paseo/tome-live/prompts/run-20261113-opus/{name}.md','w',encoding='utf-8').write(s)
    print(name, len(s.encode()))
