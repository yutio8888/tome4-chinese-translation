# 修复窗口 59：第375、376批确认的 4 条与 2026-10-01 术语统一的 40 条引用

Paseo MCP / schema5 translation_contextual_v2 implement。基线 8e2fae4e3a3a3fb84651dcbfb6591de20ec45501。

来源有两部分：

- 审核确认的 4 条：`batch-9da6a86a32b67cc82ddf`（第375批，1 条）与 `batch-93dd0d869b4d3e8058dc`（第376批，3 条）。
- 术语统一的 40 条：2026-10-01 术语库补录（8e2fae4e）发现 21 个名称在引用处存在译名漂移。经三方讨论（gpt-6-astra / claude-opus-5-5 / gemini-3.8-flash），用户 2026-10-01 同意“启动修复窗口”。另有 Hideous Visions 指错技能名、critical 错字 2 条，由宿主按事实裁定，一并修复。

Deeprock Form 三方意见不一，保持 review，不在本窗口。用户已授权合并修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。审核仍按用户要求暂停。

唯一 EXECUTOR 仅可修改以下内容：

- WORKSET.json 列出的 44 个 target（mod-tome.lua、tome-cults.lua、tome-orcs.lua）；
- TERM-EDITS.json 列出的 21 行术语（terminology/creatures.tsv、items.tsv、narrative.tsv、society.tsv、talents.tsv）；
- `evidence/quality/repair-window-59-20261001/` 下的修复证据。

不得修改 source、source_tag、section、args_order、运行键、其他译文、其他术语行、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

**先改术语库，再改译文。** TERM-EDITS.json 每项给出 `file`、`old`（现行整行）与 `new`（目标整行）。须整行精确替换，字段间 TAB、行序与其他行不变，文件末尾换行保持。

**本窗口是定向修改，不是全文重译。** 每条只改 SOURCE-CLAIMS 点名的片段：

- 术语统一类 claim 写明「旧名 → 新名」及处数，只替换这些名称，其余字一个不动。例如“堕落的罗斯戈洛斯形态”只改专名，变为“堕落的洛斯格罗斯形态”。
- 审核确认类 claim（1c38f759ab、4e496adf1d、5c0dc6d9d2、6a7d1cc720）给出了建议写法，可在不改变其意思的前提下为衔接做最小调整。
- 1c38f759ab 须按源码合并多拆的一行（去掉“然而”前多出的 LF 与两个 TAB），使 LF/TAB 结构与 source 一致。其余 43 条的 LF/TAB 结构与现译逐行一致。

即使发现别处可疑，也只在报告中列出、不改。尤其以下片段是普通词，不是技能名，不得改：

- “施放一股强力的魔法风暴”（magical wind）；
- “被念力打击击退”（telekinetic blow）；
- 伤害盾标签“反魔盾”（antimagic）。

技能说明（`*/talents/*` 段、`tformat`）中，数值占位符所在的升级预览片段不得连带汉字（片段只按 ASCII 空格、半角括号与逗号切分）。具体规则：

- 已有的占位符旁空格一律保留；
- 新写或改写时插一个 ASCII 空格；
- 全角闭合标点随前文，正负号与全角开括号随数字；
- `%s` 不受此限。

依据：审核操作指南 §6.4；strict lint `talent-placeholder-spacing`。

保留 printf 占位符、`%%`、`#TAG#`、`#{...}#`、`<?...?>` 模板片段、`[i]`/`[/i]` 等 markup 的数量、顺序及适用位置；保留 source_tag。

验证要求：

- 用 LuaJIT 加载三个译文文件，证明恰 44 个 target 变动且其他记录不变；
- 用 Python 逐行比对五个术语文件，证明只有 TERM-EDITS 的 21 行按 `new` 变动；
- 执行 strict lint 及 git diff --check。

无需完整门禁，宿主在独立复审后统一运行 17 项。

取证范围：

- 主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；
- DLC 源码只在 SOURCE-ANCHORS 给出的 checkout 下按条目路径取证，不扫 `/`、`/workspace` 或无关目录；DLC 源码仓库与 commit 未固定。

