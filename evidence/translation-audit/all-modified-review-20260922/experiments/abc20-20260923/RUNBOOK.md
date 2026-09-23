# 连续20组实验恢复入口

用户已授权累计20组，每组40条，共800条；包括最初两组。没有逐组确认要求。只写实验evidence，不改译文、术语或原campaign，不提交或push。各组身份和派发记录以STATE.json及对应组STATE为准，不能从准备完成推断实验完成。

每组3个独立参赛REVIEWER：claude/claude-opus-5-5、codex/gpt-6-sol、antigravity/gemini-3.8-flash，均high；三臂收到同一dispatches/common-prompt.txt。独立盲审及fresh匿名裁决使用codex/gpt-6-astra high。模型家族相关性需披露。Paseo mcp，workspace=wks_ac28b30c4bf45d5b，parent=3a99ff56-6868-4533-b3d5-755e411f9159。总活动child最多3，可跨组流水派发。

每次派发前live读取profiles；以用户指定模型覆盖旧profile模型，保存creation_pending再create，核验身份和lineage后保存raw启动快照。终态不follow-up。等待完成通知，不能轮询running状态。收取get_agent_activity时可能需要limit=3000：共享工作区Edit事件可能挤掉最终回复，不能把此提取问题当作模型无输出。原活动完整保存，最终报告从明确起点提取至下个Thought/Edit边界。

收取后保存reports和raw terminal；运行组record.py harvest，记录归档尝试，然后archive并live确认archivedAt，再record.py archive。故障也须终态、attention、activeTurn和工作树核验，再归档。连接故障不记内容错误；一次同prompt fresh retry，保留失败运行并使用SELECTION.json显式选中替代dispatch，不覆盖原报告。

三臂和独立盲审均完整后：

```text
python3 -B <series>/series.py adjudicate <group>
```

脚本保持每项观察原文与offset/hash，生成匿名INPUT、冻结和裁决prompt。按该prompt新建adjudication-01，禁止读取身份映射及原报告。必须裁决全40条和全部O项，输出entry/D/O三个表；证据不足保留pending，不按多数票定真值。完成后收取及归档，再执行：

```text
python3 -B <series>/series.py finish <group>
python3 -B <series>/aggregate.py
```

finish只处理机械映射与统计，不决定语义。先人工核对报告读取边界和裁决映射；有违规时不得默认纳入合规主比较。原第一组Opus旧协议违规臂仅诊断，累计合规三方汇总排除该组。原判定不能因后续裁决确认而补算检出。

后续源码：本体固定624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC只有公开快照哈希、无固定源码commit，按每组INPUT/source-access边界核验。addon-dev/items-vault未定位源码，机制疑点pending。各组FREEZE与BASELINE不可改写，原第2组文件被后续baseline引用，保持不变。

每组结果保存在RESULT.md、MERGED-FINDINGS、REFERENCE、SCORING、METRICS、VERIFICATION。总表只累计真正闭合组。须持续至20组，不得提前声称完成；必要阻塞如实记录。最终汇总是模型暂定参考，不是人工金标准或生产DONE_VERIFIED。

第10组通道恢复的唯一额外重试见 PLAN.md 2026-09-23 补充；不泛化为其他组的无界重试。
