# 修复窗口4第一次合并修复

仅修改 e433115e63… target 中两个已确认子句：

1. “为什么你不准备成为精灵们的领袖呢？”→“为什么你不是精灵们的领袖呢？”
2. “如果你成为了领袖，你可能会阻止这一切”→“如果你是领袖，你就能阻止这一切”

其余字符保持 BEFORE-FIX-1.lua，包括四项既有回忆录修复及另外16条target。固定源码 elvala.lua:138/158、裁决详见 ADJUDICATION-R0.json。

唯一写入 mod-tome.lua 两处，以及 evidence/quality/repair-window-4-20260922/ 中新增 IMPLEMENTATION-FIX-1.md、VALIDATION-FIX-1.json（必要时同名派生明细）。旧实施和验证证据保留。验证：LuaJIT加载证明相比 BEFORE-FIX-1.lua 仅上述两个子句变化；verify.py 对原baseline的17条不变量；严格lint；git diff --check与新增证据空白检查。禁止修改.ai、其他译文、术语、规则、工具、handoff/catalog/migration，禁止stage/commit/子agent。
