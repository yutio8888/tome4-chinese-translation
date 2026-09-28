# 修复窗口 50 发布记录

## 范围

窗口外宿主补充 27 条（队列耗尽、积压 0 时用户 2026-09-28 选择开窗），涉及 `mod-tome.lua`、`tome-ashes-urhrok.lua`、`tome-cults.lua`、`tome-orcs.lua` 与术语库 3 行（`classes.tsv` 改 Writhing One＝蠕动者并升 preferred；`talents.tsv` 新增 Writhing One＝蠕动者、Mind Drones＝精神无人机）。两项名称按用户纯名称授权咨询 Gemini 3.8 Flash 后采用：Writhing One＝蠕动者（职业、购买页、同名技能），Mind Drone(s)＝精神无人机（技能族 5 条）。一致性：stack of herbs 十条“一束草药”、Temporal Feast 技能名“时空盛宴”、Sher'tul 三条“夏·图尔”、entropic backlash 两条“熵能反冲”。忠实度：乌尔罗格 fearsome to behold 两条、禁忌之书描述、铜制护目镜附言。无跨组件同键兄弟（`check_siblings` 0）。

不含：Archmage `8b977dd836`（pending_repair）、Sunwall 观星台/瞭望台（待用户审第 37 项）、`59339a8b7f`（A.P.E. 缩写，漏纳入，留待后续）。主游戏按 manifest 固定 engine commit `624a673` 核验；DLC 仅固定文件 SHA，源码仓库与 commit 未固定。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修改 27 条与 3 行术语 → REVIEW(0) r0a1（GPT-6 Sol）27/27 OK → FINAL(0) f0a2（Opus 5.5）输出截断（4/27，末 key 残缺）判 INVALID（`publication/INVALID-F0A2.json`）→ f0a3 27/27 OK，cycle 0 收敛（max_cycles 5）。

## Advisory

`a5ef7ca96f`（Ashes 乌尔罗格）末句“他面对你的表情似乎并不惊讶”增译“表情”，不在点名分句内，未改。

## 门禁

17/17 全过，含严格构建（首跑门禁 03 因新增 2 行术语需把静态审计行数 732→734，宿主已改，见 `publication/HOST-NOTE-gate03-term-count.md`）；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`a674a4b5d2666da9eb8bc63cc391af56b33d4c7e`
- 新 catalog：`19d3fa4cc1b61cda24d1d9995d74d02a0458d32d7b6d180c18940c42b12e24fa`
- migration：`d98cee5629b82fc69dc51663d72e5a29c14090d6e960e4c113b109a17d70c476`

## 后续

27 个 successor 必须重新审核，不继承旧 done。

本 publication child 待宿主归档。
