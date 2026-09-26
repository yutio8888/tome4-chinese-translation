# 修复窗口 36 发布记录

## 范围与预检

- 来源批次：第 306、307、308、309 批。
- 共修复 21 条已确认问题，全部位于 `tome-cults.lua`；全仓库同 source 检查无跨组件同键。
- Cults 仅固定文件 SHA，源码仓库与 commit 未固定。
- 开窗前两个只读助手逐段比对 4 条最长的菲·维莉欧斯条目（`ea6c288d`、`e6802878`、`f4db7369`、`df6ed2f1`），宿主逐字核验引文 29/29 后并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。

## 首次 EXECUTOR

- `execute-01` 的 Codex 会话发生上下文压缩（原生日志含 `compacted` 记录），lifecycle 原生 parser 拒收；按窗口 27 先例 `output_valid=null`，`task_complete` 末条消息逐字留存，成果由宿主精确 diff（恰 21 条 target）独立核验，记录见 [`publication/HOST-EXECUTOR-AUDIT-execute-01.json`](publication/HOST-EXECUTOR-AUDIT-execute-01.json)。

## 复审路径

1. `REVIEW(0)` `r0a1` 确认 2 条：禁忌之书状态“身处书中”；岩谷手记“会是个错误／我们所有人深感痛心”；宿主另补背叛预言重复的持续时间。
2. `execute-02` → `RE_REVIEW(1)` `r1a1` 确认 1 条：`crag` 译“岩谷”而非“岩壁”；`Void Skitterer` 名与熵反冲范围 refuted（本库名；贴合实现）。
3. `execute-03` → `RE_REVIEW(2)` `r2a1` 确认 2 条：市场骚乱警卫到场顺序；幼龙“皮肤之下”裹着怪物肉团。
4. `execute-04` → `RE_REVIEW(3)` `r3a1` 确认 1 条：熵教徒解锁文本 `entropic backlash` 统一为“熵能反冲”。
5. `execute-05` → `RE_REVIEW(4)` `r4a1` 因 identity 回显少一字符被契约拒收（[`publication/INVALID-R4A1.json`](publication/INVALID-R4A1.json)），重派 `r4a2` 仅重复已 refuted 的 `Void Skitterer` 主张，收敛 → `FINAL(4)` `f4a3` 21/21 OK。

## 边界与门禁

- `r4a2` reviewer 通过 Paseo 终端执行只读命令，宿主逐条核对 18 次按键均为只读并在收取后关闭遗留终端。
- 门禁 17/17 全过，含严格构建；状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 发布标识

- 译文提交：`a2c6c9797cfaec6ddd116935bae921a85448599d`。
- 新 catalog：`f0fbe9c67db4794be2c0d6dc6c63bd8e8fee48db4555eafec7a6b677c3c9ce06`。
- migration：`990fc0dd6fb331b5744ae5ccba7d972b033c93042199e6d8d009365e3c9c6bcc`。

## 后续

- 21 个 successor 必须重新审核，不继承旧 done。
- 窗口外宿主补充项留给下一窗口：`f6030742` 导师文物 Sher'Tul“夏图尔”→“夏·图尔”（基线既有；本窗口 SPEC 专名表误写，见 [`publication/HOST-NOTE-SPEC-ERRATUM.md`](publication/HOST-NOTE-SPEC-ERRATUM.md)）；`tome-cults.lua` 第 2340 行 lore 标题“熵反馈”与第 829 行“熵反冲”按“熵能反冲”对齐；`a9c22a10` `misery`→“困难”；`a5a712dc` `Writhing One` 技能名。原“第 1557 行马基埃亚尔”已随 `ea6c288d` 修复。
- 本 publication child 待宿主归档；宿主的证据提交与推送尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
