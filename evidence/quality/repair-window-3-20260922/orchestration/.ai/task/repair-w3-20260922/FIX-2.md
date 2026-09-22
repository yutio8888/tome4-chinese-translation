# 第二次合并修复

依据 ADJUDICATION-R1.json，只修 Rosebloom 与 Dismissal 两个获准 target。独立四成员阶段 r1a3 已有效完成并全部归档；其他12条不改。

Rosebloom 固定源码优先于旧英文的50%说法。读取 HOST-MECHANISM-SUPPLEMENT.json、SOURCE-ANCHORS.json 和 HOST-MECHANISM-PROBE.json：睡眠中逐回合累积失眠，最多10回合；实际抗性为 power × remaining duration，power=20-Sandman减免；清醒后随剩余持续时间衰减。删除固定50%%说法。可用“每剩余1回合失眠提供至多20%%睡眠抗性”表达上限，并清楚说明累积和醒后衰减；避免误写整个效果至多20%。保持原有printf字面%%数量和所有换行/tab，不增占位符。若涉及特殊免疫者，可用“通常”或“可”避免无条件断言。其余段落保持。

Dismissal 仅把检定关系补为“用精神豁免的 %d%% 与本次伤害数值进行一次检定”，保留成功条件、暴击、至少减伤和所有后续内容。

允许写 mod-tome.lua 的这两条 target，以及 evidence/quality/repair-window-3-20260922/ 的本轮新证据。保留初始 SOURCE-ANCHORS.json 和旧历史；把新的22段anchors复制为 SOURCE-ANCHORS-R1.json，把本轮宿主裁决/机制补充/探针脚本和结果逐字复制到新证据文件。不可改 .ai、术语、规则、工具、handoff 或其他条目；不stage/commit、不创建agent。

用 BEFORE-FIX-2.lua 验证恰好两处target变化，运行 verify.py、严格lint、git diff --check，验证实际printf输出、换行/tab及数据加载；保存真实命令结果。局部函数探针不是全游戏运行，证据应如实表述。完成后报告实际成果。
