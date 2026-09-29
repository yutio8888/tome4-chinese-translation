已按照授权完成 `evidence/translation-audit/all-modified-review-20260922/batches/batch-001.md` 全部 40 条冻结译文的只读全量复核。复核严格基于固定版本公开源码（Commit: `624a67329fe2ad440c5b344785a9c73fcf22ae63`）、同 section 译文上下文及术语快照，逐条核验如下：

---

### entry-00001
- **结论**：未发现问题
- **可核验依据**：位于 `.always_merge`。术语快照明确规定 `exploratory farportal` 推荐译名为「探索用远行传送门」（用于夏·图尔堡垒前往随机探索区域的远行传送门，与普通 farportal 区分）。译文与术语库完全一致，无语法与格式问题。

---

### entry-00002
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Birther.lua:134`（角色创建界面的按键提示说明 `self.c_tut`）。`#00FF00#` 与 `#FFFFFF#` 颜色标记闭合完整，末尾两个换行符与原文一致；操作指令（选择、确定、返回）与对应按键/点击动作准确对应。

---

### entry-00003
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Birther.lua:197`。角色死亡时读取存档弹窗（`Character dead`）提供两个按钮选项：`_t"Recreate"` 与 `_t"New character"`。译为「重建同一角色」精准传达了基于原角色配置重新生成的机制意图，与“创建新角色”形成明确区分。

---

### entry-00004
- **结论**：存在疑点
- **可核验依据**：
  1. **代码调用失效**：在固定版本引擎公开源码 `game/engines/default/engine/Chat.lua` 中，该日志调用已在 commit `a4c226dfaa`（2021-05-05）被移除（原为 `walk_chain` 中的内部调试日志 `game.log("following chain...")`），当前固定版本中已无活跃调用点，属于历史遗留残留条目。
  2. **术语/语意偏差**：原文上下文为遍历对话树节点中的条件链（condition chain），`chain` 为链路/链条；译文译为「追踪链接…」，将数据结构上的“链”误译为了网络或引用“链接”（link）。建议交由 Sol 交叉核验。

---

### entry-00005
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/HotkeysIconsDisplay.lua:418`。用于快捷键栏未识别条目时的占位文本（`else text = _t"Unknown!" end`）。术语 unknown 对应「未知」，感叹号与原文一致，未发现问题。

---

### entry-00006
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Module.lua:638`。在 Beta 版本启动且检测到插件时弹窗提示 `Beta Addons Disabled`。译文准确表述了纯原版测试环境及自动禁用插件，末尾颜色标记 `#GREY#` 及换行与后续插件列表拼接逻辑完全匹配。

---

### entry-00007
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Module.lua:638`。作为接在 entry-00006 禁用插件列表之后的补充说明。格式标签 `#{italic}##PINK#...#{normal}#` 配对完整，语义忠实传达开发者模式下仍可测试插件的机制。

---

### entry-00008
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Module.lua:723`。模块信息展示全服统计数据（`("Total playtime of all registered players:%s\n"):tformat(ffdata.total_time)`）。占位符 `%s` 匹配，末尾单换行符与格式字符串完全一致。

---

### entry-00009
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Module.lua:1159`。模块校验未通过时向游戏日志输出警告（`game.log("#LIGHT_RED#Online profile disabled(switching to offline profile) due to %s.", hash_err or "???")`）。颜色代码 `#LIGHT_RED#` 匹配，占位符 `%s` 匹配，因果语序表达自然。

---

### entry-00010
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/PlayerProfile.lua:795, 810, 824, 839`。校验模块/插件哈希时未登录在线账户返回的错误描述（`if not self.auth then return nil, _t"no online profile active" end`）。译文「未开启在线账户」准确达意。

---

### entry-00011
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Trap.lua:105`。拆除陷阱失败时的日志输出（`game.logSeen(who, "%s fails to disarm a trap (%s).", who:getName():capitalize(), self:getName())`）。两个 `%s` 占位符顺序与角色名、陷阱名匹配，括号保留完整。

