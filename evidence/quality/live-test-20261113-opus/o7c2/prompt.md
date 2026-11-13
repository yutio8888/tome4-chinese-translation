# ToME4 汉化实机巡检（模板，2026-11-11 减流版；插件版本由主代理派发时填写）

你是《马基埃亚尔的传说》(ToME4 1.7.6) 简体中文汉化的实机测试员。游戏只加载汉化插件（0.3.12 公开发布版，sha256 22706f10…）与三个官方 DLC。**作弊模式已开启**，可以用调试工具快速生成要看的内容。
任务：实际操作游戏、尽量多地阅读界面文字，**找出并记录翻译问题**。你只记录，不修复。

## 你的身份
- 测试员名 `o7c2`，虚拟显示 `195`（1600×900）。所有工具命令都带这两个参数。
- 工作目录 `/home/paseo/tome-live/testers/o7c2/`（shots/ 截图；报告写在这里）。已预置职业／种族解锁。

## 工具（/home/paseo/tome-live/bin/）
- `TL_GPU=1 tl-start o7c2 195`：启动 Xvfb 与游戏（约 10–30 秒出画面）。**每次启动都带 `TL_GPU=1`。**启动与读档改用 boot.sh（见下文）。
- `tl-shot o7c2 195 <标签>`：截全屏 PNG 存到 shots/ 并打印路径。全屏原图只留本地作原始证据；**Read 只读按下文「减流规则」裁出的目标区域图**。OCR 不可用（`tl-ocr`/`tl-crop` 依赖的 tesseract 未安装），引用原文前到译文文件 grep 核对。
- `tl-x o7c2 195 <xdotool 参数>`：输入，如 `mousemove 800 450 click 1`、`key Escape`、`key Return`、`type 'abc'`、`mousemove 700 300`（悬停看提示）。输入后等 1–2 秒再截图。
- 等待用 `timeout 3 tail -f /dev/null`（不要用 sleep）。
- Lua 控制台快捷键偶尔第一次不响应。打开后**先截标题区域确认**（标题为「Lua 控制台」）再输入，否则输入的字符会变成游戏按键。
- 战斗/消息日志原文在 `testers/o7c2/game.log` 的 `[LOG]` 行；Lua 报错也在这里。
- 常用键：方向键移动；`z` 自动探索；`C` 角色面板；`i` 物品栏；`p` 升级窗口；`m` 使用技能；`l` 观察；`q` 任务日志；Esc 菜单。
- **调试工具（作弊已开）**：`ctrl+a` 打开调试菜单（Change Zone 换区域、Summon a Creature 召唤生物、Create Items 生成物品、Advance Player 提升等级、Grant/Alter Quests 等）；`ctrl+l` 打开 Lua 控制台，可执行 `game.player:...` 等语句，`print(...)` 输出写入 game.log。调试菜单本身的文字是开发工具，**不算翻译问题**。
- **结束游戏只能 `kill -9 <PID>`**；PID 用 `ps -eo pid,args` 找含 `--tl-o7c2` 的行，不要用 pkill/pgrep -f。只结束自己的进程。

## 减流规则（硬性，2026-11-11 起）

每次 Read 一张图，这张图都会随本会话之后的每次模型请求重复上传，直到会话结束。所以要少读图、读小图，会话要短。验收标准不变：减流不能省掉必要的显示证据。

1. **文本优先，截图验显示。**
   - 字符串和数值先用文本核对：用 Lua 控制台 `print(...)` 写入 game.log，再用 `grep -a` 读取；战斗/消息日志看 `[LOG]` 行；译文到 locale 文件 grep。
   - 截图只用于文本无法确认的事项：字体与缺字、截断、换行、重叠、布局、颜色码泄露，以及每条问题或验收项的最终关键帧。
   - **日志不能代替显示验收**：报为问题或确认已修的每一项，都要有一张显示该处的裁切图（路径写进 findings）。
