### batch-006 译文复核报告（entry-00203 至 entry-00240）

#### 1. 前置文件哈希校验
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-006.md`
- **预期 SHA-256**：`efb3487acdc338d72f4fd082614988cd2eae762e614dc654f47853b17a37a700`
- **实测 SHA-256**：`efb3487acdc338d72f4fd082614988cd2eae762e614dc654f47853b17a37a700`
- **核验结论**：哈希一致，基线确认无误。公开源码读取均基于固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

---

#### 2. 逐条复核详情（共 38 条）

---

### entry-00203
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L368)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8011) `doWear`/`doTakeoff`（line 8011, 8078）：
  ```lua
  if self:attr("sleep") and not self:attr("lucid_dreamer") then
      game.logPlayer(self, "You cannot change your equipment while sleeping!")
      return
  end
  ```
- **原文**：`You cannot change your equipment while sleeping!`
- **译文**：`你不能在睡眠中切换装备！`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，感叹号标点一致。在非清醒梦状态处于睡眠时禁止穿脱装备，译文语义及术语（sleep -> 睡眠，equipment -> 装备）准确。

---

### entry-00204
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L369)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8015) `doWear`/`doTakeoff`/`doWearTinker`（line 8015, 8082, 8177, 8213）：
  ```lua
  if self:attr("no_equipment_changes") then
      game.logPlayer(self, "You cannot change your equipment!")
      return
  end
  ```
- **原文**：`You cannot change your equipment!`
- **译文**：`你不能切换装备！`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，感叹号匹配，准确表达 `no_equipment_changes` 属性对装备更换操作的限制。

---

### entry-00205
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L375)（section: `mod-tome/class/Actor.lua`，source_tag: `_t`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8156) `transmoHelpPopup`：
  ```lua
  Dialog:simplePopup(_t"Transmogrification Chest", _t"When you close the inventory window, all items in the chest will be transmogrified.")
  ```
- **原文**：`When you close the inventory window, all items in the chest will be transmogrified.`
- **译文**：`当你关闭物品栏的时候，所有在转化之盒里的物品都会被自动转化。`
- **复核结论**：**未发现问题**
- **可核验依据**：句末句号一致，无占位符。术语“转化之盒（Transmogrification Chest）”、“物品栏（inventory window）”与转化机制说明准确。

---

### entry-00206
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L378)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8219) `doWearTinker`：
  ```lua
  if not base_o then
      game.logPlayer(self, "You can not use a tinker without the corresponding item.")
      return
  end
  ```
- **原文**：`You can not use a tinker without the corresponding item.`
- **译文**：`你不能在没有相关物品时使用配件。`
- **复核结论**：**未发现问题**
- **可核验依据**：句末句号匹配。在装备配件（tinker）但未选定或不存在底模基础装备（base_o）时的日志提示，译文“配件”与“相关物品”语义准确。

---

### entry-00207
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L379)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8224) `doWearTinker`：
  ```lua
  local ok, err = self:canUseTinker(wear_o)
  if not ok then
      game.logPlayer(self, "This item is not usable: %s.", err)
      return
  end
  ```
- **原文**：`This item is not usable: %s.`
- **译文**：`该物品不能使用：%s。`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配且位置正确，冒号与句末标点匹配，参数 `err` 为无法使用原因。

---

### entry-00208
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L380)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8227) `doWearTinker`（line 8227, 8231, 8235, 8239）：
  ```lua
  if wear_o.on_type and wear_o.on_type ~= rawget(base_o, "type") then
      game.logPlayer(self, "This tinker can not be applied to this item.")
      return
  end
  ```
- **原文**：`This tinker can not be applied to this item.`
- **译文**：`这个配件不能装在该物品上。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句末句号匹配。准确反映配件与目标装备类型/部位不符时的行为。

---

### entry-00209
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L381)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8243) `doWearTinker`：
  ```lua
  if base_o.tinker then
      if not can_remove then
          game.logPlayer(self, "You already have a tinker on this item.")
          return
  ```
