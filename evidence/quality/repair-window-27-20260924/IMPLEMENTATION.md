# 修复窗口 27 实施记录

任务 `repair-w27-20260924` 的唯一 EXECUTOR 仅修改了 `mod-tome.lua` 与
`tome-ashes-urhrok.lua` 中冻结 WORKSET 的 28 个 target，并在本目录加入实现验证证据。
未修改 source、source_tag、section、args_order、special、运行键、术语库或 `.ai/task`。

## 逐条修复

- `0523b49940c…`：恢复“恢复意识时平台正在从主大陆分裂”的时序，并补回灼热土地意象。
- `0c22616daee…`：改为带引号的“通往世界之巅的险途”。
- `0ed56881299…`：恢复“多数人逃跑”与“毁灭的工具”，去掉战争机器增译。
- `10419e2ec39…`：将邪恶火焰改为黑色火焰。
- `119af89312a…`：把斜体分别附着到“提取”和“自愿”。
- `120d3d48def…`：补回板子、手臂姿势、束缚装置、标准配发改造和抵达后首次避开监视。
- `12c3c45f81b…`：将三只手改为三条手臂，并恢复原文短句语气。
- `1be82f2f199…`：改为已从第一场伏击中脱身。
- `218c180b3f8…`：修复锦标赛、体能、乌尔洛克名内一致性及父亲对才智的直接热烈认可。
- `21d89ecd3e1…`：恢复堡垒悬停位置，去掉主动瞄准和“强大力量”增译，并修正错字、缺字。
- `28ea98973dd…`：将闪电意象改回火光。
- `295b84f066…`：Demonic Blood 合并目标首两行以匹配源串结构；9 个后续中文行保持两个 TAB 缩进，7 个技能加成行恢复 `-` 列表前缀，最终与源串同为 9 LF / 18 TAB；RE_REVIEW(2) 定点修复将“缴械和震慑抗性增加”改为“缴械和震慑免疫率提高”，以对应 `disarm and stun immunity`。
- `fcb8219fb8c…`：将主动拒绝改为无法使用法术和奥术驱动装备。
- `fd267689be1…`：整句恢复纳格尔国土、秩序与纪律、许多人、忠于皇冠等含义。
- `fd89fad0e8e…`：明确物理/时空伤害分别移除物理/魔法临时增益，每目标每回合各至多一项。
- `fd9c72bf32f…`：技能名改为“势不可挡的自然”。
- `fda88c96683…`：技能名改为“反射防御”。
- `fdff442a1e5…`：友方触发条件改为处在粘液中，并明确为双方各回复 1 点；将相邻的自身回复与友方回复分句合回同一行，最终与源串同为 5 LF / 10 TAB。
- `fe42c359a54…`：恢复越晚回来越可能看到冒烟弹坑与暴怒半身人的含义。
- `fe5a84a1b41…`：补回武器，并把体力回复条件改为每次命中。
- `fe90619ef2e…`：恢复持续火焰光环、每回合伤害及法术结束条件。
- `fec0939b43c…`：墓志铭恢复三行诗，target 共 6 个 LF。
- `ff47fb86086…`：改用“回复纹身”，恢复预判伤害并提前准备的用途。
- `ff585d0b17d…`：任务名统一为“来自深渊，吞噬四方”。
- `ff658fab295…`：将脆弱改为缥缈。
- `ffb21dd4ccd…`：将情绪“平静”改为威胁降低。
- `ffe80f4c810…`：补回奇异限定。
- `fff8487389c…`：把恒定不可阻挡改为有可能变得不可阻挡。

## 来源与结构

主游戏依据冻结 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 anchors。
Ashes 仅核对 SOURCE-ANCHORS 指定 checkout 下的 9 个文件；文件 SHA 全部匹配，仓库与
commit 仍明确为未固定。`verify.py` 通过 manifest 指定 LuaJIT 加载冻结副本和当前两文件，
逐记录证明恰 28 个 target 变化、其余字段与记录不变，并校验 placeholder、markup、LF/TAB
和 Ashes 文件 SHA。第二次 FIX 另以同一 manifest LuaJIT loader 复核两条 F1 记录：
`295b84f066…` 为 9 LF / 18 TAB，`fdff442a1e…` 为 5 LF / 10 TAB，均与各自源串一致。

未执行 stage、commit、push、queue、catalog、migration 或完整 17 项门禁；独立复审与正式
收束仍由宿主完成。

## 证据一致性修复

2026-09-24 复跑时，`verify.py` 因仍引用旧 target preimage 结构而在第 98 行退出 1；
`VALIDATION.json` 原先记录的 exit 0 与该脚本不一致。本次仅修正本证据窗口：MUCUS 改为
对照 source 校验 5 LF / 10 TAB，WRATH 改为对照 source 校验 9 LF / 18 TAB，并明确校验
后七行均以两个 TAB 加 `-` 开头。修正后同一命令真实退出 0，输出 `verified=true`、
`records=23889`、`changed_count=28`。

两份 Lua 在本次证据修复前后 SHA-256 均未变化：`mod-tome.lua` 为
`fb53d06a6ab791da2370bf413d50cb109a63b188a67c6da9d300746d6db733e5`，
`tome-ashes-urhrok.lua` 为
`c470396b63e87727d2eab4be04ea33a7197a5e4f4c56012d844626bcb265a925`。

## RE_REVIEW(2) 定点修复

仅修改 revision `295b84f066bb5e2610c84354d9f94de40a32ef9ded864d97373d29cbf3df47c5`
的 target 中“缴械和震慑抗性增加”一处，其余译文保持不变。窗口 verifier
退出 0，证明仍为 23889 条记录、恰 28 个允许 target 变化，且本条保持
9 LF / 18 TAB 与七个 `-` 列表前缀。strict lint 检查 30308 条译文，
0 errors / 0 warnings；`git diff --check` 退出 0。