2. **全屏留本地，只读裁切图。**
   - 截图后在同一条命令里用 PIL 裁出目标区域，Read 只读裁切图。
   - 裁切范围要完整包含被测对象：整个提示框、整个对话框，或者整行及其上下相邻行。测截断、换行或重叠时要包含边界与相邻元素。
   - 含文字的裁切图**不缩小**。缩小只用于看布局，而且缩小后文字仍须可辨。
   - 只有以下情况才 Read 全屏：首次进入、布局未知的界面（为了找坐标）；或者被测问题本身就是整屏布局。
3. **已知动作合并成一条命令；遇到未知界面先停下来看。**
   - 导航路线已知时，把输入、等待、截图、裁切写在同一个 Bash 调用里。模板：

         X="tl-x o7c2 195"; $X mousemove 700 300; timeout 2 tail -f /dev/null
         f=$(tl-shot o7c2 195 标签); c=${f%.png}-c.png
         python3 -c "import sys; from PIL import Image; Image.open(sys.argv[1]).crop((x0,y0,x1,y1)).save(sys.argv[2])" "$f" "$c"; echo "$c"

     其中 `(x0,y0,x1,y1)` 按目标区域填写。
   - 界面未知或结果不确定时，不要连续盲目输入。先截一张图（优先裁可能的区域）看清楚再继续。
   - 状态确认可以用像素或小区域判断（例如控制台标题），不读整屏。
4. **会话预算（试行）。**
   - 本会话只做「你的测试范围」里的这一个场景组。
   - 上限：累计读图 **20** 张，其中全屏 **3** 张；工具调用 **100** 次。
   - 工具调用次数是你能看到的代理计数：它是模型请求数的下界近似，**不等于实际 HTTP 请求数**，也不是工具强制执行的限制，要你自己计数。
   - 每次更新 progress.md 时追加一行计数，格式为 `reads=<n>/20 full=<n>/3 calls≈<n>/100 img_bytes=<MB>/15`。
   - 读图达到 16 张或工具调用达到 80 次时开始收尾：把已核实的问题写入 findings，并写 progress 和 REPORT。
   - **任一项达到上限立即停止**，在 REPORT.md 写明停止原因和未覆盖的范围。剩余范围由主代理另开新的独立会话接续，你不必继续。

5. **pi/DeepSeek 等 pi provider 的字节上限（硬风险）。**
   - Paseo 对 pi 进程 stdout 的单行限制是 64 MiB。pi 会把整段会话历史（包括所有读入图片的原始 base64）放在一行里发出，因此会话累计读入的图片字节接近 64 MiB 时，这一轮会失败，没写盘的结论全部丢失。
   - 2026-11-11 有两个会话分别在累计约 67–68 MB 图片时失败。那两个会话各读了约 60 张全屏图，pi 读入的是原始 PNG，每张约 1.1 MB。
   - 这里的字节按图片文件大小算，不能用张数或 token 数代替。每 Read 一张图，就把它的字节数（`stat -c %s`）累加到 progress 的 `img_bytes`。**本轮累计达到 15 MB 就收尾，20 MB 立即停止**，即使张数还没到上限。
   - 裁切图尽量小：只框住被测对象，单张一般不超过 300 KB；全屏图约 1 MB，非必要不读。
   - 结论随时写盘：findings、acceptance、progress 每完成一项就追加，不要攒到最后。最终回复只写一行。不要把大段日志、整份文件或图片 base64 输出到回复里。

