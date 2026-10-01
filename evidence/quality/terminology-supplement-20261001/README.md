# 术语库补录（2026-10-01）

维护者指示“先补术语库”。本次只补录术语行，不改任何译文。

## 方法

1. `dump.py`：以 LuaJIT 加载 manifest 声明的 11 个译文组件，共 30,308 条，导出到 `.artifacts/i18n/term-completeness/entries.json`（派生产物，未跟踪）。
2. `coverage.py`：按名称类 `source_tag` 统计术语库覆盖率，结果见 `coverage.json`。
3. `candidates.py`：在长文本（`tformat`、`_t`、日志、对话等）中按英文词边界统计引用次数，并检查引用处译文是否包含该名称的现译。
   - 未收录的多词技能名：被引用 ≥2 次的 124 个。
   - 未收录的大写专名：被引用 ≥3 次的 48 个；另加 `losgoroth`。
   - 统计结果见 `candidates.json`。
4. 宿主逐条复核不一致的引用：
   - 剔除普通词：Movement、Talents、Forge、Smith，以及与技能名重复的实体 Radiance。
   - 区分两类不一致：一类是省略或改写（召唤技能指代生物本身、报错提示省略技能名、Spiked X Shield 是另一技能等），另一类是真实的译名漂移。
5. `build_rows.py`：生成 181 行，见 `new_rows.tsv`（首列为目标文件）。
   - 正文机制词沿用既有 `tformat` 行惯例：Accuracy、Defense、critical、talent level。
   - 三类豁免、Melee、Armour Hardiness、Feedback 使用实测存在的 `_t` 条目。

## 结果

- 新增 181 行：`existing` 158、`review` 22、`preferred` 1（The Master＝领主，维护者 2026-09-16 裁决）。
- 术语库共 915 行。
- 所有非 `tformat` 行（177 行）的 (source, source_tag, target) 均与 LuaJIT 加载的译文逐字一致。
- `existing` 只表示整理现有译法，不表示认可。

`review` 行表示引用处存在真实译名漂移，需要维护者决定统一方向：

| 原文 | 现名称译名 | 漂移说明 |
| --- | --- | --- |
| `Aether Avatar` | 以太之体 | 技能说明引用中写作“以太形态”（1/4 处）；待统一 |
| `Antimagic Shield` | 反魔法护盾 | 技能说明引用中另有“反魔盾”（1/2 处）；待统一 |
| `Avatar of a Distant Sun` | 日耀神使 | 职业进阶提示中写作“遥远太阳的化身”（1/4 处）；待统一 |
| `Burning Wake` | 无尽之焰 | 放电柱类技能说明中写作“无尽之炎”（2/5 处）；待统一 |
| `Called Shots` | 精准射击 | 标记说明中写作“精巧射击”（1/3 处）；待统一 |
| `Deeprock Form` | 深岩形态 | 技能说明引用中写作“深岩元素形态”（1/3 处）；待统一 |
| `Hidden Blades` | 隐匿刀锋 | 技能使用提示中写作“隐藏刀片”（1/3 处）；待统一 |
| `Hideous Visions` | 惊骇幻象 | 虚空之声说明中写作“失智冲击”（1/2 处）；待统一 |
| `Mana Gale` | 魔法风暴 | 游戏提示与越层效果说明中写作“法力风暴”（4/4 处引用）；待统一 |
| `Saw Wheels` | 链锯轮滑 | 技能说明引用中写作“链锯轮”（1/2 处）；待统一 |
| `Steamgun Mastery` | 蒸汽枪掌握 | 炮台说明中写作“蒸汽枪精通”（1/3 处）；待统一 |
| `Telekinetic Punt` | 念力打击 | 学习提示中写作“念力推送”（2/2 处引用）；待统一 |
| `Celia` | 赛利亚 | 墓地任务对话中写作“塞莉娅”（1/10 处）；待统一 |
| `Harkor'Zun` | 哈卡祖 | 物品描述中写作“哈克祖”（1/4 处）；待统一 |
| `Outpost Leader John` | 前哨站队长约翰 | 引用中有“前哨站首领约翰”“前哨站领袖约翰”（2/4 处）；待统一 |
| `Drolem` | 卓勒姆 | 实体名为“卓勒姆”，职业解锁与说明中均写作“龙傀儡”（4/4 处）；待统一 |
| `losgoroth` | 洛斯格罗斯 | 状态与日志中写作“罗斯戈洛斯”（5 处），实体名为“洛斯格罗斯”（7 处）；待统一 |
| `Phoenix` | 不死鸟 | 实体名“不死鸟”；传说标题 How to Summon a Phoenix 与状态 Reviving Phoenix 用“凤凰”；待确定是否同一所指 |
| `Automated Portable Extractor` | 便携式自动材料提取仪 | 任务对话中写作“便携式自动提取仪”（1/3 处）；待统一 |
| `Shoes of Moving Quickly` | 疾行之鞋 | 物品名为“疾行之鞋”，合成提示均写作“疾行之靴”（3/3 处）；待统一 |
| `Iron Throne Profits History` | 钢铁王座盈利历史 | 实体名无“的”，各篇传说标题均写作“钢铁王座的盈利历史”；待统一 |
| `Clinician Korbek's experimental notes` | 巫医库贝克的实验笔记 | 实体名为“实验笔记”，各篇传说标题与正文均写作“实验报告”（8/8 处）；待统一 |

另记：`critical` 有 1 处“爆击几率”属错字，待修复。

## 验证

- `tools/i18n lint --strict`：0 error。
- `tools/audit_static.py`：blocking 0，advisory 不增加。
- `tools/annotate_domains.py`：unmapped 0。新增实体 source 已登记到 ITEM_SOURCES 与 CREATURE_SOURCES。
- `tools/audit_dynamic.py`：S2.1/S2.2/S2.3 计数与补录前相同。
- `tools/classify_runtime_keys.py`：通过。
- 术语相关单测通过。`test_real_terminology_is_fully_mapped` 的行数断言随之由 734 改为 915。
- `git diff --check` 通过：空 notes 行已改为填写引用计数，避免行尾 TAB。
