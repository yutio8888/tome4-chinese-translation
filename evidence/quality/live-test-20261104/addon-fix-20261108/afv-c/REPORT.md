# afv-c 实机验证报告（开发者模式 + Lua 控制台补测）

- 测试员：afv-c（显示 :133，主战役·开发者模式）、afv-c6（显示 :134，全新 profile，余烬怒火）
- 版本：ToME 1.7.6 + 汉化插件开发版（0.3.8）+ 三个官方 DLC
- 时间：2026-11-08 02:21–03:30
- 角色：AFVC1（人类·高等人类 / 战士·狂战士，简单，冒险模式，马基·埃亚尔：卓越纪）

## 逐项结果

| 项 | 判定 | 关键证据 | 屏幕原文 |
|---|---|---|---|
| 6 锁定职业描述 | PASS | afv-c6 `shots/022714-s1-hover1.png` 等 5 张 | 悬停余烬怒火锁定职业：『一朝获释，再难轻信。』『自然之能可以超越单纯的技艺…』『黑暗的思想、黑色的血液…』『有些人行走于阴影之中…』『强大的精神可以克服肉体的软弱…』（旧现象 `Once freed, twice shy.` 未复现） |
| 1 商店标题 | PASS | `shots/023644-p2-cmd1run.png` | 『商店：铸剑师（最多付款 25.00 金币，你的金币：0.00）』；商品『侵蚀之铁质大剑(15-24 伤害，1 护甲穿透)』 |
| 11 盾牌名 | PASS | `shots/025457-p2-inv4.png`、`030141-p2-inv5.png` | 『铁盾（0 闪避，2 护甲，23.5 格挡）』（列表/提示框/getName() 一致，全角逗号） |
| 13 物品「全部」 | PASS | `shots/030241-p2-cloak.png` | 『抗性改变：+7% 全部』『伤害改变：+5% 全部』 |
| 16 人偶标签 | PASS | `shots/030343-p2-equipped.png`、`030659-p2-doll2.png` | 斗篷标签『亚麻、永恒精灵』（顿号）；另有『铁』『黄铜』 |
| 2 平民喊话 | NOT_REACHED | `shots/031120-p2-emote.png`、`031246-p2-emote2.png` | 执行 doEmote 后视野内无气泡；巨魔沼泽(1) 视野内无 NPC（唯一 npc/* 实体 wolf 在视野外，挪近后仍未渲染气泡） |
| 5 立绘名牌 | FAIL | `shots/030931-p2-portrait.png` | 控制台 `1 := wolf -> wolf`，箭头右侧仍为英文 |
| 4 成就分类 | NOT_REACHED | `shots/031738-p2-ach.png`、`032136-p2-ach2.png` | 窗口全中文，但列表为空（见下） |
| 14 快捷键列 | PASS | `shots/032403-p2-tal2.png`、`032610-p2-bindscroll.png`、`032716-p2-bind11.png` | 『快捷键 10』『快捷键 11』完整显示；绑定时弹『快捷键 11 已绑定』 |

统计：**PASS 6 / FAIL 1 / NOT_REACHED 2**

## 未覆盖原因

- **2（平民喊话）**：本关（巨魔沼泽 1 层）开局视野内没有具名 NPC，`game.level.entities` 里唯一 `npc/*` 实体是 `wolf`，且在视野外。按清单原命令与自写的“先 `e:move(x+2,y)` 挪到身边再 emote”两种写法执行，控制台均无报错，但画面上没有出现气泡，无法取证，故记 NOT_REACHED（不是 FAIL）。首次执行时 shell 吞掉了 `You won't` 的撇号，第二次已确认原文原样传入。
- **4（成就分类）**：`ORCS_DONE_OUTPOST` 这个 id 在 orcs DLC 源码（`tome-orcs/data/achievements/special.lua`）里不存在，首次命令无效；改用真实 id（`ORCS_CIVILIAN_KILLER` + `CULTS_ENTROPIC_HANDICAP_200`）后 `world:gainAchievement` 也未在离线 profile 落库，成就列表仍为空，因此看不到「分类」列内容。窗口框架本身全中文（标题『马基·埃亚尔的传说成就』、筛选『只列出当前角色的／所有已经获得的／所有』、列头『成就／分类／何时／何人』）。
- **11 的“丢到地上再拾起”子步骤未完成**：游戏内 `Shift+d`（丢弃物品）只推进回合并提示『没东西可以丢弃。』（`game.log:3832`），控制台 `dropFloor` 也未留下丢弃日志；盾牌名称本身已在列表、提示框与 `getName()` 三处核验。

## Lua 报错情况

- `grep -n -i -E "error|stack traceback|superload|chn"` 在 `afv-c/game.log`（4300+ 行）与 `afv-c6/game.log`（2798 行）各查两次（开局后、收尾前）：
  - **stack traceback：0 条**
  - **superload / chn-mod / chn_supplement 相关 Lua 报错：0 条**
  - 仅有 12 条 `[aiParseTalent] FAILED TO PARSE tactical table function`（`/data/talents/*.lua`），来自游戏本体天赋数据，英文版同样出现 → advisory，不计 FAIL。
- 控制台命令级报错：本报告两条无效命令（不存在的成就 id、以及被 shell 改写的撇号）属命令写法问题，非汉化问题。

## 清单外观察（advisory）

1. **模块选择界面描述整段英文**（`shots/022956-p2-create.png`）：`Tales of Maj'Eyal: Age of Ascendancy / Welcome to Maj'Eyal…`。可能是模块 description 未走 `t()`，未查证。
2. **DLC 欢迎弹窗种族名未译**（`shots/022303-s1-campdrop.png`）：『种族选择human, elf, dwarf或halfling。』
3. **物品栏初始列表为空**（`shots/023925-p2-inv.png`）：`getInven("INVEN")` 有 2 件物品但列表不显示，点击顶部类型过滤图标后恢复正常（`shots/025305-p2-inv-clicklast.png`）。疑为类型过滤标签状态被记忆，与汉化无关，未查证；同状态下丢弃提示『没东西可以丢弃。』。
4. **大剑人偶标签只显示材质**：带双词缀的「屠杀之强酸的铁质大剑」人偶标签只显示『铁』，未显示词缀标签（斗篷正常显示『亚麻、永恒精灵』），是否为设计未查证。
5. Lua 控制台自身界面（banner、快捷键说明）为英文，属引擎层，非清单项。

## 与上一轮的差异

- 上一轮 afv-a 在「快捷键 10」看到截断（`快捷键 1(`），本轮 10 与 11 均完整显示，未复现。
- 上一轮 11/13/4 三项 NOT_REACHED，本轮 11、13 已 PASS，4 仍受成就落库限制。
