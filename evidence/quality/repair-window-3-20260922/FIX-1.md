# 修复窗口 3：第一次合并修复实施记录

本轮只实施 `ADJUDICATION-R0.json` 确认的 `RW3-R0-01` 与 `RW3-R0-02`：

- `e1177a8f9f689644a232269ab42be3597862f1d26ab23562b7d6171aa6d4faf9`：第四幅壁画 target 的最后一行由“下面有一行文字”改为“下方写着”。同一 target 的其余文本、换行以及相邻的未知／已知分支译文不变。
- `e1343327ead953361b1fefe6fb85fd1569679eb6b9a269a08a6f5c1c8a473152`：GRAPPLING target 开头由“处于擒抱状态”改为“处于抓取状态”。体力消耗、伤害转移方向、三个占位符与中断条件不变。

以只读候选副本 `.ai/task/repair-w3-20260922/BEFORE-FIX-1.lua` 经 manifest 兼容 LuaJIT 加载后的记录为基线，本轮恰好两条记录发生变化，且两条均只改变 target。其余 12 条候选 target、上述两条 target 的非获准文本、所有非 target 字段及邻接译文保持候选内容。

`RW3-R0-A1` 为非阻断 advisory，本轮未处理。没有修改术语、规则、工具、其他译文、handoff、catalog 或 `.ai`，也没有 stage、commit、创建 agent 或运行完整门禁。

实际验证结果见 `VALIDATION-FIX-1.json`；壁画两个运行时分支的实际拼接结果见 `MURAL-COMPOSITION-FIX-1.json`。原有 `IMPLEMENTATION.md` 与 `VALIDATION.json` 未改。
