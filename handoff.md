# 翻译审核当前交接

更新时间：2026-09-24（审核273已完成；下一步修复窗口27，仅处理273的2条）

**Flame 改名（2026-09-23 维护者批准）**：三方讨论一致推荐，技能名统一为「火焰术」，术语库 preferred；Shadow Mages 的 Flames 实指暗影之火。7 条 revision_changed 已入队待重审；详见 [terminology-flame-20260923](evidence/quality/terminology-flame-20260923/DECISION.md)。pending 第 7 项已裁决。
移交对象：Paseo / Codex / GPT-6-Astra

## 当前授权与实测状态

用户于2026-09-23指示先做工具维护，然后持续推进审核，无需手动确认；有争议条目列入 pending
集中审阅，不修、不阻塞。当前清单见[待用户集中审阅的争议条目](evidence/quality/pending-user-review.md)。
审核模型仍为 **surface `codex/gpt-6-sol`（medium，auto-review）**、**contextual
`claude/claude-opus-5-5`（medium，auto）**；live profile 缺失时按用户指示直接选择并保留快照。

工具维护已提交为 `b626eaf1c30ed389dff0b0a633e393225ea46843`：原生 parser 已支持 Codex 0.156.0
与 Claude Code 2.1.280（含归档末尾 `cost-state` 记录），并以 10 份真实会话验证。原“工具版本偏差”
已经解决，详见[原生 parser 版本维护](evidence/quality/native-parser-versions-20260923/summary.md)。

已核实：活动批次从 batch start 到 finalize 期间不能插入任何提交；
`production_review_v2_lite_batch.py:1084` 会检查 base commit drift，`:1909` 会检查 finalize parent。
修复窗口中 preflight 后插入提交会使 preflight 失效，必须重跑；每次提交后都需 queue rebuild。
因此工具维护只能放在批次或修复窗口之间。

修复窗口8已完成，译文提交为 `9b71efd8714678d10419f9522a93a25c92f3e841`。六条目标为无尽狩猎
描述、`ALL_DREAMS`、Yeek 换行、Thalore 诗句（含紫杉及鸫鸟/猫头鹰行）、麻痹毒素伤害方向和
《龙族传说》四处语义。`REVIEW/full`（`codex/gpt-6-sol`）原始结果为 2 OK / 4 ISSUE：诗句
确认后追加一轮有界修复，其余三条转 pending；`FINAL_REVIEW/full`（`claude/claude-opus-5-5`）
为 6 OK / 0 ISSUE。完整门禁 `run.2f4mryxp` 17/17 通过并含严格构建，任务 `DONE_VERIFIED`；
四个实施/复审 child 均已归档，本 publication child 待宿主归档。完整结果见
[窗口8出版证据](evidence/quality/repair-window-8-20260923/PUBLICATION.md)。

新 catalog 为 `8580c7207ae19005bb206138eabe0daf3fb00a7eb0513c113b64c922adbc5cf2`，migration 为
`518ce6ed86c6d746184ff38b10a45cd9755ff56c2c57a0af650d7aa03252552f`；6 条 revision changed、
29,822 条 unchanged、0 ambiguous/unmapped，6 个 successor 待重新审核，不继承 done。

窗口8的证据提交、queue rebuild 与 push 已完成（`d218e886`）。

审核255（`batch-448e3278fde3f8dfbea2`）已闭合，结果为 **72 done / 5 repair_required / 3 blocked**。
surface 四组 `codex/gpt-6-sol` 为 69 OK / 11 ISSUE（无错位），contextual `claude/claude-opus-5-5`
为 8 OK / 3 ISSUE；14 个观察裁决为 8 confirmed、1 refuted、2 advisory、3 pending。17/17 门禁含严格构建通过，
两任务快照重放 `DONE_VERIFIED`，五个 reviewer 均已归档确认。证据提交 `7b45aad4ac05a7ffb38797145fb00d4904293f89`，
详见[255宿主证据](evidence/quality/production-batches/batch-448e3278fde3f8dfbea2-host-evidence/summary.md)。
3 条 pending（blocked）已登记到待审阅清单。

潜行说明为已确认机制缺陷，按提前修复规则下一步开修复窗口9，仅处理 255 的 5 条：高阶奇术师解锁文本
`Flame` 技能名、潜行说明（in sight 与 action）、`%d runes active`、夏之眼 bright、回归之杖描述。
裁决与范围见 `.ai/task/batch-448e3278fde3f8dfbea2/WINDOW9-EARLY-REPAIR-DECISION.json`。窗口9可复用
`.ai/task/repair-w8-20260923/` 的通用 helper。

修复窗口9已完成。首轮 `repair-w9-20260923` 经 `REVIEW/full` 4 OK / 1 ISSUE、三轮 `FINAL`
（F1 4 OK / 1 ISSUE、F2 4 OK / 1 ISSUE、F3 5 OK / 0 ISSUE）收敛并通过 17/17 门禁；但宿主在
`FINAL` 失败后没有按 `translation_v2_convergence` 返回 `RE_REVIEW`，因此该任务以
`STOP_VERIFIED` 关闭。重跑任务 `repair-w9b-20260923` 逐字应用已收敛文本，
`REVIEW(0)/full` 与 `FINAL(1)/full` 均为 5 OK，完整门禁 `run.hna9wv8w` 17/17 通过并含严格构建，
任务 `DONE_VERIFIED`。译文提交为 `78be6b5a752cb5a24d0ef1e8337f0ba301180f21`；新 catalog 为
`0e554a74d6738064f4245525bed6f1be8a8463ea3df7f683ab2327e0fe0de510`，migration 为
`bdf355b65bef33ded7ac24e48c577770f33d67312fed83ab8de9d1f4c4a538d1`，5 个 successor 待重新审核，
不继承 done。`Flame` 名称争议恢复基线“火球术”并登记为 pending。完整结果见
[窗口9出版证据](evidence/quality/repair-window-9-20260923/PUBLICATION.md)。

窗口9的证据提交、queue rebuild 与 push 已完成（`9b3112f9`）；随后 Flame→火焰术改名（`829a9368`/`d87514e9`）已推送。

审核256（`batch-096b5470a753566196f9`）已闭合，结果为 **72 done / 5 repair_required / 3 blocked**。
surface 四组 `codex/gpt-6-sol` 为 63 OK / 17 ISSUE（lane-000-0 一条 OK 结果回显 identity 错 17 位，经原生日志核实后宿主 hand-attribution 恢复；
lane-000-2 因 sandbox 失败经 Paseo 终端只读读取，终端已关闭），contextual `claude/claude-opus-5-5` 为 10 OK / 7 ISSUE；
23 个观察裁决为 10 confirmed、6 refuted、3 advisory、4 pending。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，
五个 reviewer 均已归档确认。证据提交 `db20fa9a2ada06317cd8ba90d7721d23bf651e3b`。

下一步按 1:1 节奏开修复窗口10，仅处理 256 的 5 条：Plate of the Blackened Mind 描述、魔法大爆炸区域效果传送警告、
时空特工入职信（几十年 / fair game / 彩票 / quite literally 四处）、刀刃风暴构造体 short_info、碾压擒抱解除提示。
范围见 `.ai/task/batch-096b5470a753566196f9/WINDOW10-REPAIR-DECISION.json`；可复用窗口9b 模板，注意失败的 FINAL 之后必须接 RE_REVIEW。
pending 新增第 8–10 项（Blunt Thrust、传说标题、Crystal Shard）。

修复窗口10已完成。首轮 `repair-w10-20260923` 的 `REVIEW(0)/full`（`codex/gpt-6-sol`）为
3 OK / 2 ISSUE，`FINAL(1)`（`claude/claude-opus-5-5`）为 4 OK / 1 ISSUE，
`RE_REVIEW(2)` 为 4 OK / 1 ISSUE，`FINAL(3)` 为 4 OK / 1 ISSUE；确认修复长信的增译与遗漏、
构装体术语、长信整条问题、Sher'Tul 护盾条件及“被我和”主语错误。因 `max_cycles=3` 用尽仍未
收敛，任务按停止条件交回用户；用户选择以 `repair-w10b-20260923` 重跑，首轮以
`STOP_VERIFIED` 关闭，原因保存在其 `STATE.last_error`。重跑由唯一 EXECUTOR 逐字应用
`FINAL-TARGETS`（与 `CANDIDATE-FINAL` 逐字节一致），`REVIEW(0)/full` 为 4 OK / 1 ISSUE，
其中长信 `reset and try again` 措辞观察由宿主判为 pending 并登记为第 11 项，不开启修复轮；
`FINAL(1)/full` 为 5 OK。完整门禁 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。

译文提交为 `a317634cd1be2102dce66e73a51cb36890b5068f`；新 catalog 为
`0cec1688df3ca1c26258e28198f3716e5f380f00ece6024f5a30a369c83aeb5d`，migration 为
`dd5ed9cefe8b85e6c255c7cfa49431e9b8d17e4b7e8774347123b62b25dbfc81`。迁移结果为
5 条 revision_changed、29,823 条 unchanged、0 ambiguous/unmapped，5 个 successor 待重新审核，
不继承 done。首轮 executor 与 reviewer、重跑 executor 与 2 个 reviewer 均已归档确认；本
publication child 待宿主归档。完整结果见
[窗口10出版证据](evidence/quality/repair-window-10-20260923/PUBLICATION.md)。

窗口10的证据提交、queue rebuild 与 push 已完成（`d5905f2d`）。

