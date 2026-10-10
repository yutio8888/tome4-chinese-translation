# 52 条修订应用及独立复审
用户授权：应用 Gemini 草稿后再次审核；原版留存问题不处理。
角色：主代理 ORCHESTRATOR；EXECUTOR 唯一译文与具体术语行写入者；REVIEWER 只读。
输入：evidence/translation-audit/official-mechanics-20261009/gemini38-drafts/drafts.json；workset.json 为已确认机制修复依据。
允许文件：mod-tome.lua、tome-ashes-urhrok.lua、tome-cults.lua、tome-orcs.lua；terminology/creatures.tsv 仅 elemental/entity type 这一行的语境适配。不得修改其他任务或用户现有改动。
执行：精确匹配 source/source_tag/section/original_target 后应用全部 52 个 target，保留 args_order/special。M210 先更新相关术语行：这是陷阱与生物共用的 entity type 分类，不宜称元素生物；具体目标为元素，notes 说明共享分类。不得扩展为全库重命名。
执行者不自行重写草稿；如发现占位符或范围问题返回证据。原版留存疑点不扩展修复。独立审核发现的本次候选缺陷由宿主裁决，confirmed 进入有界修复。
验收：52 条实际加载值与草稿相符；严格 proposal、lint、适用完整门禁及构建；冻结实际候选及中性固定源码/术语正文；contextual v2 四 lane 复审、全量终审；必要修复；全部 child 确认归档；DONE_VERIFIED；提交范围内成果。
核心以固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 为准；DLC 以既有快照 hash 核验的 /workspace/tome4-dlcs 公开源码为准，来源/commit 未固定。

宿主有界裁决：M210 runtime key 已确认另外 9 处同键记录会覆盖本次修订，因此对 mod-tome.lua 的 elemental/entity type 同键记录统一应用既有草稿“元素”；仅这 9 个别名，不按普通英文词全局替换。该同步是 M210 的必要生效修复，不扩展到其他原版问题。

同键扫描补充：tome-orcs.lua 中 hethugoroth.lua 的 elemental/entity type 是同一跨组件运行键，追加该一个 target 同步为元素；其他 orcs 内容不变。

复审修复：M349 的固定数量上限经固定源码否定，接受改为“终极觉醒技，学习需消耗 1 点觉醒点。”；这是一条原候选的有界机制修复。最终加载验收为 51 条草稿原文加此 1 条修复，以及 10 个 M210 运行键别名。

验证范围：本任务是有界译文应用和复审，不是生产队列批次或发布。按工作流验证矩阵覆盖 strict lint、全部实际条目的 strict proposal、LuaJIT 记录对照、运行键扫描/分类、三项术语审计、空白检查和严格构建尝试，不运行无关工具改动测试。核心严格 addon 构建通过；三个 DLC 的严格构建因 manifest 无固定官方 locale/source repository 返回 INCOMPLETE。这项既有构建配置限制不阻断译文应用与只读复审，但未证明完整 DLC addon 构建，交付须明确披露，不能作为发布验证。详见 DLC-build-limitation.json。
