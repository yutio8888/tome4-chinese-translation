### 批次核验前置信息

- **复核批次**：`batch-003`
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-003.md`
- **文件 SHA-256 核验**：`4d835af4b87bb646eadc83fc1839243f4959f3ebb31251ef35f951416d86ba36`（核验一致）
- **覆盖范围**：`entry-00081` 至 `entry-00120`，共 40 条
- **源码参考**：
  - engine / boot 模块通过 `git show` 读取固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`。
  - 条目涉及的 DLC 内容参考冻结目录（注：DLC 来源未固定）。

---

### 逐条复核报告

#### entry-00081
- **条目位置**：`engine.lua:1313`（`engine/engine/interface/PlayerRun.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/PlayerRun.lua:92` 中 `game.logPlayer(self, "You don't see how to get there...")`。译文语义准确，标点使用全角省略号，无格式控制符或占位符异常。

#### entry-00082
- **条目位置**：`engine.lua:1320`（`engine/engine/interface/PlayerRun.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/PlayerRun.lua:377` 中 `game.log("Ran for %d turns (stop reason: %s).", self.running.cnt, msg)`。占位符 `%d` 与 `%s` 数量及顺序一致，标点全角化规范。

#### entry-00083
- **条目位置**：`engine.lua:1325`（`engine/engine/interface/WorldAchievements.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/WorldAchievements.lua:113` 中 `game.log("#%s#Personal New Achievement: %s!", color, a.name)`。颜色标记 `#%s#` 与名称占位符 `%s` 匹配，全角感叹号准确。

#### entry-00084
- **条目位置**：`engine.lua:1326`（`engine/engine/interface/WorldAchievements.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/WorldAchievements.lua:114` 中 `("Personal New Achievement: #%s#%s"):tformat(color, a.name)`。格式代码 `#%s#%s` 保持一致，冒号全角化。

#### entry-00085
- **条目位置**：`engine.lua:1327`（`engine/engine/interface/WorldAchievements.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/WorldAchievements.lua:155` 中 `game.log("#%s#New Achievement: %s!", color, a.name)`。占位符与颜色格式控制码一致。

#### entry-00086
- **条目位置**：`engine.lua:1328`（`engine/engine/interface/WorldAchievements.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/interface/WorldAchievements.lua:156` 中 `("New Achievement: #%s#%s"):tformat(color, a.name)`。占位符与格式控制码匹配。

#### entry-00087
- **条目位置**：`engine.lua:1388`（`engine/engine/ui/WebView.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/ui/WebView.lua:199` 中 `Dialog:yesnoPopup(_t"Confirm addon install/update", _t("Are you sure you want to install this addon: #LIGHT_GREEN##{bold}#%s#{normal}##LAST# ?"):tformat(name), ...)`。样式代码 `#LIGHT_GREEN##{bold}#%s#{normal}##LAST#` 完整一致，问号全角化。

#### entry-00088
- **条目位置**：`engine.lua:1390`（`engine/engine/ui/WebView.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/ui/WebView.lua:217` 中 `("Are you sure you want to install this module: #LIGHT_GREEN##{bold}#%s#{normal}##LAST#?"):tformat(name)`。样式与颜色标记完整匹配。

#### entry-00089
- **条目位置**：`engine.lua:1393`（`engine/engine/ui/WebView.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/engine/ui/WebView.lua:245` 中 `Dialog:simplePopup(_t"Game installed!", ...)`。语义准确，标点匹配。

#### entry-00090
- **条目位置**：`engine.lua:1420`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：细微观察
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:161`。控制码 `#GOLD#...#WHITE#` 及 URL 保持一致，专有名词“马基·埃亚尔”符合 preferred 规范。末尾“玩的开心！”中“的”字偏口语化（规范书面语常写作“玩得开心！”），但不影响机制与理解。

#### entry-00091
- **条目位置**：`engine.lua:1446`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:218`。控制码 `#LIGHT_GREEN#安全模式#WHITE#` 匹配，换行与段落匹配，对安全模式机制描述清晰。

#### entry-00092
- **条目位置**：`engine.lua:1457`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：细微观察
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:233`。3 处格式占位符（`#YELLOW#%s#LAST#` 及后续两行路径 `%s`）数量与顺序完整一致，末尾双换行匹配。译文第二句“这种情况不被支持的，会引发很多BUG”缺少联系动词“是”，语感略有瑕疵，但不影响玩家理解。

