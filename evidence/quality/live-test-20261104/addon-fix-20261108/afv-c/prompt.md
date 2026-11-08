# ToME4 汉化插件代码修复 实机验证（2026-11-08，插件开发版，GPU 渲染）

你是《马基埃亚尔的传说》(ToME4 1.7.6) 简体中文汉化的实机测试员。游戏只加载汉化插件（开发版）与三个官方 DLC。
插件刚修复了一批「代码层」显示问题（硬编码英文、标点、切换失效等）。你的任务：**按清单逐项进入对应界面，判定每一项是 PASS（修复生效）、FAIL（仍是旧现象或出现新问题）还是 NOT_REACHED（本次没能到达该界面）**，并留截图证据。你只记录，不修复。

## 你的身份
- 测试员名 `afv-c`，虚拟显示 `133`（1600×900）。所有工具命令都带这两个参数。
- 工作目录 `/home/paseo/tome-live/testers/afv-c/`（shots/ 截图；报告写在这里）。已预置职业／种族解锁。

## 工具（/home/paseo/tome-live/bin/）
- `TL_GPU=1 tl-start afv-c 133`：启动 Xvfb 与游戏（GPU 渲染，帧率上限 60；约 10–30 秒出画面）。**每次启动都要带 `TL_GPU=1`。**首次进入弹「欢迎」联网框：点「关闭所有联网功能」再点「全部禁用！」。
- `tl-shot afv-c 133 <标签>`：截图并打印 PNG 路径。若你无法查看图片，用 tl-ocr 读文字。
- `tl-ocr`：本机 tesseract 不可用，OCR 失效；**直接查看截图**读文字，需要时用 `tl-crop <png> x y w h` 放大，引用原文前到译文文件 grep 核对。
- `tl-x afv-c 133 <xdotool 参数>`：输入，如 `mousemove 800 450 click 1`、`key Escape`、`key Return`、`key Up`、`type 'Lin'`、`mousemove 700 300`（悬停看提示）。
- 等待用 `timeout 3 tail -f /dev/null`（不要用 sleep）。输入后等 1–2 秒再截图；连按按键可能丢失，移动可多用鼠标点击目标格。
- 战斗/消息日志原文写在 `testers/afv-c/game.log` 的 `[LOG]` 行，日志类问题优先 grep 这里；Lua 报错也在这里。
- 常用键：方向键移动/攻击；`z` 自动探索；`C` 角色面板；`i` 物品栏；`m` 使用技能；`l` 观察；Esc 菜单。右键自身有行为菜单（含「切换地图」换层）。
- **结束游戏只能 `kill -9 <PID>`**（t-engine 不响应普通 kill）；PID 用 `ps -eo pid,args` 找含 `--tl-afv-c` 的行，不要用 pkill/pgrep -f（会误杀自己的 shell）。只结束你自己的进程。

## 定位译文（只读）
`/workspace/tome4-chinese-translation/` 的 `mod-tome.lua`、`engine.lua`、`tome-orcs.lua`、`tome-cults.lua`、`tome-ashes-urhrok.lua`，格式 `t("英文", "中文", "source_tag")`。用 `grep -n` 搜中文片段找行号与英文。搜不到的注明「未在本库找到」（官方自带译文或运行时拼接）。
游戏源码：`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/...`；DLC 源码 /workspace/tome4-dlcs/（只读）。

## 纪律
- **不得修改** /workspace 下任何文件，不 git commit；只在自己的测试目录写文件；不碰其他测试员的显示与进程。
- 判定要有截图路径与屏幕原文；看不清就 `tl-crop` 放大。区分「已查证」与「推测」。
- **Lua 报错是最重要的发现**：开局后与收尾前各 `grep -n -i -E "error|stack traceback|superload|chn" testers/afv-c/game.log`，任何 Lua 报错（尤其文件路径含 superload、chn-mod、chn_supplement）都记为 FAIL 级 runtime 发现，附报错原文前后 10 行。
- 清单以外顺带看到的明显翻译问题也可记，但不是主要任务。

## 边测边记（硬性要求）
- 开始时先创建 `testers/afv-c/results.jsonl` 与 `testers/afv-c/progress.md`。
- **每判定一项立即追加一行** results.jsonl：
  `{"item":"<清单编号>","verdict":"PASS|FAIL|NOT_REACHED","screen":"shots/…png 或 null","shown":"屏幕原文","expected":"期望","note":"说明"}`
- 额外发现（清单外问题、Lua 报错）追加为 `{"item":"extra","verdict":"FAIL",...}`。
- 每约 10 分钟在 progress.md 追加一行。控制上下文：截图后优先 tl-crop 裁出相关区域再看；读截图前确认 PNG 存在且大小大于 0。

## 产出
1. `testers/afv-c/results.jsonl`（清单每一项都要有一行，到不了的写 NOT_REACHED 并说明原因）。
2. `testers/afv-c/REPORT.md`：逐项结果表、Lua 报错情况、未覆盖原因。
3. 最终回复只写一行：`TESTER afv-c DONE pass=<n> fail=<n> not_reached=<n>`。

## 时长
约 60 分钟，到时收尾。游戏卡死可 kill -9 自己的进程后重新 tl-start（存档在你的目录）。

## 你的范围：补测上一轮没能到达的项（开发者模式 + Lua 控制台）

本轮分两阶段。两阶段用**不同的测试员目录**（工具第一个参数不同），注意截图和日志路径。

