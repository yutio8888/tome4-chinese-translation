# 质量报告确认问题修复

mode=implement；change_class=standard；有界译文维护，采用 Paseo 和 translation_contextual_v2/schema 5。
当前授权：用户“请修复确认的问题”，仅报告 C01–C09 共 11 条 target。

允许 EXECUTOR 修改：mod-tome.lua、tome-ashes-urhrok.lua、tome-cults.lua、tome-orcs.lua 的冻结 11 条 target，以及 evidence/translation-audit/quality-assessment-20261013/repair-notes.md。
禁止：其他 target、术语库/策略、工具/规则/manifest、旧报告/旧证据、队列/catalog、用户既有改动；不 stage/commit/push；不创建 child。
输入：confirmed-workset.json 和原评估 source-anchors.json；原报告保持历史快照。

AC1：修复 C01–C04、C08–C09 的确认错误；C05–C07 以自然简洁的玩家规则替换实现旁白，保留必要且可由实际源码核实的条件，不机械回退到不准确的英文。
AC2：11 条之外零 target 改动；source/source_tag/args_order/special、参数占位符顺序、markup、newline 保持不变（固定百分比文字可压缩但不得破坏格式串）。
AC3：主程序机制以 /workspace/t-engine4 的 manifest commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 为准；DLC 为 /workspace/tome4-dlcs/<component>/tome-<component> 公开源码，来源/commit/版本 unpinned。引用源码记录文件 hash 和关键调用。
AC4：严格 proposal/lint、运行键扫描及分类、空白、范围与运行键不变量通过。目标改变显示文字，按有界维护矩阵追加严格核心 addon 构建及受影响 DLC 构建；基线限制如实记录，不启动正式生产消费者。
AC5：冻结源证据/术语正文/候选，anchor preflight，四成员 contextual REVIEW，宿主裁决，然后 whole-workset FINAL_REVIEW；默认 max_cycles=3。全部 child 终态收获和归档；ai_state_check DONE_VERIFIED。
交付：保留工作树变更和修复证据，不提交或发布，不把 advisory/pending 纳入。