#### entry-00093
- **条目位置**：`engine.lua:1474`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:309` 中 `("Updating addon: #LIGHT_GREEN#%s"):tformat(...)`。颜色标记 `#LIGHT_GREEN#%s` 保持一致，冒号全角化。

#### entry-00094
- **条目位置**：`engine.lua:1478`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：细微观察
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:580`。文本格式控制码（`#LIGHT_GREEN#...#LAST#`、`#{bold}#...#{normal}#`、`#LIGHT_BLUE#...#LAST#`）与段落列表完整对应。细微观察点：第 6 个列表项原文为 `purchaser / donator bonuses`，译文采用“购买者/赞助者独享权益”，与术语库 `Donator` 优选译法“捐赠者”略有出入（虽未违规写作“捐助者”，但使用了“赞助者”）；此外该列表项加了句号，与其余列表项标点风格略不一致。

#### entry-00095
- **条目位置**：`engine.lua:1513`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:641` 中 `Dialog:simpleWaiter(_t"Registering...", ...)`。语义准确，全角省略号匹配。

#### entry-00096
- **条目位置**：`engine.lua:1518`（`engine/modules/boot/class/Game.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/class/Game.lua:649` 中 `("Creation failed: %s (you may also register on https://te4.org/)"):tformat(err)`。占位符 `%s` 匹配，中文全角标点规范。

#### entry-00097
- **条目位置**：`engine.lua:1538`（`engine/modules/boot/data/damage_types.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/data/damage_types.lua:32` 中浮动文字 `_t"Kill!"`。击杀文本翻译准确，全角感叹号匹配。

#### entry-00098
- **条目位置**：`engine.lua:1583`（`engine/modules/boot/data/general/npcs/canine.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/data/general/npcs/canine.lua:38` 中 `wolf` 的描述文本。语义准确生动，标点规范。

#### entry-00099
- **条目位置**：`engine.lua:1596`（`engine/modules/boot/data/general/npcs/skeleton.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/data/general/npcs/skeleton.lua:42` 中实体名称 `degenerated skeleton warrior`。术语符合规范（skeleton -> 骷髅，warrior -> 战士）。

#### entry-00100
- **条目位置**：`engine.lua:1607`（`engine/modules/boot/data/general/npcs/troll.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/data/general/npcs/troll.lua:38` 中 `forest troll` 的描述文本。`humanoid` 准确译为“人形生物”，符合术语库标准。

#### entry-00101
- **条目位置**：`engine.lua:1613`（`engine/modules/boot/data/general/npcs/troll.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/data/general/npcs/troll.lua:62,72` 中 `mountain troll` 的描述文本。描述准确完整。

#### entry-00102
- **条目位置**：`engine.lua:1623`（`engine/modules/boot/data/talents.lua`）
- **复核结论**：存在疑点
- **核验依据**：
  1. 术语库现存条目（快照第 675 行）：`Flame 火球术 T.GAME.TALENT talents talent name existing core`。
  2. 源码验证：`game/engines/default/modules/boot/data/talents.lua:79-99` 中 `Flame` 定义为发射火焰弹的直接攻击法术（`tg = {type="bolt", ...}`, `DamageType.FIRE`），与主游戏中法师的 `Flame`（火球术）技能原型完全一致。
  3. 当前条目为 `talent name`，译文为“火焰”，与伤害类型/效果类型（`fire` 火焰）混淆，且偏离了既有技能术语“火球术”。

#### entry-00103
- **条目位置**：`engine.lua:1648`（`engine/modules/boot/dialogs/Addons.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/Addons.lua:43`。格式代码 `#LIGHT_BLUE##{underline}#...#{normal}#` 完整，冒号用于引出超链接控件，界面排版自然。

#### entry-00104
- **条目位置**：`engine.lua:1674`（`engine/modules/boot/dialogs/Credits.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/Credits.lua:90` 中致谢人员分类标题。译法贴切自然。

#### entry-00105
- **条目位置**：`engine.lua:1697`（`engine/modules/boot/dialogs/FirstRun.lua`）
- **复核结论**：细微观察
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/FirstRun.lua:51`。样式代码 `#{bold}##CRIMSON#...#{normal}#` 匹配，多段列表排版与换行匹配。细微观察点：
  1. 术语快照第 671 行明确注记“聊天徽章与成就名称统一为‘捐赠者’；不写作‘捐助者’”，此处列表中出现了“购买者/捐助者福利”及“发放捐助者奖励”的表述。
  2. 首行“即将禁止所有网络请求”末尾缺失标点符号。

