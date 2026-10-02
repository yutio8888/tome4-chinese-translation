# 待授权术语修正

MMR-026：建议 draining physical 的 preferred 术语由“生命汲取”改为“生命汲取（物理）”，保留类别 T.GAME.DAMAGE、source_tag damage type、scope core。同步只改 mod-tome.lua 对应目标，notes 增补固定源码依据，不作全局替换。

固定核心commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 的 damage_types.lua:3243–3263 中，DEVOUR_LIFE 调用 PHYSICAL projector 造成物理伤害，再按实际伤害治疗施法者。旧名称表达了汲取生命但漏掉物理类型。现有 preferred 条目指定“生命汲取”，须先更新术语再修改译文。精确旧新 TSV 行见 TERM-DECISION-001.json。

待用户授权，尚未修改术语或该译文。
