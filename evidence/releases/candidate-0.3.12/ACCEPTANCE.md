# 插件 0.3.12 候选验收与发布就绪审查（2026-11-11）

**结论：可发布。** 没有阻塞项，也不需要再补验。下文列出的剩余限制都不影响本轮修复的正确性。

**发布状态（2026-11-11 更新）：已按维护者指示发布。** 发布仓库 `master` 已从 `47f74c3` 快进到 `495aa448`（`a262ee4` 作为父提交一起推送）；Release [v0.3.12](https://github.com/yutio8888/tome4-chn-mod/releases/tag/v0.3.12)（id 441846059）附带的就是本报告核验过的 teaa，回下载后 sha256 仍为 `22706f10…`。凭据见 `../addon-0.3.12.json`。下文保留发布前的审查原文。

## 候选身份（已于最终审查时重新核对）

| 项 | 值 |
| --- | --- |
| 译文来源 | 本仓库 `581914a01`（0494）。此后的提交只增加证据，没有改动译文、术语、i18n 或 tools 文件 |
| 插件代码修复 | 发布仓库 `master` 上的 `a262ee48fd0a8ae7603bf913b28ebe2a45495a03`，本地提交，未推送 |
| 候选发布提交 | 发布仓库本地分支 `candidate/0.3.12` 上的 `495aa448de5971cda3dde9fd0ce012a1ef80eee5`，tree 为 `325ca79d…`，父提交为 `a262ee4` |
| 与远端的关系 | `origin/master` 为 `47f74c3`（0.3.11），是候选的祖先；候选领先 2 个提交，可以快进 |
| locale | `data/locales/zh_hans.lua` 的 sha256 为 `4e1819f9c12a12236545b66c583c0bfc29f80105ad1209b4839b745c8a0c489b`。最终审查时从当前 HEAD 重新生成一次，sha256 相同 |
| 条目数 | 13,802 条：核心 8,152、引擎 189、DLC 5,461。0.3.11 为 13,788 条 |
| teaa 包 | `.artifacts/release-candidates/0.3.12/tome-chn-mod.teaa`（未跟踪），sha256 `22706f106ce23075f937bc0d316bb8d9737253d3f5b24f52eac6e3805f2f3fff`，31 个文件 |

## 内容

1. **0480–0493 批的译文修改**：共 44 处，对应 `121ca1c6c..c11859310` 范围内译文文件的 43 个 diff 改动块（相邻条目会合并成一块）。所有修改都已完成 A/B 盲审并推送。
2. **混乱苔藓修复（0494）**：从自动化候选 `9bb157e39` 移植，只改一行。0495 盲审 A、B 两条 lane 均为 ISSUE 0。
3. **6 处插件修复（`a262ee4`）**：
   - `[leave]`
   - 捕熊陷阱 `pinned`
   - 效果类型 `otber`
   - 效果子类型 `parasitic`
   - Embers 压力强化型防斩击作战服说明
   - 物品描述中 `living` 的增伤行

## 复用的验证结果（输入未变，仍然有效）

| 检查 | 结果 |
| --- | --- |
| 0494 完整门禁（PATH 已加入 pi 1.5.1 的 `.bin`） | ALL GATES PASSED，包括 04-quality-facts-unit-tests |
| 0480–0495 双审 | 已记账，0495 双审均为 ISSUE 0 |
| 运行时键核对（publish verification） | 19,144 个运行时键：mismatched 0、missing 0、redundant 0、unexpected 0。最终审查时重跑，结果相同 |
| `tools/smoke_release.py` | SMOKE OK；三个 DLC 运行时覆盖层精确一致（743、1569、3149） |
| 插件单测与 `luajit -bl` | 通过 |
| `git diff --check`（`cr-at-eol`） | 干净 |
| 包内容 | teaa 解包与 `git archive 495aa448` 的结果逐字节一致；最终审查时重新打包，内容再次一致 |

## 最终审查补验

两个验证缺口的处理：

- **构造的 quick_reply 与真实 NPC 对话**：已补验并关闭。真实对话文件 `data/chats/corruptor-quest.lua` 由 `Chat.new` 加载，走原版的加载、`newChat`、`addChat` 路径，生成 3 个 quick_reply 节点，回答全部是「[离开]」。界面截图见 `real-npc-chat-open.png` 和 `real-npc-quick-reply.png`。
- **控制台施加与自然触发**：通过源码等价性分析关闭，存档读档部分另行补验。
  - 自然来源与控制台调用的是同一个 `setEffect`，参数也相同：
    - `traps.lua:968` 的捕熊陷阱：`{src, power=0.3, dam}`。
    - Orcs 的 `kaltor-shop/objects.lua:46` 与 `shertul-cave/objects.lua:45`：`EFF_PRESSURE_SUIT, 1, {}`。
    - `sleeping-dragons.lua:69`：`EFF_DOZING, 999, {}`。
  - 提示框读取的是效果定义上被包装的 `long_desc` 和定义里的 type/subtype，与施加方式无关。
  - 捕熊陷阱的 `pinid` 由 `activate` 在可定身时设置，与调用来源无关。
  - 补验时把参数改成陷阱实际使用的 `power=0.3`，复测通过。
- **Ctrl 比较模式**：原始问题 lv1-01 正是在比较模式下发现的。用 `getTextualDesc({比较物品})` 复测，输出为「+5% (+2%) 活物」。其他语境下的 `_t"living"` 仍是「生命」，覆盖没有外溢。
- **存档后读档**：存档、返回主菜单、读档后，存档里的捕熊陷阱效果提示仍显示「定身」（见 `after-reload-bear-trap.png`），其余项与真实对话全部复测通过。整局日志中 Lua Error 为 0。

结果见 `readiness-checks.txt`，pre 段为存档前，post 段为读档后；所用脚本为 `readiness-checks.lua`。环境为官方 1.7.6 本体加 3 个 DLC，开发者模式，加载候选 teaa（sha256 前缀 `22706f10`）。

## 推送顺序（常规 Git 操作，不需要维护者另行决定）

- 发布时把 `candidate/0.3.12`（`495aa448`）快进推送到发布仓库 `master`。`a262ee4` 是它的父提交，会随之一起推送。
- 不需要单独推送 `a262ee4`。在维护者决定发布之前，也不要单独推送：那样会让公开的 `master` 先有代码修复，而 locale 和版本号仍停在 0.3.11。
- 如果发布前发布仓库 `master` 有其他新提交，候选将不能快进，需要在新 `master` 上重跑 `publish --apply --bump` 并重新做本报告中的核对。
- 发布时上传上表记录的 teaa 文件，并核对 sha256 `22706f10…`。重新打包会得到不同的 sha256，原因是 zip 扩展字段，内容并没有变；如果重新打包，应以新的 sha256 为准，并重新回下载核验。

## 剩余限制（不阻塞发布）

- 角色信息面板「vs <类型>」行（`CharacterSheet.lua:1034`）仍使用通用键，显示「vs 生命」「vs 所有」。这是原有状态，不在 lv1-01 的范围内（lv1-01 只涉及物品提示），本轮没有引入回归。可作为后续候选项。
- 捕熊陷阱说明的列表分隔符是半角「, 」，来自上游 `table.concat(desc, ", ")`，只记作 advisory。
- 候选提交的说明写着「(local, not pushed)」，推送后这句话不再准确，只是措辞问题。如果改写提交说明，提交 hash 会变，teaa 需要重新打包和核对（tree 不变）。

## 真正剩余的维护者决定

- 是否公开发布 0.3.12。发布步骤：快进推送发布仓库，打 tag，创建 GitHub Release 并上传 teaa，回下载核验，再写入 `evidence/releases/addon-0.3.12.json`。
