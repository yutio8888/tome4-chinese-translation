### batch-015 译文复核报告（只读）

**文件信息与哈希核验**：
- 审查批次：`batch-015.md`（条目 `entry-00561` 至 `entry-00600`，共 40 条）
- 文件 SHA-256：`b47e6e5a4b1ffdfed7c943d773eaf82f991955eb46ed4e3a6471ba476109da5a`（核验一致）
- 源码核验基准：公开源码仓库固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`t-engine4`，`game/modules/tome/data/chats/` 下对应对话文件）；译文基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

#### 条目逐条复核记录

- **entry-00561**（`mod-tome/data/chats/alchemist-last-hope.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 185-188 行，三种药剂/佳酿（Brew of Brawn / Brew of Stoneskin / Brew of Foundations）与任务线对应物品及术语（蛮牛/石肤/领悟）一致；口语化改口语气转折忠实于原文；无格式、颜色码或占位符异常。

- **entry-00562**（`mod-tome/data/chats/alchemist-last-hope.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 323-328 行，颜色代码 `#LIGHT_GREEN#*...*#WHITE#` 匹配闭合；人名 Stire（斯泰尔）、Marus（马鲁斯）与隐士炼金术士对应准确；大写强调语气与感叹号标点对应完整。

- **entry-00563**（`mod-tome/data/chats/alchemist-last-hope.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 362-365 行，颜色代码 `#LIGHT_GREEN#*...*#WHITE#` 完整对应；最终奖励物品“Taint of Purging”译为“清除印记”，文意与矮人幽默语气表达流畅。

- **entry-00564**（`mod-tome/data/chats/alchemist-last-hope.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 429-432 行（`npc.errand_given == true` 分支），单句文本语义忠实，标点正确。

- **entry-00565**（`mod-tome/data/chats/alchemist-last-hope.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 436-440 行，段落空行保留一致；关于妻子朋友失踪差事的前置提示语义准确，无占位符遗漏。

- **entry-00566**（`mod-tome/data/chats/angolwen-staves-store.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 67-73 行，机制调用为 `player:setTalentTypeMastery("spell/staff-combat", player:getTalentTypeMastery("spell/staff-combat", true) + 0.2)`，括号内说明“增加技能树系数0.2”完全契合游戏内 mastery 机制与术语，金币数值 750 正确。

- **entry-00567**（`mod-tome/data/chats/antimagic-end.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 31 行，动作指示颜色标签 `#LIGHT_GREEN#[you drink the potion]` 忠实对应 `#LIGHT_GREEN#[你喝下了药剂]`，源码原样未带闭合标签，译文格式保持一致。

- **entry-00568**（`mod-tome/data/chats/arena.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码 `valfren-defeat`（第 166-188 行），动态宏占位符 `@playerdescriptor.race@` 保留正确；行内与行首颜色标签 `#LIGHT_GREEN#`、`#WHITE#`、`#RED#` 出现位置与闭合完全匹配；各段换行与空行结构一一对应。

- **entry-00569**（`mod-tome/data/chats/assassin-lord.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 38-40 行日志输出，前缀 `#LIGHT_GREEN#` 正确保留，“assassination by proxy”译为“借刀杀人”贴切传神，陷阱术语一致。

- **entry-00570**（`mod-tome/data/chats/assassin-lord.lua`）
  - **复核结论**：存在疑点
  - **可核验依据**：核对标点符号，原文为 `'And do not forget, I own you now.'`，译文为 `”别忘了，你现在归我所有了。”`。经 Unicode 码点核查，引语前引号使用了右双引号 `”`（U+201D），而非标准的中文开双引号 `“`（U+201C），导致前后引号均为闭引号。

- **entry-00571**（`mod-tome/data/chats/command-staff.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 44-45 行（sentient staff aggressive 对话），叙述口吻生动，灵魂法术失败导致肉身湮灭、收容于法杖的背景与语气传译精准，标点符号无误。

- **entry-00572**（`mod-tome/data/chats/conclave-vault-greeting.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 20-22 行，描述颜色码 `#LIGHT_GREEN#*...*#WHITE#` 完整匹配，大写命令句式、分段与结尾连续换行均与源码模板严格一致。