---

### entry-00012
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Trap.lua:108`。成功拆除陷阱时的日志输出（`game.logSeen(who, "%s disarms a trap (%s).", who:getName():capitalize(), self:getName())`）。两个 `%s` 占位符及括号格式完全匹配。

---

### entry-00013
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/Trap.lua:130`。触发陷阱时的日志输出（`game.logSeen(who, "%s triggers a trap (%s)!", who:getName():capitalize(), self:getName())`）。两个 `%s` 占位符顺序、括号及感叹号均匹配。

---

### entry-00014
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/UserChat.lua:247-255`。捐赠感谢弹窗。占位符 `%0.2f`（捐款金额）、`%d`（沃瑞钽币数量）、`%d`（仓库槽位数量）类型与顺序完全匹配；颜色与字体标签 `#{bold}#...#{normal}#`、`#LIGHT_GREEN#...#WHITE#`、`#ROYAL_BLUE#...#WHITE#`、`#TEAL#...#WHITE#`、`#{italic}#...#GOLD#...#{normal}#` 完全闭合；术语 `voratun` 对应「沃瑞钽」，段落换行与原文一致。

---

### entry-00015
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/UserChat.lua:476, 499`。查询玩家信息时弹出的等待窗口标题（`Dialog:simpleWaiter(_t"Requesting...", ...)`）。省略号使用标准中文省略号，未发现问题。

---

### entry-00016
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/UserChat.lua:476, 499`。等待窗口正文提示文本。语义准确，标点对应。

---

### entry-00017
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/UserChat.lua:486`。服务器未返回该玩家数据时的报错弹窗（`Dialog:simplePopup(_t"Error", _t"The server does not know about this player.")`）。语义通顺准确。

---

### entry-00018
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ChatFilter.lua:36`。聊天频道过滤设置项（`kind = "achievement_first"`）。括号与语义完整对应。

---

### entry-00019
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ChatFilter.lua:37`。聊天频道过滤设置项（`kind = "achievement_huge"`）。语义通顺，格式一致。

---

### entry-00020
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ChatIgnores.lua:42`。屏蔽列表顶部的操作说明文字。译文「点击一个用户以停止屏蔽他/她的消息。」忠实传达 UI 操作。

---

### entry-00021
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/DisplayResolution.lua:77`。分辨率更改需要重启游戏时的弹窗提问（`("Continue? %s"):tformat(...)`）。占位符 `%s` 匹配，后接 entry-00022。

---

### entry-00022
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/DisplayResolution.lua:77`。作为 entry-00021 的格式化参数（非创建角色时追加 `_t" (progress will be saved)"`）。前置空格准确保留，拼接后排版正常。

---

### entry-00023
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/GetQuantity.lua:59`。未输入数量点击确认时的错误弹窗正文。语义准确。

---

### entry-00024
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/GetQuantitySlider.lua:59`。滑动条数量输入界面的空值校验报错。语义准确。

---

### entry-00025
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/GetText.lua:67`。文本长度超出范围时的报错提示（`("Must be between %i and %i characters."):tformat(self.min, self.max)`）。两个 `%i` 占位符顺序与类型匹配。

---

### entry-00026
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/KeyBinder.lua:82`。绑定按键对话框标题（`("      Press a key (escape to cancel, backspace to remove) for: %s"):tformat(tostring(t.name))`）。前置 6 个空格严格保留以匹配 UI 缩进对齐，`%s` 占位符匹配。

---

### entry-00027
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/KeyBinder.lua:135`。手势绑定对话框标题。`%s` 占位符匹配，操作说明清晰准确。

---

### entry-00028
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowAchievements.lua:121`。成就详情展示文本（参数依次为达成时间、达成者、共享信息、描述）。4 个 `%s` 占位符、`#GOLD#...#LAST#` 颜色标记及各行换行符完全匹配。

