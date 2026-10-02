# 机制译文修正首包

mode: implement；change_class: standard；review_contract: translation_contextual_v2；schema_version:5；max_cycles:3。

范围仅 REPAIR-INPUT.json 的3条：MMR-010、MMR050、MMR053。唯一写入 EXECUTOR；允许文件 tome-orcs.lua, mod-tome.lua, tome-cults.lua，其中只改3个对应t调用的target。允许写 .artifacts/i18n/modified-mechanics-repair-20261002/executor-001-report.json 和自身临时文件。其他调用不得改变，不改术语库、源码、.ai、旧evidence，不stage/commit/push。

验收：保留 source/source_tag/args_order/special/placeholder种类顺序/markup/newline；MMR-010 明确奥术资源不限法力；MMR050 明确每项既有负面效果增加本技能减速持续时间1回合，不改变原负面效果持续期；MMR053 用施法者而非目标作为相邻侧格中心，按固定消费者核对方向。整句通顺且保持技能升级预览ASCII分词。实际机制以冻结commit/快照调用链为准。运行 strict lint，宿主核验proposal及不变量、运行键扫描/分类/空白/相关组件严格构建，独立REVIEW及FINAL_REVIEW收敛，所有child归档且ai_state_check DONE_VERIFIED。

当前包合并同一条目的已授权UPSTREAM118：按消费者修正疯狂值为每回合首次触手攻击非友方目标时获得一次。其余允许边界不扩大。