- **entry-00573**（`mod-tome/data/chats/eidolon-plane.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 24-32 行，颜色码 `#LIGHT_GREEN#*...*#WHITE#` 及样式标记 `#{bold}#`、`#{normal}#` 匹配；源码原文末尾单独成行的句点 `.` 在译文中对应为单独成行的中文句号 `。`，格式保持一致。

- **entry-00574**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：细微观察
  - **可核验依据**：核对源码第 56-65 行，Zemekkys（泽梅基斯）、Sunwall（太阳堡垒）、farportals（远行传送门）、Orb of Many Ways（多元水晶球）、Maj'Eyal（马基·埃亚尔）等专名术语均准确。段落空行保留一致。仅第 2 行“创造一个远行传送门达到马基·埃亚尔”中，“达到”疑为“到达”之笔误，但不影响语义理解。

- **entry-00575**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 77 行，the Peak 对应巅峰（High Peak），句意顺畅准确。

- **entry-00576**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 85-88 行，第二行开头的制表符 `\t` 缩进格式严格保留；四颗宝球（Undeath / Destruction / Dragons / Elemental might）与指令水晶球（orbs of command）名称准确。

- **entry-00577**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 106 行，玩家集齐宝球后的应答语气与剧情推进逻辑相符，表达清晰自然。

- **entry-00578**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 170-184 行，四大兽人部落名称（Rak'shor / Gorbat / Vor / Grushnak）及地理方位描述准确无误；列表排版格式完全一致。

- **entry-00579**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：细微观察
  - **可核验依据**：核对源码第 217-219 行，此处“Sorcerers”指代主线最终首领二人组（焦痕之地与巅峰 Boss），在成就列表中多统一译为“巫师”（如“杀死2名巫师”），此处对话译为“法师”，存在与常规奥术法师（mage）混淆的倾向；但句意传达准确，不构成阻断性硬伤。

- **entry-00580**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 221 行，衔接上文“good men lost their lives for this”，回答“我会替你的人报仇”准确忠实。

- **entry-00581**（`mod-tome/data/chats/gates-of-morning-main.lua`）
  - **复核结论**：细微观察
  - **可核验依据**：核对源码第 228-230 行（焦痕之地失败分支），与 entry-00579 同理，“Sorcerers”译为“法师”（成就不一致地译为“巫师”）；句意完整通顺。

- **entry-00582**（`mod-tome/data/chats/golbug-explains.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 20-24 行，宏占位符 `@playerdescriptor.race@` 完整保留；颜色标签 `#VIOLET#*...*#LAST#` 闭合正确；烈焰与寒冰状态描述及兽人部落台词传译准确。

- **entry-00583**（`mod-tome/data/chats/jewelry-store.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 56 行，格式化占位符 `%d` 正确对应数值（`price`），`tformat` 运行时宏机制相符，无多余空格或漏转。

- **entry-00584**（`mod-tome/data/chats/jewelry-store.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 90 行，NPC 人名 Limmir（利米尔）和“magical plating”（魔法镀层）术语准确，弹窗提示语意清晰。

- **entry-00585**（`mod-tome/data/chats/jewelry-store.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 141 行，标准告别选项语句，翻译准确自然。

- **entry-00586**（`mod-tome/data/chats/keepsake-berethh-encounter.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 25 行，人名严格采用任务线统一术语“凯勒斯”（Kyless，取代旧译“克里斯”），句意准确。

- **entry-00587**（`mod-tome/data/chats/keepsake-berethh-encounter.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 31-33 行，颜色标签 `#LIGHT_GREEN#[Attack]#LAST#` 对应 `#LIGHT_GREEN#[攻击]#LAST#`，人名“凯勒斯”统一。

