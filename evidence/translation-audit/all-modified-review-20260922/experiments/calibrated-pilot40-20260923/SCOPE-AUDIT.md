# 共用机制术语范围审查

`scope=core` 当前确实表示适用组件范围，不是术语最早发现于本体。`TERMINOLOGY.md` 和 `tools/i18nlib/workset.py:247–257` 均将五个 DLC 组件排除在 core 外。因此旧审核用 core 行直接判 DLC 术语违规，不能成立。另一方面，游戏共用机制没有天然的语言隔离理由：应把确实共用的具体术语行调整到 global，而不是让 reviewer 临时绕开 scope。

本次筛查了 `T.GAME.STAT/DAMAGE/EFFECT/RESOURCE` 中全部78条 core 记录，原始逐行清单见 SCOPE-AUDIT.json。词形筛查只覆盖4144条修改清单，要求同 source_tag 和大小写一致的词边界；它不是全仓所有译文或所有 DLC 的覆盖证明。未命中不等于没有跨组件用途。

建议只修改下列3行的 scope，保留 source/target/category/tag/status。可检查补丁为 TERM-SCOPE-PROPOSAL.patch；尚未应用，冻结实验输入也未采用提案。

| 文件行 | 术语 / tag | 建议 | 证据 |
|---|---|---|---|
| terminology/combat.tsv:135 | global speed / _t | core → global | Orcs entry-03844 海报直接提到同一全局速度机制。它是叙事引用，不声称海报实际施加减速；现行 notes 本就包括叙述语境。 |
| terminology/combat.tsv:136 | global speed / tformat | core → global | Cults entry-03620 的 TWISTED_SPEED 写入 global_speed_add；Orcs entry-03973 Toxic Shell 施加 METAL_POISONING，physical.lua:805–815 写入同一属性。 |
| terminology/combat.tsv:140 | Physical Power / tformat | core → global | Orcs Steamgun Mastery 的 getDamage=30，Combat.lua superload:22 注册 T_STEAMGUN_MASTERY；固定本体 Combat.lua:1215–1219 读取训练增量，:1746 纳入 combatPhysicalpowerRaw。不是另造一个 DLC 属性。 |

源码路径前缀：`../abc20-20260923/sources/orcs/tome-orcs/`。速度调用来自 `data/talents/steam/other.lua:1833–1850` → `data/timed_effects/physical.lua:805–815`；物理强度来自 `data/talents/steam/gunner-training.lua:20–40` → `superload/mod/class/interface/Combat.lua:22`。Cults 佐证来自 `../abc20-20260923/sources/cults/tome-cults/data/timed_effects.lua:2219`。本体为 `/workspace/t-engine4` 的 `624a67329fe2ad440c5b344785a9c73fcf22ae63`，文件 `game/modules/tome/class/interface/Combat.lua`。DLC 均已核哈希，源码仓库/commit 和目标版本映射未固定；共享字段和调用的快照证据支持范围提案，不是目标发行版机制验收。

没有批量扩大的理由：

- `stone / _t` 的4处 DLC 命中都是普通石头语境，不能强套“石化”。
- `Life / _t` 命中出生页面 Life per level 文案；该行 notes 的面板标签与生命值说明需要语境区分，词出现并不证明整行约束适用。
- `Mana / _t`、`Vim / _t` 是 existing；这次没有借范围审查把它们提升成强制规范。
- `Global speed` 大写及 `global action speed` 等其他行，在本次修改清单没有同标签命中；不能由小写两行的证据替它们完成全局范围审查。

提案若后续应用，应另建只覆盖实际 target 受影响项的有界工作集，重新冻结术语来源；不追溯改写旧14组或10条校准的记录。
