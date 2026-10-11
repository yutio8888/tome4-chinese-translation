# 原版遗留问题真实性与最小修订确认

用户明确指定 GPT 6 Astra High。mode=review_only，change_class=standard；ORCHESTRATOR 与 SENIOR_REVIEWER/purpose=scope_audit。审核既有 310 项问题，非重新盲审或扩展全仓审核。旧 finding 和模型结论只是待核实主张。逐条查实际源码机制，并确认该问题在官方原译中留存。核心固定 commit；DLC 必须核对 SHA 快照并明确来源未固定。

只读，不修改任何文件（包括 /tmp），不运行写入门禁，不提交、不推送、不创建子 agent。每项只返回角色 schema 的八字段校准结论；需要修订的条目在 Minimum sufficient action 给最小充分动作及必要的建议译文，可仅替换缺陷句段。译文须通顺自然、简洁易读，不添加过多机制解释、实现细节或生硬文字。数值、触发条件、效果范围、占位符及标记必须准确；不得为了流畅而遗漏关键机制。对上游英文/代码冲突、纯布局/措辞问题须区别处理，不自动一律修改。

本次只确认并提出建议，由宿主判断 confirmed/pending/advisory 后另行有界应用；审核者不承担译文文件写入。不展开高复用术语全局策略修改。输入不足则说明证据缺口。
