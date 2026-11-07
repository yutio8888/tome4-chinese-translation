# 第九轮实机测试裁决（2026-11-07）

测试员 r9-opus（Opus 5.5，agent b46f3a87）：主战役，人类散兵 Opus9，简单／冒险，新存档；6 级（目标 12 级未达成，投石索射程下自动战斗脚本反复卡住）；德斯荒野→巨魔沼泽 1–3（击败普罗克斯）→德斯镇→最后的希望→魔法大爆炸之痕（死亡 1 次）→伊格→古老森林 1；约 85 个界面。15 条发现，均为 minor。

新存档复核：r8-opus-04（区域名「德斯镇」）在新存档中已生效，上一轮旧存档显示「德斯」确为存档内持久化的名字；r8-opus-03/05/06 与「铁制弹丸」已生效。

修改前均先检索同类问题。

- r9-opus-01 confirmed：以牙还牙「每回合最多可发动 %d + 1 次反击」在升级预览展开数列后读作「4, 4 + 1」，改为「每回合最多可发动 %d 次反击，外加 1 次。」（仍按实现 blocks+1）。
- r9-opus-02 confirmed：散兵投石索技能说明的「石弹」「弹矢」统一为「弹丸」（快速射击、飓风连射、连环炮击），延续 11-06 用户「改成弹丸」。同类检索：其余「弹矢」均为 Orcs 爆矢枪的 flechette，不改。
- r9-opus-03 confirmed：「双倍弓箭速度 (%d%% 回合)」→「双倍弓箭(%d%%回合)」，与通用「%s(%d%%回合)」一致。
- r9-opus-06 confirmed：抛射物「速度：%d%%%s」→「速度：%d%%，方向：%s」（Projectile.lua:58 的 %s 为方位词）。
- r9-opus-08 confirmed：解除陷阱说明改为「你搜索邻近的一个地格中隐藏的陷阱（侦察强度 %d）， 并在可能时将其解除（解除强度 %d， 取决于你的%s技能）。」；两处全角逗号后的空格是 talent-placeholder-spacing 规则要求（升级预览 token）。
- r9-opus-11 confirmed：护甲训练「减少 %d%% 近战和远程攻击的暴击几率」→「使近战或远程攻击对你造成暴击的几率降低 %d%%」。
- r9-opus-12 confirmed：Grim-looking fighter 名牌「面目狰狞的斗士」→「面色阴沉的斗士」（两处），与对话正文一致。
- r9-opus-14 confirmed：护送头衔「%s，迷路的堕落者」与 Fallen「堕落者」撞名；纯名称项按用户 2026-09-27 指示交 Gemini 4 Argon（`names-r9.md/json`），采用「%s，迷路的堕落术士」，双向检索无冲突。
- r9-opus-15 confirmed：技能 Buckler Expertise 与技能树 Buckler Training 同名「盾牌训练」；测试员建议的「盾牌专精」已被 Shield Expertise 占用。交 Gemini 4 Argon，采用「格挡专精」（与同树「格挡大师」成对），双向检索无冲突；以牙还牙说明同步。
- r9-opus-07 rejected（用户规则）：「%d%%， 持续」全角逗号后的空格是 2026-10-01 用户选定、lint `talent-placeholder-spacing` 强制的升级预览空格，按规则保留。
- r9-opus-13 rejected（重复）：护送「接受了任务“”！」即 r3-sonnet-05，上游时序问题，已驳回。
- r9-opus-05 confirmed，延后：UseTalents 状态「Active」译「激活」，但 `_t"Active"` 与移除持续技能对话、插件列表共用一个键，那两处「激活」正确；区分需插件代码。
- r9-opus-04、09、10 confirmed，延后（插件代码）：UseTalents.lua:79-80 LeftClick/MiddleClick 硬编码；Object.lua:646 getShortName 用半角「, 」拼接关键词；6 个经 `npc.store:interact(player)` 打开的聊天商店标题显示英文实体名（与 r7-opus-03 同根因）。
