# 批次 batch-069 译文复核报告

### 1. 批次哈希核对
- **目标文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-069.md`
- **预期 SHA-256**：`2c349073a9d239b6b816ccb0f216bc882fd8a79f4969d1ceefd3afc9fc9fec2b`
- **实测 SHA-256**：`2c349073a9d239b6b816ccb0f216bc882fd8a79f4969d1ceefd3afc9fc9fec2b`
- **核验结论**：哈希一致，冻结文件有效。

---

### 2. 条目逐条复核记录（entry-02148 至 entry-02187，共 40 条）

#### entry-02148 (`mod-tome.lua:27892`, `mod-tome/data/talents/psionic/slumber.lua`)
- **结论**：存在疑点 / 细微观察
- **依据**：
  1. **存在疑点（实体术语不一致）**：原文中 `dream projections` 与 `projections` 被译为“梦境守卫”。然而查阅固定 commit 源码 `timed_effects/other.lua:2042`，该实体生成时的名字为 `("%s's dream projection"):tformat(...)`，在译文文件 `mod-tome.lua:36642` 中对应译名为 `%s的梦境投影`；生成时的日志 `mod-tome.lua:36644` 为 `%s产生了一个梦境投影来保护自己的心智！`。技能描述中使用“梦境守卫”与游戏实际生成的实体名及日志“梦境投影”存在不一致。
  2. **细微观察**：原文 `brainlocked for one turn` 译文补充了“（可叠加）”。查源码 `other.lua:2207`：`eff.target:setEffect(eff.target.EFF_BRAINLOCKED, kills, {})`，持续回合数直接等于被击杀的投影数 `kills`，译文补充括号说明与底层机制相符，属于解释性增补。占位符 `%d`、`50%%`、`10%%`、`%d%%` 数量与顺序正确。

#### entry-02149 (`mod-tome.