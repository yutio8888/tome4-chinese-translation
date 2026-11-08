# 汉化插件代码修复（执行者规格，2026-11-08）

你是本任务唯一的写入者。工作目录：插件仓库 `/workspace/tome4-chn-mod`（ToME4 1.7.6 简体中文汉化插件，即发布仓库）。**只修改本规格列出的插件代码与新增文件；不要改 `data/locales/zh_hans.lua`（由工具生成）；不要 git add/commit/push；不要动 `/workspace/tome4-chinese-translation`。**

依据：分析报告 `/workspace/tome4-chinese-translation/evidence/quality/live-test-20261104/addon-code-issues-analysis-20261108.md`（请先完整阅读；行号以固定源码 `git -C /workspace/t-engine4 show 624a67329fe2:game/...` 为准；DLC 源码 `/workspace/tome4-dlcs/`，来源未固定）。先读插件现有的 `init.lua`、`hooks/load.lua`、`superload/`、`overload/` 了解写法（superload 文件以 `local _M = loadPrevious(...)` 开头、`return _M` 结尾）。动手前对每一项再核对一次固定源码，报告里的行号或推断有误时以源码为准并在报告中说明。

## 用户裁决（2026-11-08）
- L（物品属性行「+7% 所有」）：方案 A —— 只在物品属性描述（`getTextualDesc` 的 7 个属性行）里把 `all` 显示为「全部」，**不改全局 `all` 译文**。
- F（装备人偶标签）：**只显示简称**（保持材质简称，不改成完整物品名），只把关键词分隔符改为中文「、」。

