# 修复窗口 43 发布记录

## 范围

来源批次 339、340、341、342 共 25 条确认问题（339 批 8、340 批 5、341 批 6、342 批 6），均为 tome-orcs.lua，已全部修复；无宿主补充，无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 预检

开窗前宿主逐句预检 3 条长条目（[ADJUDICATION-HOST-PRECHECK-C0](publication/ADJUDICATION-HOST-PRECHECK-C0.json)：GEM 录音、阿马克泰尔颂诗、心脏切割附言），追加修复点并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修复 25 条 → REVIEW(0) r0a1（GPT-6 Sol）25/25 OK → FINAL(0) f0a2（Opus 5.5）25/25 OK，cycle 0 收敛（max_cycles 5）。r0a1 原生工具审计中 2 处 `rm ` 模式命中为只读 sed 说明文字里 “confirm ” 的子串，非命令。

## 宿主更正

SPEC.md 验证段残留上一窗口模板的“恰23个”，execute-01 按 25 条执行并在报告指出；宿主随后更正为“恰25个”（见 [HOST-NOTES.md](publication/HOST-NOTES.md)）。

## 门禁与标识

门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

- 译文提交：`fbc29d590362a73b946e70dee78489d2088911ab`
- 新 catalog：`dc90e6baa755d8ab3785318d9357ceabad07b3d4a6073de2962b0a87f21d80bf`
- migration：`be5eb8a9ad03621b7d23e9bec7816b8ab3f2fecea4d239f67e8ae4d2afde055b`

## 后续

25 个 successor 必须重新审核，不继承旧 done。待用户审阅第32–37项不变。

本 publication child 待宿主归档。
