# lv3 实机巡检报告（2026-11-11，DLC 专属界面）

## 实际覆盖
- 创角界面：高等人类+链锯屠夫（Embers 工匠系四职业说明）、Cults 疯狂系（蠕动者/邪教徒）、Ashes 堕落系（收割者/腐化者/毁灭使者/恶魔使者）、兽人战役（余烬怒火）介绍与种族说明。
- 实机进入：Cults 起始区（克诺什库尔避难所）、Embers 巨魔沼泽与克鲁克部落（兽人战役）、Ashes 兽人恶魔使者开局。
- 界面：欢迎框、任务日志、角色面板（常规/攻击/防御）、物品栏、商店、资源条悬停（蒸汽/弹药/活力）、技能栏悬停（制造配件、药剂）、配件制作界面（火箭靴）、升级窗口（恶魔契约 恶魔之种提示）、NPC 观察提示。
- 控制台批量转储（getTalentFullDescription / getDesc / tempeffect long_desc）：
  - 蒸汽科技 181 个技能、全部 2056 个技能的描述（重点读 Cults 疯狂系 102 条、Ashes 堕落系 ~100 条、Embers 蒸汽科技）。
  - 三个 DLC 全部 ~100 件神器/专属物品的物品说明（Ashes 黑之套装、Cults 禁忌之书与脊笼等、Embers 蒸汽枪与链锯）。
  - 830 个状态效果说明文本。
- 静态比对：DLC 源码中所有未注释的 _t/tformat 字面量对照本库 locale（Ashes 0 条漏；Cults/Embers 仅余官方注释掉的废弃内容）；tformat 占位符一致性（14 条数量差异，已逐条看，均为 %% 与多行折叠造成的计数差，无真实错位）。

## 未覆盖
- 恶魔种子实物（需击杀宿主）、禁忌之书阅读弹窗、疯狂值资源条（Cults 角色未实际战斗）、各 DLC 剧情区域（Kroshkkur 外、Anteroom of Agony 等）、Embers 商店/Vaporous Emporium 对话、医疗注射器使用流程。
- 屏幕截图仅覆盖约 22 屏，其余问题来自控制台转储（findings 里 screen 字段为转储文件名，不是图片）。

## 问题统计
共 7 条：mistranslation 2、awkward 2、format 1、untranslated 1、inconsistent 1。其中 lv3-05、lv3-07 为静态推断（verified=false），其余已对源码/locale 核对。
## 补充
- 控制台创建/转储对象后，在地图上右键会触发「unknown inscription RUNE:_FROZEN_SPEAR_5」Lua 错误，系转储时克隆符文物品造成，非翻译问题，不报。
- 持续技能的「消耗蒸汽／蒸汽消耗」语序不一致为既往 orcs-05（advisory），未重复报。
