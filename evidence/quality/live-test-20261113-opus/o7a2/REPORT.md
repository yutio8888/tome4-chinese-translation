# REPORT o7a2 — 沃尔部落(1) 接续（装备对比 / 观察详情 / 效果）

- 基线：公开 v0.3.12（共享安装只读，未改动）、官方 1.7.6 + 三 DLC；模型 Opus；存档 Astajed（50 级半身人炼金术士，半神）。boot.sh 读档，区域裁切确认「沃尔部落 (1)」。
- 停止原因：**budget**（读图达到 16 张提前收尾线；全屏额度 3/3 已用尽）。
- 计数：reads=16/20，full=3/3（含 1 张 400×225 缩小整屏），工具调用≈72/100，读入图片累计 3.90 MB/15。

## 覆盖（全部为 debug-ui，除注明外）
| 类别 | 查看 | 通过 | 异常 | 未到达 |
|---|---|---|---|---|
| item | 3（生成匕首对比已装备法杖、生成腰带、紫黄晶默认提示） | 3 | 0 | 0 |
| monster（角色面板） | 1 只（冰霜兽人龙战士：常规页左右两半、技能页） | 1 | 0 | 0 |
| talent | 2 debug-ui（冰肤术、兽人狂暴）+1 console（冻结施放日志） | 3 | 0 | 0 |
| effect | 0 | 0 | 0 | 1（法术冲击/冰冻：仅日志） |

findings：0 条。

## 已查但不报（非译文问题，供主代理参考）
- 匕首对比行「获得技能: +0(+-1) 法杖掌控」：上游 Object.lua `("(+%d) "):format(diff)` 对负值产生「+-1」，英文同样出现，非译文问题。
- 非玩家角色面板「类型：」「子类：」为空：上游 CharacterSheet.lua:619/622 `_t(player:descriptorDisplayName(...) or "")` 返回空串（Lua 中为真值），不会回退到 `_t(player.type)`；英文同样空白，非译文问题（实体 type=humanoid subtype=orc 均有译文）。
- 物品栏标题显示「Inventory」：是本会话控制台 `showEquipInven("Inventory")` 自传的英文参数，不是游戏文本。
- Ctrl 按住未出现并排比较框；对比以括号差值内联显示（匕首 vs 已装备法杖）。腰带位无已装备物，无对比项。
- 兽人种族技能 Hold the Ground＝兽族忍耐、Pride of the Orcs＝兽族荣耀、Orcish Fury＝兽人狂暴，兽族/兽人用字并存，属既有译名，未达改名门槛，不报。
- 兽人狂暴说明「1.6%， 持续」逗号后空格为占位符 lint 要求的既定格式。
- game.log 中 aiParseTalent「attempt to index local 'self'」为上游 AI 解析提示，与文字无关。

## 未覆盖
- 效果提示（任务 3）：KP_5/s 未推进回合（game.turn 始终 0；期间角色面板曾在后台残留，按键可能被面板吞掉），改用控制台 `C:forceUseTalent(T_FREEZE)`：日志「高阶兽人冰霜术士施放了冻结。」「Astajed豁免了效果“冰冻”！」，玩家获得 EFF_SPELLSHOCKED（detrimental）与既有 EFF_ZONE_AURA_VOR，但未定位到效果图标位置，悬停提示未看到。建议接续会话：先关闭所有对话框，用 1 张全屏确认左侧效果图标坐标，再悬停法术冲击与沃尔区域光环。
- 第 2 只兽人仅看 1–2 条技能（冰肤术、兽人狂暴）；其余技能（冰爪、冰息术、散兵等）与攻击/防御/装备页未看。
- 兽人主题/唯一装备未生成（只用随机词缀 ego_chance=1000 生成两件）。

## 调试手段
控制台 makeEntity/identify/addObject、showEquipInven、CharacterSheet.new、Actor:move(force)、setTarget、forceUseTalent；明细见 debug-actions.md。con.sh 像素校验在后半段失效（控制台已开时仍报 CONSOLE NOT OPEN），改为 windowfocus 2097160 后直接 ctrl+l 输入。结束时已 kill -9 本会话 t-engine（pid 773885）。
