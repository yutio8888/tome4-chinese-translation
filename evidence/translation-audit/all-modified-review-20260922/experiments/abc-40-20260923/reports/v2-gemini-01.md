| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03172 | 未发现问题 | 原文按钮与译文语义及标点一致 |
| entry-03173 | 未发现问题 | 教程弹窗上下文内语义完整忠实 |
| entry-03174 | 仅建议 | claim-03174-1 (单数指示代词与逗号规范建议) |
| entry-03175 | 未发现问题 | 颜色标记换行完整，背景提示准确 |
| entry-03176 | 存在问题 | claim-03176-1 (机制误述沿袭上游描述), claim-03176-2 (机制指代泛化偏译) |
| entry-03177 | 未发现问题 | 捐赠弹窗按钮译名准确对齐术语 |
| entry-03178 | 未发现问题 | 捐赠者特权提示准确，术语对齐 |
| entry-03179 | 存在问题 | claim-03179-1 (作用对象所属关系颠倒) |
| entry-03180 | 未发现问题 | 全角冒号排版等价，占位符保留 |
| entry-03181 | 未发现问题 | 随机种子标签与颜色占位符正确 |
| entry-03182 | 未发现问题 | 濒死阈值格式化符号与语义正确 |
| entry-03183 | 未发现问题 | 生命回复加成逻辑与标记无误 |
| entry-03184 | 未发现问题 | 拼接逗号与空格格式完全匹配 |
| entry-03185 | 未发现问题 | 缴械禁用状态前导空格保留完整 |
| entry-03186 | 未发现问题 | 防御面板属性标题与颜色一致 |
| entry-03187 | 未发现问题 | 死亡弹窗标题颜色与结构准确 |
| entry-03188 | 未发现问题 | 登录状态聊天日志选项语义无误 |
| entry-03189 | 未发现问题 | 捐赠特性描述与颜色标记一致 |
| entry-03190 | 未发现问题 | 幻化机制与颜色标记准确 |
| entry-03191 | 仅建议 | claim-03191-1 (第二段末句遗漏句号建议) |
| entry-03192 | 未发现问题 | 平滑移动动画参数意译准确 |
| entry-03193 | 未发现问题 | 抖动动画选项与复合标记匹配 |
| entry-03194 | 未发现问题 | 经典HUD战斗日志限制说明准确 |
| entry-03195 | 未发现问题 | 日志渐隐时间参数语义准确 |
| entry-03196 | 未发现问题 | 战术视图四档模式与快捷键准确 |
| entry-03197 | 未发现问题 | WASD对角线移动操作说明准确 |
| entry-03198 | 未发现问题 | 滑块范围提示排版等价准确 |
| entry-03199 | 未发现问题 | 滚屏边界距离与居中机制准确 |
| entry-03200 | 未发现问题 | 掉血警告比例数值范围准确 |
| entry-03201 | 未发现问题 | Discord丰富状态说明完整，颜色保留 |
| entry-03202 | 未发现问题 | 网页金库角色表备份说明忠实 |
| entry-03203 | 存在问题 | claim-03203-1 (版本检测误译为无法更新) |
| entry-03204 | 未发现问题 | 斗篷兜帽替换头部显示说明准确 |
| entry-03205 | 未发现问题 | 纸娃娃系统术语与括注对齐准确 |
| entry-03206 | 未发现问题 | 高级贴图特性说明准确 |
| entry-03207 | 未发现问题 | 升级界面标题占位符消费正确 |
| entry-03208 | 未发现问题 | 属性等级上限提示准确 |
| entry-03209 | 未发现问题 | 四类加点剩余数量与标记一一对应 |
| entry-03210 | 仅建议 | claim-03210-1 (施受关系理顺建议) |
| entry-03211 | 未发现问题 | 属性点按钮文本及占位符消费无误 |

---

### Claim 详情与核验证据

#### claim-03174-1
- **条目**：[entry-03174](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L52-L67)
- **短引**：原文 `...will make locked campaigns, races and classes permanently available.` / 译文 `...可以永久解锁这个战役，种族，职业。`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`Birther.lua:804`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L804)（以及 826、858、890、944 行）。`locktext` 作为统一模板追加在未解锁的战役、难度、死亡模式、种族和职业描述后展示给玩家。
- **说明**：原文为总括性复数表述（locked campaigns, races and classes），译文使用单数指示代词“这个”并以逗号并列，风格偏口语化；但由于附着于具体未解锁项后显示，语义指向清晰，无实质信息缺失或机制误导，仅属文字规范与标点偏好。

#### claim-03176-1
- **条目**：[entry-03176](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L82-L111)
- **短引**：原文 `You will need an online profile active and connected for the tile selector to enable.` / 译文 `你需要一个已激活并保持连接的在线档案，贴图选择器才能启用。`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`Birther.lua:1385`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L1385)（`_M:selectExplorationNoDonations`）。该弹窗是未捐赠玩家在创角界面尝试选择“探索模式”（Exploration Mode）时弹出的捐赠说明弹窗。
- **问题内容**：源码英文在此处系由第 1401 行自定义贴图弹窗（`_M:selectTileNoDonations`）直接复制而来的上游文本笔误，导致在探索模式弹窗中错误地向玩家说明为“tile selector”（贴图选择器）的激活条件。译文忠实复制了该英文文本，面向玩家构成机制说明上的事实错误。本条确认为**面向玩家的机制误述**，且为**沿袭上游描述**，非翻译新增。