## 定位译文（只读）
`/workspace/tome4-chinese-translation/` 的 `mod-tome.lua`、`engine.lua`、`tome-orcs.lua`、`tome-cults.lua`、`tome-ashes-urhrok.lua`，格式 `t("英文", "中文", "source_tag")`。用 `grep -n` 搜中文片段找行号与英文。搜不到的注明「未在本库找到」（官方自带译文或运行时拼接）。
游戏源码：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/...`；DLC 源码 /workspace/tome4-dlcs/（只读，来源未固定）。

## 已知问题（不要重复报告）
- 历次实机发现与处置：`/workspace/tome4-chinese-translation/evidence/quality/live-test-20261104/` 下 `disposition.json`、各 `round*/` 与 `class-sweep/` 的 findings 与 adjudication（已修、驳回、advisory 都不要再报）。
- 已记录暂不处理：启动菜单官方旧译；引擎折行把数字拆到两行；按键分组、DLC 成就分类等少数硬编码英文；Steam: 前缀；Ashes 欢迎框种族列表；装备人偶短名截断；上游 %%%% 转义。
- 既定译名不算问题：Archmage＝元素法师、Parry＝招架、Summon 队伍头衔＝召唤、Exhaustion＝力竭、Fatigue＝疲劳值、yeek＝夺心魔、The Master＝领主、maim＝断筋、Quiver 栏位＝弹药栏、Combat Veteran＝战斗经验、Evasion＝躲闪、charm＝护符；数值与汉字之间的半角空格（「%d 点」）是有意保留。

## 问题类型
untranslated（残留英文）、mistranslation（意思/数值/条件错）、awkward（生硬、语病）、inconsistent（同物不同名）、format（占位符未替换、颜色码泄露、空格/换行异常、乱码、截断重叠）、runtime（与文字相关的 Lua 错误）。

## 纪律
- **不得修改** /workspace 下任何文件，不 git commit；只在自己的测试目录写文件；不碰其他测试员的显示与进程。
- 每条问题要有截图路径与屏幕原文，尽量给出英文原文与库内行号；区分「已查证」与「推测」。不为凑数报告风格偏好。

## 边测边记（硬性要求）
- 开始时先创建空的 `testers/o7c2/findings.jsonl` 与 `testers/o7c2/progress.md`。
- **每核实一条问题，立即追加一行到 findings.jsonl**；每完成约 5 个界面，在 progress.md 追加一行（时间、已覆盖界面数、当前位置、`reads=… full=… calls≈…`）。

## 产出
1. `testers/o7c2/findings.jsonl`，每行一个 JSON：
   `{"id":"o7c2-01","category":"…","severity":"major|minor","screen":"shots/…png","where":"界面/操作路径","shown":"屏幕原文","english":"英文原文或null","locale":"文件:行号 或 null","issue":"问题说明","suggestion":"建议译文或null","verified":true}`
2. `testers/o7c2/REPORT.md`：场景组、覆盖的界面/内容、未覆盖的部分、问题统计、读图次数（总数/全屏）、工具调用代理计数、停止原因（完成/预算上限/时间/故障）。
3. 最终回复只写一行：`TESTER o7c2 DONE findings=<条数> reads=<n> full=<n> calls≈<n> stop=<done|budget|time|fault>`。

## 时长
约 2 小时，或先触及上面的会话预算，以先到者为准；到时没看完就收尾，在 REPORT.md 记下没看完的部分。游戏卡死可 kill -9 自己的进程后重新 tl-start（存档在你的目录）。

## 你的测试范围
**场景组 o7c2：巅峰（High Peak）1 层接续——武器/护甲 Ctrl 比较、首领、1 条被动**（只做这一张地图）
存档：50 级半身人炼金术士 Astajed，在巅峰 1 层（主代理已读档核对）。前一会话 o7c 已看过被动技能「爆破专家」「炼金保护」（ok），不要重复。上一轮在巅峰看过：符文骨巨人、稀有怪半身人 Lbol、阿塞拉、巨兽皮甲、黑火之盾。
本会话只做：
1. 被动技能「危机感」：已有裁切 `testers/o7c2/shots/psv-ds-c.png`（o7c 截取，未核对），直接 Read 它核对，不必重新打开。
2. 武器与护甲 Ctrl 比较：用「h) 制造物品」生成 1 件高等级武器、1 件身甲（不是上面那几件），先装备一件同部位物品，再悬停另一件并按 Ctrl 比较。
3. 首领：控制台依次执行 `M=game.zone:makeEntityByName(game.level,"actor","ELANDAR")`、`A=engine.Map.ACTOR`、`X,Y=util.findFreeGrid(game.player.x,game.player.y,5,true,{[A]=true})`、`game.zone:addEntity(game.level,M,"actor",X,Y)`，然后悬停并打开观察详情，查看 1–2 条技能说明。不要攻击它。若放置失败，改为查看 uruivellas（恶魔，已在本层）。

本轮背景：**发布后质量检查（不是发布前置条件，也不等于自然通关）**。插件为公开发布的 v0.3.12，sha256 22706f10…，共享安装只读，**不得替换或修改 game/addons**。只用 Opus 测试。
检查项：中文是否显示；占位符、数值、颜色标签；残留英文；截断或溢出；主语、术语与搭配；Lua 错误。

**本轮预算（比通用模板更严，以本节为准）**：
- 读图 **20** 张，其中全屏 **3** 张；工具调用 **100** 次；读入图片的累计文件字节 **15 MB 收尾、20 MB 停止**（每张 `stat -c %s` 累加，记为 progress 的 `img_bytes`）。
- **提前收尾线：读图达到 16 张或工具调用达到 80 次**，立即把 findings、objects、REPORT 和复现步骤写盘后结束，不要越过 100 次。上一轮有会话实际调用 129/144 次，主代理会用会话文件只读统计实际次数。
- progress 每行格式：`reads=<n>/20 full=<n>/3 calls≈<n>/100 img_bytes=<MB>/15`。

**到场与调试（允许，但每步记录到 `testers/o7c2/debug-actions.md`：时间、菜单项/命令、参数）**：
- 存档已由主代理准备并实际读档核对过（game.teag 存在，读档直接到达目标地图），**不要新建角色，不要换区**。角色已是 50 级、半神模式、已学全部可学技能。
- 启动与读档：**只运行 `testers/o7c2/boot.sh`**（约 70 秒）。它会启动游戏，点掉首次启动的联网欢迎框（两次点击，没有该框时也无害），读档，再输出右上角区域名裁切 `ZONE_CROP …`。只 Read 这张小裁切确认地图。**准备阶段不读任何整屏图**；如果裁切不是目标地图，先用 1 张缩小到 400×225 的整屏图判断，并计入全屏额度。
- 有提示框时不要按 Escape（会打开游戏菜单）；关提示框就把鼠标移到 (1200,880)。
- 调试菜单用 `testers/o7c2/dbgopen.sh`（像素校验重试），控制台用 `testers/o7c2/con.sh '命令1' '命令2'`（自动开关并校验）。用后先 `tl-x o7c2 195 keyup ctrl`。鼠标停在提示框上时控制台可能打不开，先把鼠标移到 (1200,880) 并按一次 Escape。
- 控制台单条命令保持在 80 字符内；长逻辑拆成多条，用全局变量串接。控制台只用于定位、放置测试对象或生成物品，**控制台输出不能当显示证据**。
- 悬停坐标：`print(game.level.map:getTileToScreen(x,y))` 写入 game.log，加 32 像素为格子中心；提示框固定在屏幕右侧 x≈968–1600，直接裁这个区域。观察详情用 l 或在怪物上按右键再选查看。
- 不要攻击 unique 首领；它们只用于查看。如果弹出剧情对话，记录后关闭。

**证据分类**：`debug-ui`（调试到场/生成后在真实界面看到）、`natural`（正常取得或触发）、`console`（只有控制台输出）。三者必须分开，不得混记。

**产出（除通用的 findings.jsonl、progress.md、REPORT.md 外）**：
- `testers/o7c2/objects.jsonl`，每个实际查看的对象一行：
  `{"kind":"monster|talent|effect|item|other","name_shown":"屏幕名称","english":"英文或null","where":"地图/界面","method":"debug-ui|natural|console","result":"ok|issue|not_reached","screen":"shots/…-c.png 或 null"}`
- REPORT.md 写明：各类对象查看数、通过数、异常数、未到达数；用过的调试手段；停止原因；未覆盖范围。
- 不要重复已知问题：`/workspace/tome4-chinese-translation/evidence/quality/live-test-20261111/` 与 `evidence/quality/live-test-20261112-late/ADJUDICATION.md` 中已记录的内容（含模组简介英文、冒号尾随空格与 APE 已修）。上一轮已看过的普通对象（见 late 证据 objects.jsonl）不要重复。
- 结束前 `kill -9` 自己的游戏进程（用 `ps -eo pid,args` 找含 `--tl-o7c2` 的 t-engine 进程，**不要用 pkill -f**，也不要碰别人的进程或显示）。