审核257（`batch-88cfb30f797898ed8ef5`）已闭合，结果为 **76 done / 4 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 75 OK / 5 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致），
contextual `claude/claude-opus-5-5` 为 2 OK / 3 ISSUE；8 个观察裁决为 7 confirmed、1 advisory。17/17 门禁含严格构建通过，
两任务快照重放 `DONE_VERIFIED`，五个 reviewer 均已归档确认。证据提交 `cd70d0cd20c79ef76fe72b2de01c6d6f7eb99469`，
详见[257宿主证据](evidence/quality/production-batches/batch-88cfb30f797898ed8ef5-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口11，仅处理 257 的 4 条：Trollmire 日记残页（两处空行与 get wind of 习语）、
Torment 伤害阈值“超过至少”、鼠巫妖头骨未鉴定名 dusty rat skull、角色面板 Effect resistances 标题（免疫→抗性）。
范围见 `.ai/task/batch-88cfb30f797898ed8ef5/WINDOW11-REPAIR-DECISION.json`；可复用窗口10b 模板，失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口11已完成。任务 `repair-w11-20260923` 的 `execute-01` 实施审核257的4条确认项：
Trollmire 日记残页两处空行与 `get wind of` 习语、Torment 伤害阈值与判定方式、鼠巫妖头骨
未鉴定名、角色面板“状态效果抗性”标题。`REVIEW(0)/full`（`codex/gpt-6-sol`）为
3 OK / 1 ISSUE：Torment 应对每个冷却中的技能分别判定概率；reviewer 回显 `revision_key`
有一段重复，经原生日志核实后由宿主 hand-attribution，原始字节保留于 `r0a1-original.raw`，
宿主最初判为 pending。`FINAL(1)/full`（`claude/claude-opus-5-5`）同样为 3 OK / 1 ISSUE；
宿主依据固定源码和 `AGENTS.md` 将同一机制问题更正为 confirmed 一级缺陷，R0 的 pending 记录
已标 superseded 且不列入待审阅清单。`execute-02` 有界修复为“每个冷却中的技能各有 %d%% 概率
减少 1 回合冷却时间”；`RE_REVIEW(2)`（`gpt-6-sol`）与 `FINAL(3)`（`opus-5-5`）均为
4 OK。`execute-01` 后与 `execute-02` 后的完整门禁均为 17/17 通过并含严格构建，任务
`DONE_VERIFIED`。2 个 executor 与 4 个 reviewer 均已归档确认；本 publication child 待宿主归档。

译文提交为 `6eca6f9952781a1e98d117d35fac2c7028bacb85`；新 catalog 为
`5020a313d684c44e837ce0bd2bd8a4062ad42a784b356cc802a934d6dfa1d957`，migration 为
`5033b3e3c151150bebed931811e95f1cd91e7838e16773d0fe2e43bf4135a176`。迁移结果为
4 条 revision changed、29,824 条 unchanged、0 ambiguous/unmapped，4 个 successor 待重新审核，
不继承 done。完整结果见[窗口11出版证据](evidence/quality/repair-window-11-20260923/PUBLICATION.md)。

窗口11的证据提交、queue rebuild 与 push 已完成（`6343aeaf`）。

审核258（`batch-13b90e85d842da2d4f41`）已闭合，结果为 **77 done / 3 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 71 OK / 9 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致），
contextual `claude/claude-opus-5-5` 为 7 OK / 2 ISSUE；11 个观察裁决为 5 confirmed、4 refuted、2 advisory。17/17 门禁含严格构建通过，
两任务快照重放 `DONE_VERIFIED`，五个 reviewer 均已归档确认。证据提交 `b5417468a754dbbd5127d3739e3534b3d5ac3800`，
详见[258宿主证据](evidence/quality/production-batches/batch-13b90e85d842da2d4f41-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口12，仅处理 258 的 3 条：格斗家职业描述（漏 pit-fighter、“门外汉”、职业名）、
零点城镇 NPC timeless elf（“中年精灵”）、岱卡拉任务日志 huge fire dragon。
范围见 `.ai/task/batch-13b90e85d842da2d4f41/WINDOW12-REPAIR-DECISION.json`；可复用窗口11 模板，失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口12已完成。任务 `repair-w12-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施审核258的
3条确认项：格斗家职业描述补回 `pit-fighter`、`boxer`、`amateur practitioner` 与“格斗家的技能”；
零点城镇 NPC 的 `timeless elf` 改为“不显年岁的精灵”；岱卡拉任务日志补回 `huge`，改为
“盘踞在那里的巨型火龙”。同族冰龙条目在 `mod-tome.lua` 中同样漏译 `huge`，不在本窗口范围。
`REVIEW(0)/full`（`codex/gpt-6-sol`）与 `FINAL(1)/full`（`claude-opus-5-5`）均为 3 OK，
完整门禁 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。1 个 executor 与 2 个 reviewer 均已归档确认；
本 publication child 待宿主归档。

译文提交为 `c48bc78cb518d99cc1d00b9b21bcb88398eff8f4`；新 catalog 为
`832d278c51b49423331e1dde7102c1204e064924b82965456c432d013470a77a`，migration 为
`7b4b4ec774313a86d7d5c7af3fed5c62dc4acdf527fd0d546bc829bba58e2566`。迁移结果为
3 条 revision changed、29,825 条 unchanged、0 ambiguous/unmapped，3 个 successor 待重新审核，
不继承 done。完整结果见[窗口12出版证据](evidence/quality/repair-window-12-20260923/PUBLICATION.md)。

窗口12的证据提交、queue rebuild 与 push 已完成（`6996b69b`）。

审核259（`batch-73136994056fb59bf591`）已闭合，结果为 **76 done / 4 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 68 OK / 12 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致），
contextual `claude/claude-opus-5-5` 为 10 OK / 2 ISSUE；14 个观察裁决为 6 confirmed、4 refuted、4 advisory。17/17 门禁含严格构建通过，
两任务快照重放 `DONE_VERIFIED`，五个 reviewer 均已归档确认。证据提交 `61b6ce5a4a64e429612c05366330cca58bb2e54f`，
详见[259宿主证据](evidence/quality/production-batches/batch-73136994056fb59bf591-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口13，仅处理 259 的 4 条：Self-Judgement 流血死亡信息（“死得其所”→罪有应得）、
Body of Stone 描述（化为石头、强制位移、冷却缩减百分比）、魔杖类型描述（漏制造者）、Crushing Hold 全局速度术语。
范围见 `.ai/task/batch-73136994056fb59bf591/WINDOW13-REPAIR-DECISION.json`；可复用窗口12 模板，失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口13已完成。任务 `repair-w13-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施审核259的
4条确认项：Self-Judgement 流血死亡信息由“死得其所”改为“罪有应得”；Body of Stone 描述改为
“化为石头”，恢复“强制位移”，并明确冷却缩减按百分比计算；魔杖类型描述补回“由强大的炼金术师
和大法师制造”；Crushing Hold 使用术语“全局速度”，补回“每次抓取”，并删除 `#RED#` 后的多余空格。
`REVIEW(0)/full`（`codex/gpt-6-sol`）为 3 OK / 1 ISSUE：魔杖 `Archmagi` 与职业名“元素法师”不一致；
宿主驳回，因为 `classes.tsv:22` 仅约束职业名 birth descriptor name，非职业语境本库一致使用“大法师”。
`FINAL(1)/full`（`claude-opus-5-5`）为 4 OK，任务收敛。完整门禁 17/17 通过并含严格构建，任务
`DONE_VERIFIED`。1 个 executor 与 2 个 reviewer 均已归档确认；本 publication child 待宿主归档。

译文提交为 `88dd316752e399c6d42957a7424bec1629773c23`；新 catalog 为
`e3b869612116e4b4c4f837e0f0a35017d85f9793fdf80a1109226edf075df753`，migration 为
`52c71f8d968c2229e1d67f931e2585a4f32069ae74a26315acd0210ce9341aff`。迁移结果为
4 条 revision changed、29,824 条 unchanged、0 ambiguous/unmapped，4 个 successor 待重新审核，
不继承 done。完整结果见[窗口13出版证据](evidence/quality/repair-window-13-20260923/PUBLICATION.md)。

窗口13的证据提交、queue rebuild 与 push 已完成（`6b212707`）。

审核260（`batch-6b8acfddd3cc0c11f471`）已闭合，结果为 **77 done / 3 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 73 OK / 7 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致）；
contextual `claude/claude-opus-5-5` 首次 full-000 在 JSON 前多一句英文导语被判无效，归档确认后以 full-001（attempt 2，retry_of full-000）重派，4 OK / 3 ISSUE。
10 个观察裁决为 5 confirmed、2 refuted、3 advisory。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，六个 reviewer child 均已归档确认。证据提交 `b686e1f33b9fbb73fc4e965771b8c01db7645a78`，
详见[260宿主证据](evidence/quality/production-batches/batch-6b8acfddd3cc0c11f471-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口14，仅处理 260 的 3 条：珠宝师对话冬潮之月传说（漏“融化”、增添“融入大地”、“更强大”）、
Guided Shot 念力导引（telekinetic nudges、“精确地”）、巨狼描述 snaps at you（“咆哮”）。
范围见 `.ai/task/batch-6b8acfddd3cc0c11f471/WINDOW14-REPAIR-DECISION.json`；可复用窗口13 模板，失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口14已完成。任务 `repair-w14-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施审核260的
3条确认项：珠宝师对话中的 Wintertide Moon 传说补回“融化”，删除增添的“融入大地”，将“更强大”改为
“强力”；Guided Shot 补回 `telekinetic nudges` 的“念力微调”与“精确地”；巨狼描述中的
`snaps at you` 改为“朝你猛咬”。`REVIEW(0)/full`（`codex/gpt-6-sol`）为 3 OK；宿主另立
`R0-HOST-WINTERTIDE-NAME`，确认“冬潮之月”沿用了宿主 SPEC 措辞，而本库既有名为“霜华”，
`execute-02` 修为“霜华的一部分”。`RE_REVIEW(1)`（`gpt-6-sol`）为 2 OK / 1 ISSUE，确认
`R1-WINTERTIDE-MOON-SENSE`：裸“霜华”兼作日历月份名，丢失“月亮”义，且 elvala 传说已用
“霜华之月”；`execute-03` 改为“霜华之月的一部分”。`RE_REVIEW(2)` 为 3 OK；
`FINAL(3)/full`（`claude-opus-5-5`）为 3 OK，任务收敛。完整门禁 17/17 通过并含严格构建，任务
`DONE_VERIFIED`。3 个 executor 与 3 个 reviewer 均已归档确认；本 publication child 待宿主归档。

译文提交为 `5babfdaf1c331e52df1efc5480794457449f4c99`；新 catalog 为
`fb1a42e597f4bcec63cb05b5ed0d66aa29272e60581584c31f96ea6acb8f7c50`，migration 为
`a3f47a5e5f30a66b9a56b4ba416a571a91a906ea9562229f4e4c52d5c8632d1d`。迁移结果为
3 条 revision changed、29,825 条 unchanged、0 ambiguous/unmapped，3 个 successor 待重新审核，
不继承 done。完整结果见[窗口14出版证据](evidence/quality/repair-window-14-20260923/PUBLICATION.md)。

窗口14的证据提交、queue rebuild 与 push 已完成（`9dedbbc9`）。

审核261（`batch-b1809d747f471912638d`）已闭合，结果为 **76 done / 2 repair_required / 2 blocked**。
surface 四组 `codex/gpt-6-sol` 为 73 OK / 7 ISSUE；harvest 前逐位比对回显 identity，lane-000-2 第17条（判 OK）回显漏“199”，
宿主手工归因并以更正 raw 收取（原字节留档于宿主证据 captures261/）。contextual `claude/claude-opus-5-5` 为 4 OK / 3 ISSUE。
10 个观察裁决为 3 confirmed、3 advisory、4 pending。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `c79806c35598879d3b4285ce6d6e97a950ceb809`，
详见[261宿主证据](evidence/quality/production-batches/batch-b1809d747f471912638d-host-evidence/summary.md)。
2 条 pending（blocked）已登记到[待审阅清单](evidence/quality/pending-user-review.md)第 12、13 项：Virulent Strike 技能名“撕裂”、死亡描述 grandfathered 人称错位（归入死亡描述词表族）。

下一步按 1:1 节奏开修复窗口15，仅处理 261 的 2 条：半身人创世论（other gods were responsible / ridiculous ideals / entitlement）、
半身人遗迹紧急召回提示多出“救他”。范围见 `.ai/task/batch-b1809d747f471912638d/WINDOW15-REPAIR-DECISION.json`；
`setup_window15_task.py` 已写好（continuation-20260923），可复用窗口14 helper，失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口15已完成。任务 `repair-w15-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施审核261的
2条确认项：半身人创世论逐句修正 `other gods were responsible`、漏译的
`lesser gods copied his grand design`、`ridiculous ideals`、`entitlement` 及其余明显增删；
半身人遗迹紧急召回提示删除原文没有的“救他”，改为“发誓日后再回来”。
`REVIEW(0)/full`（`codex/gpt-6-sol`）为 2 OK；`FINAL(1)/full`
（`claude-opus-5-5`）为 1 OK / 1 ISSUE，确认 `F1-LORE-PRESUME-LOGIC`：第 232 行夏·图尔段
推测语气颠倒、第 234 行众神冲突前提被降为并列选项；`execute-02` 有界修复末两段。
`RE_REVIEW(2)`（`gpt-6-sol`）与 `FINAL(3)/full`（`claude-opus-5-5`）均为 2 OK，任务收敛。
完整门禁 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。2 个 executor 与 4 个 reviewer 均已归档确认；
本 publication child 待宿主归档。

译文提交为 `a039ff12c97f0c2f5071f7111442b17b465166f3`；新 catalog 为
`f4d10da25eb9e968b74997635ef6bcb09cdaf25095caef96a3f220db494c660b`，migration 为
`de68e389782940517c064da7cdaaa19d6207e7dc1da4c1ca4dc5728b05e25d71`。迁移结果为
2 条 revision changed、29,826 条 unchanged、0 ambiguous/unmapped，2 个 successor 待重新审核，
不继承 done。完整结果见[窗口15出版证据](evidence/quality/repair-window-15-20260923/PUBLICATION.md)。

窗口15的证据提交、queue rebuild 与 push 已完成（`f56aa48f`）。

审核262（`batch-cdef103673c1cf6a37ae`）已闭合，结果为 **71 done / 7 repair_required / 2 blocked**。
surface 四组 `codex/gpt-6-sol` 为 67 OK / 13 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致；lane-000-3 经 MCP 建终端只读，宿主核验后已关闭）；
contextual `claude/claude-opus-5-5` 首次 full-000 在 JSON 前多一句英文导语被判无效，归档确认后以 full-001 重派，8 OK / 5 ISSUE。
18 个观察裁决为 11 confirmed、3 refuted、2 advisory、2 pending。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，六个 reviewer child 均已归档确认。证据提交 `8200412298bc92f9a3dbdbbc5eb50ba0c868bd0c`，
详见[262宿主证据](evidence/quality/production-batches/batch-cdef103673c1cf6a37ae-host-evidence/summary.md)。
2 条 pending（blocked）已登记到[待审阅清单](evidence/quality/pending-user-review.md)第 14、15 项：神器 Exiler“放逐”、技能系 Crimson Templar“赤红守卫”。
宿主准备脚本新增 lowercased-entity-name 证据分支（gem.lua lapis lazuli），首次失败被管道吞掉但在派发前已补跑。

下一步按 1:1 节奏开修复窗口16，仅处理 262 的 7 条：50级祝贺空行、星辰契约 bond/光辉引力拉向目标/缩进、
不死猎人指南多处增译夸大、矮人加料与宿醉玩笑、虚空传送门成就 closing、牺牲死讯 %s 反身代词、剧毒弹自然伤害。
范围见 `.ai/task/batch-cdef103673c1cf6a37ae/WINDOW16-REPAIR-DECISION.json`；`setup_window16_task.py` 已写好（continuation-20260923），
可复用窗口15 helper（verify_migration 有两处条数硬编码），失败的 FINAL 之后必须接 RE_REVIEW。

修复窗口16已完成。任务 `repair-w16-20260923` 的 `execute-01`（`codex/gpt-5.6-sol`）实施审核262的
7条确认项：50级祝贺段间空行与“勇敢地”；星辰契约 `bond` 改为“羁绊”，明确光辉引力拉向被击中目标并恢复 `\t\t` 缩进；
不死猎人指南修正六处增译、夸大、因果错置、弱化和巫妖段反义，将多拆出的段落并回，LF 86→72 与原文一致；
矮人送药改为“加了点好料，明早可有你受的”；成就改为“以自身为祭品关闭虚空传送门”；牺牲死讯改为
“牺牲了%s，将维网带给众生”；强化弹药 Venomous 改为“自然伤害”。宿主 verify 暴露 lore 段落拆分，
`execute-02` 只合并段落。`REVIEW(0)/full`（`codex/gpt-6-sol`）为 6 OK / 1 ISSUE：Eyal 被译为
“埃亚尔大陆”（Eyal 实为世界名），裁决为 advisory 并列入 pending #16；`FINAL(1)/full`（`claude-opus-5-5`）为
6 OK / 1 ISSUE：署名“不死猎人”存在歧义，宿主初判 advisory，但 DONE 检查要求最新 FINAL 无 ISSUE，
故改判二级并有界修复；`execute-03` 只将署名改为“一名不死生物猎人的指南”。`RE_REVIEW(2)`
（`gpt-6-sol`）为 6 OK / 1 ISSUE（同一 Eyal 观察，advisory）；`FINAL(3)/full`
（`claude-opus-5-5`）为 7 OK，任务收敛。完整门禁 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。
3 个 executor、4 个 reviewer 与 publication child 均已归档确认。

译文提交为 `3a21f17035b51c61f592858e2b5ca7a6e9c51d6d`；新 catalog 为
`9b4f2e06ce73c07cc0ca9810db96caba529a5f15b175558803b21f1313fb2b4e`，migration 为
`456baa4ae824b48ffdd8c7ec72c1c93055e8fb4c51077e79eab0852d8c2747a0`。迁移结果为
7 条 revision changed、29,821 条 unchanged、0 ambiguous/unmapped，7 个 successor 待重新审核，
不继承 done。pending 新增第 16 项（Eyal 全库译法）和第 17 项（lore 标题“不死猎人指南”两处），
由宿主在证据提交中写入。完整结果见[窗口16出版证据](evidence/quality/repair-window-16-20260923/PUBLICATION.md)。

窗口16的证据提交、queue rebuild 与 push 已完成（`95070219`）。

审核263（`batch-8963e835a427bdbf7ae1`）已闭合，结果为 **75 done / 5 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 67 OK / 13 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致）；contextual `claude/claude-opus-5-5` full-000 为 10 OK / 3 ISSUE。
16 个观察裁决为 8 confirmed、6 refuted、2 advisory。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `07d04ea8`，
详见[263宿主证据](evidence/quality/production-batches/batch-8963e835a427bdbf7ae1-host-evidence/summary.md)。本批无新增 pending。

下一步按 1:1 节奏开修复窗口17，仅处理 263 的 5 条：猎头者挑战“暂停敌人”误述（实为敌人失去对你的锁定）、Exploit Weakness 删近战限定、
单项效果抵抗提示泛化、教程结束文本词中硬换行、思维形态说明多余换行与“狂战士”名不一致。
范围见 `.ai/task/batch-8963e835a427bdbf7ae1/WINDOW17-REPAIR-DECISION.json`；可复用窗口16 helper（verify.py 的 LF/TAB 对照 source；verify_migration 有两处条数硬编码），
失败的 FINAL 之后必须接 RE_REVIEW；FINAL 中任何 ISSUE（即使宿主判 advisory）都会让 DONE 检查失败。

修复窗口17已完成审核263确认的5条：猎头者挑战播报改为“你取下了 %s 的首级，令本层所有敌人为之迟疑”，不再误述为“暂停”；Exploit Weakness 写明近战攻击命中并恢复结尾 `\n\t\t`；单项效果抵抗提示改为“效果抵抗几率/完全抵抗该特定效果的几率”；教程完成文本删去3处词中硬换行（LF 14→11）；思维形态说明恢复原文换行结构（LF 7→3），并将 `warrior` 按本库术语译为“战士”。

`execute-01`（`codex/gpt-5.6-sol`）实施5条；`REVIEW(0)/full`（`codex/gpt-6-sol`）为4 OK / 1 ISSUE，确认 `R0-HEADHUNTER-OVERSTATE`：增译“失去对你的锁定”扩大了 `setTarget` 的实际范围；`execute-02` 仅删去该分句。`FINAL(1)/full`（`claude-opus-5-5`）为5 OK并收敛。完整门禁17/17通过且含严格构建，状态为 `DONE_VERIFIED`。两个 executor、两个 reviewer child 均已归档确认；publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `8390dd69d6d3ea359ada0ea2ea838cd533e14aa4`；新 catalog 为 `78635878a70f7ff2d9a1d4e36e7ad9115ab8a80d906670ecff0fce7332abd239`；migration 为 `5168dcc75a66cf6b89dc5c5ee1f0753064d427cc9461ad4a7ca1680c0fb084ec`。迁移结果为5条 revision changed、29,823条 unchanged、0 ambiguous/unmapped，5个 successor 待重新审核且不继承 done。完整结果见[窗口17发布证据](evidence/quality/repair-window-17-20260923/PUBLICATION.md)。

窗口17的证据提交、queue rebuild 与 push 已完成（`7cf827e3`）。

审核264（`batch-abb89c7e815afaa13bb2`）已闭合，结果为 **76 done / 4 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 70 OK / 10 ISSUE（harvest 前逐位比对 80 个回显 identity 全部一致）；contextual `claude/claude-opus-5-5` full-000 为 7 OK / 3 ISSUE。
13 个观察裁决为 7 confirmed、4 refuted、2 advisory。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `7031c106`，
详见[264宿主证据](evidence/quality/production-batches/batch-abb89c7e815afaa13bb2-host-evidence/summary.md)。本批无新增 pending。

下一步按 1:1 节奏开修复窗口18，仅处理 264 的 4 条：“#Target# is being crushed”误译“被击碎”（改“正被碾压”）、队友行为菜单 Standby“乖乖站好”（改“待命”）、
Offhand Jab 删去“以徒手突袭替代副手攻击”并多一处换行、Z’quikzshl 日记两处语义误译（trivial、corruption of his own name）与“它/他”混用及 Ruby of Eldoral 丢“红宝石”。
范围见 `.ai/task/batch-abb89c7e815afaa13bb2/WINDOW18-REPAIR-DECISION.json`；可复用窗口17 helper（verify.py 的 LF/TAB 对照 source；verify_migration 有两处条数硬编码）。

修复窗口18已完成审核264确认的4条：“#Target# is being crushed.”由“被击碎”改为进行态“正被碾压”；队友行为菜单 `Standby` 由“乖乖站好”改为与日志一致的“待命”；`Offhand Jab` 首句补出以出其不意的徒手攻击替代通常的副手攻击，并删去一处多余换行，使 LF 与原文一致；Z’quikzshl 日记改正 `trivial`、名字走音末句、代词与“艾德瑞尔红宝石”，并把 `not ready for the rites of lichdom` 改为“还没准备好接受巫妖仪式”。

`execute-01`（`codex/gpt-5.6-sol`）实施4条；`REVIEW(0)/full`（`codex/gpt-6-sol`）为3 OK / 1 ISSUE，确认 `R0-ZQUIK-RITES-READINESS`：“没有做巫妖的条件”把准备程度改成资格判断；`execute-02` 仅改该分句。`FINAL(1)/full`（`claude-opus-5-5`）为4 OK并收敛。完整门禁17/17通过且含严格构建，状态为 `DONE_VERIFIED`。两个 executor、两个 reviewer child 均已归档确认；publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `8f71effdeded7b84df4fa5d9625289d0d10a0b4b`；新 catalog 为 `2cd472deee7159e35cb53656b3311a9232752be19817adb5edee7e5db494b7c2`；migration 为 `4847d321cc828a85d29b12b3c05a399eee35a700288d9ade838f8b84a443f58f`。迁移结果为4条 revision changed、29,824条 unchanged、0 ambiguous/unmapped，4个 successor 待重新审核且不继承 done。完整结果见[窗口18发布证据](evidence/quality/repair-window-18-20260923/PUBLICATION.md)。

窗口18的证据提交（`ad68e95b`）、queue rebuild 与 push 已完成；首次证据提交在 verify_pack 未通过时被推送（publication 把 pack manifest 副本放进了 orchestration/），已由更正提交 `47283341` 移回窗口根目录并记录 verify_pack 通过。

审核265（`batch-2a0994cfc83862de29c3`）已闭合，结果为 **76 done / 4 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 72 OK / 8 ISSUE；lane-000-0 两处判 OK 的 identity 回显错误，harvest 前逐位比对发现并由宿主手工归因（原字节留档）。contextual `claude/claude-opus-5-5` full-000 为 5 OK / 3 ISSUE。
11 个观察裁决为 7 confirmed、2 refuted、2 advisory。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `1fc4af85`，
详见[265宿主证据](evidence/quality/production-batches/batch-2a0994cfc83862de29c3-host-evidence/summary.md)。本批无新增 pending。

下一步按 1:1 节奏开修复窗口19，仅处理 265 的 4 条：念动弓说明（漏“每回合”“伤害”与一个行首 TAB）、Burrow 说明（第三行空格代替 TAB、漏“土质”）、
Nightshade 陷阱（漏“中毒”，持续 4 回合应同时覆盖震慑与中毒）、野蛮种族记载（mod-tome.lua:43247 位于 load.lua 段但因后写覆盖而实际生效的重复行：首句、speech、几百年、烈火纪末期、恶魔释放酸液/黑暗之云）。
范围见 `.ai/task/batch-2a0994cfc83862de29c3/WINDOW19-REPAIR-DECISION.json`；可复用窗口18 helper；PUBLICATION-SCOPE 要写明 pack manifest 副本放在窗口根目录。

修复窗口19已完成审核265确认的4条修复：念动弓说明补“每回合”、将 `attack` 译为“命中”并恢复行首 TAB；`Burrow` 第三行恢复 TAB 并补“土质墙壁”；`Nightshade` 补“中毒”且明确4回合覆盖震慑与中毒；野蛮种族记载仅改 `mod-tome.lua` 中 `section mod-tome/load.lua` 下因后写覆盖而实际生效的那一行，完成首句、言语能力、时间、烈火纪、恶魔能力、理论支持及最终4处子串修正。`REVIEW(0)` 的2项 ISSUE、`FINAL(1)` 的1项 ISSUE均确认并修复；`RE_REVIEW(2)` 为4 OK；`FINAL(3)` 首次 `f3a1` 因英文导语判无效、不入账，重试 `f3a2` 为4 OK并收敛。完整门禁17/17通过且含严格构建，状态为 `DONE_VERIFIED`。3 个 executor、4 个有效 reviewer 及无效 `f3a1` 均已归档确认；publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `e602df35477fe2a6f2ffa9fd66029b51e83186a7`；新 catalog 为 `c5085a75a7796f11c91d64f39f454ac2f10dea491b28565222fdea5883057d35`；migration 为 `e5935d7e04f86d7d3a09d9a9e6d2afcc69c0f5e3a8c8b1ace3fac0e7a1649fec`。迁移结果为4条 revision changed、29,824条 unchanged、0 ambiguous/unmapped，4个 successor 待重新审核且不继承 done。完整结果见[窗口19发布证据](evidence/quality/repair-window-19-20260923/PUBLICATION.md)。范围外遗留为同一 source 的 `lore/misc` 段旧句；该行运行时被覆盖、不生效，本窗口未修改，留待后续审核。

窗口19的证据提交（`601cb466`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核266（`batch-d0f6e929a87d869ee983`）已闭合，结果为 **73 done / 7 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 71 OK / 9 ISSUE，80 个回显 identity 全部一致、均以原生日志收取；contextual `claude/claude-opus-5-5` full-000 为 2 OK / 7 ISSUE，与 surface 确认项同向。
16 个观察裁决为 14 confirmed、1 refuted、1 advisory。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `bd5a0dfd`，
详见[266宿主证据](evidence/quality/production-batches/batch-d0f6e929a87d869ee983-host-evidence/summary.md)。本批无新增 pending。
冻结 MISS 两条：窗口19后继的 load.lua 段 lore 行（本批 OK），以及失落商人日志行 `The merchant carefully hands you: %s`——已登记于 known-dead-keys.json 的死键，译文正确按 done 闭合，死键迁移仍待维护者。

下一步按 1:1 节奏开修复窗口20，仅处理 266 的 7 条：念力核心项圈外观（删“似乎”增“所有”）、邪眼 bloodshot、Utterly Destroyed 说明（thrill of the death 与 creature）、
离线模式说明的“版本检查”、时空法术类别说明（学派）、梅琳达成就“落难少女”、蛛毒魔棒未鉴定名 wand＝魔杖。
范围见 `.ai/task/batch-d0f6e929a87d869ee983/WINDOW20-REPAIR-DECISION.json`；setup 脚本 `setup_window20_task.py` 已生成，helper 从窗口19复制（verify/verify_catalog/verify_migration 的条数 4→7）。

修复窗口20已完成审核266确认的7条修复：念力核心项圈外观保留“似乎”并去掉增译的“所有”；邪眼 `bloodshot` 改为“布满血丝”；`Utterly Destroyed` 说明将 `creature` 改为“生物”、`thrill of the death` 改为“击杀带来的快感”；离线模式说明修正版本检查、角色仓库、游戏更新信息及错位空行；时空法术类别改为“操控时间的法术学派”；梅琳达成就改为“落难少女拯救者”；蛛毒魔棒未鉴定名改为“魔杖”。`REVIEW(0)` 的1项 ISSUE 与 `FINAL(1)` 的1项 ISSUE均确认并分别由 `execute-02`、`execute-03` 修复；`RE_REVIEW(2)` 与 `FINAL(3)` 均为7 OK。完整门禁17/17通过且含严格构建，状态为 `DONE_VERIFIED`。3 个 executor、4 个 reviewer child 均已归档确认；publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `ffa53351b8e490c859ec029fdc655bd4c8f3bab5`；新 catalog 为 `e97aaf89de5fca113d500beccb80df23b2c5731eb3f8215495e93805b6c4c76c`；migration 为 `99c7ebd419a3f9ceebf2bba12de24d4561cbba3805972d941cda1f7fa83c6def`。迁移结果为7条 revision changed、29,821条 unchanged、0 ambiguous/unmapped，7个 successor 待重新审核且不继承 done。完整结果见[窗口20发布证据](evidence/quality/repair-window-20-20260923/PUBLICATION.md)。本窗口的空行教训：`verify.py` 只比较 LF/TAB 数量，发现不了空行挪位；多段 target 必须逐行比较空行下标。

窗口20的证据提交（`11b3e963`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核267（`batch-551646311ef6b61a7a4d`）已闭合，结果为 **74 done / 5 repair_required / 1 blocked**。
surface 四组 `codex/gpt-6-sol` 为 73 OK / 7 ISSUE；lane-000-1 一处判 OK 的 identity 回显错误，harvest 前逐位比对发现并由宿主手工归因（原字节留档）。contextual `claude/claude-opus-5-5` full-000 为 2 OK / 5 ISSUE。
12 个观察裁决为 9 confirmed、1 refuted、2 pending（同一条的 surface 与 contextual 两个观察）。17/17 门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `86a4257a`，
详见[267宿主证据](evidence/quality/production-batches/batch-551646311ef6b61a7a4d-host-evidence/summary.md)。
新增 pending 第 18 项：枯萎死亡描述“死前吸入过多剧毒瘴气”，随死亡描述词表整族待用户裁定（见 `evidence/quality/pending-user-review.md`）。

下一步按 1:1 节奏开修复窗口21，仅处理 267 的 5 条：Sun Flare 技能名改“太阳耀斑”（维护者 2026-09-23 批准）、盾牌敏捷格挡日志“(%d deflected)”、
枯萎遗迹 lore 多出的换行与制表符、Solipsist 职业引语（共同之梦、发掘梦境潜能）、静电网漏“每停留一回合”累加。
范围见 `.ai/task/batch-551646311ef6b61a7a4d/WINDOW21-REPAIR-DECISION.json`；setup 脚本 `setup_window21_task.py` 已生成，helper 从窗口20复制（条数 7→5）。

修复窗口21已完成审核267确认的5条修复：`Sun Flare` 技能名按维护者2026-09-23批准由“日珥闪耀”改为“太阳耀斑”；敏捷防御格挡日志由“(%d 敏捷防御)”经复审最终改为“(%d 被抵挡)”，与同技能说明“抵挡攻击”一致；荒芜遗迹 lore 删去原文没有的换行与制表符；`Solipsist` 引言改为“世界是其居民共同的梦……发掘梦境的潜能”；静电网说明补出“每停留一回合”的累加机制，并保持3个换行与制表符。`REVIEW(0)` 为4 OK / 1 ISSUE，技能名“静电网络”与说明“静电捕网”不一致因技能名行不在窗口内而裁决为 advisory，留作后续修复候选；`FINAL(1)` 为4 OK / 1 ISSUE，确认“被偏转”与说明“抵挡”不一致；`execute-02` 改为“被抵挡”后，`RE_REVIEW(2)` 与 `FINAL(3)` 均为5 OK。完整门禁全部通过且含严格构建，状态为 `DONE_VERIFIED`。2个 executor、3个 reviewer child 均已归档确认；publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `5342f1b06943cefb1d9f393d2a186c9c6cc8a6e6`；新 catalog 为 `b7389c85c66e7e755fd3904f3072ca0d5688901a6bb548f8e662f4c11a9f77ae`；migration 为 `e0b1d6770808ef8df692f46880076b2b792443a54134343b39bd72edf34400c2`。迁移结果为5条 `revision_changed`、29,823条 `unchanged`、0条 `ambiguous/unmapped`，5个 successor 待重新审核且不继承 `done`。完整结果见[窗口21发布证据](evidence/quality/repair-window-21-20260923/PUBLICATION.md)。本窗口的流程教训是：SPEC 指定替换词前必须先检查同技能相邻条目（尤其 `info`）已经使用的译法。

窗口21的证据提交（`460fd473`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核268（`batch-35fcb3df1560de7c5b2d`）已闭合，结果为 **74 done / 6 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 72 OK / 8 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 为 4 OK / 4 ISSUE。
12 个观察裁决为 10 confirmed、2 refuted，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `d6bed738`，
详见[268宿主证据](evidence/quality/production-batches/batch-35fcb3df1560de7c5b2d-host-evidence/summary.md)。
驳回两条：瞬间技能失败日志补出的“本回合无法再次使用”即实现行为；难辨构造（Indiscernible Anatomy）英文写“几率免疫暴击”，实现为按比例削减暴击倍率，现译贴合实现。

下一步按 1:1 节奏开修复窗口22，仅处理 268 的 6 条：欺诈斗篷“看起来像人类”、电鳗尾“其实没多大关系”、厄奇斯成就漏 mad/onslaught、
太阳堡垒创建者挂坠的赤铁矿之月与金色太阳、腐化蒸汽主语缺失、分裂（Mitosis）漏视线内/召唤上限/技能生效期间三处限定。
范围见 `.ai/task/batch-35fcb3df1560de7c5b2d/WINDOW22-REPAIR-DECISION.json`。

修复窗口22已完成审核268确认的6条修复：欺诈斗篷生效日志改为“一层幻影出现在#Target#周围，让%s看起来像人类”；电鳗尾炼金说明改为“电鳗到哪儿为止、尾巴又从哪儿开始？其实没多大关系”；厄奇斯成就补回“疯狂的”与“猛攻”；太阳堡垒创建者挂坠改为“赤铁矿之月遮蔽金色太阳”；腐化蒸汽补回主语，改为“腐化的蒸汽在目标位置升起”；分裂（Mitosis）补回视线内、召唤上限、技能激活期间三处限定，并恢复为与原文一致的7行。`REVIEW(0)/full` 为5 OK / 1 ISSUE，确认欺诈斗篷漏译“出现”；`execute-02` 修复。`FINAL(1)/full` 为5 OK / 1 ISSUE，确认电鳗句将 `stop` 译成起点（源于宿主 SPEC 措辞）；`execute-03` 修复。`RE_REVIEW(2)/full` 为5 OK / 1 ISSUE，宿主因 `Cunning=灵巧` 为本库属性名而驳回；`FINAL(3)/full` 为6 OK，任务收敛。完整门禁全部通过并含严格构建，状态为 `DONE_VERIFIED`。3个 executor、4个 reviewer child 均已归档确认；本 publication child 待宿主归档。本窗口无新增 pending。流程教训是：SPEC 中给出的示例译文本身也必须逐词对照原文。

译文提交为 `e3ad691d2819f29598d974d99d0139a3b373de20`；新 catalog 为 `b239aafd8d5887f41de2065795f6913737ac9847cac1725c390e2fc2a421a197`；migration 为 `1cd5583de937a86439dcbc7ae0c2953e201574c2c53aa687ab592d39a5479508`。迁移结果为6条 `revision_changed`、29,822条 `unchanged`、0条 `ambiguous/unmapped`，6个 successor 待重新审核且不继承 `done`。完整结果见[窗口22发布证据](evidence/quality/repair-window-22-20260923/PUBLICATION.md)。窗口22的证据提交（`d5d6e0aa`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核269（`batch-cfd398e96c387cc31dc0`）已闭合，结果为 **77 done / 3 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 71 OK / 9 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 为 8 OK / 1 ISSUE。
10 个观察裁决为 4 confirmed、3 refuted、3 advisory，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `de307884`，
详见[269宿主证据](evidence/quality/production-batches/batch-cfd398e96c387cc31dc0-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口23，仅处理 269 的 3 条：夺心魔任务“至少清除一个威胁”（漏 at least）、埃亚尔之怒（eyal's fury）技能类别说明漏“周围的”、
奥术漩涡说明漏射线贯穿路径上全部目标与本体同时受伤。范围见 `.ai/task/batch-cfd398e96c387cc31dc0/WINDOW23-REPAIR-DECISION.json`。

修复窗口23已完成审核269确认的3条修复：夺心魔任务开场补回“至少”，改为“你被派去至少清除一个对夺心魔的威胁。”并保留末尾换行；埃亚尔之怒说明补回“你周围的”；奥术漩涡说明改为射线射向视野内随机敌人，对附着目标与射线路径上所有目标造成伤害；无敌人时，本回合漩涡对附着目标造成的伤害提高 50%；目标死亡时，残余伤害转化为半径 2 的奥术爆炸。`execute-01`（`codex/gpt-5.6-sol`）实施3条；`REVIEW(0)/full`（`codex/gpt-6-sol`）为 2 OK / 1 ISSUE，宿主核对 `timed_effects/magical.lua:2686-2687`（`624a673`）确认无敌人分支是一次 `eff.dam * 1.5` 伤害，而非目标易伤；`execute-02` 修复该句；`FINAL(1)/full`（`claude-opus-5-5`）为 3 OK，任务收敛。完整门禁全部通过并含严格构建，状态为 `DONE_VERIFIED`。2个 executor 与2个 reviewer child 均已归档确认；本 publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `78c3562727a947c49dd8ec65daff61707920b893`；新 catalog 为 `c975ad861660d866b62f8d2530be93926af2977852846d6367216e28e5d9e480`；migration 为 `d2075cb1e0938d0607405e8d8d85400e38b06f9245584e5838e455993014585f`。迁移结果为3条 `revision_changed`、29,825条 `unchanged`、0条 `ambiguous/unmapped`，3个 successor 待重新审核且不继承 `done`。完整结果见[窗口23发布证据](evidence/quality/repair-window-23-20260923/PUBLICATION.md)。窗口23的证据提交（`62e2c555`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核270（`batch-b7ce18a7bdce48ba8086`）已闭合，结果为 **74 done / 6 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 66 OK / 14 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 因 JSON 前带英文导语被判无效并归档，重派 full-001 为 12 OK / 2 ISSUE。
16 个观察裁决为 7 confirmed、5 refuted、4 advisory，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，六个 reviewer child 均已归档确认。证据提交 `0480131c`，
详见[270宿主证据](evidence/quality/production-batches/batch-b7ce18a7bdce48ba8086-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口24，仅处理 270 的 6 条：飞镖发射器抵抗日志“睡眠”改与效果名“被镇静”一致；敏锐直觉说明去“直觉”并恢复 3 行；
狂热 4 次快速攻击（each 指每次攻击、always 总是攻击被追踪猎物、盾牌句前空行）；奥术至上法杖描述恢复换行并改“单独一件似乎并不完整”；
吸食抗性说明删多余换行；意志属性说明删增译“精神力”。范围见 `.ai/task/batch-b7ce18a7bdce48ba8086/WINDOW24-REPAIR-DECISION.json`。

修复窗口24已完成审核270确认的6条修复：飞镖发射器抵抗日志“睡眠”改为“镇静”，与效果名“被镇静”一致；敏锐直觉说明去掉增译的“直觉”并恢复原文3行；狂热说明改为4次快速攻击、每次攻击造成伤害、附近有被追踪的猎物时总是攻击它，并恢复盾牌句前的空行；奥术至上法杖描述恢复两句间换行，末句改为“单独一件时似乎并不完整”（该法杖与奥术理解之帽成套）；吸食抗性说明删去多余换行恢复2行；意志属性说明删去增译的“精神力”。`execute-01`（`codex/gpt-5.6-sol`）实施6条，宿主逐条逐行核对行数、空行下标与行首 TAB；`REVIEW(0)/full`（`codex/gpt-6-sol`）为 6 OK，`FINAL(1)/full`（`claude-opus-5-5`）为 6 OK，任务收敛，无修复轮。完整门禁全部通过并含严格构建，状态为 `DONE_VERIFIED`。1个 executor 与2个 reviewer child 均已归档确认；本 publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `fc091427e93c42cd73fad1b49cd450580e9778e8`；新 catalog 为 `6870324089f8919e8cef200a38011d2493e276ac717690655f2abede3c1b7b3c`；migration 为 `534b8e86c940f0be3dedb147e8e3381b12ec2a101b5b70958e3181b7ad8d41cd`。迁移结果为6条 `revision_changed`、29,822条 `unchanged`、0条 `ambiguous/unmapped`，6个 successor 待重新审核且不继承 `done`。完整结果见[窗口24发布证据](evidence/quality/repair-window-24-20260923/PUBLICATION.md)。窗口24的证据提交（`57652734`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核271（`batch-ae5b45a9e4a7a8ffdb3e`）已闭合，结果为 **72 done / 8 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 65 OK / 15 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 为 8 OK / 7 ISSUE。
22 个观察裁决为 14 confirmed、7 refuted、1 advisory，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `df789866`，
详见[271宿主证据](evidence/quality/production-batches/batch-ae5b45a9e4a7a8ffdb3e-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口25，仅处理 271 的 8 条：疲劳圣印说明补“敌人”限定；指令水晶球（亡灵）描述改“黑暗的幻象充满脑海”；血祭施法效果说明改指堕落系法术；
减速（Speed Sap）说明补末尾换行；摄魂剑·莫瑞格日志改“汲取被困的灵魂，施展…”；第一滴血补“命中时”与“（若能标记）”；夏图尔壁画阿马克泰尔创世文本；盗匪日志（贵族迟早追杀、绑在柱上烧死）。
范围见 `.ai/task/batch-ae5b45a9e4a7a8ffdb3e/WINDOW25-REPAIR-DECISION.json`。

修复窗口25已完成审核271确认的8条修复：疲劳圣印改为“经过圣印的敌人会减速”；指令水晶球（亡灵）描述改为“黑暗的幻象充满你的脑海”；血祭施法效果改为“堕落系法术消耗生命值而非活力值”；减速说明恢复末尾换行与缩进；摄魂剑·莫瑞格日志改为“汲取了%s的被困灵魂，施展%s”；第一滴血补回“命中时”与“（若能标记）”；阿马克泰尔壁画 lore 逐句重译；盗匪首领日志恢复威胁语气与“绑在柱上烧死”。`execute-01`（`codex/gpt-5.6-sol`）实施8条，宿主逐条逐行核对行数、空行下标与行首 TAB；其原生日志含2次 Codex `wait` function_call，仓库解析器白名单未收录，宿主经仅增补这两类条目的临时解析器副本收取，详见 `HOST-EXECUTOR-AUDIT.json`。`REVIEW(0)/full`（`codex/gpt-6-sol`）为 7 OK / 1 ISSUE：血祭施法效果英文原句本身与 `incVim` 实现不符，实际仅在活力不足时以生命支付缺额；译文忠实原句，宿主判为 advisory，并登记 pending 第19项。`FINAL(1)/full`（`claude-opus-5-5`）为 8 OK，任务收敛，无修复轮。完整门禁全部通过并含严格构建，状态为 `DONE_VERIFIED`。1个 executor 与2个 reviewer child 均已归档确认；本 publication child 待宿主归档。

译文提交为 `805a9f155dff64cc18cf644b0af2856b0936e06f`；新 catalog 为 `38cb5f33c905a333728676e30a67692632830852be8790e532980702de21a18f`；migration 为 `f2ddf2cbd8e0610b40955d746594ed530f3dbadc05dee7153fff88b708434f38`。迁移结果为8条 `revision_changed`、29,820条 `unchanged`、0条 `ambiguous/unmapped`，8个 successor 待重新审核且不继承 `done`。本窗口新增 pending 第19项，pending 文件由宿主维护。完整结果见[窗口25发布证据](evidence/quality/repair-window-25-20260923/PUBLICATION.md)。

窗口25的证据提交（`27141793`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。随后以 `5c2f8459` 把 Codex `function_call`/`function_call_output` 加入原生解析白名单（附回归测试），此后不再需要临时解析器副本。

审核272（`batch-54be748f9582a3f09434`）已闭合，结果为 **75 done / 5 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 75 OK / 5 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 仅复核这 5 条，5 条均为 ISSUE 且与 surface 同向。
10 个观察全部 confirmed，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `594fbd4f`，
详见[272宿主证据](evidence/quality/production-batches/batch-54be748f9582a3f09434-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口26，仅处理 272 的 5 条：思维形态技能系说明“灵能召唤术”改“灵能召唤物”；罗尔夫致威斯曼信逐段重译（巨蚁母体、嘲讽、勇气，段落与空行对齐原文，地名用古老树林、德斯）；
泰坦的箭袋描述补“锋利”“几乎无法折断”等分句；阿塔玛森红宝石眼睛描述删多余换行并补“重创”；梅琳达任务日志补“袭击队”（夺魂魔保持）。注意：Weisman 本库有“魏斯曼”（mod-tome.lua:11443）与“威斯曼”（信件标题）两种写法，窗口内信件正文沿用标题的“威斯曼”，统一与否另议。
范围见 `.ai/task/batch-54be748f9582a3f09434/WINDOW26-REPAIR-DECISION.json`。

修复窗口26已完成审核272确认的5条修复：思维形态技能系说明将“灵能召唤术”改为“灵能召唤物”；《写给威斯曼的信 (1)》逐段重译，补回轻蔑、胆识与豪侠气概、巨蚁始祖、愚蠢等原意，地名采用“古老森林”“德斯”，并恢复原文8个换行及署名前空行；泰坦的箭袋描述补回“磨得锋利无比”“几乎无法折断”“比任何箭都更像长钉”；阿塔玛森丢失的红宝石眼睛描述删除多余换行，明确被毁的武器是阿塔玛森这具傀儡，并补回“给兽人以重创”；梅琳达任务日志补回“袭击队”。`execute-01`（`codex/gpt-5.6-sol`）实施5条，宿主逐条逐行核对行数、空行下标与行首 TAB；其冻结 prompt 因宿主写文件多一个尾换行，与 Paseo 实际投递文本相差一个 LF，宿主核实后将冻结 prompt 对齐投递文本并保留原件，详见 `HOST-EXECUTOR-AUDIT.json`。`REVIEW(0)/full`（`codex/gpt-6-sol`）为 3 OK / 2 ISSUE，宿主均判 confirmed：威斯曼信中的 Old Forest 应采用“古老森林”，而非窗口 SPEC 误取的“古老树林”；阿塔玛森眼睛描述中的“它”易被读作眼睛。`execute-02` 定点修复两处；`FINAL(1)/full`（`claude-opus-5-5`）为 5 OK，任务收敛。完整门禁全部通过并含严格构建，状态为 `DONE_VERIFIED`。2个 executor 与2个 reviewer child 均已归档确认；本 publication child 待宿主归档。本窗口无新增 pending。

译文提交为 `df937b894d02a01ff4ca0c1b2d7ccfd22918b2c4`；新 catalog 为 `2a349020c440d5766776ac1396bd949c94f99c0c97852b314543776fc9acf280`；migration 为 `6f8736fb807babfeda9ddd927ffc5958251ddd23bba538dc87f6ee40d6314302`。迁移结果为5条 `revision_changed`、29,823条 `unchanged`、0条 `ambiguous/unmapped`，5个 successor 待重新审核且不继承 `done`。审核272 surface 裁决记载的“LF 10→9”实测应为 8→9，裁决结论不变，详见[勘误](evidence/quality/repair-window-26-20260923/ERRATUM-BATCH272-LF.md)与[窗口26发布证据](evidence/quality/repair-window-26-20260923/PUBLICATION.md)。

窗口26的证据提交（`b2ebc16d`）、queue rebuild 与 push 已完成，提交前 verify_pack 通过。

审核273（`batch-5e69946bed52ed5a5cbc`）已闭合，结果为 **78 done / 2 repair_required / 0 blocked**。
surface 四组 `codex/gpt-6-sol` 为 71 OK / 9 ISSUE，80 个 identity 回显逐位一致；contextual `claude/claude-opus-5-5` full-000 复核这 9 条，为 8 OK / 1 ISSUE。
10 个观察裁决为 3 confirmed、7 refuted，无新增 pending。门禁含严格构建通过，两任务快照重放 `DONE_VERIFIED`，五个 reviewer child 均已归档确认。证据提交 `5aef7d5a`，
详见[273宿主证据](evidence/quality/production-batches/batch-5e69946bed52ed5a5cbc-host-evidence/summary.md)。

下一步按 1:1 节奏开修复窗口27，仅处理 273 的 2 条：“反魔法”提示说明第三行“拒绝使用法术”改为无法使用法术与奥术驱动的装备（forbid_arcane 是硬限制；contextual 判 OK，宿主按源码维持 confirmed）；
领袖的皇冠描述整句修复（许多人而非大部分、秩序与纪律、效忠皇冠、称呼统一为“皇冠”、纳格尔领土而非大陆）。另：窗口11 的 r2a1 reviewer（`4e9cc148`）曾因在界面中打开 tab 被取消归档，已于本批期间重新归档，与 w11 记录一致。
范围见 `.ai/task/batch-5e69946bed52ed5a5cbc/WINDOW27-REPAIR-DECISION.json`。

### 窗口7闭合时的暂停记录（历史）

用户于2026-09-22明确要求“这轮修复完成后暂停并撰写handoff文档”；该暂停已由2026-09-23指示解除。

审核253（`batch-ba766c90924912867b02`）已完全闭合，结果为 **72 done / 8 repair_required**。
证据提交`3927ca05a43daee81bb2a2fadaf77d2b3b881d0b`、收尾提交
`e103379a5e809923401aa0099cfbdc9f104725ca`，收尾后的queue、push、远端HEAD与SQLite evidence
head核验均已完成。详见[253宿主证据](evidence/quality/production-batches/batch-ba766c90924912867b02-host-evidence/summary.md)、
[finalize收据](evidence/quality/production-batches/batch-ba766c90924912867b02-host-evidence/FINALIZE-RECEIPT.json)
及[收尾核验](evidence/quality/repair-window-7-20260922/publication/review253-push-verification.json)。

修复窗口7的八个target已完成并提交为`312dcd6844f80fff34911999bffab7a8f954e34f`。四成员复审各轮
原始结果依次为R0 6 OK / 2 ISSUE、R1 6 OK / 2 ISSUE、R2 6 OK / 2 ISSUE、R3 7 OK / 1 ISSUE；
这些历史finding均保留。R0经宿主源码确认并有界修复疾病传播全部疾病和盾牌跃击动作；R1只接受
Mind Storm总量量词修复，spinneret兄弟项保持范围外advisory。第二轮后SENIOR scope audit对挽歌
触发条件为`keep`、对spinneret兄弟项为`narrow`，宿主仅接受一个触发句修复，默认cycle 3上限
没有扩大。R3的Vault选择坐标/落点观察裁决为非阻断advisory。最终full review为 **8 OK / 0 ISSUE**，
不倒改历轮原始结果。

最终完整门禁`run.4d0v0980`为17/17通过并含strict build；任务与452项、2,317,751 bytes的
immutable快照均`DONE_VERIFIED`。实施/复审22个child及publication child共23个均已确认归档；最终状态检查通过。
完整结果见[窗口7出版证据](evidence/quality/repair-window-7-20260922/PUBLICATION.md)。

一次catalog build和migration-chain已完成，不得重跑。当前catalog为
`0fece77f6c05306c2706b263729cc1a3b5fcdf1dc29f58bd41af380204595696`，migration为
`677e6622a2146f9f9686ee91c9d1bc3f02990c8d08547df721786877dd287325`；8 revision changed、
29,820 unchanged、0 ambiguous/unmapped，8个successor已入队且须重新审核，不继承旧done。

### 已完成的收尾与暂停边界

证据/catalog/migration提交为`bfa1a096da0b6d790167de0f600c7aff41dfcb59`，提交后的第二次queue rebuild、push与远端核验
均已于`2026-09-22T16:14:31.628477+00:00`完成；本地HEAD、origin/develop与SQLite evidence head一致。
队列实测 **22254 done / 1 repair_required / 24 blocked / 7549 queued**；本轮8个新revision逐条确认queued，须重新审核。
详见[收尾核验](evidence/quality/repair-window-7-20260922/closure/orchestration/.ai/task/repair-w7-20260922/PUBLICATION-CLOSURE.json)。

原452项immutable快照保持原字节；收尾增量共27项，包含publication生命周期、
提交/队列/push证明，与基础快照合并后独立重放为`DONE_VERIFIED`。
见[增量重放结果](evidence/quality/repair-window-7-20260922/closure/replay-verification.json)。
本交接和收尾证明随最终文档提交保存，提交后仅同步queue并push，不再产生译文或新批次。
（当时为STOP；已于2026-09-23由用户新授权解除，审核254已完成。）

旧Archmage、旧回忆录pending、`RW1-SIB-01/02`、旧blocked及范围外兄弟条目保持原状态。
`.ai/consult/`、recipe和15个旧source-workset继续保留。

### 已闭合的修复窗口6

窗口6两条修复（日记省略号前后空行、古战场成就惊扰行为）已完整闭合：译文提交
`38e666aaae9e5738819e3b6525398b9bfc9872eb`，证据/catalog/migration提交
`1351d3f4fb0f8efe4d017039ad236848a13290df`。第二次queue、push与远端/本地/SQLite三方核验
于14:06:43完成，4个child全部确认归档，最终STATE再次DONE_VERIFIED。
原97文件、765623 bytes的immutable包保持不变；发布收尾与生命周期证据已附在本批253
快照中独立重放。原生审计调用汇总12已纠正为11；冻结证据5处历史空白有逐字节例外记录，
没有清洗或改写冻结输入。17/17门禁及严格构建通过。

窗口6闭合时catalog为`6f08ccf5394d2f0431a066c1315ba5abcdeaed1928e4781a0b1cb65e37e68405`，
窗口6migration为`92da0238e3a17f7b5d3b4e46156ef0b9d5bacfd653bb2e00618d6f0ede25a83d`。
两条successor曾重新入队，本次253均通过审核；不得重复catalog build/migration。
窗口6闭合时队列实测22182 done / 1 repair_required / 24 blocked / 7621 queued；后续以本批
收尾rebuild与实际SQLite结果为准。

审核252及Git索引测试夹具维护已闭合并于13:27推送`805b67263c3359441a4e6e12f3ebd0d2bdc5a0da`。
夹具已改为长度无关的非法索引构造；生产解析器未改，默认131模块测试及7/8/12/40位负例通过。
252原失败日志和有界诊断均保留；后续门禁恢复默认Git环境。

### 已闭合的修复窗口5

窗口5执行时用户授权连续审核和每批 push；现以顶部暂停指令为准。审核 250、251 均已完成；窗口 5 因高影响机制问题在
251 安全边界提前进入修复，没有等待第三批。18 条修复由两次真实 repair preflight 的 16 条
（250 十条、251 六条）和 251 宿主独立补充 2 条组成；补充条目没有被伪称为生产
`repair_required`。

译文提交为 `f0560f5d888a9c5a84f21c1216e43eb1645437d3`，只修改 `mod-tome.lua`
的 18 个 target；source、source_tag、args_order 等保持不变，只有原授权 `e56b636891…`
恢复源码 1 LF / 2 TAB 布局。没有术语库变更。三轮上限后的最终复审发现 source 188 的
`hum` 被译成“呼吸”，任务真实暂停 `WAIT_USER`；用户“同意”额外一轮，SENIOR 范围校准
`keep`，仅改成“嗡嗡作响”。本次 `max_cycles=4` 是单次明确授权，不是后续默认规则。

最新最终全量原始结果为 16 `OK` 加 2 `ISSUE`，不是 18 `OK`。宿主裁决范围内无
accepted/deferred 后 completed：回忆录 source 358 清醒时喂水及 source 380 前往 Elvala
的未编辑子句保留 pending；Corruptor 职业 birth descriptor existing 条目不强制映射叙事 `_t`，
保留 advisory。其他历轮范围外回忆录和称谓建议保持原记录，不新增修复。身份或读取边界不合格的
复审尝试及 fresh retries 均原样保留，未把无效结果用作审核依据。

最终完整门禁 `run.rlohbmvk` 为 17/17 通过并含严格构建，任务 `DONE_VERIFIED`。738 文件、
8,798,915 bytes 的冻结包已独立 snapshot 重放通过；归档 STATE 使用 immutable checkpoint。
五个 candidate catalog 文件、migration 与 12 份 publication 原始附件均已逐字安装并复核。
窗口5闭合时 catalog 为 `c267a00eaf39f49b99266912241cfed79dfcbda440903763975ea2e4334a239d`，
migration 为 `198b6812cf2fc2865016eb39153f90a70f244d3984a6ca81009bde8c2e897b6a`。
单次 catalog build 与 migration-chain 已完成，禁止重做；18 条 revision changed、29,810 条
unchanged，0 ambiguous/unmapped，18 个 successor 已入队且须重新审核，不继承旧 revision 完成态。
完整边界、哈希与计时见[窗口5出版证据](evidence/quality/repair-window-5-20260922/PUBLICATION.md)。

窗口5证据提交`901fce3886d5b565bc55b205e5ab27086621aa8f`、提交后的第二次queue rebuild、
push及远端复核均已于12:28完成，18个successor当时逐条验证入队；不再重做。
旧Archmage、范围外pending、旧blocked及`RW1-SIB-01/02`不扩大；`.ai/consult/`、`recipe` 和 15 个旧 source-workset 保留，不纳入
本次提交或清理。

## 审核251：修复窗口5第二批，提前修复边界

`batch-c8180aa79c1822c18e7c`，80条固定tome来源，**74 done / 6 repair_required**。
12条正式上下文复核；16项观察裁决为9 confirmed、3 refuted、4 advisory。另2条独立补充复核
确认击退碰撞日志和可用于治疗的精神暴击日志，保持原生产状态不变，单独纳入修复。
9个真实child全部归档，其中6份有效结果、3份拒收结果；两次revision标识错误及一次读取越界
均保留原始证据，未修补输出或冒充正式结果。最终Opus复审有效，5个有效Sol结果来自surface及补充任务。
三个任务及206文件、1,522,597 bytes的独立快照均DONE_VERIFIED，17项完整门禁与严格构建通过。
证据提交 `e0148fc67c09c8b1f6da0fab77b30aeface0e7f5` 已finalize，运行时contextual字节与提交逐一核验归档。
详情见[251宿主证据](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/summary.md)和
[finalize收据](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/FINALIZE-RECEIPT.json)。

正式修复范围：暴击失衡值方向、闪避适用范围、盾牌抵御/时期/时间修饰语、受伤触发描述、战术边框用途、
伐木工说话状态及恐怖描述。兽族忍耐命名、人物音译、轮/回合只记建议；击退、潜行及按物品分项的聚焦效果误报撤销。
提前修复依据见[窗口决定](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/orchestration/.ai/task/batch-c8180aa79c1822c18e7c/WINDOW5-EARLY-REPAIR-DECISION.json)。
补充两条为 `e68cd1e92d…`、`e6976768f9…`，来源见[补充裁决](evidence/quality/production-batches/batch-c8180aa79c1822c18e7c-host-evidence/orchestration/.ai/task/batch251-host-contextual-20260922/HOST-ADJUDICATION.json)。

## 审核250：修复窗口5第一批

`batch-990137011625a41fa36b`，80条固定tome来源，**70 done / 10 repair_required**。
12条上下文复核；22项观察为19 confirmed、1 refuted、2 advisory，按revision合并为10条待修复。
五位真实reviewer均已核验原始结果、读取边界及归档；两个任务及其独立快照重放均DONE_VERIFIED。
17项完整门禁和严格addon构建通过，证据提交 `16c82d316f07007ac7bcbb48ce1bcb2f202414d6` 已finalize。
详情见[250宿主证据](evidence/quality/production-batches/batch-990137011625a41fa36b-host-evidence/summary.md)及
[finalize收据](evidence/quality/production-batches/batch-990137011625a41fa36b-host-evidence/FINALIZE-RECEIPT.json)。
运行时contextual输入及输出与该提交逐字节一致，已保留归档并腾出下一批运行路径。

本批保留了三项宿主准备偏差的真实记录：首次未创建child的profile准备被拒、行政元数据晚补、
producer envelope提前导出后经preflight才重新冻结正式任务输入；所有contextual child均在后者之后派发。
251须在surface派发前完成SPEC/PLAN/SCOPE，并在contextual export前完成准确draft的preflight。
待修复包括幽灵人形、啃噬疫病后续死亡限定、触手追踪上限与换行、生命之泉分类、肢解含义、
自然精灵领地、法师初始知识和两条回忆录局部问题。
Ritch名称误报撤销；See Threads命名及其他非阻断建议不自动扩大修复范围。

## 审核249：修复窗口4第三批

`batch-1da0a9afd2d1888c2099`，80条固定tome来源，**72 done / 8 repair_required**。
13条上下文复核；22项观察裁决为14 confirmed、3 refuted、5 advisory，按revision去重为8条待修复。
5位真实reviewer均通过strict、原生来源与读取边界核验并确认归档；两个任务DONE_VERIFIED，
127文件宿主快照独立重放通过，17项完整门禁和严格addon构建通过。
详情见[249宿主证据](evidence/quality/production-batches/batch-1da0a9afd2d1888c2099-host-evidence/summary.md)。

待修复为`e454e243b1…`换行、`e4871be69c…`腰带修饰关系、`e4afe73e4f…`大罪字幕、
`e4c192463a…`兽人历史、`e4c5fea288…`自然精灵亚种、`e4c8e60909…`治疗反转敌方限定、
`e50eb91c9e…`诗句可能情态、`e542306f47…`潜行动作及句界。
基础伤害与颠茄毒素有源码支持；神器名称、传送门激活措辞、诗歌偏见意译与刃缘形状精细化仅为非阻断建议。
临时准备脚本的旧契约节号说明已更正，实际派发prompt始终允许完整契约；未改冻结输入或既有审核记录。
运行时contextual输入在finalize后已与提交原文逐字节核验并保留归档。

## 审核248：修复窗口4第二批

`batch-d83278160a384bef39ff`，80条固定tome来源，**73 done / 6 repair_required / 1 blocked**。
10条正式上下文复核；18项观察裁决为11 confirmed、1 refuted、6 advisory，confirmed按revision去重为6条。
另有一条长篇回忆录独立补充复核，作为窗口4的补充修复候选，不改写原surface OK或生产状态。
六位真实reviewer均通过strict、原生来源与读取边界核验并确认归档；三个任务DONE_VERIFIED，
157文件归档快照独立重放通过，17项完整门禁与严格addon构建通过。
详情见[248宿主证据](evidence/quality/production-batches/batch-d83278160a384bef39ff-host-evidence/summary.md)。

正式待修复项为峰顶限定`e318607df2…`、Fireflash爆炸半径`e359df96b1…`、建筑内外方位`e3aebb4595…`、
噩梦新增清醒限制`e3b3e027a2…`、毒素集合`e3ed20c85b…`、组装物品关系`e407b46fe5…`。
独立补充`e433115e63…`只修复已确认的裸体/兴奋场景、向东出发及气氛转折、条件性恨意和水晶塔比喻；
依据见[补充裁决](evidence/quality/production-batches/batch-d83278160a384bef39ff-host-evidence/orchestration/.ai/task/batch248-host-contextual-20260922/HOST-ADJUDICATION.json)。

`e3eec8e65c…`旧任务完成提示键与固定源码的空格不同；实际消费者在PlayerQuestPopup.lua。
已按正式host-block记录阻断，[完整来源归因](evidence/quality/production-batches/batch-d83278160a384bef39ff-source-attribution.json)包含全固定源码精确检索和调用位置。
不把表面OK算作done，不在此任务迁移source key。岩石藤蔓有源码支持，标题措辞、传送门简称/空格和
技能树简述只记建议；不扩大距离单位“码”的跨批策略。运行时contextual输入已在finalize后与已提交原文逐字节核验并归档。

## 审核 247：修复窗口 4 第一批

`batch-fe19bbe5e5898a0c3547`，80 条固定 tome 来源，**78 done / 2 repair_required**。
11 条进入上下文复核；13 条观察裁决为 4 confirmed、7 refuted、2 advisory，confirmed
按 revision 去重为 2 条。5 个真实 reviewer 均完成 strict、读取边界及来源核验并确认归档；
初筛和上下文两个任务均 DONE_VERIFIED，134 文件宿主快照独立重放通过。17 项完整门禁
及严格 addon 构建通过。详情见 [247 宿主证据](evidence/quality/production-batches/batch-fe19bbe5e5898a0c3547-host-evidence/summary.md)。

待修复项为 `e22d6fff0c…` 自定义贴图捐赠条件与段落换行、`e2be3d8377…` 腐化者自身腐化之血。
随机选敌、Dismissal 生命上限调整、失眠累积、锥形战吼、Feed Power 和死亡阈值均经固定源码
核验；不能因英文说明陈旧而回改当前译文。Fear 措辞、中文冒号空格及 Wanderer 省略仅为非阻断建议。

首次 surface prepared 配置与 profile 不符，在任何 child 创建前拒绝，保留原 prepared 记录；
实际使用 attempt 2 完整四 lane。首次 contextual export 因246旧运行时槽位占用失败，
对照已提交246原文逐字节核验后保留备份再重试；本批 preflight 在首次 freeze 之前实际通过。
不修改冻结候选，不更改工具防护。后续批次在 finalize 后按既有路径和哈希保留归档其运行时输入，
避免将旧槽位误认为新批次候选；不得据目录残留自行扩展当前 checkpoint 的 refs。

## 审核 246 与流程维护

- 审核 246（`batch-a5489a23ea457e1c6fde`）固定来源 tome，共 80 条，生产结果
  **74 done / 6 repair_required**。8 条正式语境复审、15 条观察裁决、17 项完整门禁和
  严格 addon 构建通过；证据提交
  `7b32ba676f6445970b1547f01b701ed79df8739c` 已 finalize。详情见
  [246 宿主证据](evidence/quality/production-batches/batch-a5489a23ea457e1c6fde-host-evidence/summary.md)。
- 另有 GRAPPLING、Battle Cry 两条宿主独立补充候选；没有改写原 surface 结果或伪造
  原生产 `repair_required`。相关 task 均 `DONE_VERIFIED`，child 已归档，冻结快照回放通过。
- 流程维护 `review-input-policy-20260922` 已 `DONE_VERIFIED`：13 文件统一角色、契约、
  三行 prompt 和实际消费者；249 项定向测试、完整 ci-gates、两轮独立双模型复审通过。
  维护提交已包含在远端基线 `9fb5ec1…`。详情见
  [流程修订验收](evidence/quality/review-input-policy-20260922/summary.md)。

## 修复窗口 3

244—246 的 14 条已确认 target 已在提交 `254ad2b…` 修正，其中 11 条来自原生产裁决，
Rosebloom、擒抱和战吼 3 条为宿主独立补充。候选及当前 `mod-tome.lua` SHA-256 为
`dd793e3d0f4336c881f30e7cb4e62bdccfc90dbaa263182ce4b57a18ad4c76c8`。

- 三批 repair preflight、固定源码核验、两轮合并修复、三轮四 lane v2 复审和最终全量复审完成。
  有效轮次是 r0a3、r1a3、r2a1，最终为 cycle 2 attempt 2 / `f2a1`，14 条全部 `OK`。
  r0a1/r0a2/r1a1/r1a2 为已记录的失效尝试，不计入有效复审；最终 terminal 坐标更正没有
  改写 envelope/raw/prompt/native 结果，也不是新增复审运行。
- 17 项完整门禁、严格 addon 构建和 `DONE_VERIFIED` 已完成。本次出版又从 464 文件、
  3,764,919 bytes 的受跟踪归档快照独立回放，RC 0；冻结包中 STATE 表示出版 child 之前
  全部译文/审核 child 已归档的验证边界，不是出版 child 的实时 STATE。
- 第一次 queue rebuild RC 0；catalog 只构建一次；migration-chain 只运行一次且 plan/check/apply
  均 RC 0。旧 catalog
  `2a8b6f4ac30dba6abff9e96dc37295d5e0f20acb5e4b97067160261b346e358d`
  迁移到 `75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`；
  migration 为 `5dccee54c4aed46e7b80f17a523eb61d9058add7926f7e292ba5eb45350ad0bf`。
  结果为 14 changed / 29,814 unchanged，0 ambiguous/unmapped，14 个 successor 已入队且必须重新审核。
- catalog/schema/policy、migration、464 文件归档及 publication 输入均按来源逐字节安装并复核。
  证据提交 `081d3a03…`、第二次队列同步和远端核验均已完成；完整边界、哈希与真实计时见
  [窗口 3 出版证据](evidence/quality/repair-window-3-20260922/summary.md)。

本窗口只修正获准 target，没有术语库修改、全局改名或跨批策略变更。固定 tome/engine 源码为
`624a67329fe2ad440c5b344785a9c73fcf22ae63`，244—246 无 DLC。距离单位“码”的跨批统一、
“不死亡灵”、generic spellcrit 空格及其他 advisory 均未借机扩大范围。

## 修复预检兼容维护

窗口4首次repair preflight中247通过，248的host_blocks_sha256被修复消费者旧字段集合拒绝，249未运行。
已将前置解析统一为现有封闭schema解析器，保留全部hash、来源、winner和preimage验证。
新增混合repair/blocked回归在修改前复现、修改后通过，3项定向测试和16项完整工具检查通过；
实际三个来源批次重新preflight全部成功（2/6/8条）。原失败尝试及产物保留，正式新workset使用attempt02路径。
此代码维护不改变addon输出，按矩阵跳过构建；后续17条正式译文修复仍需完整构建。
详情见[兼容维护证据](evidence/quality/repair-preflight-host-blocks-20260922/summary.md)。
当时须先提交本维护、同步队列并推送，再以新HEAD启动IMPLEMENT；这些步骤现已作为历史闭合，
已验证的catalog和17条preimage没有变化。

## 保留边界与历史

- Archmage `8b977dd836…`仍为范围外 pending；`RW1-SIB-01`、`RW1-SIB-02` 永久排除，
  不计可执行阈值，不改译或清状态。
- 244 证据提交 `79e81d1ac08123c626fedb9e299c033498e26f97`，78 done / 2 repair_required。
  245 证据提交 `023dcd03addcd342125f1c8908302250ec4af012`，77 done / 3 repair_required；
  244 补充更正和 245 收尾提交 `39cbeefcc36edae80da024cc84931c187381ba62`。旧证据保持不变。
- 修复窗口 2 译文 `14c755659d18a5f0989ec75d67f0245de3f0cc13`、证据
  `e117983a360b8dcb360ab35f0b5414148d534605` 已推送，不重做。
- REVIEWER 仍只使用冻结 envelope 内授权译文/术语正文；正式派发使用统一 builder 和三行 prompt，
  JSON 有效性、读取范围与 child 生命周期分别核验。更早细节见
  [历史交接](docs/handoff-history-through-20260919.md)，当前会话授权优先。
