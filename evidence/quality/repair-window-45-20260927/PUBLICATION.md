# 修复窗口 45 发布记录

## 范围

来源批次 349、350、351、352 共 24 条确认问题（349 批 2、350 批 9、351 批 7、352 批 6），加宿主补充 3 条（用户 2026-09-27 裁决的灵能蠕虫 `tformat` 裸 `%`；窗口 44 advisory 的毁灭号 beaded panel 两条），合计 27 条，均为 `tome-orcs.lua`，已全部修复；无跨组件同键兄弟（`check_siblings` 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 预检

开窗前宿主预检 6 个结构/运行时要点（[`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)：制表符、换行与灵能蠕虫 `tformat` 裸 `%`），并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修复 27 条 → REVIEW(0) r0a1（GPT-6 Sol）2 条确认（Electricity 频率：第 350 批宿主 claim 误判“每隔一级”，按 `craft_levelup` 实为逐级；沉睡洞穴日志单数“我”）＋宿主自查 1 条（成就 Boss 名）→ execute-02（漏改 Boss 名）→ execute-03 补做 → RE_REVIEW(1) r1a1 1 条 advisory（Ureslak 音译，待审第 40 项）→ FINAL(1) f1a2 3 条确认（灵能蠕虫传播对象/豁免、毁灭号启动句、成就句内统一“乌瑞斯拉克”）→ execute-04 → RE_REVIEW(2) r2a1 1 条确认（a handful→几名）＋1 条 advisory（tinker）→ execute-05 → RE_REVIEW(3) r3a1 PASS → FINAL(3) f3a2 1 条（tinker，宿主判 advisory）→ RE_REVIEW(4) r4a1 同一条第三次被指出，宿主改判确认 → execute-06（“电子蒸汽工具”）→ RE_REVIEW(5) r5a1 PASS → FINAL(5) f5a2 27/27 OK，cycle 5 收敛（max_cycles 5）。

## 门禁

17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`41dbeade832bbf97b88ad43dc8b3d9b6440bfd14`
- 新 catalog：`d78ae4f3870aa9ce25dc60a1165755d58d7419c617b6859ad2a3018ca3ad4649`
- migration：`2866e76c1a7ebda59d6e5cfeab63713726a5a90aa25f6a6041d4f30c8409ab17`

## 后续

27 个 successor 必须重新审核，不继承旧 done。新增待审第 40 项（Ureslak 音译）与第 41 项（tinker 道具/蒸汽工具，同族另五条排入窗口 46 宿主补充）。strict lint 漏检非法 `%` 的修复在本窗口译文之后由宿主另行提交。

本 publication child 待宿主归档。
