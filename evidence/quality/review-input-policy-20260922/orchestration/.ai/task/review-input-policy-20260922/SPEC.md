# 统一审核读取边界与正式 prompt
用户授权：2026-09-22“请调整流程和prompt后继续”。本任务是独立于活动生产246的有界流程维护；不得改其冻结envelope/raw/STATE，或其生产checkpoint/queue，禁止commit/push。

问题：明确引用内容未区分术语file provenance与读取授权；role仅第六节而contextual契约第六七节；临时prompt与正式三行模板漂移，读取契约额外章节造成无谓重试。

接受标准：
1. 前瞻统一v2 contextual与surface输入政策：译文、术语只按冻结envelope提供的快照；file/line/hash仅来源信息，不授予搜索当前译文/术语库权限。明确的其他引用须有精确范围；缺少术语依据时不得自行搜库或凭偏好判错，按现有输出schema记录具体证据不足（确有疑点才ISSUE），宿主补充中性快照/重新preflight/freeze；不得扩展schema。
2. 允许完整读取当前对应审核契约作为流程说明，不再因读取该文档额外章节/标题元数据拒收。contextual仍可沿固定公开源码相关调用链补查；surface不能借此增加源码调查权限。禁止其他task/review/prior findings/currenttranslation，禁止写文件。
3. role、契约、正式三行prompt一致；统一正式builder，旧dispatch_reviewers如含重复prompt应复用同一surface builder，不借机重构其CLI。<=800 UTF8字节含最长合法实际路径；超限如原来fail-closed。不再手填文档行号；废弃ignored临时builder的操作替代由宿主完成。
4. 有效边界政策与历史版本明确：不追溯新规则、不改旧candidate/hash/raw/result schema；保留精确prompt派发记录；取证审计区分JSON/实际读取/生命周期。原先合法已归档输出不因新规则重跑，当前未采纳输出由宿主按旧dispatch审计后裁决。
5. 增加有意义的定向测试：正式prompt与契约模板一致，三行/字节界限，role与边界声明一致，contextual/source与surface差异。不要字符串自抄作假测试或改身份公式；版本/条款如需改动应保持contract checker要求。
6. 本任务不影响addon输出、打包、加载；host最终按共享流程变更运行ci-gates --skip-build、兼容测试、契约检查、双模型独立review+cross review与DONE检查。

允许文件：
- .ai/roles/reviewer.md
- docs/paseo-translation-context-review-v2-contract.md
- docs/paseo-translation-surface-screen-v1-contract.md
- tools/orchestration/dispatch_contextual.py
- tools/orchestration/dispatch_surface.py
- tools/orchestration/dispatch_reviewers.py
- tools/orchestration/review_prompts.py
- tools/orchestration/README.md
- tests/i18n/test_review_prompts.py
- docs/paseo-orchestration-v2-contract.md

保留基线全部untracked与所有生产证据。不得修改AGENTS.md、任何翻译/术语数据/版本清单/production消费者。