- **原文**：`You already have a tinker on this item.`
- **译文**：`这个物品上已经有了配件。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句末句号匹配，机制判定为目标物品已装有配件且不可直接替换时的提示。

---

### entry-00210
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L382)（section: `mod-tome/class/Actor.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L8267) `doWearTinker`：
  ```lua
  game.logPlayer(self, "You attach %s to your %s.", wear_o:getName{do_color=true}, base_o:getName{do_color=true})
  ```
- **原文**：`You attach %s to your %s.`
- **译文**：`你将%s附着于%s。`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符数量（2个 `%s`）及顺序（第1个为配件名称 `wear_o`，第2个为本体装备名称 `base_o`）与源码调用完全对应，句末标点一致。

---

### entry-00211
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L395)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L44) `listGivers` 战士护送：
  ```lua
  name = _t"%s, the lost warrior",
  ```
- **原文**：`%s, the lost warrior`
- **译文**：`%s，迷路的战士`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，逗号对应中文全角逗号。此处为护送任务中战士 NPC 实体名称，译为“战士”符合语境。

---

### entry-00212
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L398)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L67) `listGivers` 先知护送：
  ```lua
  name = _t"%s, the injured seer",
  ```
- **原文**：`%s, the injured seer`
- **译文**：`%s，受伤的先知`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，全角逗号对应半角逗号，seer 译作“先知”准确。

---

### entry-00213
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L400)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L91) `listGivers` 盗贼护送：
  ```lua
  name = _t"%s, the repented thief",
  ```
- **原文**：`%s, the repented thief`
- **译文**：`%s，忏悔的盗贼`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，逗号对应中文全角逗号，语义准确。

---

### entry-00214
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L401)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L124) `listGivers` 炼金术师护送：
  ```lua
  name = _t"%s, the lone alchemist",
  ```
- **原文**：`%s, the lone alchemist`
- **译文**：`%s，落单的炼金术师`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，术语 `Alchemist` 译为“炼金术师”，符合术语库标准条目。

---

### entry-00215
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L402)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L150) `listGivers` 太阳骑士护送：
  ```lua
  name = _t"%s, the lost sun paladin",
  ```
- **原文**：`%s, the lost sun paladin`
- **译文**：`%s，迷路的太阳骑士`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，术语 `Sun Paladin` 译为“太阳骑士”，符合术语库标准条目。

---

### entry-00216
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L403)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L176) `listGivers` defiler 护送：
  ```lua
  defiler = {
      chance = 70,
      classes = {"Corruptor", "Reaver"},
      escort = { name="lost defiler", random="female",
          actor = {
              name = _t"%s, the lost defiler", ...
  ```
- **原文**：`%s, the lost defiler`
- **译文**：`%s，迷路的腐化者`
- **复核结论**：**细微观察**
- **可核验依据**：在 ToME4 机制中，`Defiler` 是职业大系（对应术语库 `Defiler -> 堕落系`），包含 `Corruptor`（腐化者）与 `Reaver`（收割者）。此处护送 NPC 原文为 `defiler`，涵盖 Corruptor 与 Reaver 两类子职业，而译文将其译为「腐化者」，与具体职业名称 `Corruptor`（腐化者）产生重合；若该 NPC 实际职业判定为 Reaver 时，称谓称作“腐化者”在概念上有重叠之嫌（通常概念对应“堕落者”）。占位符 `%s` 与标点格式本身无语法错误。

---

### entry-00217
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L410)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L211) `listGivers` 时空探索者护送：
  ```lua
  name = _t"%s, temporal explorer",
  ```
- **原文**：`%s, temporal explorer`
- **译文**：`%s，时空旅行者`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，全角逗号匹配。结合剧情台词（“ME?! So I was right, this is not my original time-thread!”），译为“时空旅行者”贴合时间线穿越背景，符合习惯。

---

