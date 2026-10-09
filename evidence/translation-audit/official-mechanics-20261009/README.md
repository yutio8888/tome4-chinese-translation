# 官方译文对照专项审核（2026-10-09）

状态：清单已冻结；首批技能、状态、装备共 180 条已完成独立审核、宿主裁决、归档与 DONE_VERIFIED；整轮审核尚未完成。

范围为当前提交 `d8d570af41bae05e74f3030b6aa5563c8c785abd` 相对官方存在变化或新增的技能、状态、装备、资源与战斗规则、相关标签和界面描述。覆盖本体、三个官方 DLC、引擎及启动模块；保留 occurrence 映射，不以英文去重。未变化条目和纯剧情不作为独立审核对象。

本体官方与源码以 manifest 固定 commit 为准；DLC 以实际取得的官方 locale 文件 SHA-256 对照，来源／commit 未固定，提取快照不等于源码版本。源码逐文件哈希见 source-workset.json；未固定来源的相关机制结论按实际证据注明边界。

清单共 5628 条 occurrence、5325 个组件内运行键，另外登记 4 个官方有而项目缺失的重点运行键。按每批至多 60 条形成 108 个独立只读 contextual v2 full 任务。coverage.json 是进度与缺漏对账入口；inventory.json 保留原文、官方译文、项目译文及身份；excluded_changed_entries 保留边界外改动与排除理由。

不修复译文或术语，不写入生产审核队列，不 push 或发布。审核输出分为 confirmed、pending、advisory，并区分项目新增回退、官方问题遗留、合理改善；独立模型结果不作为源码事实。全部批次的覆盖、宿主裁决、raw 校验、子进程归档与 DONE_VERIFIED 均完成后才可宣称本轮完整审核完成。

首批结论：4 条 confirmed（2 条项目机制回退、2 条官方问题遗留），1 条 advisory。详见 initial-findings.json。待审核部分仍留在 coverage.json，不计为完成；完整结果将在所有冻结批次及官方缺失键核验完成后汇总。
