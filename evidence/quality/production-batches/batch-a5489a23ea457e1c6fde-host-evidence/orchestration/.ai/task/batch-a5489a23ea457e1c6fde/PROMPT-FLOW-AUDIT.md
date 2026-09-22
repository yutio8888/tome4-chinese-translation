# 第246批 prompt 与输入边界检查

用户要求：检查反复读取输入外术语行是否源于 prompt 或流程偏差。本检查不修改正式规则、工具、译文或冻结输入。

## 确认的问题

1. **引用粒度未定义。** contextual v2 契约第98、118行仅称“输入／明确引用的内容”。输入术语对象包含 file、line、file_sha256 及完整行快照，但没有区分出处元数据与扩展读取授权。full-r2 的 input 仅嵌入 combat.tsv:140 Physical Power；审核者查询同文件得到113 Defense:与118 Willpower。额外读取是事实，把它直接描述为违反明确“仅这些行”禁令则证据不足，因为旧 prompt 没写这项禁令。
2. **角色与契约失同步。** `.ai/roles/reviewer.md` contextual-v2 分支只许第六节；契约和正式 dispatch builder 允许第六、七节及固定源码调用链补查。角色文件可能引发不同解释；尚无证据证明该 child 实际读了角色文件，故不冒称其直接原因。
3. **临时派发绕开固定模板。** 本轮使用 ignored `dispatch_contextual_bounded.py` 单段模板，而不是 `tools/orchestration/dispatch_contextual.py` 的三行模板。前两次未明确禁止术语文件读取，后续又临时加行号与禁令；这属于主代理引入的流程漂移。800字节检查只验证长度，不验证三行模板等价、读取政策或模板版本。
4. **后验边界判定替代前置定义。** 只在读完后人工判断引用粒度，导致保守拒收和 fresh retry；不应把事后补充规则追溯用于旧 dispatch。contract introduction 的版本/角色元数据读取也不等同于读取其他候选或 prior finding。
5. **检查能力被高估。** strict result/DONE验证身份、JSON、顺序与归档；不能证明只读调用边界。`paseo_contract_check.py`只验证版本/条款引用，不比较角色与派发模板语义。这些检查通过不排除上述问题。

## 辅助因素

术语打包由 `build_evidence_pack.py:441-443` 按 component scope、source_tag 和英文词面匹配。这次没有嵌入 Defense:/Willpower 行：前者包含冒号且 tag不匹配，后者英文原文为will，并非Willpower。该筛选有语境理由，不能直接判为漏包bug；但缺少术语时的明确处置路径，会诱使 reviewer 自行搜库。整文件hash是来源证明，不应被含混地当成整文件阅读授权。

## 本批失败分类

表面复审的四次显式拒收涉及读取契约第七节，其中一次还写临时文件；另有两份有效但同组未闭合的输出未采纳。补充复审第一次失败是revision key不符；第二次才是上述术语引用歧义。不能把这些统称为反复的术语越界。

## 建议的最小修正

统一正式契约、角色和唯一dispatch builder，前置写明：术语以envelope内快照为准；术语file/line/hash只标出处、不授予扩大读取；固定公开游戏源码可沿相关调用链补查。术语不足时在observation记录证据不足，由主代理补充中性术语快照并重新preflight/freeze；不要自行grep术语库。

将规则章节边界统一由稳定章节提取或冻结规则片段提供，避免手写易过期行号；保留800字节上限。派发前验证模板与角色的读取边界一致；收获时分别报告JSON合格、读取边界、生命周期，避免把strict result当作行为验证。

已有raw、envelope、rejection事实不改写。full-r2的故障归因已由ATTEMPT2-DIAGNOSIS-CORRECTION.json更正为“引用粒度歧义下的保守不采纳”，未恢复为接受。后续规则只能前瞻生效。

## 收尾状态

两次在途复审均已自然结束、strict结果校验通过并确认归档；调用审计未再发现术语文件读取。尚未发布accepted records或导入生产上下文结果。当前批次保留现场，不把规则检查冒充批次完成。正式契约检查实际返回“PASS: 10 active Paseo documents; 4 live versions, 16 clause declarations”，但其覆盖不包含以上语义一致性。