### entry-00218
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L412)（section: `mod-tome/class/EscortRewards.lua`，source_tag: `_t`）
- **固定源码参照**：[`EscortRewards.lua`](file:///workspace/t-engine4/game/modules/tome/class/EscortRewards.lua#L241) `listGivers` 贤者护送：
  ```lua
  name = _t"%s, the worried loremaster",
  ```
- **原文**：`%s, the worried loremaster`
- **译文**：`%s，担忧的贤者`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%s` 匹配，全角逗号匹配，loremaster 译为“贤者”符合习惯。

---

### entry-00219
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L451)（section: `mod-tome/class/Game.lua`，source_tag: `_t`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L168)：
  ```lua
  local s = core.display.drawStringBlendedNewSurface(lfont, _t"<Scroll mode, press direction keys to scroll, press again to exit>", unpack(colors.simple(colors.GOLD)))
  ```
- **原文**：`<Scroll mode, press direction keys to scroll, press again to exit>`
- **译文**：`<地图滚动模式，按方向键滚动地图，再次按键退出>`
- **复核结论**：**未发现问题**
- **可核验依据**：定界符 `<...>` 完整保留，无占位符，全角逗号对应英文半角逗号，功能说明准确。

---

### entry-00220
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L462)（section: `mod-tome/class/Game.lua`，source_tag: `tformat`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L827) `getVaultDescription`：
  ```lua
  name = ([[%s the %s %s]]):tformat(e.name, _t(e.descriptor.subrace, "birth descriptor name"), _t(e.descriptor.subclass, "birth descriptor name")),
  ```
- **原文**：`%s the %s %s`
- **译文**：`%s，%s %s`
- **复核结论**：**未发现问题**
- **可核验依据**：3 个 `%s` 占位符齐全且顺序一致（角色名、种族、职业）；中文将定冠词“the”转换为“，”符合中文角色名衔称述习惯。

---

### entry-00221
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L469)（section: `mod-tome/class/Game.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L925) `changeLevelCheck`：
  ```lua
  if not self.player.can_change_level then
      self.logPlayer(self.player, "#LIGHT_RED#You may not change level without your own body!")
      return false
  end
  if zone and not self.player.can_change_zone then
      self.logPlayer(self.player, "#LIGHT_RED#You may not leave the zone with this character!")
      return false
  end
  ```
- **原文**：`#LIGHT_RED#You may not change level without your own body!`
- **译文**：`#LIGHT_RED#你只能用自己的身体离开地图！`
- **复核结论**：**细微观察**
- **可核验依据**：
  1. 概念混淆：在源码中，`level`（楼层/层）与 `zone`（区域/地图）有严格区分。本句检查的是 `can_change_level`（上下楼梯或换层），而下一句（entry-00222）检查的才是 `can_change_zone`（离开整个区域/地图）。译文将“change level”译为“离开地图”，既容易造成玩家误以为自己在尝试脱离大地图，又与 entry-00222（离开地图）概念重合。
  2. 颜色标记 `#LIGHT_RED#` 及感叹号保留完整，无占位符。

---

### entry-00222
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L470)（section: `mod-tome/class/Game.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L929) `changeLevelCheck`：
  ```lua
  if zone and not self.player.can_change_zone then
      self.logPlayer(self.player, "#LIGHT_RED#You may not leave the zone with this character!")
      return false
  end
  ```
- **原文**：`#LIGHT_RED#You may not leave the zone with this character!`
- **译文**：`#LIGHT_RED#你不能用这个角色离开地图！`
- **复核结论**：**未发现问题**
- **可核验依据**：颜色标记 `#LIGHT_RED#` 匹配，无占位符，标点匹配。此处置处于 `can_change_zone` 判定（脱离区域），译为“离开地图”符合语境。

---

### entry-00223
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L471)（section: `mod-tome/class/Game.lua`，source_tag: `logPlayer`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L933) `changeLevelCheck`：
  ```lua
  if self.player:hasEffect(self.player.EFF_PARADOX_CLONE) or self.player:hasEffect(self.player.EFF_IMMINENT_PARADOX_CLONE) then
      self.logPlayer(self.player, "#LIGHT_RED#You cannot escape your fate by leaving the level!")
      return false
  end
  ```
