# 插件 0.3.12 候选验收报告（2026-11-11）

状态：**可审阅候选，未发布**。未推送发布仓库，未创建 tag 或 GitHub Release；是否发布由维护者决定。

## 候选身份

| 项 | 值 |
| --- | --- |
| 译文来源 | 本仓库 `581914a01`（0494）；0495 盲审提交 `59a6fb8cd`，不改译文 |
| 插件代码修复 | 发布仓库 `master` 上的 `a262ee4`（本地提交，未推送） |
| 候选发布提交 | 发布仓库本地分支 `candidate/0.3.12` → `495aa448de5971cda3dde9fd0ce012a1ef80eee5`（父提交为 `a262ee4`） |
| locale | `data/locales/zh_hans.lua` sha256 `4e1819f9c12a12236545b66c583c0bfc29f80105ad1209b4839b745c8a0c489b` |
| 条目数 | 13,802 条：核心 8,152、引擎 189、DLC 5,461。0.3.11 为 13,788 条：核心 8,140、引擎 187 |
| teaa | `.artifacts/release-candidates/0.3.12/tome-chn-mod.teaa`（未跟踪），sha256 `22706f106ce23075f937bc0d316bb8d9737253d3f5b24f52eac6e3805f2f3fff`，`git archive` 后用 `zip -r -0` 打包 |

## 内容

1. **0480–0493 批的译文修改**：此前报告为 44 处。本次复核 `121ca1c6c..c11859310` 范围内的译文文件，共 43 个 diff 改动块（相邻条目会合并成一块）。所有修改都已完成 A/B 盲审并推送。
2. **混乱苔藓修复（0494）**：从自动化候选 `9bb157e39` 移植，只改一行。原文写「有 %d%% 概率使经过的敌人混乱」，改为「每回合有 %d%% 概率使范围内的敌人混乱」。
   - 源码依据：`moss.lua:197-204`、`Map.lua:1258-1277`、`damage_types.lua:3011-3023`。
   - 候选证据保存在 `evidence/quality/automation-pilot/20261111-e88c3f22/`。
   - 0495 盲审 A、B 两条 lane 均为 ISSUE 0。
3. **6 处插件修复（`a262ee4`）**：
   - `[leave]`
   - 捕熊陷阱 `pinned`
   - 效果类型 `otber`
   - 效果子类型 `parasitic`
   - Embers 压力强化型防斩击作战服说明
   - 物品描述中 `living` 的增伤行

## 验证证据

| 检查 | 结果 |
| --- | --- |
| 0494 完整门禁（PATH 已加入 pi `.bin`，pi 1.5.1） | ALL GATES PASSED，包括 04-quality-facts-unit-tests；此前缺 pi 依赖导致的失败已不再出现 |
| `publish --apply --bump`（写入临时克隆） | verification 结果为 mismatched 0、missing 0、redundant 0、unexpected 0，19,144 个运行时键全部核对；详见 `publish-dry-apply.json` |
| `tools/smoke_release.py` | SMOKE OK；三个 DLC 运行时覆盖层精确一致（743、1569、3149） |
| 插件测试 `tests/test_talent_description_diff.lua` | 通过 |
| 三个改动的 Lua 文件 `luajit -bl` | 通过 |
| `git diff --check`（`cr-at-eol`） | 干净 |
| teaa 解包与 `git archive` 结果比对 | 逐字节一致 |
| 实机：工作树构建的插件（1.7.6 官方本体＋3 个 DLC，开发者模式） | 6 项全部在界面上显示中文，截图见 `../../quality/live-test-20261111/addonfix/` |
| 实机：候选 teaa | 插件正常加载，新建角色进入游戏，日志 0 条 Lua Error；6 项与苔藓技能说明复测通过，见 `candidate-live-checks.txt` |

## 验证缺口与说明

- `[leave]` 用的是 `engine.Chat:addChat` 手工构造的 quick_reply 对话，没有走真实 NPC 剧情对话（如 Melinda 父亲、corruptor 任务）。两者走同一条 `Chat:add` 代码路径，但真实剧情对话本身没有实测。
- 6 个效果和 `living` 行都是用控制台施加效果、构造测试戒指后悬停查看的，不是在自然游戏流程中触发。测试戒指缺少 `desc` 字段时引发过一次 Lua Error，属于测试物品构造问题，补上字段后正常。
- 捕熊陷阱说明里的列表分隔符仍是半角「, 」，来自上游 `table.concat(desc, ", ")`，不属于本轮范围，只记作 advisory。
- 发布仓库 README 中的条数只在候选分支里改了，`master` 上未改。

## 待维护者决定

- 是否发布 0.3.12。发布需要：推送发布仓库（候选分支或在 `master` 上重做 publish）、打 tag、创建 GitHub Release 并上传 teaa、回下载核验，再写入 `evidence/releases/addon-0.3.12.json`。
- 发布仓库 `master` 的 `a262ee4` 是否单独推送（本轮未推送）。
