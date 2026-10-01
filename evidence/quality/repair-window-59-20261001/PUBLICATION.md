# 修复窗口 59 发布记录

## 范围

本窗口发布 44 条译文（主游戏 33、Cults 1、Orcs 10）与 21 行术语（creatures/items/narrative/society/talents，改为 preferred）。

来源一：第375批（`batch-9da6a86a32b67cc82ddf`）与第376批（`batch-93dd0d869b4d3e8058dc`）确认的 4 条：`1c38f759ab` 引导异常目标并合并多拆一行、`4e496adf1d` 太阳赞歌“距离三格及以上”、`5c0dc6d9d2` 阴影消隐“受到攻击时”、`6a7d1cc720` 吞噬“尝试吞噬：若成功则”。

来源二：2026-10-01 术语补录（`8e2fae4e`）发现 21 个名称的引用漂移，经三方讨论（gpt-6-astra / claude-opus-5-5 / gemini-3.8-flash），用户同意“启动修复窗口”，统一 40 处引用；另宿主按事实裁定 Hideous Visions 错指技能名与 critical 错字 2 条。主游戏按 manifest 固定 commit `624a673` 核验；DLC 来源仓库与 commit 未固定。Deeprock Form 三方不一，不在本窗口，待用户定。无同键兄弟。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-*.json`](publication/)：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）6 ISSUE：5 确认（Celia 悲痛发疯、凤凰描述重译、飓风限定词、Mana Gale／Telekinetic Punt 术语 target），1 驳回（精准射击 vulnerable to 忠实）→ execute-02 → RE_REVIEW(1) r1a1 44 OK → FINAL(1) f1a2（Opus 5.5）2 确认（`5c0dc6d9d2` 单行结构、`a38a4fc495` 命中时与第三行缩进）→ execute-03 → RE_REVIEW(2) r2a1 1 advisory（吞噬“恢复失衡值”，用户 2026-10-01 裁定保留全库译法）→ FINAL(2) f2a2 revision_key 缩写、契约校验拒收（[`INVALID-F2A2.json`](publication/INVALID-F2A2.json)，不计轮次）→ fresh retry f2a3 44/44 OK，cycle 2 收敛（max_cycles 5）。

advisory carry_forward：Korbek 实验笔记正文标题“：N”与物品名“，第N部分”格式不一（4 条）。

宿主备注：前三轮冻结简报误写“审3条”（模板遗留），各轮 reviewer 均全覆盖 44 条；自 r2a1 起改为“审44条”。

## 门禁

17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`e6dce58129eee458c9bd3db2d769755206817775`
- 新 catalog：`0e9e1d992c510295a74b2f33bcdcf413872855f10cf6763599ffc2b51db21e9c`
- migration：`dd0d78d9bc040f1eed73862fcf7ad3b1e283681d8096eac44fa9505e0793acf0`

## 后续

44 个 successor 必须重新审核，不继承旧 done。窗口 60 积压 0 条。

本 publication child 待宿主归档。