---

### entry-00029
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowAchievements.lua:123`。成就进度前缀（`desc:add(true, true, {"color","GOLD"}, _t"Progress: ", {"color","LAST"})`）。后置单空格准确保留，保证与后续进度数字正确拼接。

---

### entry-00030
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowErrorStack.lua:70`。错误报告弹窗的说明文本。句意通顺完整，括号保留。

---

### entry-00031
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowErrorStack.lua:72`。已向服务器上报过该错误时的提示。`#LIGHT_GREEN#already reported#WHITE#` 颜色标记与括号完全匹配。

---

### entry-00032
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowErrorStack.lua:135`。日志文件保存路径展示与点击复制提示。颜色标记 `#LIGHT_BLUE#` 与占位符 `%s` 匹配，语义准确。

---

### entry-00033
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/ShowErrorStack.lua:178`。错误上报完成时的日志消息（`game.log("#YELLOW#Error report sent, thank you.")`）。颜色代码 `#YELLOW#` 匹配，未发现问题。

---

### entry-00034
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/SteamOptions.lua:86`。清理 Steam 云存档设置项的详细说明（英文原文包含笔误 `cloud cloud`，译文合理规避）。末尾闭合标签 `#WHITE#` 及单换行符完全匹配。

---

### entry-00035
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/UseTalents.lua:37`。使用技能界面的快捷键绑定指引。末尾两个换行符与多行字符串完全匹配，操作逻辑翻译清晰。

---

### entry-00036
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/UserInfo.lua:35`。用户信息界面的「正在玩： 」属性标签（`str:add({"color","ANTIQUE_WHITE"}, _t"Currently playing: ", ...)`）。后置单空格准确保留。

---

### entry-00037
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/UserInfo.lua:42`。用户信息界面的「认证状态： 」属性标签。后置单空格准确保留，保证与后续校验结果文字连接正常。

---

### entry-00038
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/VideoOptions.lua:152`。高级着色器选项的说明文本。换行结构（首行功能 + 选项说明紧随性能影响 + 空行 + 重启提示）完全一致，`#LIGHT_RED#...#WHITE#` 颜色标记闭合无误。

---

### entry-00039
- **结论**：存在疑点
- **可核验依据**：
  1. **标点符号错误**：首行末尾使用了中文逗号「，」而非句号「。」（对照 entry-00038 与 entry-00040 首行均为句号结束）。
  2. **遗漏标点**：第二行末尾「（例如会造成视觉扭曲的法术）」后遗漏了句号。
  3. **非预期硬换行导致排版断裂**：原文第二句 `Disabling it can improve performance.` 紧随第一段同一行内（换行总数为 3）；译文在「（例如会造成视觉扭曲的法术）」后多了一次硬回车换行（换行数变为 4），将「关闭它可以提升运行速度。」单独拆行，与同组其他两个着色器选项（entry-00038、entry-00040）的段落排版格式产生不一致。建议交由 Sol 交叉核验。

---

### entry-00040
- **结论**：未发现问题
- **可核验依据**：源码位于 `game/engines/default/engine/dialogs/VideoOptions.lua:170`。体积着色器选项说明（原文笔误 `volumetricion` 对应体积特效）。排版结构与 entry-00038 一致，颜色标记 `#LIGHT_RED#...#WHITE#` 匹配，换行与句意准确完整。

---

### 疑点汇总（移交 Sol 交叉核验）
1. **entry-00004**（`engine.lua:366`）：源码调用点已在 commit `a4c226dfaa` 移除（已无活跃调用），且「追踪链接…」存在将条件链（chain）误作网络链接（link）的疑点。
2. **entry-00039**（`engine.lua:999`）：首行逗号错误、次行遗漏句号、中间多出一处硬换行导致与同组选项排版格式不一致。
