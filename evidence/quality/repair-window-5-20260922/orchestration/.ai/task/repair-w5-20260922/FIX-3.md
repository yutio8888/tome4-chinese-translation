# 第三轮合并修复

依据ADJUDICATION-R2及已完成scope_audit，仅应用FIX-3-REPLACEMENTS.json的两处精确替换。相对BEFORE-FIX-3.lua其余字符完全不变；保持18个原revision工作集。仅可修改mod-tome.lua及新增evidence/quality/repair-window-5-20260922/IMPLEMENTATION-FIX-3.md、VALIDATION-FIX-3.json。保留所有旧报告。执行verify_fix3.py、verify.py、严格lint、git diff --check和新证据空白检查；不跑完整门禁、stage/commit或其他出版操作。
