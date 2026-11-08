# 汉化插件代码复审（只读）

你是独立代码复审员。**只读**：不得修改任何仓库文件，不 git add/commit；可在 /tmp/addonfix-review/ 写草稿。

对象：ToME4 1.7.6 简体中文汉化插件 `/workspace/tome4-chn-mod` 的未提交改动（`git -C /workspace/tome4-chn-mod status --short` 与 `git diff`；新文件直接读）。插件机制：`superload/<path>.lua` 以 `local _M = loadPrevious(...)` 取得原模块并返回；`hooks/load.lua` 在 addon 加载时执行；`data/*.lua` 是 locale 文件（`t(src, dst, tag)`）。

游戏源码（固定版本）：`git -C /workspace/t-engine4 show 624a67329fe2:game/engines/default/engine/...` 与 `...:game/modules/tome/...`；DLC 源码 `/workspace/tome4-dlcs/{orcs,cults,ashes-urhrok}/`（来源未固定）。I18N 机制见 `engine/I18N.lua`（注意 `t()` 同时写 tag 表与 "nil" 兜底表）。

每个改动对照对应源码函数核对：
1. **正确性**：包装的签名/返回值是否与原函数一致（含多返回值、varargs）；`self` 用法；对继承（单基类 inherit、多基类复制）下 superload 时机是否生效；ToME:load 钩子顺序。
2. **安全性**：临时替换（全局 `_t`、`self.add_name`、`TreeList.new`、`game.logPlayer`）在异常路径是否一定恢复；是否可能把翻译后的值写进存档（序列化字段）；重入/递归（如 getTextualDesc 内部再调 getTextualDesc、getName 递归）时恢复是否正确。
3. **英文 locale 行为不变**（除报告里声明的上游 bug 修正）。
4. **补充词条 `data/chn_supplement.lua`**：键是否独有、是否会经 "nil" 兜底表改变其他 tag 的已有译文（对照 `/workspace/tome4-chn-mod/data/locales/zh_hans.lua` 和官方 locale——官方包在 `~/tome-live/t-engine4-linux64-1.7.6/game/` 下的 .team 文件里，执行者已解压到 /tmp/addonfix/off/ 可直接读）；译文是否自然、颜色码/换行/占位符是否保留。
5. **遗漏**：被修函数在源码里还有没有其他同类路径没覆盖；有无性能问题（热路径上的每次调用开销，例如 getName 在列表渲染时被频繁调用）。

执行者报告：`/tmp/addonfix/report.md`（参考，但以源码为准；不要假设报告正确）。用户裁决：物品属性行 all 只在 getTextualDesc 期间显示「全部」不改全局；装备人偶只用材质简称，只改分隔符。这两点不要再提替代方案。

## 产出
写 `/tmp/addonfix/review.json`：数组，每条
`{"id":"R1","severity":"blocker|major|minor|nit","file":"…","line":N,"issue":"…","evidence":"源码路径:行号 与关键代码","suggestion":"…"}`。没有问题写 `[]`。
不报风格偏好；每条必须有源码证据。最终回复只写一行：`REVIEW addonfix DONE findings=<n>`。
