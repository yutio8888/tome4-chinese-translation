# Opus 5.5 问题真实性排查

用户要求启动 Opus 5.5，将既有问题列表发送给它，排查问题是否属实。本次仅核验既有 374 项，不修复译文或术语库。

模型身份由运行时元数据确认为 `claude / claude-opus-5-5`。完整逐项意见见 [原始报告](raw-claims-a1.md)，结构化意见见 [parsed-assessments.json](parsed-assessments.json)。输入见 [frozen-input.json](frozen-input.json)，派发要求见 [dispatch-prompt.txt](dispatch-prompt.txt)。输入 SHA256 为 `251f5e9729629abfe7af08c2c2ea6fd2a46ceca05c6cfded480da6f445114aa1`。

模型建议：keep 238、downgrade 116、narrow 14、reject 4、defer_to_user 2。这些是模型意见，不是自动生效的宿主裁决。

宿主独立核验关键反证后，叠加列表为 **323 confirmed、49 advisory、2 withdrawn**，完整记录见 [host-adjudication.json](host-adjudication.json)。原始 findings.json 不改写；未列入下述六项的既有状态、优先级继续保留，不宣称本次重新独立核验了所有 374 项。

- M136 撤销：固定源码 inscriptions.lua:245–248 使用含 `to a maximum of 100%%` 的新运行键；本项旧键不显示。实际键 M143 的换行问题仍保留。
- M278 撤销：cults timed_effects.lua:1596–1657 的长描述仅在层数超过 6 且有 avoid 时显示。calamity.lua:56 以一层初始化，进入长描述分支前 on_merge 已正向增加闪避和豁免。首次负值实现问题对应 M277。
- M328、M347 降为格式建议：分别核对 throwing-knives.lua:391–394、uber/wil.lua:390–410，换行数与空行位置相同，仅空行上的制表符不同。
- M350、M351 降为术语策略建议：项目技能名与引用一致使用“食尸鬼跳跃”；快照“定向跳跃”为 existing。TERMINOLOGY.md 明确禁止将 existing 提升为强制规范，本次不修改术语策略。

核心证据适用固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。DLC 来源与 commit 未固定，结论限于冻结哈希匹配的公开源码快照；cults timed_effects.lua SHA256 为 `0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c`。

模型建议将 91 项纯换行问题降为 advisory；宿主未接受此统一策略，因为 TERMINOLOGY.md 要求换行原样保留。上游英文与实现冲突继续按既有来源分类记录，不能仅因译文忠实于英文就否定源码事实。其余优先级降低和范围缩窄意见留供后续参考。

模型承认在 `/tmp/mc/` 写了辅助脚本，违反派发的禁止写文件要求；见 [boundary-incident.json](boundary-incident.json)。因此本次输出保存为非合规模型意见，不认证为正式独立复审。宿主确认译文文件哈希未变，未发现 reviewer 的仓库改动。所有 child 已归档，见 [archive-confirmation.json](archive-confirmation.json)；任务以 STOP 关闭，离线检查结果为 `STOP_VERIFIED`。用户请求的模型咨询已交付，不启动修复或新一轮审核。
