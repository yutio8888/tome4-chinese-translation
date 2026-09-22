# 修复窗口 4：Cults 运行时 sibling 实施记录

## 范围与改动

- `tome-cults.lua` 的 `tome-cults/data/zones/test/npcs.lua` 中，唯一
  `t("thalore wilder", ..., "entity name")` 的 target 从“精灵自然师”改为
  “自然精灵自然师”。source、source_tag、section、调用参数个数以及
  args_order/special 均未改变。
- `mod-tome.lua` 仅作为父任务当前同键译文的只读参照；实施前后 SHA-256 均为
  `08251b2534bcf69b9970009c6f458fa2f9592a294a11b81916418ae7bfaa6e1d`，
  本任务未改变其字节。
- `docs/runtime-key-collisions.md` 记录本次跨组件冲突、裁决、来源边界与验证结果。
- 未修改术语、规则、工具、catalog、migration、handoff 或其他译文；未执行
  stage、commit、push、发布写入、完整门禁或 addon 构建。

## 裁决依据与来源边界

Cults 公开源码快照显示该 NPC 继承 `subtype = "thalore"` 与
`faction = "thalore"`，采用 `wildcaster` 自动加点并拥有 Rimebark 与 War Hound
召唤天赋。因此沿用父任务 core 条目的“自然精灵自然师”，只消除同一运行时键的
加载顺序差异，不建立新的术语或 NPC 命名策略。

Cults 快照 SHA-256 为
`6cc08be3041889e6e7223c27b056f6d8db173e75108e881fb20aea64234b5cb9`。
该来源公开且文件头为 GPL-3.0-or-later，但上游源码仓库、源码 commit 与版本均未固定；
catalog 的 `snapshot:ed0b1126c2636738204f2cafa3259812092fe47f5393ba3b81d696fb56865747`
只是提取快照身份，不是源码 commit。

## 发布层定向核验

固定 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 core 官方 locale
将该键译为“精灵自然师”，当前 `mod-tome.lua` 为“自然精灵自然师”，因此 core addon
层会生成 override。Cults 组件没有固定 `source_repository` 或 `official_locale`，当前 addon
构建逻辑会跳过该组件；所以该共享键的实际发布值来自 core 覆盖层。本结论来自定向读取
固定官方 locale、manifest 与当前译文，没有替代父任务后续要求的严格 addon 构建。
