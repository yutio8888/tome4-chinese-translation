# repair-w60-20261001 EXECUTOR 第 1 轮修复

## 范围与裁决

- 基线 revision：`281ad0eff272259bf8c0bf67670c35a0ba7b7353`。
- 裁决输入：`.ai/task/repair-w60-20261001/ADJUDICATION-F0.json`的唯一 confirmed finding，revision `1ebce25bfc96776d0baba0c17448747471b9b6bc02acf02d58b47f8fd2925219`。
- ADJUDICATION-F0 已明确废止 SPEC／SOURCE-CLAIMS 中“第一行不动”的旧要求。
- 本轮仅修改 `mod-tome.lua` 中 `mod-tome/data/talents/spells/deeprock.lua` 的该 target；未修改术语库、其他 target、`.ai/task`或无关文件。

## 实施内容

修复前完整 target：

```text
当你进入深岩元素形态时，你获得 %d%% 流血、毒素、疾病和震慑免疫。
		技能等级 5 或以上时，在深岩形态下，你将用物理抗性取代其他伤害抗性。
```

修复后完整 target：

```text
处于深岩形态时，你获得 %d%% 流血、毒素、疾病和震慑免疫。
		技能等级 5 或以上时，在深岩形态下，你将用物理抗性取代其他伤害抗性。
```

本轮唯一替换为：“当你进入深岩元素形态时，你获得” → “处于深岩形态时，你获得”。其余文字、`%d%%` 占位符、单个 LF 及第二行的两个前导 TAB 不变。

## 验证摘要

- `python3 -B tools/i18n doctor`：通过；Lua 5.1 / LuaJIT 2.1.0-beta3，LPeg 0.10.2-1。三个公开 DLC 的 `source-unpinned` 警告符合 manifest 预期。
- manifest 对应 LuaJIT `LocaleLoader` 对基线 revision 与工作树逐记录比较：加载 22,989 条记录，其中 21,688 条 translation；仍恰有 WORKSET 的 6 个 target 变动，其他记录及所有非 target 字段不变。
- 6 个变动 target 的 LF／TAB／placeholder／markup 不变量通过。
- `terminology/talents.tsv` 相对同一基线可由 TERM-EDITS 精确重放为 1 行插入和 1 行替换，其他行、TAB 与文件末换行不变。
- `python3 -B tools/i18n lint --strict`：检查 30,308 条译文，0 errors，0 warnings。
- `git diff --check`：通过，无输出。

未 stage、commit或 push，未创建 agent。独立复审、任务状态收束与提交发布仍由宿主负责。
