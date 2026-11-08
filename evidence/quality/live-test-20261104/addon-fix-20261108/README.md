# 插件代码修复（2026-11-08）

依据 `../addon-code-issues-analysis-20261108.md` 第 1–3 组（不含 I 折行、Steam:、Ashes 种族列表）。
用户裁决：L 采用方案 A（只在 getTextualDesc 期间把 all 显示为「全部」）；F 人偶只显示简称，只改分隔符。

- 执行：Opus 执行者，规格 `SPEC.md`，报告 `report.md`（13 个文件）。
- 代码复审：codex gpt-6.1-sol，`review.json` 为空（0 条）。主代理另行核对 Object.lua 与 hooks/load.lua。
- 实机：afv-a（主战役）、afv-b（余烬怒火）、afv-c（开发者模式补测＋全新存档测锁定职业）。
  - afv-a 发现「快捷键 10」被 75px 列截断 → 列宽改 95px，afv-c 复测通过。
  - afv-c 第 5 项 FAIL 不成立：wolf 无立绘文件，getActorPortrait 返回 actor 本身，名牌走 ChatPortrait.lua:33 的 actor:getName()（已翻译）；包装只作用于新建的立绘实体。测试命令只读 `.name`，是测法问题。
  - 未取得屏幕证据：2 平民喊话（视野内无 NPC）、4 成就分类（开发者模式下成就不写入 profile，列表为空）、5 新建立绘实体的名牌。逻辑由执行者离线 harness 覆盖。
  - 三个目录 game.log 均无插件相关 Lua 报错。
- 插件仓库本地提交 4a86895（未推送、未发布）。
