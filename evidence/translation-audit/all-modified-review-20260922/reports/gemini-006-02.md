### 复核前置校验与环境信息

- **目标批次**：`batch-006`（条目 `entry-00201` 至 `entry-00240`，共 40 条）
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-006.md`
- **校验结果**：经核对，SHA-256 值为 `efb3487acdc338d72f4fd082614988cd2eae762e614dc654f47853b17a37a700`，与给定的冻结哈希完全一致。
- **源码比对基准**：固定公开 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取 `/workspace/t-engine4`）。本批全部 40 条条目均属于主游戏 `mod-tome` 模块，未涉及未固定 DLC 源码。
- **译文语境基准**：当前工作区 `mod-tome.lua`（commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`）。

---

### 逐条复核报告

#### entry-00201
- **位置**：`mod-tome.lua:359` ｜ **section**：`mod-tome/class/Actor.lua` ｜ **source_tag**：`logPlayer`
- **原文**：`You can not drop %s (plot item).`
- **译文**：`你不能丢弃%s（剧情物品）。`
- **复核结论**：未发现问题
- **核验依据**：固定源码 `game/modules/tome/class/Actor.lua:7958`（`game.logPlayer(self, "You can not drop %s (plot item).", o:getName{do_colour=true})`）。单个 `%s` 正确匹配物品名，中文全角括号与句号规范，剧情物品（plot item）判定机制与用词准确。

#### entry-00202
- **位置**：`mod-tome.lua:360` ｜ **section**：`mod-tome/class/Actor.lua` ｜ **source_tag**：`logPlayer`
- **原文**：`You can not drop %s (tagged).`
- **译文**：`你不能丢弃%s（已被标记）。`
- **复核结论**：未发现问题
- **核验依据**：固定源码 `Actor.lua:7963`（`game.logPlayer(self, "You can not drop %s (tagged).", o:getName{do_colour=true})`）。对应玩家给物品打标签标记防误丢机制，`%s` 占位符保留，语义准确。

#### entry-00203
- **位置**