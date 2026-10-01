# 修复窗口 63：意志之力 maces（1 条）

Paseo MCP / schema5 translation_contextual_v2 implement。基线 ba4a610931a0b0e235f173746be7c0155011d28d。

## 来源

- 第381批 `batch-4584eb6ddb5e3110acab` 宿主确认 1 条：意志之力（Strength of Purpose）把 maces 译作“权杖”。
- 审核队列清空后，用户 2026-10-01 选择“开窗口63修这 1 条”（未达 20 条阈值，经用户批准开窗）。

用户已授权修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。

## 写入权限

唯一 EXECUTOR 仅可修改以下内容：

- WORKSET.json 列出的 1 个 target（mod-tome.lua）；
- `evidence/quality/repair-window-63-20261001/` 下的修复证据。

不得修改：source、source_tag、section、args_order、运行键、其他译文、术语库、规则工具或旧证据。

不得 stage、commit、push，不得创建 agent，不得修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

## 改写要求

按 SOURCE-CLAIMS 的“修复：”与整句对照，只改第一行：

- “当使用剑、斧、权杖、匕首或者弓箭时，增加武器伤害 %d%%， 物理强度30。”
- 改为“当使用剑、斧、狼牙棒、匕首或者弓箭时，增加 %d%% 武器伤害和 30 点物理强度。”

第二、三行与 LF／`\t\t` 缩进结构不变。保留 `%d%%` 与 source_tag。

## 验证要求

- 用 LuaJIT 加载 mod-tome.lua，证明恰 1 个 target 变动、其他记录不变；
- 执行 strict lint 及 git diff --check。

无需完整门禁，宿主在独立复审后统一运行 17 项。

## 取证范围

- 主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证。
- 不扫 `/`、`/workspace` 或无关目录。

## 审查安排

- cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）。
- 收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。
- v2 FINAL 有任何 ISSUE 时，先修复并完成 RE_REVIEW，再重新 FINAL。max_cycles=5。
- reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。

## 宿主裁决依据

与已记录用户裁决相冲的指摘，宿主按裁决驳回。与本窗口修改无关的既有问题记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 6bba1ea093fbdbd9337545d78f19492567fabcd943fd86729a5f3aece736266a | mod-tome.lua | mod-tome/data/talents/chronomancy/guardian.lua | 固定 commit 624a673 game/modules/tome/data/talents/chronomancy/guardian.lua:22-38 意志之力（Strength of Purpose）info 原文 “when using swords, axes, maces, knives, or bows”，maces 指锤类武器；本库同句式的 data/talents/techniques/combat-training.lua:188 武器掌握（Weapons Mastery）“swords, axes or maces” 译“剑、斧、狼牙棒”，武器子类型 mace 作“锤子”，具体锤类物品作“狼牙棒”；权杖在本库专指 sceptre（大巫妖权杖、白骨雕刻的权杖）。现译“权杖”把锤类武器误作另一类物品，且与本条覆盖的武器掌握不一致。确认（contextual 判 OK，宿主以源码与本库译法为准）。修复：“剑、斧、权杖、匕首或者弓箭”→“剑、斧、狼牙棒、匕首或者弓箭”，其余不变。 同句整句对照：原文 “Increases weapon damage by %d%% and physical power by 30”，现译“增加武器伤害 %d%%， 物理强度30。”全角逗号后多一空格、后半缺谓语；一并改为“增加 %d%% 武器伤害和 30 点物理强度。”（physical power＝物理强度）。第二、三行不变。