审查安排：

- cycle-0 `REVIEW/full` 用 Codex GPT-6.1 Sol（medium）；确认的问题合并给一次 EXECUTOR fix。
- 收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL（同 cycle 用下一个 attempt）。max_cycles=5。
- reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。
- 与已记录裁决相冲的指摘由宿主按裁决驳回，包括以上 21 个统一译名与 Phoenix＝凤凰；与本窗口修改无关的既有问题记 advisory 并 carry_forward。

## 条目与已确认修复依据

- 077d4a024ae4f1b6cb378f98cca954b0ca32776529ead34f486b25fcee7228ed | tome-orcs.lua | tome-orcs/overload/data/texts/unlock-orcs_tinker_eyal.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Outpost Leader John 统一为“前哨站首领约翰”，依据：John 是整座前哨站的负责人，“首领”避免“队长”的小队长联想（三方 2:1）。本条把「前哨站领袖约翰」→「前哨站首领约翰」（1 处），其余文字、标点、markup 与换行一律不变。
- 0a4a495b5827d478f460902b947bb725d00adb1dd94dd724be1b6582bc5929ef | mod-tome.lua | mod-tome/data/zones/tannen-tower/npcs.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Drolem 统一为“龙傀儡”，依据：Drolem 是泰恩的龙形傀儡（tannen-tower/npcs.lua:98 “a HUGE golem in the rough shape of a dragon”），本库小写 drolem 已译“龙傀儡”。本条把「卓勒姆」→「龙傀儡」（1 处），其余文字、标点、markup 与换行一律不变。
- 164b35f5290fa677407b4186ba01523ca9987553f36aeee491e9988c7f501b51 | tome-cults.lua | tome-cults/data/timed_effects.lua | 2026-10-01 术语统一（宿主按事实裁定，用户同意）：Hideous Visions 统一为“惊骇幻象”，依据：“失智冲击”是另一技能 Sanity Warp 的译名，此处指 Hideous Visions，属指错技能名。本条把「失智冲击」→「惊骇幻象」（1 处），其余文字、标点、markup 与换行一律不变。
- 16c9372e0195d31a885290376e55d0c7febe8d2bb5470188857609738dbb2aa1 | mod-tome.lua | mod-tome/data/talents/techniques/magical-combat.lua | 2026-10-01 术语统一（宿主按事实裁定，用户同意）：critical 统一为“暴击”，依据：“爆击”为“暴击”错字。本条把「爆击」→「暴击」（1 处），其余文字、标点、markup 与换行一律不变。
- 1c38f759ab9063105dfb70a5f7385e7c6435a9e9440ef6cb896b2f8028c006df | mod-tome.lua | mod-tome/data/talents/chronomancy/flux.lua | 第375批 surface 确认（宿主按固定 commit 624a673 独立核验）：固定 commit 624a673 game/modules/tome/data/talents/chronomancy/flux.lua:34 引导异常（Induce Anomaly）的 action 调用 paradoxDoAnomaly(..., {allow_target=self:knowTalent(self.T_TWIST_FATE)})：学会扭曲命运（Twist Fate）后，本技能引发的异常可由玩家选择目标。原文“you may target Induced Anomalies”即为引导异常选择目标；现译“你可以选中引导异常作为目标”把异常本身说成被选中的对象，机制颠倒。另：info 第二行（L41 “Induced Anomalies may not be held … However upon learning Twist Fate you may target Induced Anomalies.”）是一行，现译在“然而”前多拆一行（多一个 LF 与两个 TAB），属换行不变量缺陷。确认。修复：去掉该换行，并改为“…也不会触发被延后的异常。然而，学会扭曲命运后，你可以为引导异常选择目标。”，其余不变（“%d。 这个”处空格为 §6.4 补空格规则所致，保留）。
- 2956eeac47c09b8da33238b4d5aa48a615bc231882c6d5fccc038b9276371ccb | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- 34475db9b1986168e05f451ac28eedc01384085c5af842806e8cf246669675c8 | mod-tome.lua | mod-tome/data/chats/alchemist-last-hope.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Celia 统一为“赛利亚”，依据：任务文本 12:1 用“赛利亚”。本条把「塞莉娅」→「赛利亚」（1 处），其余文字、标点、markup 与换行一律不变。
- 3483acbd787763b9089aa4ed8e02dfe511ee7213864b878f823c22a67c091cc3 | mod-tome.lua | mod-tome/data/general/npcs/bird.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Phoenix 统一为“凤凰”，依据：凤凰是西方 phoenix 的通行译法，官方简中 zh_hans 亦作“凤凰”；“不死”在本库多指亡灵（95/109 处），不死鸟易误读。本条把「不死鸟」→「凤凰」（1 处），其余文字、标点、markup 与换行一律不变。
- 3b3e509910a12dbc269ca68548be08ee4dd413808f6c1c8073d032ed420f0710 | mod-tome.lua | mod-tome/data/chats/avatar-distant-sun.chat | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Avatar of a Distant Sun 统一为“日耀神使”，依据：职业进阶名为“日耀神使”。本条把「遥远太阳的化身」→「日耀神使」（1 处），其余文字、标点、markup 与换行一律不变。
- 4589d38432175d1b8b980ccf5d7e351d49f20c2ac4eca30707be70d143057ae1 | tome-orcs.lua | tome-orcs/data/lore/sunwall.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Outpost Leader John 统一为“前哨站首领约翰”，依据：John 是整座前哨站的负责人，“首领”避免“队长”的小队长联想（三方 2:1）。本条把「前哨站队长约翰」→「前哨站首领约翰」（1 处），其余文字、标点、markup 与换行一律不变。
- 460d7fd73a5560387078bcd54970d7b6fbfe9827b49251fc1173d7cf13d01feb | mod-tome.lua | mod-tome/data/zones/reknor/objects.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Iron Throne Profits History 统一为“钢铁王座的盈利历史”，依据：四个分卷标题均为“钢铁王座的盈利历史”。本条把「钢铁王座盈利历史」→「钢铁王座的盈利历史」（1 处），其余文字、标点、markup 与换行一律不变。
- 4e496adf1df4348a788b16c0d99c54750f2d1050b9a4e6bb2df2226ca1deb6de | mod-tome.lua | mod-tome/data/talents/celestial/chants.lua | 第376批 surface 确认（宿主按固定 commit 624a673 独立核验）：固定 commit 624a673 game/modules/tome/data/talents/celestial/chants.lua:165-170 callbackOnTakeDamage 判定 core.fov.distance(self, src) > 2 即减伤，即距离 ≥3 格（含恰为 3 格）。原文“enemies 3 or more spaces away”与实现一致；现译“三格外敌人”读作超过三格，排除了恰为 3 格的敌人，边界错误。确认。修复：“减少三格外敌人对你造成的伤害”→“减少距离三格及以上的敌人对你造成的伤害”，其余不变。
- 4f1bf93f22ef3a7761b240bdeabb288cec8a07bb9d9346c40a2644e5645b195a | tome-orcs.lua | tome-orcs/data/general/objects/world-artifacts.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Shoes of Moving Quickly 统一为“疾行之靴”，依据：Cults 同系列“缓步之靴”“缓步疾行之靴”及 3 处引用均用“靴”，追问后三方一致。本条把「疾行之鞋」→「疾行之靴」（1 处），其余文字、标点、markup 与换行一律不变。
- 5a79af3a69eb9f48559373886a50843aa220c3a9c439fde9334616fc7919c08a | mod-tome.lua | mod-tome/data/general/objects/world-artifacts.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Harkor'Zun 统一为“哈卡祖”，依据：本体实体名与重组日志用“哈卡祖”（6:3）。本条把「哈克祖」→「哈卡祖」（1 处），其余文字、标点、markup 与换行一律不变。
- 5c0dc6d9d2a91113376ed0ba28a1f7d5267d8df9dd0079c7b0d8b58ba0743b2b | mod-tome.lua | mod-tome/data/talents/cursed/shadows.lua | 第376批 surface 确认（宿主按固定 commit 624a673 独立核验）：固定 commit 624a673 game/modules/tome/data/talents/cursed/shadows.lua:316-325 阴影的 onTakeHit 在受到伤害（value > 0）且消隐（Fade，T_SHADOW_FADE）未冷却时 forceUseTalent 自动触发消隐。原文“gain the ability to Fade when hit”交代了触发条件；现译“拥有消隐的能力，免疫所有伤害直到下一回合开始”漏掉“受到攻击时”这一触发条件，读作主动能力或常驻免伤。确认（完整性）。修复：“它们同时拥有消隐的能力，免疫所有伤害直到下一回合开始”→“它们同时拥有消隐的能力：受到攻击时免疫所有伤害，直到下一回合开始”，其余（含“ （%d 回合冷却时间）”）不变。contextual 判 OK，宿主以源码为准。
- 5c20f5ba0d5bae5c30ad984a731172d3b8dd088901493026a133122ce7b22b2d | tome-orcs.lua | tome-orcs/data/chats/aaf.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Automated Portable Extractor 统一为“便携式自动材料提取仪”，依据：实体名与设置提示均为“便携式自动材料提取仪”。本条把「便携式自动提取仪」→「便携式自动材料提取仪」（1 处），其余文字、标点、markup 与换行一律不变。
- 616a6086265ab848ec987fac01cff95764a8323658c69c4b466a3c939fa78df1 | tome-orcs.lua | tome-orcs/data/general/objects/world-artifacts.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Saw Wheels 统一为“链锯轮滑”，依据：技能名为“链锯轮滑”（三方 2:1）。本条把「链锯轮」→「链锯轮滑」（1 处），其余文字、标点、markup 与换行一律不变。
- 66017f63712ce90086704d589f3e946b174334df1def0b03be8197a1147c638d | mod-tome.lua | mod-tome/data/talents/uber/cun.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Antimagic Shield 统一为“反魔法护盾”，依据：技能名为“反魔法护盾”。本条把「反魔盾」→「反魔法护盾」（1 处），其余文字、标点、markup 与换行一律不变。
- 6a7d1cc7200cb491d20d6a487d79b03969b155ee5ff20224a0a830388ee6de98 | mod-tome.lua | mod-tome/data/talents/gifts/sand-drake.lua | 第376批 surface 确认（宿主按固定 commit 624a673 独立核验）：固定 commit 624a673 game/modules/tome/data/talents/gifts/sand-drake.lua:45-79 吞噬（Swallow）命中且目标生命比例低于阈值（或已死）后，还需 target:checkHit(物理强度 vs 物理豁免) 且目标可被秒杀（canBe instakill 或生命 ≤5%）才杀死并回复，否则记“resists”。原文“you attempt to swallow it”是尝试；现译“你会吞噬它，立刻将其杀死”把尝试说成必然成功，与下一句豁免相矛盾（删限定词类缺陷）。确认。修复：“你会吞噬它，立刻将其杀死，并根据其等级恢复生命值和失衡值”→“你会尝试吞噬它：若成功则立刻将其杀死，并根据其等级恢复生命值和失衡值”，其余不变。contextual 判 OK，宿主以源码为准。
- 72bf25a3c7db3b7d19f3b806521dc4d7731ce8a35615c5da2da2da53b9bfdcd1 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- 7abfa1439401cff8b10346e735d6939c3ad46d642257e3413391791775fd43a5 | mod-tome.lua | mod-tome/data/general/npcs/bird.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Phoenix 统一为“凤凰”，依据：凤凰是西方 phoenix 的通行译法，官方简中 zh_hans 亦作“凤凰”；“不死”在本库多指亡灵（95/109 处），不死鸟易误读。本条把「不死鸟」→「凤凰」（1 处），其余文字、标点、markup 与换行一律不变。
- 8237e192c36085b766a2a86d007006184011d15e3e0dcd9069418d302e798548 | mod-tome.lua | mod-tome/data/talents.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Aether Avatar 统一为“以太之体”，依据：技能名为“以太之体”。本条把「以太形态」→「以太之体」（1 处），其余文字、标点、markup 与换行一律不变。
- 846b50b12645c14ce0ae170302b90dc0dc84460f1b72a7097b4f9fbeefb5fd46 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- 86192a30aa44a613d9eb0679c529a673a0146701dd3e5fedc1b8fc97b4edc75d | tome-orcs.lua | tome-orcs/data/talents/spells/galvanic-technomancy.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Burning Wake 统一为“无尽之焰”，依据：主游戏技能名为“无尽之焰”（4:2）。本条把「无尽之炎」→「无尽之焰」（1 处），其余文字、标点、markup 与换行一律不变。
- 86b01ce4f3a363181ce9c6d4c1b83d2e109e393efffa6cfe280714150382026d | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- 9750a84b4038bb1baccc9d3c132588c02260ecab2f46ced061119724f1dd90ce | tome-orcs.lua | tome-orcs/data/lore/sunwall.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Outpost Leader John 统一为“前哨站首领约翰”，依据：John 是整座前哨站的负责人，“首领”避免“队长”的小队长联想（三方 2:1）。本条把「前哨站队长约翰」→「前哨站首领约翰」（1 处），其余文字、标点、markup 与换行一律不变。
- 9c2578df9180de61fc949327a0db5c83cd3417fd13dbfa0b1aabed4e84f718c1 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- a38a4fc495b51fcb53ca3f07ef4b555548b0f71ac8f7ee1627106d354c2c4205 | mod-tome.lua | mod-tome/data/talents/techniques/marksmanship.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Called Shots 统一为“精准射击”，依据：技能名与技能树均为“精准射击”。本条把「精巧射击」→「精准射击」（1 处），其余文字、标点、markup 与换行一律不变。
- ac1f5a5a291916af742147f35898779eb6c9c76aae3f069849d99187c80cf2c6 | mod-tome.lua | mod-tome/data/achievements/kills.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Harkor'Zun 统一为“哈卡祖”，依据：本体实体名与重组日志用“哈卡祖”（6:3）。本条把「哈克祖」→「哈卡祖」（1 处），其余文字、标点、markup 与换行一律不变。
- b1826b4a6461e75ebad7fe70729988d82b7667bde460f5a905b276d9701f4cda | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：losgoroth 统一为“洛斯格罗斯”，依据：实体名与种族说明均为“洛斯格罗斯”（7:5）。本条把「罗斯戈洛斯」→「洛斯格罗斯」（1 处），其余文字、标点、markup 与换行一律不变。
- b2e781e786aa460c0242f6bcbab53bffe0f2674245e86ab2dc534e485ca353c9 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- b6c6dceda1749c9bcd0184a1f88561f1c87c26ead1913821aea0967fd8a25194 | mod-tome.lua | mod-tome/data/talents/misc/tutorial.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Telekinetic Punt 统一为“念力推送”，依据：符文与习得提示均为“念力推送”。本条把「念力打击」→「念力推送」（1 处），其余文字、标点、markup 与换行一律不变。
- bf68ee4deedb7455dd0c23134b9c5eb6a9ba10003d926e1c19dbbd12c569a7d2 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- c098185a7f7f8c5f847b6582c824cd7c7c239f827e1fbf33191e643d35f10035 | mod-tome.lua | mod-tome/data/lore/orc-prides.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Clinician Korbek's experimental notes 统一为“实验笔记”，依据：notes 为第一人称研究手记，实体名已为“实验笔记”（三方 2:1）。本条把「实验报告」→「实验笔记」（1 处），其余文字、标点、markup 与换行一律不变。
- c37f1fd8de9bd130f2fe3fe8975008ac295300e3f5f3d4b4090fe029fa8001da | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：losgoroth 统一为“洛斯格罗斯”，依据：实体名与种族说明均为“洛斯格罗斯”（7:5）。本条把「罗斯戈洛斯」→「洛斯格罗斯」（1 处），其余文字、标点、markup 与换行一律不变。
- d1f7a9a7b5bb668f3dde95657c94835c800e8e74820221adabaad147c0907f45 | mod-tome.lua | mod-tome/data/talents/misc/tutorial.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Mana Gale 统一为“法力风暴”，依据：符文、习得提示与教学文本均为“法力风暴”。本条把「魔法风暴」→「法力风暴」（1 处），其余文字、标点、markup 与换行一律不变。
- db5514a63cfa3676ac075f55ed64828069eea1a6fdf2aad6d81a8798ae0f74ac | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：losgoroth 统一为“洛斯格罗斯”，依据：实体名与种族说明均为“洛斯格罗斯”（7:5）。本条把「罗斯戈洛斯」→「洛斯格罗斯」（1 处），其余文字、标点、markup 与换行一律不变。
- dec9c15562abf0748f806a4dbf89e66ff3755bf498ee59cea77cb934856f7a71 | tome-orcs.lua | tome-orcs/data/zones/sunwall-outpost/npcs.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Outpost Leader John 统一为“前哨站首领约翰”，依据：John 是整座前哨站的负责人，“首领”避免“队长”的小队长联想（三方 2:1）。本条把「前哨站队长约翰」→「前哨站首领约翰」（1 处），其余文字、标点、markup 与换行一律不变。
- df5708e892deb9639393e0de9e8d809f792a2bc782f24e43a511c6eaf0b4e835 | mod-tome.lua | mod-tome/data/general/objects/world-artifacts.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Harkor'Zun 统一为“哈卡祖”，依据：本体实体名与重组日志用“哈卡祖”（6:3）。本条把「哈克祖」→「哈卡祖」（1 处），其余文字、标点、markup 与换行一律不变。
- eb676f60c860f09635157731c2d361be7e6731c8d77f989e20eb4d734a46f393 | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：losgoroth 统一为“洛斯格罗斯”，依据：实体名与种族说明均为“洛斯格罗斯”（7:5）。本条把「罗斯戈洛斯」→「洛斯格罗斯」（1 处），其余文字、标点、markup 与换行一律不变。
- efaa568d82a79a889943177e82fe7df9bfca43cdaa819d83f50336168ffe11a8 | tome-orcs.lua | tome-orcs/data/talents/spells/galvanic-technomancy.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Burning Wake 统一为“无尽之焰”，依据：主游戏技能名为“无尽之焰”（4:2）。本条把「无尽之炎」→「无尽之焰」（1 处），其余文字、标点、markup 与换行一律不变。
- f17c95ac6661d0e5f27a39198f2c9a8af1c1aa6cca01d85dff635b35d7958721 | mod-tome.lua | mod-tome/data/talents/cunning/artifice.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Hidden Blades 统一为“隐匿刀锋”，依据：技能名为“隐匿刀锋”。本条把「隐藏刀片」→「隐匿刀锋」（1 处），其余文字、标点、markup 与换行一律不变。
- f269fd9bbe32c1443a97f28bc2efec21142f7b5f8d88c1d4ce1688f2f622a8f2 | tome-orcs.lua | tome-orcs/data/talents/steam/turrets.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：Steamgun Mastery 统一为“蒸汽枪掌握”，依据：技能名为“蒸汽枪掌握”。本条把「蒸汽枪精通」→「蒸汽枪掌握」（1 处），其余文字、标点、markup 与换行一律不变。
- f340fb4ca44a095dfd1319069c9561f06aba72555bec05487dfc4c21f48418ac | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 2026-10-01 术语统一（三方讨论 gpt-6-astra/opus-5-5/gemini-3.8-flash，用户同意）：losgoroth 统一为“洛斯格罗斯”，依据：实体名与种族说明均为“洛斯格罗斯”（7:5）。本条把「罗斯戈洛斯」→「洛斯格罗斯」（1 处），其余文字、标点、markup 与换行一律不变。
