# 窗口5第一次合并修复

仅按 FIX-1-REPLACEMENTS.json 修改三个现有revision中的五处精确子句；其余字符与 BEFORE-FIX-1.lua 完全一致。宿主范围校准和源码裁决见 ADJUDICATION-R0.json。既有18条修复保持，绝不全面重译两篇回忆录。

仅可写 mod-tome.lua 和 evidence/quality/repair-window-5-20260922/ 新增 IMPLEMENTATION-FIX-1.md、VALIDATION-FIX-1.json；保留既有证据。执行 verify_fix1.py（验证当前文件恰为五处替换）、verify.py（相对原baseline仍18条）、严格lint、git diff --check及新增证据空白检查。禁止写.ai、其他译文、术语、规则、工具、handoff/catalog/migration，禁止stage/commit/创建agent，不跑完整门禁。报告真实变更和验证结果。