#### claim-03176-2
- **条目**：[entry-03176](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L82-L111)
- **短引**：原文 `I realize this can not please everybody and after multiple requests I have decided to grant exploration mode to donators...` / 译文 `我觉得这款游戏可能不会被所有人接受并且在收到多次请求后，我决定开放探索模式给捐赠者...`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`Birther.lua:1380`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua#L1380)（`_M:selectExplorationNoDonations`）。上下文紧承前句“Tales of Maj'Eyal is meant to be a very replayable game in which you get better by learning from mistakes (and thus from dying too)”。
- **问题内容**：代词“this”明确指向前句阐述的“在死亡与错误中学习”的高惩罚性永久死亡机制（即这种严苛的硬核玩法无法取悦所有人，因而才提供无限命探索模式）。译文译为“我觉得这款游戏可能不会被所有人接受”，误将对局内死亡机制的指代扩大至整款游戏本身，属于**翻译新增**的语义偏差。

#### claim-03179-1
- **条目**：[entry-03179](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L136-L147)
- **短引**：原文 `#RED#Displaying %s set for %s (equipment NOT switched)` / 译文 `#RED#展示 %s 套装给 %s 看（装备未切换）`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`CharacterSheet.lua:74`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/CharacterSheet.lua#L74)（`init` 中 `c_equipment.on_change`）。当玩家在人物面板的装备标签页切换显示主手/副手武器配置时，触发 `game.logPlayer(self.actor, ...)`。`%1$s` 消费 `self.equip_set`（即 `"main"` 或 `"off"`，在界面对应“主手”或“副手”），`%2$s` 消费 `self.actor:getName():capitalize()`（被查看角色的名称）。
- **问题内容**：原文“Displaying %s set for %s”表达的是“正在为角色 %2$s 显示 %1$s 武器配置/槽位”。译文译作“展示 %s 套装给 %s 看”，将作为所属主体的角色 %2$s 扭曲成了接收展示的受众观众（“给...看”），颠倒了作用对象与所属关系；同时武器配置（set）在装备槽语境并非套装装备（item set），译为“套装”容易引起机制概念混淆。

#### claim-03191-1
- **条目**：[entry-03191](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L280-L303)
- **短引**：原文 `...so I have come to disturb you here and now to ask for your kindness.` / 译文 `...所以我来这里打扰你，希望得到你的帮助`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`Donation.lua:51`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Donation.lua#L51)（`init` 中 `desc` 文本区域）。
- **说明**：第二段末句“希望得到你的帮助”句末遗漏句号。由于不丢失实质语义，亦不影响格式化参数与换行渲染，仅属标点完整性层面的排版优化建议。

#### claim-03203-1
- **条目**：[entry-03203](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L452-L495)
- **短引**：原文 `- Version checks: Addons will not be checked for new versions.` / 译文 `- 插件版本更新：无法更新插件的版本。`
- **状态**：存在问题
- **源码依据与消费逻辑**：[`GameOptions.lua:672`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/GameOptions.lua#L672)（`generateListOnline` 中 `disable_all_connectivity` 选项说明）。该选项为“禁用全部网络连接”，此段为列举受其影响的各项功能。
- **问题内容**：前一项（`Easy addons downloading & installation`）中已明确说明玩家虽无法在游戏内一键下载，但“仍可手动安装”（`You may still do so manually. / 但仍可手动安装`）。本项“Version checks”特指客户端自动向远端发起的插件新版本在线检测机制。译文将其译为“- 插件版本更新：无法更新插件的版本。”，不仅混淆了“自动版本检测”与“更新插件”，更在逻辑上直接推翻了上一条允许手动更新安装的说明，向玩家传递了错误的限制事实。

#### claim-03210-1
- **条目**：[entry-03210](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md#L574-L597)
- **短引**：原文 `Some races or items may increase them as well.` / 译文 `某些种族和物品可以获得额外的点数。`
- **状态**：仅建议
- **源码依据与消费逻辑**：[`LevelupDialog.lua:655`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/LevelupDialog.lua#L655)（`desc_types`，加点界面中技能树解锁点的机制说明）。
- **说明**：原文指部分特定种族特性（如柯纳克族开局奖励）或物品能够额外增加该类点数。译文“某些种族和物品可以获得额外的点数”在施受逻辑上略有瑕疵（字面将种族和物品作为获得点数的主体），但玩家在角色成长界面的语境下能明确理解其实际效果，未造成机制理解偏差，仅属句意流畅度润色建议。

---

### 读取边界与执行审计记录

1. **实际读取的所有路径与版本**：
   - 输入与规则：[`protocol-v2/INPUT.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/INPUT.md)
   - 冻结条目元数据：[`protocol-v2/entries.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/entries.json)
   - 邻近语境参考：[`protocol-v2/context.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/context.lua)
   - 源码访问规范：[`protocol-v2/source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/source-access.json)
   - 冻结源码（对应固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）：
     - [`Birther.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Birther.lua)
     - [`CharacterSheet.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/CharacterSheet.lua)
     - [`DeathDialog.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/DeathDialog.lua)
     - [`Donation.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/Donation.lua)
     - [`GameOptions.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/GameOptions.lua)
     - [`GraphicMode.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/GraphicMode.lua)
     - [`LevelupDialog.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/sources/game/modules/tome/dialogs/LevelupDialog.lua)
2. **额外源码路径的调用链来源**：无。40 条条目的消费逻辑均完全包含在上述 7 份授权的对话框源码内部，无需追溯额外公开源码文件。
3. **无法核验或越界情况**：无无法核验项，无越界读取行为。未访问任何同目录其他实验臂文件、历史审查报告、生产状态或其它模型输出。
4. **属性声明**：本输出仅为依据协议执行的只读独立复核观察记录，不作为系统最终真值，不输出生产契约，不宣称 `DONE_VERIFIED`。