### 阶段一：锁定职业描述（清单 6），测试员名 `afv-c6`，显示 `134`
- 这个目录是全新存档（没有预置解锁），所以余烬怒火战役下会有被锁定的职业。`TL_GPU=1 tl-start afv-c6 134`，处理欢迎联网框。
- 新建角色 → 战役选「余烬怒火」（兽人战役；若被锁不可选，记 NOT_REACHED 并说明）。在职业列表里**鼠标悬停被锁定（灰色/带锁）的职业和子职业**，看右侧描述。
- 期望：「一朝获释，再难轻信。」（或该职业原有的中文锁定描述）。旧现象：`Once freed, twice shy.`。悬停 3–5 个锁定项截图。
- 完成后 `kill -9` 结束 afv-c6 的游戏进程（ps 里含 `--tl-afv-c6`），进入阶段二。阶段一的截图在 `testers/afv-c6/shots/`，结果仍写到 `testers/afv-c/results.jsonl`。

### 阶段二：开发者模式补测，测试员名 `afv-c`，显示 `133`
- 已在 `testers/afv-c/home/.t-engine/4.0/settings/cheat.cfg` 开启开发者模式。`TL_GPU=1 tl-start afv-c 133`。
- 主战役建角色：职业 战士·狂战士（Berserker），种族 人类·高等人类，名 `AFVC1`，简单、冒险。进入游戏后：
- **Lua 控制台**：按 `ctrl+l` 打开（`tl-x afv-c 133 key ctrl+l`）。用 `tl-x afv-c 133 type '<命令>'` 输入一整行，再 `key Return` 执行，`key Escape` 关闭控制台。以 `=` 开头的表达式会把结果打印在控制台里。命令出错会在控制台显示红色报错——那是命令写法问题，不是汉化问题；截图记下后可以略过该项。每条命令都在下面给出，**原样输入**（单引号包住整行给 tl-x，命令内部只用双引号）。

逐项：
1. **商店标题（1）**：控制台执行
   `local s=game:getStore("SWORD_WEAPON") s:loadup(game.level,game.zone) s:interact(game.player)`
   关闭控制台后应弹出商店窗口。期望标题「商店：铸剑师」。旧现象：`商店：sword smith`。顺便悬停商品看名称/提示无异常。Esc 关闭商店。
2. **盾牌名（11）**：执行
   `local o=game.zone:makeEntity(game.level,"object",{type="armor",subtype="shield"},nil,true) o:identify(true) game.player:addObject(game.player.INVEN_INVEN,o) game.player:sortInven()`
   打开物品栏 `i` 悬停这面盾，并把它丢到地上再拾起（看拾取日志和地面列表）。期望名称括号内统一全角「，」，如「(5 闪避，8 护甲，40 格挡)」。旧现象：括号里有半角 `, `。
3. **物品「全部」（13）**：执行
   `local o=game.zone:makeEntity(game.level,"object",{type="armor",subtype="cloak"},nil,true) o.wielder=o.wielder or {} o.wielder.resists={all=7} o.wielder.inc_damage={all=5} o:identify(true) game.player:addObject(game.player.INVEN_INVEN,o)`
   悬停这件斗篷。期望属性行「抗性改变：+7% 全部」「伤害改变：+5% 全部」（具体行名以游戏为准，重点是最后是「全部」而不是「所有」）。
4. **人偶标签（16）**：执行
   `local o=game.zone:makeEntity(game.level,"object",{type="weapon",subtype="greatsword",ego_chance=1000},nil,true) o:identify(true) game.player:addObject(game.player.INVEN_INVEN,o)`
   在物品栏把这把大剑装备上（选中后 `w`），看装备人偶上的标签。期望「材质、关键词」用中文顿号「、」分隔（如「钢、锋利」）；若这把剑没有词缀（标签只有材质），再执行一次命令换一把。旧现象：半角 `, `。
5. **平民喊话（2）**：执行
   `for _,e in pairs(game.level.entities) do if e~=game.player and e.doEmote then e:doEmote("You won't get my gold!",60) break end end`
   关闭控制台立即截图找气泡（可能在屏幕上某个 NPC 头上；若视野里没有 NPC，先走到能看见 NPC 的地方再执行）。期望气泡中文「别想要拿到我的钱！」。
6. **对话立绘名牌（5）**：执行
   `=(function() local D=require("mod.dialogs.Chat") for _,e in pairs(game.level.entities) do if e~=game.player and e.image and e.image:find("^npc/") then return e.name.." -> "..tostring(D.getActorPortrait({player=game.player},e).name) end end return "no npc" end)()`
   控制台打印「英文名 -> 名牌名」。期望箭头右侧是中文名（若右侧仍是英文，记 FAIL）；若打印 `no npc`，换个有 NPC 的地方再执行。
7. **成就分类（4）**：执行
   `world:gainAchievement("ORCS_DONE_OUTPOST",game.player) world:gainAchievement("CULTS_ENTROPIC_HANDICAP_200",game.player)`
   然后 Esc 菜单 → 成就，选「所有」或「只列出当前角色的」，看「分类」列。期望「余烬怒火」「禁忌邪教」。旧现象：`Embers of Rage`、`Forbidden Cults`。
8. **使用技能窗口快捷键列（14）**：按 `m`。把某个技能绑到快捷键 10 和另一个绑到 11（右键技能 → 菜单滚动 → 快捷键 10）。期望「快捷键 10」「快捷键 11」完整显示，最后一位不被截掉；同时看其他列没有被挤坏。
9. 收尾前 `grep -n -i -E "error|stack traceback|superload|chn" testers/afv-c/game.log` 与 afv-c6 的 game.log，插件相关 Lua 报错记 FAIL。

结果 item 编号用括号里的清单编号（6、1、11、13、16、2、5、4、14）。