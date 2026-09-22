# 初始清单验证

- doctor：LuaJIT 5.1、LPeg 0.10.2、固定 engine/extractor/addon 身份通过；DLC source-unpinned 原样保留。
- 11 组件逐提交语义记录扫描；含 merge first-parent 差异；每个组件最后记录与冻结提交全量相等。
- 4144 个 audit_id 唯一；4134 个排队条目与 10 个已覆盖条目互斥且并集完整；130 批逐项无重叠。
- source/target/source_tag/args_order/special 来自 LuaJIT loader；历史发生过修改但恢复原值者仍保留。
- 不更改生产 queue/catalog，不修改译文，不执行发布或修复。
