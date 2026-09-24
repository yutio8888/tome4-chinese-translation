# 修复窗口 22 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次唯一 EXECUTOR 仅修改 `mod-tome.lua` 中冻结 WORKSET 的 6 个 target：

- 欺诈斗篷生效日志：将错误的“看起来像活着一样”修为“看起来像人类”。
- 电鳗尾炼金说明：逐句修为“电鳗从哪儿算起、尾巴从哪儿开始”“其实没多大关系”“最后十英寸左右就够了”。
- 厄奇斯成就说明：补出“疯狂的”与“猛攻”，保留“风暴魔导师”“厄奇斯”“德斯镇”。
- 日月垂饰说明：将“红月吞日”修为“赤铁矿之月遮蔽金色太阳”，并明确物品曾由太阳堡垒的一位建立者佩戴。
- 腐化蒸汽说明：补出主语“腐化的蒸汽”以及“在目标位置升起”，保留 `%0.2f`、`%d` 和一组 `\n\t\t`。
- 有丝分裂说明：恢复与原文一一对应的 7 行结构，补出“在附近视线内”、技能等级与召唤上限限制、技能激活期间的伤害均摊，并将 `take damage` 译为“受到伤害”；沿用“浮肿软泥怪”。

其余已忠实句子未重写；只对同一条目中明显的错译、漏译和病句作了有界修正，未处理 advisory、pending 或其他 repair。`source`、`source_tag`、参数顺序、printf 占位符、`%%` 与 markup 均保持基线。专用验证确认前四条均为 0 个 LF；腐化蒸汽 source/target 均为 1 个 LF，续行均以 2 个 TAB 开头；有丝分裂 source/target 均为 7 行（6 个 LF），首行均无 TAB，其余 6 行均以 2 个 TAB 开头。

`PREFLIGHT-BATCH268.json`、`HOST-WORKSET.json` 与 `SOURCE-ANCHORS.json` 均从 `.ai/task/repair-w22-20260923/` 机械复制并逐字节核验一致。真实检查结果见 `VALIDATION.json`。

本执行未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。独立 REVIEW、FINAL_REVIEW、完整门禁、构建与 `DONE_VERIFIED` 仍由宿主继续。

## 第 1 轮修复

根据 `ADJUDICATION-R0.json` 的唯一 confirmed finding `R0-CLOAK-ILLUSION-APPEARS`，将欺诈斗篷生效日志的完整 target 从“`#Target#周围的幻影让%s看起来像人类。`”有界修为“`一层幻影出现在#Target#周围，让%s看起来像人类。`”，补全 `appears` 所表达的幻影出现事件。`#LIGHT_BLUE#`、`#Target#`、`%s`、source 与 `source_tag` 均保持不变；首次实施中的其余五条 target 保持不变。本轮仍未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。验证结果追加记录于 `VALIDATION.json`。

## 第 2 轮修复

根据 `ADJUDICATION-F1.json` 的唯一 confirmed finding `F1-EEL-STOP-VS-START`，仅将电鳗尾炼金说明 target 中的“`电鳗从哪儿算起、尾巴从哪儿开始？`”逐字替换为“`电鳗到哪儿为止、尾巴又从哪儿开始？`”，修正 `stop` 所指的终点与 `start` 所指的起点。该条其余文字、source、source_tag 与首次实施中的其余五条 target 均保持不变。本轮仍未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit 或 push，并保留无关未跟踪文件。验证结果追加记录于 `VALIDATION.json`。
