# o8a REPORT — 巅峰(1) 首领埃兰达/艾格尼尔（2026-11-13，Opus，v0.3.12 公开包）

## 范围与方法
- boot.sh 读档（区域裁切确认「巅峰 (1)」），setup.sh 控制台放置 ELANDAR(8,71)/ARGONIEL(9,71)；角色面板经 con.sh 调用 CharacterSheet.new(M) 打开（均 debug-ui，记于 debug-actions.md）。未攻击首领，未弹出剧情对话。
- 证据分类：全部为 debug-ui；无 natural；控制台仅用于放置/打印 type，不作显示证据。

## 覆盖
- 埃兰达：常规页（全屏 1 张定位）、攻击页、防御页、技能页悬停 3 条（石化皮肤、暗影圣诗、时间加速）—— 全部 ok。
- 艾格尼尔（提示中写作「阿尔格尼尔」，本库实际译名「艾格尼尔」，mod-tome.lua:37994/38663，与匕首/日记等一致）：地图悬停、角色面板技能页、技能悬停 2 条（无尽灾厄、毁伤）—— 全部 ok。
- 对象统计：monster 1（ok 1）；talent 5（ok 5）；other/界面页 3（ok 3）；异常 0；未到达 0。

## 核对后未报（非翻译问题）
- 常规页「类型:」「子类:」值为空：上游 CharacterSheet.lua:619/622 对有 descriptorDisplayName 方法的 Actor 走该分支，NPC 无 descriptor 返回 nil→""，英文同样为空（E1 type=humanoid/shalore）。
- 防御页「伤害亲和:」「被击中后反击伤害:」标题下为空：源码对无数据也绘制标题，属正常。
- 无尽灾厄末行「（冷却时间）」：对应上游 "(Cooldowns)" 后接冷却列表，NPC 列表为空，译文忠实。
- 悬停中的 UID/invis.png/room_map 为作弊模式调试信息。
- game.log 中 talents "attempt to index local 'self'" 为启动期技能定义检查记录，非界面操作触发，无插件相关 Lua 报错。

## 统计
- findings 0。读图 13 张（全屏 1），图片累计 2.61 MB；工具调用代理计数 ≈30/100（不等于 HTTP 请求数）。
- 预算浪费：1 张悬停裁切未框中提示框（063501-e1stone-c.png），随后从同一全屏原图重裁，未额外截图。
- 停止原因：done（本场景组全部完成）。
- 未覆盖：艾格尼尔的攻击/防御页（不在本会话范围）；首领实战技能日志（禁止攻击）。