- **原文**：`#LIGHT_RED#You cannot escape your fate by leaving the level!`
- **译文**：`#LIGHT_RED#你不能离开地图以求逃避命运！`
- **复核结论**：**细微观察**
- **可核验依据**：颜色标记 `#LIGHT_RED#` 与感叹号一致。该限制由时空克隆体（`EFF_PARADOX_CLONE`）触发，禁止玩家通过楼梯离开当前楼层逃避克隆异相。原文为 `leaving the level`（离开当前楼层/离开该层），译文表述为“离开地图”。虽然叙事含义通畅，但严格机制对应为“楼层”。

---

### entry-00224
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L475)（section: `mod-tome/class/Game.lua`，source_tag: `_t`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L1000)：
  ```lua
  table.insert(choices, {name=_t"Debug the problem (move to the failed zone/level)", choice="debug"})
  ```
- **原文**：`Debug the problem (move to the failed zone/level)`
- **译文**：`调试问题（进入失败的地图/楼层）`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，括号与斜杠标点一致，zone/level 准确译为“地图/楼层”，语义清晰。

---

### entry-00225
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L496)（section: `mod-tome/class/Game.lua`，source_tag: `logMessage`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L1740)：
  ```lua
  game.uiset.logdisplay(self:logMessage(src, dams.srcSeen, target, dams.tgtSeen, "#Source# hits #Target# for %s (#RED##{bold}#%0.0f#LAST##{normal}# total damage)%s.", table.concat(dams.descs, ", "), dams.total, dams.healing<0 and (" #LIGHT_GREEN#[%0.0f healing]#LAST#"):tformat(-dams.healing) or ""))
  ```
- **原文**：`#Source# hits #Target# for %s (#RED##{bold}#%0.0f#LAST##{normal}# total damage)%s.`
- **译文**：`#Source#击中#Target#造成%s (#RED##{bold}#%0.0f#LAST##{normal}#合计伤害)%s。`
- **复核结论**：**未发现问题**
- **可核验依据**：
  1. 宏替换标记 `#Source#`、`#Target#` 保持原样；
  2. 样式与颜色标记 `#RED#`、`#{bold}#`、`#LAST#`、`#{normal}#` 配对完整；
  3. 占位符 `%s`（伤害类型拆分文本）、`%0.0f`（总伤害数值）、`%s`（治疗/吸收附加项）数量、顺序与类型均完全一致；
  4. 括号与句末标点位置无误。

---

### entry-00226
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L501)（section: `mod-tome/class/Game.lua`，source_tag: `tformat`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L1756)：
  ```lua
  self.flyers:add(sx, sy, 30, (rng.range(0,2)-1) * 0.5, rng.float(-2.5, -1.5), ("Kill (%d)!"):tformat(dams.total), {255,0,255}, true)
  ```
- **原文**：`Kill (%d)!`
- **译文**：`杀死 (%d)！`
- **复核结论**：**细微观察**
- **可核验依据**：占位符 `%d` 与括号、感叹号均匹配。此字符串为敌人死亡时在地图实体上方弹出的伤害飘字（flyer），常规游戏用语中多表达为“击杀 (%d)！”；“杀死 (%d)！”略带直译色彩，但含义准确。

---

### entry-00227
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L503)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2021) `setTacticalMode`：
  ```lua
  if not silent then self.log("Showing big healthbars and tactical borders.") end
  ```
- **原文**：`Showing big healthbars and tactical borders.`
- **译文**：`显示大血条+边框。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句末句号匹配。“大血条+边框”为界面战术模式快捷切换提示，表达简练且对应机制。

---

### entry-00228
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L504)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2026) `setTacticalMode`：
  ```lua
  if not silent then self.log("Showing healthbars only.") end
  ```
- **原文**：`Showing healthbars only.`
- **译文**：`只显示血条信息。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句号匹配，语义准确。

---

### entry-00229
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L505)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2031) `setTacticalMode`：
  ```lua
  if not silent then self.log("Showing no tactical information.") end
  ```
