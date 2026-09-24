第275批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：69 OK / 11 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000 复核 surface 标出的 11 条：7 OK / 4 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。

宿主对15个观察裁决{"confirmed": 10, "refuted": 5}，结果74条完成、6条修复、0条pending。修复项：燃烧之手补“（及武器）”并把体力回复改为“每次命中”（stamina_regen_on_hit）；恶魔空间补“每回合”、持续光环与“法术结束时”；黑暗者古尔莫特墓志铭拆回三行（LF 6→5 实测）；回复纹身加载提示整句修复（预判伤害、提前准备，物品名统一“回复纹身”）；任务名 From bellow, it devours 与本库 38225 行对齐为“来自深渊，吞噬四方”；wispy purple cloak“脆弱的”改“缥缈的”。驳回：两处 ego 前缀空格、冒号标签尾空格、兽人部落“击败”同族一致、赤红守卫持续时间暴击（贴合 spellCrit 实现）。

攒批节奏：修复项计入积压（累计 13 条），未达 20 条不开窗。
