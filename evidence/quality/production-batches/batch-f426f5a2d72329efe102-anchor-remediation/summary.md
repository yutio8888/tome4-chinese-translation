# 第244批锚点检查遗漏的补充核验

更正：本目录首次补充复审的边界验收已撤销，见 HOST-BOUNDARY-CORRECTION.json。下文 DONE 与归档是当时机械验收事实，不代表该次读取边界合规；该次结果不作为有效独立复审。replacement/ 保存随后全新复审的真实记录、边界审计与可回放 DONE 快照。

原批次 `batch-f426f5a2d72329efe102` 已提交并推送为 `79e81d1`，其上下文冻结前漏跑独立 `contextual_anchor_preflight.py`，原 SCOPE 也缺 schema_version。宿主误以为 dispatch 的 envelope 校验覆盖该检查；这是宿主流程错误。原有完整门禁、复审和 DONE 结果不能证明这个前置步骤已执行。

本补充不追溯改写原 SCOPE、STATE、输入、复审、提交或时间戳，也不把事后检查称为原批次 preflight。另建只读任务 `batch244-anchor-remediation-20260921`，针对相同三条 payload 建立正确 SCOPE，2026-09-21 13:54:44 UTC 实际 preflight 成功后，于13:55:05 UTC重新冻结，再派发全新独立复审。候选 identity 与原 payload 相同。实际先后顺序及原遗漏诊断保存在 orchestration/.ai/task 下。

新复审三条 observation 经固定源码核验，保持原结论：念动弓每回合/伤害遗漏、阴影持续补召/数量上限遗漏两条待修；巨石恐魔名称为 advisory，不自动重命名；“最近目标”要求被实际随机选敌实现否定。原批次78 done / 2 repair_required不变，未重新导入或覆盖原生产记录。新任务严格结果与 DONE 验收通过，唯一 child 已确认归档；冻结快照可独立回放。

没有修改译文、术语库、工具或契约；原批次17项完整门禁适用于同一未变译文，本次没有重跑或伪造门禁收据。后续上下文批次必须先对 draft 运行独立 anchor preflight，再执行会冻结/哈希的 contextual-export。第245批仅预留、未派发，预留已成功释放且 active checkpoint 不存在，允许单独提交本补充。

替代复审 task `batch244-anchor-remediation-retry-20260921` 再次先独立 preflight、后冻结，再由全新 agent 复核；结果为名称OK、两条技能ISSUE，宿主确认两条既有修复项。唯一child已确认归档，strict与DONE验收通过。契约文档读取范围偏宽的非候选内容读取如实记入边界审计advisory；没有搜索当前译文或历史意见。
