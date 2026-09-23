# 译文复核观察报告：entry-03212 至 entry-03251（共40条）

本报告基于冻结输入、`entries.json`、`context.lua` 以及 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下的冻结源码完成独立只读复核。以下输出为审核观察记录，不声称生产 `DONE_VERIFIED`。

---

## 40条复核判定汇总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03212 | 未发现问题 | 属性加成标题描述准确，冒号与排版一致 |
| entry-03213 | 未发现问题 | 术语符合规范（combat/_t/preferred），全角冒号规范 |
| entry-03214 | 未发现问题 | 术语符合规范（combat/_t/preferred），全角冒号规范 |
| entry-03215 | 未发现问题 | 术语符合规范（combat/_t/preferred），全角冒号规范 |
| entry-03216 | 未发现问题 | 技能树点数获取等级（10、20、34）与机制一致，段落完整 |
| entry-03217 | 未发现问题 | 切换简单显示快捷键与UI提示准确 |
| entry-03218 | 未发现问题 | 切换进阶显示快捷键与UI提示准确 |
| entry-03219 | 存在问题 | C01 |
| entry-03220 | 未发现问题 | 颜色代码与新任务提示完整准确 |
| entry-03221 | 未发现问题 | 颜色代码保留，任务日志/面板交互指引准确 |
| entry-03222 | 仅建议 | C02 |
| entry-03223 | 未发现问题 | 4个 `%s` 占位符与颜色代码顺序一致 |
| entry-03224 | 未发现问题 | 3个 `%s` 占位符与颜色代码顺序一致 |
| entry-03225 | 未发现问题 | 商店最高收购预算与自身金币占位符格式一致，保留前置空格 |
| entry-03226 | 未发现问题 | 替换即爆状态后缀语义完整，保留前置空格 |
| entry-03227 | 未发现问题 | 即爆状态后缀语义完整，保留前置空格 |
| entry-03228 | 未发现问题 | 陷阱已准备状态标签完整 |
| entry-03229 | 未发现问题 | 陷阱准备中状态标签完整 |
| entry-03230 | 未发现问题 | 陷阱拆解状态标签完整 |
| entry-03231 | 存在问题 | C03 |
| entry-03232 | 未发现问题 | 无法准备陷阱日志占位符与颜色格式完整 |
| entry-03233 | 未发现问题 | 陷阱精通技能等级不足提示准确 |
| entry-03234 | 未发现问题 | 恢复常规触发状态日志提示准确 |
| entry-03235 | 未发现问题 | 陷阱准备数量上限 `%d` 占位符与逻辑一致 |
| entry-03236 | 未发现问题 | 觉醒技核心属性50及25/42级获取机制准确，占位符保留 |
| entry-03237 | 未发现问题 | 解锁提示占位符与格式准确 |
| entry-03238 | 未发现问题 | 附魔/插件无可用装备提示完整准确 |
| entry-03239 | 未发现问题 | 流浪者职业随机技能树说明完整准确 |
| entry-03240 | 未发现问题 | 调试角色升级等级输入框前后空格与格式一致 |
| entry-03241 | 未发现问题 | 调试还原备份占位符与版本号格式一致 |
| entry-03242 | 未发现问题 | 调试设置基础属性输入框前后空格与格式一致 |
| entry-03243 | 未发现问题 | 调试设置额外属性输入框前后空格与格式一致 |
| entry-03244 | 未发现问题 | 调试解锁并学习技能输入框末尾空格与格式一致 |
| entry-03245 | 未发现问题 | 调试角色输入日志占位符与颜色代码一致 |
| entry-03246 | 未发现问题 | 调试阵营变更弹窗占位符一致 |
| entry-03247 | 未发现问题 | 调试物品加载日志占位符与换行缩进一致 |
| entry-03248 | 未发现问题 | 调试生成样品复选框末尾空格与说明一致 |
| entry-03249 | 未发现问题 | 调试物品生成错误日志占位符与换行格式一致 |
| entry-03250 | 未发现问题 | 调试错误弹窗占位符与换行格式一致 |
| entry-03251 | 未发现问题 | 调试玩家标识前置空格与颜色代码一致 |

---

## 观察与 Claim 详情

