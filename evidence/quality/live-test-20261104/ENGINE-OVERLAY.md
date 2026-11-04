# engine 译文能否由插件覆盖（2026-11-04 实测）

用户要求比较两种方式：overload 与在插件译文后追加 engine 条目。测试用硬链接复制的游戏副本（共享安装未改），测试插件在 0.3.7 包上加两处哨兵：

| 方式 | 改动 | 日志 | Esc 菜单 |
|---|---|---|---|
| A overload | `overload/data/locales/engine/zh_hans.lua`，打印标记并把 Key Bindings 改为「按键绑定【A-overload】」 | 标记从未出现 | 「按键绑定」未变 |
| B 插件 locale | `data/locales/zh_hans.lua` 末尾打印标记并把 Audio Options 改为「音频设置【B-addon-locale】」 | `CHN-TEST route B` 在 `/data-chn-mod/locales/zh_hans.lua` 加载时打印 | 显示「音频设置【B-addon-locale】」 |

原因：模块启动时先加载 `/data/locales/engine/zh_hans.lua`，之后才挂载插件，engine locale 不会重载；插件 locale 最后加载，`I18N:t()` 后写覆盖先写。结论采用 B。

实现（`tools/i18nlib/publish.py` `_engine_overlay_entries`）：engine.lua 中与官方 engine locale 运行语义不同的条目写入插件 `section "engine"`。

- 引擎缺陷：`I18N:t()` 注册不带 args_order 的条目时清空该 tag 的参数表，查找回退到 "nil" 表；官方 engine locale 中日期行（tag "nil"、{3,2,1,4,5}）之后还有 114 条 "nil" 普通条目，所以官方日期年/日颠倒。插件若写 "nil" 普通条目会清掉 tome 官方 55 条 tformat 参数顺序，故普通 "nil" 条目以 "_t" 写出（set() 同时写 "nil" 表，查找结果相同），带 args_order 的日期行保留 "nil"。
- "nil" 表跨 tag 共享，与 tome 层同源文本的 engine 条目跳过（15 条），沿用 DLC 不遮蔽主游戏的规则。
- 固定提交 624a6732 的官方 engine/tome locale 与官方 1.7.6 安装包内文件逐字节一致。
- 启动菜单（boot 模块）在插件加载前显示，无法由插件覆盖；用户指示暂不考虑。
