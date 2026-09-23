# 修复窗口 8：R0 单项有界修复

依据 `.ai/task/repair-w8-20260923/ADJUDICATION-R0.json`，本 fresh EXECUTOR run 仅实施 `status=confirmed` 的 `R0-POEM-YEW-THRUSH`：

- `e9253668295a71c738227e4186efa5e9fa86c30ccc629240168490030d584083` 中将“挂满鲜亮浆果紫衫之地”更正为“挂满鲜亮浆果紫杉之地”。
- 将 `Once thrush and owl did screech and cry` 对应译文更正为“曾经鸫鸟与猫头鹰尖啸哀鸣”，恢复鸫鸟与猫头鹰两个主体及其叫声含义。

其余诗句、LF/TAB、markup 均未修改；上一轮 6 个 target 的既有修改保持。`R0-YEEK-CUNNING`、`R0-BLIGHT-EQUALLY-LIKELY`、`R0-DRAGON-FIRST-PERSON` 均为 `pending`，本轮未修改。

实际验证命令与结果见 `VALIDATION.json` 的 `r0_bounded_fix`。
