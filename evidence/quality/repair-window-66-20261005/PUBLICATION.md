# 修复窗口 66 发布记录

## 范围

本窗口包含 25 条译文：`mod-tome.lua` 14 条、`tome-cults.lua` 5 条、`tome-orcs.lua` 4 条、`tome-ashes-urhrok.lua` 2 条；无术语改动。

- 2026-10-05 第二轮重新复审第 397–403 批宿主确认 16 条（各批 `HOST-FINAL-DECISIONS.json`）：换行不变量 2 条（阿尔德胡格尔日志第七篇、兽人军官日志）；忠实性与引号 14 条（阿尔德胡格尔纸片引号与“应当”、《魔法究竟是什么？》四处、科斯汀随笔三处、半身人纸条“磨洋工”、Ashes S 的留言与恶魔紧急便条、Cults 厄格莫斯“抵御文明”、菲·维莉欧斯两卷与“热能射线符文”统一、诸神前言“琐碎卑微的动机”、食人魔迎战末句、Orcs 天文学家日志“过去一个世纪”、梅塔什致谢补“克里布尔部族”、帕默日志补回左引号）。
- 宿主补充 9 条（不计积压，第 398–402 批 `HOST-FINAL-DECISIONS.json` 的 `additional_host_observations`）：均为换行不变量，删多余换行或补回缺失换行，文字不变；唯《苍白之王（下）》在窗口内另经 FINAL f1a2 确认，末尾残缺羊皮纸的 Dreadfe... 残片改译（见下）。
- 新译文由宿主按各条“修复：”与整句对照写定（[`publication/NEW-TARGETS.json`](publication/NEW-TARGETS.json)），EXECUTOR 逐字替换；宿主核验 25 条 after 与 new_target 逐字相等（[`publication/HOST-EXACT-DIFF.json`](publication/HOST-EXACT-DIFF.json)）。窗口内三次修复后宿主均重新逐字核验 25 条：REVIEW r0a1 确认的诸神前言“安格列文”→“安格利文”（execute-02，[`publication/HOST-EXACT-DIFF-POST-FIX1.json`](publication/HOST-EXACT-DIFF-POST-FIX1.json)）；FINAL f1a2 确认的《苍白之王（下）》残缺羊皮纸 Dreadfe... 残片改作“恐惧王……”（execute-03，[`publication/HOST-EXACT-DIFF-POST-FIX2.json`](publication/HOST-EXACT-DIFF-POST-FIX2.json)）；RE_REVIEW r2a1 确认的三处既有误译：克里尔·费扬雕像便条 only now 改作“直到那时我才动用它”、战况便条 secondary team 按恶搞变体统一为“第二支队伍”、梅塔什致谢“灭族危机”改作“几乎注定的死亡”（execute-04，[`publication/HOST-EXACT-DIFF-POST-FIX3.json`](publication/HOST-EXACT-DIFF-POST-FIX3.json)）。`NEW-TARGETS.json` 是 execute-01 的冻结输入，保留这五条的初稿；终稿以 [`publication/rewrites.json`](publication/rewrites.json) 的 new_target 与三份 POST-FIX 核验为准。
- 主游戏按 manifest 固定 commit `624a673` 核验；三个 DLC 源码来源未固定，按公开源码核验并如实标注。四个 locale 文件中无同键兄弟。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 → REVIEW r0a1（gpt-6.1-sol）24 OK／1 ISSUE，确认术语 1 条（诸神前言“安格列文”→“安格利文”，execute-02）→ RE_REVIEW r1a1 25/25 OK → FINAL f1a2（Opus 5.5）24 OK／1 ISSUE，确认 1 条（《苍白之王（下）》残缺羊皮纸 Dreadfe... 残片→“恐惧王……”，execute-03）→ RE_REVIEW r2a1 22 OK／3 ISSUE，确认既有误译 3 条（克里尔·费扬雕像便条 only now、战况便条 secondary team、梅塔什致谢 near-certain deaths，execute-04）→ RE_REVIEW r3a1 25/25 OK → FINAL f3a2（Opus 5.5）25/25 OK；第 3 轮收敛（`max_cycles` 5），无无效尝试。

门禁 17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`fd7c6a613caa2f8fbf61bdc0f5bb3043427bc1fb`
- 新 catalog：`ef31a0ea5bf16f8e410b260c8ba90e7fe6b468e3394cbd32ea875936629a8fe4`
- migration：`defcd152d0e8ae9f9333fe13b2ae428d3e5363af4a9b18bccab8f557b3ab8c23`

## 后续

- 25 个 successor 必须重新审核，不继承旧 done。
- 下一个修复窗口（67）积压 0 条；宿主补充（不计）`9d3fc01bdf` Cults 奎科加章节（`kroshkkur.lua`，源文 records of Anglowen）的“安格列文”待按 Angolwen＝安格利文 修正，不在本窗口 workset。
- 用户已指示修复后发布插件新版本。

本 publication child 待宿主归档。
