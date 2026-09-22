# 用户授权的第四轮修复

仅应用FIX-4-REPLACEMENTS.json的一处精确替换。相对BEFORE-FIX-4.lua其余字符完全不变；保持原18个revision工作集。只可修改mod-tome.lua及新增evidence/quality/repair-window-5-20260922/IMPLEMENTATION-FIX-4.md、VALIDATION-FIX-4.json。保留旧报告，不改其他条目和术语。执行verify_fix4.py、verify.py、严格lint、git diff --check和新证据空白检查；不运行完整门禁、queue/catalog/migration或stage/commit/push。须先由宿主接受SCOPE-AUDIT-R3的范围校准后才派发执行。
