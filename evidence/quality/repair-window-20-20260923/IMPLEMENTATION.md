# 修复窗口 20 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 7 个 target；source、section、source_tag、args_order、printf 占位符、`%%`、markup、LF 与 TAB 均未改变。未扩展 advisory、pending、同族 Conveyance 或其他 repair。

## 实际修复

- `f58a8172af…`：念力核心项圈外观恢复“似乎”的推测语气，删除原文没有的“所有”，译为“这副沉重的项圈似乎会把附近的物体吸向自己。”
- `f5928e3331…`：将邪眼的 `bloodshot` 从“带血的”改为“布满血丝的”。
- `f5d4f8ef89…`：将 `creature` 改为“生物”，并将 `the thrill of the death` 改为“击杀带来的快感”；两行结构、第二行两个 TAB、`%0.1f`、`50%%` 和 `%d` 均保持。
- `f5f90d5b06…`：离线模式说明仅将 Version checks 一行改为“版本检查：不再检查插件是否有新版本。”；其余句子、换行、空行及 `#{bold}#`、`#{normal}#`、`#CRIMSON#` 等标记不动。
- `f603e1fbc9…`：将时空法术类别说明改为名词短语“操控时间的法术学派。”；未修改 Conveyance 等同族说明。
- `f6060b573a…`：将梅琳达成就名改为“落难少女拯救者”。
- `f62d40cfde…`：将未鉴定名改为“滴着毒液的魔杖”，沿用库内 `wand` 的既有译名。

## 固定源码补查

仅使用 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查了 7 个固定源码位置。念力核心只有主动 `T_PSIONIC_PULL`；Utterly Destroyed 的 `callbackOnKill` 与 `callbackOnSummonKill` 共用触发逻辑；其余文本与 `SOURCE-ANCHORS.json`、`SOURCE-CLAIMS.json` 一致，未发现范围冲突。

## 不变量与验证

窗口专用脚本通过全记录比较确认恰有 7 个 target 变化，其他记录字段不变，并验证 printf 占位符、markup、LF 与 TAB 保持基线。严格 lint、语义 claim 回归和 `git diff --check` 均通过；真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH266.json` 是 `.ai/task/repair-w20-20260923/PREFLIGHT-BATCH266.json` 的逐字节副本，SHA-256 为 `69dfd74936515591d47ba685500d01128560a386caad412a2029e7f0c2e82a21`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w20-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `69877059cd5cf5245ef3e24e94de0e42477192cae8fbfe3d855e5e181735fdf3`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w20-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `66a283542831cb1a929824768533d73a6f10f6d3560f553450e11f55a0fd17a5`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续。本执行未 stage、commit、queue、catalog/migration 或 push，也未修改 `.ai`、handoff 或 catalog。

## 第 1 轮修复（新会话）

依据 `ADJUDICATION-R0.json` 的唯一 confirmed finding `R0-OFFLINE-CHARVAULT-SHOWCASE`，仅在离线模式说明条目中将“角色备份”整行逐字替换为“角色仓库：不能将任何角色上传到在线仓库来展示你的荣耀。”。该条其余文字、换行、空行与 `#{bold}#`、`#{normal}#`、`#CRIMSON#` 等标记均未改动；其他译文条目也未改动。本轮未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。

## 第 2 轮修复（新会话）

依据 `ADJUDICATION-F1.json` 的唯一 confirmed finding `F1-OFFLINE-BLANKLINE-AND-NEWS`，仅在离线模式说明条目的 target 内做两处逐字替换：将“游戏内新闻”行改为“- 游戏内新闻：主菜单将不再显示有关游戏更新的信息。”并在其后增加一个空行；将“是用来更新游戏的。”与 `#{bold}##CRIMSON#` 之间的两个空行减为一个。逐行比对确认 source 与 target 均为 17 行、包含 16 个 LF，且 0 起计第 11、14 行均为空行。本轮未改该条其他文字或任何其他译文条目，未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。窗口验证、严格 lint、语义 claim 回归与 `git diff --check` 的真实结果记录于 `VALIDATION.json`。
