# 修复窗口 26 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 5 个 target，并在本目录保存冻结副本与真实验证结果；source、section、source_tag、args_order、printf 占位符、`%%`、markup 均未改变。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `fc0f5daae4…`（思维形态系说明）：把误译为技能的“灵能召唤术”改为实体“灵能召唤物”。
- `fc3dc9f6fb…`（写给威斯曼的信 (1)）：按原文三段重译；第一段恢复“主要是好笑，外加不少轻蔑”及勇敢、胆识与豪侠气概的讥讽，第二段恢复近期考验、古老树林、德斯、丑恶臃肿且渗着黏液并吱吱作响的怪物、巨蚁始祖、成群甲壳幼虫及大地涌来吞噬的意象，第三段恢复“让你看清自己的愚蠢”，并删去原文没有的“世界如此巨大”等改写。
- `fc5311ffa7…`（泰坦的箭袋）：补全箭矢被磨得锋利无比、看上去几乎无法折断、比见过的任何箭都更像长钉三个要点。
- `fc60ee27ed…`（阿塔玛森丢失的红宝石眼睛）：把第二、三句合回同一行，并补全杀死兽人首领吞噬者加库尔、给兽人以重创。
- `fc7538838d…`（梅琳达任务日志）：补回夺魂魔“袭击队”。

## 固定源码与专名核对

仅使用 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查五条对应源码：`game/modules/tome/data/talents/psionic/psionic.lua:49`、`game/modules/tome/data/lore/misc.lua:90-98`、`game/modules/tome/data/general/objects/world-artifacts.lua:5678`、`game/modules/tome/data/zones/sandworm-lair/objects.lua:109-110`、`game/modules/tome/data/quests/love-melinda.lua:28`。实际源码与冻结 `SOURCE-ANCHORS.json` 一致。

在 `mod-tome.lua` 中核对并沿用：思维形态、威斯曼、罗尔夫、古老树林、德斯、泰坦的箭袋、阿塔玛森、半身人、烈火纪、吞噬者加库尔、梅琳达、夺魂魔。未新造专名，未修改术语库。

## LF/TAB 逐行核对

空行下标同时记录 0 起点和 1 起点；TAB 数组按每行行首 TAB 数排列。五条 source/target 完全一致：

- 思维形态说明：`0` 个 LF、`1` 行；空行 `[]`；TAB `[0]`。
- 写给威斯曼的信 (1)：`8` 个 LF、`9` 行；空行 0 起点 `[1,3,5,7]`（1 起点 `[2,4,6,8]`）；TAB `[0,0,0,0,0,0,0,0,0]`。结构为称呼、空行、第一段、空行、第二段、空行、第三段、空行、署名。
- 泰坦的箭袋：`0` 个 LF、`1` 行；空行 `[]`；TAB `[0]`。
- 阿塔玛森红宝石眼睛：`1` 个 LF、`2` 行；空行 `[]`；TAB `[0,0]`。
- 梅琳达任务日志：`0` 个 LF、`1` 行；空行 `[]`；TAB `[0]`。

窗口专用验证脚本同时按全记录比较确认恰有 5 个 target 变化；独立逐行断言确认每条 source/target 的 LF 数、行数、空行下标和逐行 TAB 数组相同。

## 冻结副本

- `PREFLIGHT-BATCH272.json` 是 `.ai/task/repair-w26-20260923/PREFLIGHT-BATCH272.json` 的逐字节副本，SHA-256 为 `49f507c92f7934ec553550912b18bec3189f2f047ac89fd38520802eb5a98254`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w26-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `21581566b7d3d56e535f5954b9607433fbc02b3502c028ef2b4f574c29ee7f23`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w26-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `2c19eb261a0f4635c875386f28e998e21c61b258e9b8a8e18802361d7926a49e`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未修改 `.ai`、规则、工具、术语库或 handoff。

## 第 1 轮修复（新 EXECUTOR 会话）

依据 `.ai/task/repair-w26-20260923/ADJUDICATION-R0.json` 的两条 confirmed finding，本轮只对已修复的 5 个 target 中的两处做有界调整：

- `fc3dc9f6fb…`：将叙事/lore 语境中的“古老树林”改为术语库与同类条目使用的“古老森林”。其余文字未动，target 仍为 8 个 LF、9 行，空行位置不变；未修改区域名条目中的“古老树林”。
- `fc60ee27ed…`：将第二行中造武器、被毁且杀死加库尔的主体明确为“阿塔玛森/这具傀儡”，避免误读为红宝石眼睛。第一行未动，target 仍仅 1 个 LF、2 行。

另外三个 target 未修改。本轮仍未 stage、commit 或 push，未写入 `.ai`，未修改规则、工具、术语库、handoff、catalog 或 migration，并保留无关 untracked 文件。
