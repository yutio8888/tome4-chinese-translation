# 修复窗口 60：deeprock 技能树改名与 Korbek 实验笔记标题统一（6 条）

Paseo MCP / schema5 translation_contextual_v2 implement。基线 281ad0eff272259bf8c0bf67670c35a0ba7b7353。

来源：用户 2026-10-01 两项裁决。

- “将deeprock技能树修改为深岩”：技能树 deeprock 由“深岩形态”改为“深岩”。技能 Deeprock Form 保持“深岩形态”。deeprock 技能说明中明指技能名的 “while Deeprock Form is active” 随之由“深岩元素形态”改为“深岩形态”。共 2 条。
- “一并修复之前发现的非阻断问题”：Korbek 实验笔记 part one–four 的正文首行标题由“：一/二/三/四”改为“，第一/二/三/四部分”，与物品名一致（窗口59 ADJUDICATION-F2 advisory）。共 4 条。

另一项 advisory“恢复失衡值”已由用户裁定保留，不在本窗口。用户已授权合并修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。审核仍按用户要求暂停。

唯一 EXECUTOR 仅可修改以下内容：

- WORKSET.json 列出的 6 个 target（均在 mod-tome.lua）；
- TERM-EDITS.json 列出的 2 处术语改动（terminology/talents.tsv）；
- `evidence/quality/repair-window-60-20261001/` 下的修复证据。

不得修改 source、source_tag、section、args_order、运行键、其他译文、其他术语行、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

**先改术语库，再改译文。** TERM-EDITS.json 共两项：

- `old` 为 null 的一项：在 `insert_before` 那一整行之前插入 `new` 整行。
- 另一项：把 `old` 整行精确替换为 `new`。

字段间 TAB、其他行与行序不变，文件末尾换行保持。

**本窗口是定向修改，不是全文重译。** 每条只改 SOURCE-CLAIMS 点名的片段，其余字一个不动。尤其以下片段不得改：

- deeprock 技能说明第一行的“当你进入深岩元素形态时”（对应小写 while in deeprock form）；
- 其他对应 Deeprock Elemental 的“深岩元素形态”。

LF/TAB 结构与现译逐行一致。保留 printf 占位符、`%%`、`#{bold}#`/`#{normal}#` 等 markup 的数量、顺序及位置；保留 source_tag。

验证要求：

- 用 LuaJIT 加载 mod-tome.lua，证明恰 6 个 target 变动且其他记录不变；
- 用 Python 逐行比对 terminology/talents.tsv，证明只有 TERM-EDITS 的一行插入与一行替换；
- 执行 strict lint 及 git diff --check。

无需完整门禁，宿主在独立复审后统一运行 17 项。

取证范围：主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证，不扫 `/`、`/workspace` 或无关目录。

审查安排：

- cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）；确认的问题合并给一次 EXECUTOR fix。
- 收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL（同 cycle 用下一个 attempt）。max_cycles=5。
- reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。
- 与已记录用户裁决相冲的指摘由宿主按裁决驳回（深岩／深岩形态、恢复失衡值）；与本窗口修改无关的既有问题记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 1ebce25bfc96776d0baba0c17448747471b9b6bc02acf02d58b47f8fd2925219 | mod-tome.lua | mod-tome/data/talents/spells/deeprock.lua | 用户 2026-10-01 裁决（技能树改“深岩”，技能 Deeprock Form 保持“深岩形态”）：固定 commit 624a673 game/modules/tome/data/talents/spells/deeprock.lua:104-105 第二行 “while Deeprock Form is active” 明指技能名 Deeprock Form（大写专名），现译“在深岩元素形态下”与技能名“深岩形态”不一致（terminology/talents.tsv Deeprock Form 行 note 记录的 1/3 处漂移）。修复：仅第二行“在深岩元素形态下”→“在深岩形态下”；第一行“当你进入深岩元素形态时”（while in deeprock form，小写普通描述）不改，其余文字、占位符与换行不变。
- 233e49293ab2977f455a83e3031f8eed294ec429fd91cd2a001ff4a408e9dded | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 用户 2026-10-01 裁决“一并修复之前发现的非阻断问题”（窗口59 ADJUDICATION-F2 advisory）：固定 commit 624a673 game/modules/tome/data/lore/orc-prides.lua:322-323 中正文首行标题与物品名为同一英文串 “Clinician Korbek's experimental notes part …”，物品名译“巫医库贝克的实验笔记，第四部分”，本条正文标题却译“巫医库贝克的实验笔记：四”。修复：仅把首行 #{bold}#…#{normal}# 内的“巫医库贝克的实验笔记：四”→“巫医库贝克的实验笔记，第四部分”，markup、正文与换行不变。
- 58faaf57f67bf14953281c940ab862ed2a8b19ecdbfc1622e282750d8661c72f | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 用户 2026-10-01 裁决“一并修复之前发现的非阻断问题”（窗口59 ADJUDICATION-F2 advisory）：固定 commit 624a673 game/modules/tome/data/lore/orc-prides.lua:309-310 中正文首行标题与物品名为同一英文串 “Clinician Korbek's experimental notes part …”，物品名译“巫医库贝克的实验笔记，第三部分”，本条正文标题却译“巫医库贝克的实验笔记：三”。修复：仅把首行 #{bold}#…#{normal}# 内的“巫医库贝克的实验笔记：三”→“巫医库贝克的实验笔记，第三部分”，markup、正文与换行不变。
- 874773600493edbe38bc2e3b37b3866456fe6d23f15070d81f6aefd3fe76b0fe | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 用户 2026-10-01 裁决“一并修复之前发现的非阻断问题”（窗口59 ADJUDICATION-F2 advisory）：固定 commit 624a673 game/modules/tome/data/lore/orc-prides.lua:283-284 中正文首行标题与物品名为同一英文串 “Clinician Korbek's experimental notes part …”，物品名译“巫医库贝克的实验笔记，第一部分”，本条正文标题却译“巫医库贝克的实验笔记：一”。修复：仅把首行 #{bold}#…#{normal}# 内的“巫医库贝克的实验笔记：一”→“巫医库贝克的实验笔记，第一部分”，markup、正文与换行不变。
- 926d166627394205715e2e9fee61d7598939cd5685683fc2bf8000f5e939eca3 | mod-tome.lua | mod-tome/data/talents/spells/spells.lua | 用户 2026-10-01 裁决“将deeprock技能树修改为深岩”：固定 commit 624a673 game/modules/tome/data/talents/spells/spells.lua:78 newTalentType type="spell/deeprock", name=_t("deeprock","talent type")，是技能树名；现译“深岩形态”与该树下技能 Deeprock Form（“深岩形态”）同名。修复：整条 target “深岩形态”→“深岩”。
- b9fa6649f154fedc3fa782d006499546285556c802b4bd4d65241eccc5551137 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 用户 2026-10-01 裁决“一并修复之前发现的非阻断问题”（窗口59 ADJUDICATION-F2 advisory）：固定 commit 624a673 game/modules/tome/data/lore/orc-prides.lua:296-297 中正文首行标题与物品名为同一英文串 “Clinician Korbek's experimental notes part …”，物品名译“巫医库贝克的实验笔记，第二部分”，本条正文标题却译“巫医库贝克的实验笔记：二”。修复：仅把首行 #{bold}#…#{normal}# 内的“巫医库贝克的实验笔记：二”→“巫医库贝克的实验笔记，第二部分”，markup、正文与换行不变。
