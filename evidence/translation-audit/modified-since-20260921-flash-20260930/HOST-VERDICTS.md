# 宿主复核裁决（Gemini 疑点）
| 条目 | 位置 | 裁决 | 说明／建议 |
|---|---|---|---|
| entry-00221 | mod-tome.lua:14681 | confirmed | 错别字「右手带着…之戒」→「戴着」 |
| entry-00063 | mod-tome.lua:2777 | confirmed（二级，措辞） | thanks to 译成动词「感谢」致句子不通；同族 2761–2775 均为「……，通关ToME。」；建议「多亏一名夏·图尔人在最后一刻阻止你开启通往你那疯狂的太阳主上的传送门，得以通关ToME。」 |
| entry-00002 | engine.lua:999 | confirmed（换行，低影响） | 原文第二段为一行，译文多一处硬换行「……法术）。\n关闭它……」；合并为一行 |
| entry-00011 / entry-00019 | engine.lua:1697 / mod-boot.lua:282 | advisory | 原文自身把「禁用网络」与「该选项」混指；译文「关闭后……打开」沿袭原文歧义，未错译。可选改为「如果你关闭了网络功能，之后仍可在游戏设置菜单的在线选项卡中重新开启」，两文件须同步 |
| entry-00107 | mod-tome.lua:6884 | refuted | 2026-09-27 用户裁决（pending-user-review #18）；模板「……而死」已承载 before falling |
| entry-00113 | mod-tome.lua:7049 | refuted | 术语 draining physical＝生命汲取 preferred（combat.tsv:158，注明不写作物理吸收） |
| entry-00114 | mod-tome.lua:7055 | refuted | 同节惯例「属性＋名称」（奥术沉默、奥术法力燃烧）；hrq-00080 已裁决 |
| entry-00126 | mod-tome.lua:8188 | confirmed（二级，语病） | 首句缺介词「乌鲁洛克的吐息中诞生」，漏 himself；建议「由乌鲁洛克亲自吐息赋予形体……」。「她」指女妖（ruin banshee），不算错 |
| entry-00129 | mod-tome.lua:8267 | refuted | 术语 creatures.tsv:24 注明 Eldritch eye 保留音译「艾尔德里奇之眼」 |
| entry-00142 | mod-tome.lua:9195 | refuted | 原文孤立右括号是上游笔误（boss-artifacts-far-east.lua:513 无对应左括号），删去正确 |
| entry-00154 | mod-tome.lua:11597 | confirmed（二级，语病） | yet 转折误作句末「虽然它毫无侵蚀的痕迹。」；改「……很久以前制造的，却毫无侵蚀的痕迹。」 |
| entry-00164 | mod-tome.lua:12276 | confirmed（低影响漏译） | 漏 of Ru'Khan、However/first：改「不过第一次试验并不成功，能量爆炸之后，鲁·克汉只剩下一双烧焦的靴子。」 |
| entry-00190 | mod-tome.lua:12881 | refuted | 实现 world-artifacts.lua 中 `for i = 1, 2` 至多驱散两项；译文贴合实现（上游文本与实现矛盾） |
| entry-00216#1 | mod-tome.lua:14042 | refuted | Conclave 全库 44 处＝孔克雷夫；「长老会」是 Overseers（Opus 交叉 x01） |
| entry-00216#2 | 同上 | confirmed（二级，语病） | 「虽然我们做的一切感到骄傲」→「虽然我为我们在这里所做的一切感到骄傲」 |
| entry-00222#1 | mod-tome.lua:14721 | confirmed（换行不变量） | 「“舞会开始了。”」被拆成独立段落，LF 44→46；并回上一段 |
| entry-00222#4 | 同上 | confirmed（二级） | 同句你/您混用：「您的安全」→「你的安全」 |
| entry-00222#2/#3/#5 | 同上 | advisory | 标题行空格、「回忆」→「回忆录」需全系列同步；「艾伦尼恩先生」多出敬称属风格 |
| elvala 回忆录标题（entry-00222/00223/00224 等 8 章） | mod-tome.lua elvala.lua 各章首行 | confirmed（需 8 章同步） | 「时任……领袖」与正文矛盾（本章时他尚非领袖），memoirs 为回忆录；建议「摘自埃尔瓦拉最高议会领袖艾伦尼恩·加威尔的回忆录」，并去掉多余空格 |
| entry-00223#2–#8 | mod-tome.lua:14813 | confirmed ×7 | dark eyes 漏译；「或许问过许多次」；凭空「微笑」；低吟来源/looking upwards/橙色火焰；specks 主语与「从宇宙俯瞰」增译；gasp for air 改写；「地」「它们」。修正片段见 cross-reports/x02.md |
| entry-00224#2/#4 | mod-tome.lua:14987 | confirmed ×2 | 漏 in his northern city；「小小的谎……一生也无法赔付」改变原意 |
| entry-00224#3、entry-00225#4 | — | refuted | 上游 elvala.lua:36「his twin daughters」，「孪生姐妹」正确且全文一致 |
| entry-00225#1/#3/#5 | mod-tome.lua:15093 | confirmed ×3 | 漏译 What could have caused this?；get my bearings 误译；「非常接近的人」→「无比亲近的人」 |
| entry-00225#2 | 同上 | advisory | divination＝侦查 为本库学派名（驳回改占卜）；仅语序与「仅存」增译可调 |
| entry-00226#1–#3 | mod-tome.lua:15167 | confirmed ×3 | 「躺在的地方」语病；漏 you have returned to us；漏 and his mages |