#### entry-00106
- **条目位置**：`engine.lua:1737`（`engine/modules/boot/dialogs/LoadGame.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/LoadGame.lua:118`。调用参数为 `(mod.long_name, save.name, v1, v2, v3, addons_str, save.description)`，占位符 `%s: %s`、`%d.%d.%d`、`%s`、`%s` 顺序与数量完全匹配，样式代码及换行保持一致。

#### entry-00107
- **条目位置**：`engine.lua:1755`（`engine/modules/boot/dialogs/LoadGame.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/LoadGame.lua:198`。颜色标记 `#LIGHT_RED#警告：#LAST#` 匹配；将“permanently invalidate it”翻译为“不可逆地将其标记为作弊存档”，准确表达了开发者模式下存档失效的实际游戏机制。

#### entry-00108
- **条目位置**：`engine.lua:1761`（`engine/modules/boot/dialogs/LoadGame.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/LoadGame.lua:258` 中 `_t"Downloading old game data: #LIGHT_GREEN#"..dl.name`。尾部颜色控制码 `#LIGHT_GREEN#` 完整保留。

#### entry-00109
- **条目位置**：`engine.lua:1762`（`engine/modules/boot/dialogs/LoadGame.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/LoadGame.lua:272` 中 `("Old game data for %s correctly installed. You can now play."):tformat(version_string)`。占位符 `%s` 匹配，语义准确。

#### entry-00110
- **条目位置**：`engine.lua:1779`（`engine/modules/boot/dialogs/MainMenu.lua`）
- **复核结论**：存在疑点
- **核验依据**：
  1. 术语库注记（快照第 684 行）：`Maj'Eyal 马基·埃亚尔 T.PN.WORLD places _t preferred core 维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代`。
  2. 译文第 2 段斜体介绍中出现“很多马基埃亚尔的居民……”，缺失间隔号“·”，未遵循已裁定的 preferred 专有名词规范（同批其余条目如 entry-00090、00094、00112、00116 均已采用“马基·埃亚尔”）。
  3. 注：该条涉及 DLC《乌鲁洛克之烬》（Ashes of Urh'Rok），DLC 来源未固定。

#### entry-00111
- **条目位置**：`engine.lua:1800`（`engine/modules/boot/dialogs/MainMenu.lua`）
- **复核结论**：存在疑点
- **核验依据**：
  1. 专有名词违背：术语快照第 694 行明确记录 `Scourge from the West 西方天灾 T.PN.PERSON society _t preferred dlc Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”`。译文中两处（第 2 段与第 5 段）均写作“西方灾星”，直接违背 preferred 规范。
  2. 职业名不一致：职业列表（第 4 段）中 `Psyshots` 译为“念力射手”，而术语库现存条目（`terminology/classes.tsv:46` 及快照第 691 行）为 `Psyshot 灵能射手 T.GAME.CLASS`。
  3. 注：该条涉及 DLC《余烬怒火》（Embers of Rage），DLC 来源未固定。

#### entry-00112
- **条目位置**：`engine.lua:1823`（`engine/modules/boot/dialogs/MainMenu.lua`）
- **复核结论**：存在疑点
- **核验依据**：
  1. 职业名不一致：新职业 `Writhing Ones` 译为“扭动者”，而术语库（`terminology/classes.tsv:43` 及快照第 706 行）中该 DLC 职业明确记录为 `Writhing One 蜿蜒怪人 T.GAME.CLASS`。
  2. 区域名不一致：新区域 `Scourge Pits` 译为“瘟疫之穴”，但在 DLC 对应文本 `tome-cults.lua:4465` 中该区域统一译为“天灾之穴”。
  3. 细微观察：原文 `Nethergames` 实为作者拼写错误（指代 `Nethergates` 彼世之门），汉化准确纠正还原为“彼世之门”；`(不要问我你是怎么*进来*的)` 使用了半角圆括号。
  4. 注：该条涉及 DLC《禁忌邪教》（Forgotten Cults），DLC 来源未固定。

