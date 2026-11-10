# 剩余译文反向检查修复（执行者规格，2026-11-10）

你是 ToME4 简体中文汉化仓库 `/workspace/tome4-chinese-translation` 本任务唯一的写入者。只修改译文文件 `mod-tome.lua`、`engine.lua`、`tome-items-vault.lua`、`tome-addon-dev.lua`（以及同英文条目所在的其他组件文件）。**不要 git add / commit / push，不要动 evidence/、tools/、tests/、terminology/。**

输入：`/tmp/revchk/rem-decisions.json`，98 条，主代理已核实裁决。每条有 `en_full`（英文原文，即库中 t() 的第一个参数）、`zh_current`（当前译文，插件未覆盖，等于官方中文）、`issue`、`suggestion`、`decision`。
- `decision=apply`：按 issue 修改该条译文。suggestion 是参考，可以调整措辞，但必须解决 issue；若 suggestion 只给了片段，要放回整条译文。
- `decision=apply-reversed`：按 note 处理。
- `decision=skip`：不动。

## 定位
按 `en_full` 在库文件里找 `t("<en_full>", ...)` 或 `t([[...]], ...)` 条目（注意多行 [[ ]] 写法与转义）。同一英文可能在多个组件文件或多个 section 中都有条目：**所有同英文条目都要同步修改**（除非 tag 或语境明显不同）。若当前库里的译文已经与 zh_current 不同（develop 已改过），对照 issue 判断是否仍需修改，并在报告中说明。

## 硬性规则
1. 只改 target；source 与 tag 不变。改完 `python3 /tmp/srccheck.py mod-tome.lua tome-orcs.lua tome-cults.lua tome-ashes-urhrok.lua` 必须全部 identical。
2. 占位符数量、种类、顺序不变（有 args_order 的条目保持对应）；颜色码、#{bold}# 等标记成对完整；target 换行数 = source 换行数，续行行首 TAB 保持。
3. 升级预览空格规则：tformat 说明里数值占位符所在 token 连着汉字或全角标点时须有 ASCII 空格（「%d 点」「伤害， %d」「%d （」）。以 `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict` 0 错误为准；lint 要求的空格必须保留，只删 lint 不要求的多余空格（如 #46、#48、#94 那类非占位符旁的空格）。
4. 修改要对照整条译文通读，修完的句子要通顺；同条里同类问题一并改。不要扩大到无关条目。
5. 用 Python 精确替换（assert 命中次数）或 Edit；不要用 shell heredoc 写中文；不要整文件重写。
6. 术语以 `terminology/*.tsv` 中 preferred 行为准（只读）。

## 完成标准与报告
- lint strict 0 错误；srccheck 全部 identical；`git diff --check` 无输出。
- 写 `/tmp/revchk/rem-exec-report.json`：数组，每条 `{"n":编号,"status":"applied|skipped|not_found|already_ok","files":["文件:行号",...],"old":"…","new":"…","note":"…"}`（skip 的也列出）。
- 最终回复只写一行：`EXECUTOR remchk DONE applied=<n> skipped=<n> not_found=<n>`。