### C01 | entry-03219 | 存在问题
- **原文短引**：`%s cannot receive items while asleep!`
- **译文短引**：`%s不能在睡眠中接收物品！`
- **问题具体内容**：面向玩家的机制误述（沿袭上游描述，非翻译新增）。源码中将“目标无物品栏空间”与“目标处于睡眠”在同一个 `if` 逻辑分支中判定并统一输出此条日志。当队友处于清醒状态但背包已满时，玩家尝试转移物品同样会触发此消息，向玩家误报队友“在睡眠中”。译文忠实还原英文原文，无翻译新增错误，但沿袭了上游代码导致的事实/触发条件误导。
- **状态**：存在问题（沿袭上游描述）
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/PartySendItem.lua:53-56`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/PartySendItem.lua#L53-L56) 中的 `_M:use(item)` 函数：
  ```lua
  if not item or not item.actor:canAddToInven(item.actor.INVEN_INVEN) or (item.actor:attr("sleep") and not item.actor:attr("lucid_dreamer")) then
      game.log("%s cannot receive items while asleep!", item.actor:getName():capitalize())
      return
  end
  ```
  消费逻辑为玩家在队友物品转移界面确认交付时，通过 `game.log` 向控制台输出操作失败原因。

---

### C02 | entry-03222 | 仅建议
- **原文短引**：`Keyboard: ... right key ... left key ...`
- **译文短引**：`键盘：... 右键 ... 左键 ...`
- **问题具体内容**：措辞偏好建议。在键盘操作说明中将 `right key` 和 `left key` 译为“右键”和“左键”，在中文直觉下容易与鼠标“左键/右键”产生表面混淆。若表达为“右方向键”与“左方向键”（或“方向键右/左”），与下一行“鼠标：#00FF00#左键点击...右键点击...”对比时更清晰工整。然而鉴于本句已位于明确的“键盘：”段落内且紧随“上/下键”，玩家实际操作不会产生实质误解，故仅属表达偏好。
- **状态**：仅建议
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/SentientWeapon.lua:53-56, 195-196`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/SentientWeapon.lua#L53-L56) 中的 `_M:init` 与 `_M:drawDialog`。消费逻辑为智能武器属性调整界面顶部说明区域文本。

---

### C03 | entry-03231 | 存在问题
- **原文短引**：` (need more skill)`
- **译文短引**：` （需要更多技能）`
- **问题具体内容**：语义与机制条件误译（翻译新增）。源码判断条件为 `item.tier > self.mastery_level`，其中 `self.mastery_level` 为当前玩家“陷阱精通”（Trap Mastery）技能的等级（1–5）。英文中 `skill` 为不可数名词，在此语境指技能熟练度/技能等级（即需要更高的陷阱技能等级）。译文译为“需要更多技能”，使玩家误以为需要去学习更多数量的其他技能。对比同文件同一触发条件的日志条目 entry-03233（[`TrapsSelect.lua:143`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua#L143)），该处已被正确译为“你的技能等级不足，无法准备这个陷阱。”，证明 entry-03231 存在对机制条件的理解与翻译偏差。
- **状态**：存在问题（翻译新增）
- **源码路径与调用逻辑**：[`game/modules/tome/dialogs/TrapsSelect.lua:122-124`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/sources/game/modules/tome/dialogs/TrapsSelect.lua#L122-L124) 中的 `_M:formatItem(item)`：
  ```lua
  elseif item.tier > self.mastery_level then
      item.color = colors_simple.GREY
      add_text = _t" (need more skill)"
  ```
  消费逻辑为在陷阱选择对话框中，当陷阱阶数（tier）超出玩家当前精通等级时，作为置灰后缀字符串拼接到条目名称尾部显示。

---

## 核验边界与路径记录

1. **实际读取的所有路径与版本**：
   - 输入配置与上下文：
     - [`evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/INPUT.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/INPUT.md)
     - [`evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/source-access.json)
     - [`evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/entries.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/entries.json)
     - [`evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/context.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-b096-20260923/context.lua)
   - 冻结源码（commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，路径位于本实验包 `sources/` 目录下）：
     - `game/modules/tome/dialogs/LevelupDialog.lua`
     - `game/modules/tome/dialogs/PartySendItem.lua`
     - `game/modules/tome/dialogs/QuestPopup.lua`
     - `game/modules/tome/dialogs/SentientWeapon.lua`
     - `game/modules/tome/dialogs/ShowIngredients.lua`
     - `game/modules/tome/dialogs/ShowLore.lua`
     - `game/modules/tome/dialogs/ShowStore.lua`
     - `game/modules/tome/dialogs/TrapsSelect.lua`
     - `game/modules/tome/dialogs/UberTalent.lua`
     - `game/modules/tome/dialogs/UnlockDialog.lua`
     - `game/modules/tome/dialogs/UseItemDialog.lua`
     - `game/modules/tome/dialogs/WandererSeed.lua`
     - `game/modules/tome/dialogs/debug/AdvanceActor.lua`
     - `game/modules/tome/dialogs/debug/AlterFaction.lua`
     - `game/modules/tome/dialogs/debug/CreateItem.lua`

2. **额外源码路径的调用链来源**：
   - 无。所有条目的 UI 显示、字符串格式化及逻辑触发分支均由上述 15 份已授权冻结源码完全覆盖，未引入额外源码文件。

3. **无法核验或越界说明**：
   - 全程无无法核验条目。
   - 无任何越界访问；未扫描工作树外部代码或未授权目录；未创建子 agent；未修改任何仓库或生产文件；未读取其他实验报告或对比结论。