## 实施范围（分析报告第 1–3 组；不做 I 折行、不做 Steam: 与 Ashes 种族列表）
0. 基础设施：新建插件自有补充词条文件 `data/chn_supplement.lua`（格式仿 `data/null_translation.lua` 的 locale 头与 `t(...)` 写法），在 `hooks/load.lua` 中像 null_translation 一样 `I18N:loadLocale("/data-chn-mod/chn_supplement.lua")`。**新增键必须独有**（例如 `"Active##use_talents"`、`"all##item_property"`）或用独有 tag，避免写进 `"nil"` 兜底表覆盖其他 tag 的已有译文；对自然英文句子（如 "Once freed, twice shy."、自动探索中断原因）先确认固定源码与三个 DLC 里没有同字面量的其他用法再加。需要 `ToME:load` 回调的修补都集中在 `hooks/load.lua` 的一个回调里。
1. B 商店标题：`superload/mod/class/Store.lua` 包装 `interact`，`name or _t(self.name, "entity name")`。
2. D 裸 emote：`superload/mod/class/NPC.lua` 包装 `doEmote`，字符串先 `_t`。
3. K 疯狂值 `%%`：`ToME:load` 中为缺少 `CharacterSheet.status_text` 的资源补一个 `(st(a)):format()` 版本（先判断资源存在）。
4. 成就分类：superload `engine/dialogs/ShowAchievements.lua` 包装 `generateList`，对 category 做 `_t`。
5. 立绘名牌：superload `mod/dialogs/Chat.lua` 包装 `getActorPortrait`，用 `_t(name, "entity name")` 或 `src:getName()`。
6. A locked_desc：`ToME:load` 中包装 class/subclass 的函数型 `locked_desc`（防重复包装），补充词条加 "Once freed, twice shy." → 「一朝获释，再难轻信。」（tag `_t`）。
7. 自动探索中断原因：superload `engine/interface/PlayerRun.lua` 包装 `runStop`，msg 做 `_t`；补充词条加 `runCheck` 返回的全部原因（逐条查源码，给出自然中文）。
8. 快捷栏翻页弹窗等裸字面量弹窗：在 `hooks/load.lua` 包装 `engine.ui.Dialog.simpleLongPopup`/`simplePopup`（仿现有 listPopup 包装），标题和正文 `_t`；补充词条加 `Player.lua` 翻页教学的标题与正文（译文自然、保留颜色码与换行）。
9. 按键绑定分组标题：superload `engine/dialogs/KeyBinder.lua` 包装 `generateList`，组名 `_t(group:capitalize())`；若中文下出现重复的「移动」组，合并同名组。缺的组名加补充词条。
10. 战役名：补充词条加 `"Orcs"` 等存档描述用到但缺失的 world 名（tag `birth descriptor name`；先确认无其他 `_t"Orcs"` 用法；译名查 `/workspace/tome4-chinese-translation/mod-tome.lua` 与 `tome-orcs.lua` 现有战役名，Orcs 战役＝「余烬怒火」）。
11. E 盾牌逗号：superload `mod/class/Object.lua` 包装 `getName`，在调用期间临时用 `_t(add_name, "entity add_name")` 替换 `self.add_name`（pcall 保护并恢复原值，不写存档）；补充词条加 `" (#ARMOR#, #SHIELD#)"` → `" (#ARMOR#，#SHIELD#)"`。
12. J 装备组：superload `mod/dialogs/CharacterSheet.lua` 包装 `init`：内部枚举保持英文 "main"/"off"，显示和日志用 `_t(...)`，修掉 `self.equip_set` 初值存中文导致的切换失效。
13. L 物品「所有」：同一 `superload/mod/class/Object.lua` 包装 `getTextualDesc`，调用期间拦截 `_t("all")`（tag 为 nil 或 "_t"）返回 `_t("all##item_property")`（补充词条译「全部」），pcall 保护并恢复全局 `_t`。
14. G/H/H.Key UseTalents：superload `mod/dialogs/UseTalents.lua` 包装 `init`，调用期间拦截 `TreeList.new` 的 columns（按列 name 匹配，匹配不到就不改）：状态列 Active→`_t("Active##use_talents")`（「可用」）；快捷键列 `H.Key %d`→「快捷键 %d」；鼠标列 `_t"LeftClick"`/`_t"MiddleClick"`→「左键」「中键」。
15. C 开局日志：superload `mod/class/Party.lua` 包装 `setPlayer`，`not game.state` 时临时静默 `game.logPlayer`（pcall 后恢复）。
16. F 人偶标签：superload `mod/class/Object.lua` 重写/包装 `getShortName`，仅把关键词分隔符 `", "` 改为 `_t(", ", "short_name sep")`（补充词条 →「、」），取名策略不变。

## 通用要求
- 每个包装都要：存在性检查（目标函数/对象不存在时直接返回原行为）、英文 locale 下行为不变、不写入存档字段（临时替换必须用 pcall 并恢复）、不重复包装。
- 同一个 superload 文件里的多个包装（Object.lua 的 getName/getTextualDesc/getShortName）合并在一个文件。
- 代码风格与现有插件文件一致（缩进 4 空格、注释简短说明为什么）。每个新 superload 文件顶部保留与现有文件一致的 GPL 头（照抄现有文件的头）。
- 自检：对每个新增/修改的 Lua 文件运行 `luajit -bl <file> > /dev/null`（语法检查）；补充词条文件用 `luajit -e 'function t() end; function locale() end; function setFlag() end; dofile("data/chn_supplement.lua")'` 之类方式确认可加载（按文件头实际用到的函数补桩）。若插件有 `tests/` 下可运行的测试，照现有方式运行。
- 不确定、或需要游戏内确认的点写进报告，不要猜。

## 交付
- 写 `/tmp/addonfix/report.md`：逐项（0–16）列出：改了哪些文件/函数、核对到的源码依据、与分析报告不一致之处、需要实机验证的具体操作（界面路径＋期望显示）。
- 写 `/tmp/addonfix/verify-checklist.md`：给实机测试员用的验证清单（每项：怎么进到该界面、期望看到的中文、英文/旧现象作为对照）。
- 最终回复只写一行：`EXECUTOR addonfix DONE files=<改动文件数>`。
