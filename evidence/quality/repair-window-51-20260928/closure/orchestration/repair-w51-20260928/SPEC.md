# 合并修复窗口 51：第361批确认项与 A.P.E. 缩写，2 条

Paseo MCP / schema5 translation_contextual_v2 implement。基线 d11abfc3242aa9fd497e95f5e66d10db7dc137c6。审核队列已耗尽（第361批后 queued=0），积压 1 条低于 20 的开窗阈值；用户 2026-09-28 明确选择开窗口 51 修第361批确认的 1 条及窗口50漏纳入的 A.P.E. 缩写 1 条（不含范围外 Archmage 8b977dd836 与待用户第 37 项的 Sunwall 译名）。用户已授权连续审核与合并修复、提交与推送；max_cycles=5（用户 2026-09-25 授权）。

唯一 EXECUTOR 仅可修改：WORKSET.json 列出的 2 个 target（mod-tome.lua、tome-orcs.lua 各一条），以及 `evidence/quality/repair-window-51-20260928/` 下的修复证据。不得修改 source、source_tag、section、args_order、运行键、其他译文、术语库、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

**本窗口是定向修改，不是全文重译。** 每条只改 SOURCE-CLAIMS 点名的词语或句子（以及为此必须调整的衔接字），不得借机改写其余部分；即使发现别处可疑，也只在报告中列出、不改（宿主另行登记）。修改点名句时须对照整句原文，不留同句其他旧错。专名沿用本库既有译法（夏·图尔、太阳主上、便携式自动材料提取仪等）；A.P.E. 条的 Archmages＝元素法师牵涉待定的 Archmage 裁决，不得改动。

保留 printf 占位符、`%%`、`#TAG#`、`#{italic}#`、`#{normal}#`、`#{bold}#`、`<?=...?>` 模板、`@name@` 等 markup 的数量、顺序及适用位置；保留 source_tag。LF/TAB 结构与现译逐行一致（本窗口不改换行）。用 LuaJIT 加载 mod-tome.lua 与 tome-orcs.lua，证明恰 2 个 target 变动且其他记录不变；执行 strict lint 及 git diff --check。无需完整门禁，宿主在独立复审后统一运行 17 项。主游戏源码只从 /workspace/t-engine4 固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63 取证；DLC 源码只在 SOURCE-ANCHORS 给出的 checkout 下按条目路径取证，不扫 `/`、`/workspace` 或无关目录；DLC 源码仓库与 commit 未固定。

审查：cycle-0 `REVIEW/full` 用 Codex GPT-6 Sol；确认问题合并给一次 EXECUTOR fix；收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL（同 cycle 用下一个 attempt）。max_cycles=5。reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。与本窗口裁决无关的既有问题由宿主记 advisory 并 carry_forward 到后续审核，不扩大本窗口范围。

## 条目与已确认修复依据

- 20fa052d6c3f569c56a139a845e16a768b7b1562be6c5e92e0deed27395f1d63 | mod-tome.lua | mod-tome/data/achievements/quests.lua | 第361批确认（固定 commit 624a673 game/modules/tome/data/achievements/quests.lua:132 成就 They Came Back For Eyal "…stopping you at the last moment from opening a portal to your mad patron sun."）：chats/sorcerer-end.lua:42/44/102 表明遥远太阳是玩家侍奉的主神（your patron），本库同族对话已把 patron sun 译作“太阳主上”（mod-tome.lua “你的心智已被太阳主上焚毁”）。现译“阻止了你为疯狂的太阳开启传送门”漏掉 your…patron，并把 a portal to（通往……的传送门）误作“为……开启”。改为“阻止了你开启通往你那疯狂的太阳主上的传送门”一类；“感谢夏·图尔人在最后一刻”与“，通关ToME。”保留。
- 59339a8b7f5d4c9a282d0997e8f039419658f5295f4ec4ae4a212d1cdc5347ae | tome-orcs.lua | tome-orcs/data/talents/uber/mag.lua | 宿主补充（第337批 advisory，窗口50漏纳入；公开 Orcs tome-orcs/data/talents/uber/mag.lua:199 科技法师进阶说明列表项 "- An Automated Portable Extractor (A.P.E.)"）：现译“- 一个便携式自动材料提取仪。”漏译缩写 (A.P.E.)，并多出原文没有的句号；A.P.E. 是该物品在游戏界面中的通用简称（同 DLC 物品菜单 "APE" 相关文本均作“提取仪”指称）。只把该行改为“- 一个便携式自动材料提取仪（A.P.E.）”，保留 TAB 缩进；同条其他行（含 Archmages＝元素法师，牵涉 Archmage 待定裁决）一律不动。