- **entry-00588**（`mod-tome/data/chats/keepsake-caravan-destroyed.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 24-26 行，颜色标签 `#LIGHT_GREEN#[Kill him]#LAST#` 对应 `#LIGHT_GREEN#[杀了他]#LAST#`，文意忠实流畅。

- **entry-00589**（`mod-tome/data/chats/keepsake-caravan-destroyed.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 31-33 行，颜色标签 `#LIGHT_GREEN#[Help him]#LAST#` 对应 `#LIGHT_GREEN#[帮助他]#LAST#`，格式完整无损。

- **entry-00590**（`mod-tome/data/chats/keepsake-kyless-death.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 20-22 行，动作标签 `#VIOLET#*...*#LAST#` 闭合完整；人名“凯勒斯”准确；源码中原文笔误“destoyed!”在译文中正常传译为“它必须被毁掉！”，句意完整。

- **entry-00591**（`mod-tome/data/chats/keepsake-kyless-death.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 41 行，动作标签 `#VIOLET#*...*#LAST#` 完整，人名“凯勒斯”准确，句意准确。

- **entry-00592**（`mod-tome/data/chats/keepsake-kyless-death.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 43 行，人名“凯勒斯”准确，标点完整。

- **entry-00593**（`mod-tome/data/chats/keepsake-kyless-death.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 47 行，动作标签 `#VIOLET#*...*#LAST#` 完整，人名“凯勒斯”准确，收书入包并发现死亡的动作过程翻译流畅。

- **entry-00594**（`mod-tome/data/chats/last-hope-melinda-father.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 80-82 行，城镇名称 Derth 采用统一术语“德斯镇”，地宫（crypt）指代梅琳达获救处的邪教地宫；段落换行完全对应。

- **entry-00595**（`mod-tome/data/chats/mage-apprentice-quest.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 67 行，标准退出对话选项，标点与语义准确。

- **entry-00596**（`mod-tome/data/chats/mage-apprentice-quest.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 74 行，学徒询问时的离开选项，语气自然准确。

- **entry-00597**（`mod-tome/data/chats/melinda-fortress.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 71-73 行，动作颜色标签 `#LIGHT_GREEN#[smile playfully at her]` 对应 `#LIGHT_GREEN#[你调皮地冲她微笑]`，源码此处未带有闭合标签，译文与其结构完全一致。

- **entry-00598**（`mod-tome/data/chats/ring-of-blood-orb.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 20-22 行，颜色标签 `#LIGHT_GREEN#*...*#WHITE#` 匹配；入场费 150 金币数值准确，行文结构一致。

- **entry-00599**（`mod-tome/data/chats/sage-kitty.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 36 行，颜色标签 `#LIGHT_GREEN#...#WHITE#` 匹配；任务道具 troll intestines 与术语快照中的“巨魔”一致，译为“巨魔肠子”准确生动。

- **entry-00600**（`mod-tome/data/chats/shertul-fortress-butler.lua`）
  - **复核结论**：未发现问题
  - **可核验依据**：核对源码第 36 行，farportal 统一译为“远行传送门”，玩家受管家通知返回要塞对话的语境契合，疑问语气正确。

---

#### 总结与关键发现概括

1. **本批覆盖情况**：已对 `entry-00561` 至 `entry-00600` 全部 40 条记录进行逐条核验，无任何遗漏。
2. **存在疑点（1 处）**：
   - `entry-00570`：译文中前引号误使用了右双引号 `”`（U+201D），而非中文左双引号 `“`（U+201C）。
3. **细微观察（2 处）**：
   - `entry-00574`：“达到马基·埃亚尔”疑为“到达”的语病笔误。
   - `entry-00579` / `entry-00581`：主线 Boss 组合“Sorcerers”在成就中多译为“巫师”，在对话中译为“法师”，存在跨模块一致性与术语辨识度的细微差异。
4. **占位符与颜色码**：本批所有 `@playerdescriptor.race@`、`%d` 及各种颜色/排版控制标签全部对应完整，无丢失或破坏。