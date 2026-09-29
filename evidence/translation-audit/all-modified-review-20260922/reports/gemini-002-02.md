已完成对 [batch-002.md](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/batches/batch-002.md) 内全部 40 条冻结译文（entry-00041 至 entry-00080）的只读核验。核验过程沿公开引擎源码固定版本（commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）及同 section 上下文查证，未修改任何文件，未派发子 agent。

以下为逐条审核结论，已发现的疑点与可核验依据整理记录如下，交由 Sol 交叉核验：

---

### 逐条审核结论（40 条）

- **entry-00041**：**发现疑点**
  - **核验依据**：[VideoOptions.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/VideoOptions.lua#L214)。
  - **疑点分析**：
    1. 标点缺失：英文末尾控制标签前有句号（`...user.#WHITE#`），译文末尾 `#WHITE#` 前缺失句号（`...自动恢复原值#WHITE#`）。
    2. 语序逻辑微瑕：原文机制为十秒倒计时内若未确认则超时还原（“revert after ten seconds if not confirmed by the user”），译文“在十秒后不进行确认”略显逻辑倒置，建议改为“若在十秒内未确认，该数值将在十秒后自动恢复”。

- **entry-00042**：**未发现问题**
  - **核验依据**：[MTXMain.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/MTXMain.lua)。格式控制标签（`#{italic}#`、`#{bold}#`、`#GOLD#`、`#CRIMSON#` 等）全部闭合配对；专名 `Maj'Eyal` 依术语优先项统一译为“马基·埃亚尔”；语气忠实符合作者第一人称说明。

- **entry-00043**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L36)。占位符 `%d` 及样式标签完整保留，在线仓库空间增量表述准确。

- **entry-00044**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L40)。术语“沃瑞钽硬币”（voratun coins）与术语库 `voratun -> 沃瑞钽` 一致，`#GOLD##{italic}#...#{normal}#` 标签闭合无误。

- **entry-00045**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。连接服务器提示，颜色标签 `#YELLOW#` 保留，翻译准确。

- **entry-00046**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。外部浏览器跳转按钮文本，翻译通顺规范。

- **entry-00047**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L286)。用于拼接窗口标题，前置两格半角空格与占位符 `%d`、`%s` 完整保留。

- **entry-00048**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。时装包安装完成提示，语义准确。

- **entry-00049**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L330)。虽然英文原文有打字错误（“weng wrong”），但译文准确传达了动态挂载失败与手动安装指引。

- **entry-00050**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L342)。占位符 `%s` 与颜色标签 `#LIGHT_GREEN#` 正确保留。

- **entry-00051**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L370)。占位符 `%s` 与 `%d` 及前置复合样式标签均完整保留，触发提示清晰。

- **entry-00052**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua#L372)。占位符 `%s`、`%d` 及标签完整，共享装备库空间扩充语义准确。

- **entry-00053**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。单角色限购事件机制说明准确，`#{bold}#` 强调标签完整对应。

- **entry-00054**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。术语“反射之镜”（Mirror of Reflection）与“时装包”一致，福利描述及标签完整。

- **entry-00055**：**未发现问题**
  - **核验依据**：[ShowPurchasable.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/ShowPurchasable.lua)。UI 组合包自动安装提示，标签与语义准确。

