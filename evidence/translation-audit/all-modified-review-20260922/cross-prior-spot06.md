# 上轮疑点交叉核验

你是只读 REVIEWER；用户指定 Codex/GPT-5.6-Sol/Medium 核验疑点。自然语言逐 claim 给出 confirmed/refuted/pending/advisory、源码路径/commit/行号和理由；不得写文件、修改译文、派发其他 agent。主代理只记录，不替你裁决。

条目：entry-01917；mod-tome.lua:25317

原文：
Your body's internal organs are indistinct, disguising your vital areas.
		You have a %d%% chance to shrug off all direct critical hits (physical, mental, spell).
		In addition you gain %d%% resistance to disease, poison, wounds and blindness.

译文：
你体内的器官模糊难辨，掩盖了你的要害部位。
		你受到的直接暴击（物理、精神、法术）的额外伤害降低 %d%%。
		你将额外获得 %d%% 的疾病、毒素、流血和目盲免疫。

Gemini 原始观察允许读取：evidence/spotchecks/modified-translation-spotcheck-20260921/reviewer-full-02.md 的 spot-06（含暴击概率 vs 减伤、wounds vs 流血、blindness vs 目盲）。不要读取宿主旧裁决。请独立核验。源码访问见 source-access.json；可沿固定源码调用链，包括 damage_types.lua 和 timed_effects，查属性实际生效。允许查询 terminology/combat.tsv 与同 section 相邻译文。不能仅凭属性名/英文描述/术语泛化。源码不足时明确 pending，不猜测。