#### entry-00113
- **条目位置**：`engine.lua:1864`（`engine/modules/boot/dialogs/MainMenu.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/MainMenu.lua:278,281` 中 `Dialog:simplePopup("Steam", _t"Steam client not found.")`。语义准确。

#### entry-00114
- **条目位置**：`engine.lua:1911`（`engine/modules/boot/dialogs/ProfileLogin.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileLogin.lua:68`。控制码 `#{bold}#偶尔#{normal}#` 匹配，括号全角化，意思准确。

#### entry-00115
- **条目位置**：`engine.lua:1914`（`engine/modules/boot/dialogs/ProfileLogin.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileLogin.lua:71`。按钮文本翻译准确，全角括号规范。

#### entry-00116
- **条目位置**：`engine.lua:1929`（`engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileSteamRegister.lua:32`。控制码 `#GOLD#...#LAST#` 与 `#{bold}#...#{normal}#` 匹配，专有名词“马基·埃亚尔”规范，末尾换行一致。

#### entry-00117
- **条目位置**：`engine.lua:1938`（`engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileSteamRegister.lua:44`。格式控制码与条目 entry-00114 一致，全角括号规范。

#### entry-00118
- **条目位置**：`engine.lua:1942`（`engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileSteamRegister.lua:48`。与条目 entry-00115 一致，按钮文本翻译规范。

#### entry-00119
- **条目位置**：`engine.lua:1949`（`engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileSteamRegister.lua:79`。等待弹窗文本与 entry-00095 一致，全角省略号匹配。

#### entry-00120
- **条目位置**：`engine.lua:1951`（`engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **复核结论**：未发现问题
- **核验依据**：源码对应 `game/engines/default/modules/boot/dialogs/ProfileSteamRegister.lua:80,83`。与 entry-00113 一致，弹窗提示翻译准确。

---

### 疑点汇总清单（供后续裁决）

| 编号 | 位置 | 严重级别倾向 | 疑点摘要 | 核验依据与来源说明 |
| :--- | :--- | :--- | :--- | :--- |
| **entry-00102** | `engine.lua:1623` | 存在疑点 | 技能名 `Flame` 译为“火焰” | 术语库现存为“火球术”（`T.GAME.TALENT`，`talent name`）。源码对应发射火焰弹的直接攻击法术，与主游戏同名法术原型一致。译作“火焰”混淆了伤害类型。 |
| **entry-00110** | `engine.lua:1779` | 存在疑点 | 地名 `Maj'Eyal` 写作“马基埃亚尔” | 缺失间隔号。术语库明确裁定统一为“马基·埃亚尔”，注记“‘马基埃亚尔’已被取代”。（注：涉及 DLC 来源未固定） |
| **entry-00111** | `engine.lua:1800` | 存在疑点 | 专名违背与职业名不一致 | 1. 2 处出现“西方灾星”，术语库裁定 preferred 统一为“西方天灾”，明确注记“不写作‘灾星’”。<br/>2. 职业名 `Psyshots` 译为“念力射手”，术语库现存为“灵能射手”（`classes.tsv:46`）。（注：涉及 DLC 来源未固定） |
| **entry-00112** | `engine.lua:1823` | 存在疑点 | 职业名与区域名不一致 | 1. 职业名 `Writhing Ones` 译为“扭动者”，术语库现存为“蜿蜒怪人”（`classes.tsv:43`）。<br/>2. 区域名 `Scourge Pits` 译为“瘟疫之穴”，DLC 既有译文统一为“天灾之穴”（`tome-cults.lua:4465`）。（注：涉及 DLC 来源未固定） |
| **entry-00090** | `engine.lua:1420` | 细微观察 | 语病/用字细节 | 末尾“玩的开心！”书面语建议写作“玩得开心！”。 |
| **entry-00092** | `engine.lua:1457` | 细微观察 | 语法语感瑕疵 | “这种情况不被支持的，会引发很多BUG”缺少动词“是”（应为“这种情况是不被支持的”）。 |
| **entry-00094** | `engine.lua:1478` | 细微观察 | 术语一致性倾向 | `donator bonuses` 译为“赞助者独享权益”，与术语库 `Donator` 优选“捐赠者”略有偏差；列表标点风格略不一致。 |
| **entry-00105** | `engine.lua:1697` | 细微观察 | 术语一致性与标点 | 列表中使用了“购买者/捐助者”；首行缺少标点。 |