- **entry-00056**：**未发现问题**
  - **核验依据**：[UsePurchased.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/UsePurchased.lua#L51)。连接服务器提示，标签完整。

- **entry-00057**：**未发现问题**
  - **核验依据**：[UsePurchased.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/UsePurchased.lua#L76)。检查 `game.zone.wilderness` 时的提示，意译为“请不要在世界地图上使用”完全符合语义。

- **entry-00058**：**未发现问题**
  - **核验依据**：[UsePurchased.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/UsePurchased.lua#L86-L89)。战役“竞技场”（The Arena）与选项标签 `#GOLD##{bold}#...` 完全对齐，末尾保留空行。

- **entry-00059**：**未发现问题**
  - **核验依据**：[UsePurchased.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/UsePurchased.lua#L96)。重复安装提示，准确。

- **entry-00060**：**未发现问题**
  - **核验依据**：[UsePurchased.lua](file:///workspace/t-engine4/game/engines/default/engine/dialogs/microtxn/UsePurchased.lua)。占位符 `%s` 保留，准确。

- **entry-00061**：**未发现问题**（格式细微观察）
  - **核验依据**：[ActorInventory.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorInventory.lua#L250)。
  - **核验分析**：4 个 `%s` 占位符顺序保留完整。英文原文在快捷键后带点（`(%s.)`），中文采用无点全角括号（`（%s）`），符合游戏内中文字符排版规范，未发现功能性问题。

- **entry-00062**：**未发现问题**
  - **核验依据**：[ActorInventory.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorInventory.lua#L530)。4 个 `%s`（角色名、槽位名称、装备名、错误信息）顺序与传参完全一致。

- **entry-00063**：**发现疑点**
  - **核验依据**：[ActorInventory.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorInventory.lua#L538)。
  - **疑点分析**：译文首个 `%s` 与“装备了”之间存在多余半角空格（`%s 装备了：%s。`），与同模块 entry-00064（`%s副手装备了`）、entry-00065（`%s装备`）排版不一致。

- **entry-00064**：**未发现问题**
  - **核验依据**：[ActorInventory.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorInventory.lua#L541)。`offslot` 准确译为“副手”，占位符 `%s` 完整保留。

- **entry-00065**：**未发现问题**
  - **核验依据**：[ActorInventory.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorInventory.lua#L555)。3 个 `%s`（角色名、被替换装备、新装备）顺序及对应关系完全正确。

- **entry-00066**：**未发现问题**
  - **核验依据**：[ActorLife.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorLife.lua#L102)。两处 `%s`（攻击方、受击方）顺序正确。

- **entry-00067**：**未发现问题**
  - **核验依据**：[ActorTalents.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorTalents.lua#L170)。占位符 `%s` 与 `%d` 保留，冷却回合提示准确。

- **entry-00068**：**未发现问题**
  - **核验依据**：[ActorTalents.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorTalents.lua#L330)。技能确认弹窗标题，占位符 `%s` 保留，翻译简洁。

- **entry-00069**：**发现疑点**
  - **核验依据**：[ActorTalents.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorTalents.lua#L753)（调用 `self:getStat(s) < v` 检查属性点数值）。
  - **疑点分析**：同 section `engine/engine/interface/ActorInventory.lua` 第 1204 行将 `not enough stat` 译为“属性值不足”。此处译为“属性点不足：%s”，易误导玩家以为是缺乏可分配属性点数，而非属性数值未达标。建议核验是否统一为“属性值不足：%s”或“属性不足：%s”。

- **entry-00070**：**未发现问题**
  - **核验依据**：[ActorTalents.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorTalents.lua#L828)。占位符 `%d` 保留，同系技能阶数前置要求表达清晰。

- **entry-00071**：**未发现问题**
  - **核验依据**：[ActorTalents.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ActorTalents.lua#L861)。占位符 `%s` 保留，互斥前置未学条件表达准确。

- **entry-00072**：**未发现问题**
  - **核验依据**：[GameTargeting.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/GameTargeting.lua#L115)。战术视图关闭提示，快捷键 Shift+T 及语义准确。

- **entry-00073**：**未发现问题**
  - **核验依据**：[GameTargeting.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/GameTargeting.lua#L148)。战术视图启用提示，与 entry-00072 对称规范。

- **entry-00074**：**未发现问题**
  - **核验依据**：[ObjectActivable.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ObjectActivable.lua#L52)。4 个占位符 `%s`、`%d`、`%d`、`%d` 顺序完全一致，power 在物品激活语境译为“能量”符合术语规范。

- **entry-00075**：**未发现问题**（标点细微观察）
  - **核验依据**：[ObjectActivable.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ObjectActivable.lua#L58)。占位符 `%s`、`%d` 正确。细微排版差异：括号采用了半角空格+半角括号 `(等级 %d)`，与 entry-00076 全角 `（等级 %d）` 略有风格差异。

- **entry-00076**：**未发现问题**
  - **核验依据**：[ObjectActivable.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/ObjectActivable.lua#L60)。5 个占位符 `%s`、`%d`、`%d`、`%d`、`%d` 顺序完全正确，能量消耗与当前/最大值表达清晰。

- **entry-00077**：**未发现问题**
  - **核验依据**：[PlayerExplore.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/PlayerExplore.lua#L428)。自动探索弹窗提示，翻译准确。

- **entry-00078**：**未发现问题**
  - **核验依据**：[PlayerHotkeys.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/PlayerHotkeys.lua#L164)。热键绑定提示，说明按 M 键打开技能窗口，准确且对玩家更具指导性。

- **entry-00079**：**未发现问题**
  - **核验依据**：[PlayerRest.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/PlayerRest.lua#L37)。用于弹窗标题 `("%s..."):tformat(what:capitalize())`，传入 `resting`（休息）显示为“休息中…”，准确。

- **entry-00080**：**未发现问题**
  - **核验依据**：[PlayerRest.lua](file:///workspace/t-engine4/game/engines/default/engine/interface/PlayerRest.lua#L43)。用于日志 `("%s starts..."):format(what:capitalize())`，传入 `resting`（休息）显示为“休息开始了…”，准确。

---

### 汇总疑点清单（供 Sol 交叉核验）

1. **entry-00041**：末尾 `#WHITE#` 前缺少句号；“十秒后不进行确认”在中文逻辑上可润色为“十秒内未确认”。
2. **entry-00063**：`%s 装备了：%s。` 首个占位符后存在多余半角空格，建议比对同文件其余条目排版。
3. **entry-00069**：`not enough stat: %s` 译为“属性点不足：%s”，与 line 1204 “属性值不足”存在术语歧义，易误解为未分配加点不足，建议核验是否统一为“属性值不足：%s”。