- **原文**：`Showing no tactical information.`
- **译文**：`不显示战术信息。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句号匹配，战术信息（tactical information）术语一致。

---

### entry-00230
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L506)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2036) `setTacticalMode`：
  ```lua
  if not silent then self.log("Showing small healthbars and tactical borders.") end
  ```
- **原文**：`Showing small healthbars and tactical borders.`
- **译文**：`显示小血条+边框。`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，句号匹配，与 entry-00227 格式呼应保持一致。

---

### entry-00231
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L510)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2210) 与 [`Map.lua`](file:///workspace/t-engine4/game/engines/default/engine/Map.lua#L1508)：
  ```lua
  local dir = game.level.map:compassDirection(seen[1].x - self.player.x, seen[1].y - self.player.y)
  self.log("You may not auto-explore with enemies in sight (%s to the %s%s)!", seen[1].actor:getName(), dir, self.level.map:isOnScreen(seen[1].x, seen[1].y) and "" or " - offscreen")
  ```
- **原文**：`You may not auto-explore with enemies in sight (%s to the %s%s)!`
- **译文**：`当有敌人在视野里时，你不能自动探索！(%s 在 %s方%s)！`
- **复核结论**：**存在疑点**
- **可核验依据**：
  1. **标点不一致（双感叹号）**：英文原文全句仅在括号外末尾有一个感叹号（`(...)!`）；译文在括号前额外增加了一个感叹号（`...自动探索！(...)！`），导致全句出现双感叹号。
  2. **方位词后缀重复拼接**：第二个占位符 `%s` 传入的是 `compassDirection` 返回的 `_t(dir)`。在 `engine.lua` 中，8 个基本方位词均已翻译为带“面”字的表述（例如 `north` -> `北面`、`southwest` -> `西南面` 等）。译文在 `%s` 后硬编码了“方”字（`在 %s方`），运行时将被格式化为「在 北面方」或「在 东南面方」，存在语素重复。

---

### entry-00232
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L532)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2477) `LOOK_AROUND`：
  ```lua
  self.log("Looking around... (direction keys to select interesting things, shift+direction keys to move freely)")
  ```
- **原文**：`Looking around... (direction keys to select interesting things, shift+direction keys to move freely)`
- **译文**：`正在观察四周…（按方向键定位有趣的东西，按 Shift+方向键自由移动）`
- **复核结论**：**未发现问题**
- **可核验依据**：省略号 `...` 对应 `…`，括号 `()` 对应全角括号 `（）`，操作按键说明准确，无占位符。

---

### entry-00233
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L533)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2532) `TOGGLE_BUMP_ATTACK`：
  ```lua
  self.log("Movement Mode: #LIGHT_GREEN#Default#LAST#.")
  ```
- **原文**：`Movement Mode: #LIGHT_GREEN#Default#LAST#.`
- **译文**：`移动模式：#LIGHT_GREEN#默认#LAST#。`
- **复核结论**：**未发现问题**
- **可核验依据**：颜色代码 `#LIGHT_GREEN#` 与闭合标签 `#LAST#` 完整一致，冒号与句号对应无误。

---

### entry-00234
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L534)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2535) `TOGGLE_BUMP_ATTACK`：
  ```lua
  self.log("Movement Mode: #LIGHT_RED#Passive#LAST#.")
  ```
- **原文**：`Movement Mode: #LIGHT_RED#Passive#LAST#.`
- **译文**：`移动模式：#LIGHT_RED#被动#LAST#。`
- **复核结论**：**未发现问题**
- **可核验依据**：颜色代码 `#LIGHT_RED#` 与闭合标签 `#LAST#` 完整一致，标点规范，语义准确。

---

### entry-00235
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L535)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2666)：
  ```lua
  if target then game._cheat_move_actor = target game.log("#GOLD#CHEAT MOVE ACTOR %s: ctrl+shift+alt+right click on an empty map spot to move it", target:getName())
  ```
- **原文**：`#GOLD#CHEAT MOVE ACTOR %s: ctrl+shift+alt+right click on an empty map spot to move it`
- **译文**：`#GOLD#CHEAT MOVE ACTOR %s: Ctrl+Shift+Alt+右键点击地图上的空白位置来移动它`
- **复核结论**：**未发现问题**
- **可核验依据**：颜色标签 `#GOLD#` 保留，占位符 `%s` 保留且位置准确，作弊指令前缀保留英文原样，按键操作说明翻译准确。

---

