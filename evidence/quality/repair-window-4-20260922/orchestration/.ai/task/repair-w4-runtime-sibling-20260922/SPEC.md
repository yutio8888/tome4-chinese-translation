# 修复窗口4：Cults 同键附属修复

父任务 repair-w4-20260922 的17条候选已复审收束，但完整门禁 run.zali0fkv 的跨组件扫描报告一处 thalore wilder/entity name 冲突。父任务原17条review身份和输入均保持，本任务独立覆盖一个Cults sibling。既有连续译文修复授权涵盖保证同键运行一致的有界附属修复；不改术语或命名策略，不伪造production repair preflight。

唯一EXECUTOR可写 tome-cults.lua 中 section tome-cults/data/zones/test/npcs.lua、source thalore wilder、source_tag entity name 的唯一target：精灵自然师→自然精灵自然师；docs/runtime-key-collisions.md 增加本次发现与解决记录；evidence/quality/repair-window-4-20260922/runtime-sibling/ 本任务证据。其他译文/内容不变，父任务 mod-tome.lua 必须逐字保持。不得改.ai、规则、工具、术语、handoff/catalog/migration，不得stage/commit/push或创建agent。

源码：Cults公开来源 data/zones/test/npcs.lua 见 SOURCE-PROVENANCE.json/CULTS-PUBLIC-SOURCE.lua，subtype/faction=thalore，wildcaster与召唤天赋；SHA256 6cc08be3041889e6e7223c27b056f6d8db173e75108e881fb20aea64234b5cb9。上游源码仓库、commit及版本未固定，不能称其为固定1.7.4或manifest源码commit。原catalog仅固定提取快照。引擎本体固定624a67329fe2ad440c5b344785a9c73fcf22ae63的I18N.lua按src/tag写locale且section运行时忽略。

验收：相对baseline只一处target变化且本体字节不变；严格lint；实际跨组件扫描归零；两个加载顺序的同键结果一致；git diff --check及新证据空白检查；正式单条REVIEW/full及FINAL_REVIEW/full；之后与父任务共同运行完整17门禁及核心严格addon构建，记录Cults来源未固定。这个键存在固定官方核心locale、DLC发布函数排除官方共享键，因此实际发布落在核心覆盖层；另核验该共享键的层选择。所有写入/复审child归档，DONE_VERIFIED。与父任务共同提交译文及仅一次catalog/migration（18条实际target），successors待重新审核。