### entry-00236
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L540)（section: `mod-tome/class/Game.lua`，source_tag: `log`）
- **固定源码参照**：[`Game.lua`](file:///workspace/t-engine4/game/modules/tome/class/Game.lua#L2885) 存盘日志：
  ```lua
  self.log("Saving game...")
  ```
- **原文**：`Saving game...`
- **译文**：`保存游戏…`
- **复核结论**：**未发现问题**
- **可核验依据**：无占位符，省略号对应 `…`，简练准确。

---

### entry-00237
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L578)（section: `mod-tome/class/GameState.lua`，source_tag: `_t`）
- **固定源码参照**：[`GameState.lua`](file:///workspace/t-engine4/game/modules/tome/class/GameState.lua#L3400) 无尽地下城和平主义者挑战：
  ```lua
  self:makeChallengeQuest(level, _t"Pacifist", _t"Leave the level (to the next level) without killing a single creature. You will get #{italic}#two#{normal}# rewards.", ...
  ```
- **原文**：`Leave the level (to the next level) without killing a single creature. You will get #{italic}#two#{normal}# rewards.`
- **译文**：`在不杀死任何怪物的情况下离开这一层（到达下一层）。你将得到#{italic}#两份#{normal}# 奖励。`
- **复核结论**：**未发现问题**
- **可核验依据**：斜体标记 `#{italic}#` 与恢复标签 `#{normal}#` 配对完整，无占位符，挑战机制说明准确。

---

### entry-00238
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L586)（section: `mod-tome/class/GameState.lua`，source_tag: `tformat`）
- **固定源码参照**：[`GameState.lua`](file:///workspace/t-engine4/game/modules/tome/class/GameState.lua#L3450) 无尽地下城决胜时刻挑战：
  ```lua
  ("Proceed directly to the next Infinite Dungeon level in less than %d turns (an exit is revealed on your map)."):tformat(turns)
  ```
- **原文**：`Proceed directly to the next Infinite Dungeon level in less than %d turns (an exit is revealed on your map).`
- **译文**：`在%d回合内到达无尽地下城的下一层（出口已标记在地图上）。`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%d` 匹配，括号与句号匹配，专有名词 `Infinite Dungeon` 对应标准术语“无尽地下城”，语义完整。

---

### entry-00239
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L587)（section: `mod-tome/class/GameState.lua`，source_tag: `tformat`）
- **固定源码参照**：[`GameState.lua`](file:///workspace/t-engine4/game/modules/tome/class/GameState.lua#L3453) 动态描述：
  ```lua
  desc[#desc+1] = ("Turns left: #LIGHT_GREEN#%d"):tformat(self.turns_left)
  ```
- **原文**：`Turns left: #LIGHT_GREEN#%d`
- **译文**：`剩余回合：#LIGHT_GREEN#%d`
- **复核结论**：**未发现问题**
- **可核验依据**：占位符 `%d` 与颜色标签 `#LIGHT_GREEN#` 完整，冒号匹配，无遗漏闭合符（原文源码亦无 `#LAST#`）。

---

### entry-00240
- **位置与源语境**：[mod-tome.lua](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L588)（section: `mod-tome/class/GameState.lua`，source_tag: `log`）
- **固定源码参照**：[`GameState.lua`](file:///workspace/t-engine4/game/modules/tome/class/GameState.lua#L3470)：
  ```lua
  game.log("\n#ORCHID# Rush Hour: %s turns left!\n", self.turns_left)
  ```
- **原文**：
  ```text

  #ORCHID# Rush Hour: %s turns left!

  ```
- **译文**：
  ```text

  #ORCHID#决胜时刻：剩余%s回合！

  ```
- **复核结论**：**未发现问题**
- **可核验依据**：首尾换行符完整一致，颜色代码 `#ORCHID#` 匹配，占位符 `%s` 匹配，任务名“Rush Hour”对应“决胜时刻”，标点规范。

---

#### 3. 统计汇总
- **复核总数**：38 条（entry-00203 至 entry-00240）
- **未发现问题**：34 条
- **细微观察**：3 条（entry-00216、entry-00221、entry-00226）
- **存在疑点**：1 条（entry-00231）