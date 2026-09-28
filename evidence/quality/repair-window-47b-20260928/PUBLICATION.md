# 修复窗口 47b 发布记录

## 范围

B 组（用户 2026-09-27 对待审清单的裁决中单条措辞与名称的部分：第 3、6、8–14、17、18、20–29、31–35、38、39、41 项）48 条，加窗口 47a 转入 8 条（“火魔婴”→“火焰小鬼”6、“物品黑暗麻木”→“物品暗影麻木”1、雕像名“莎西·凯希”1），共 56 条宿主补充，涉及 `mod-tome.lua`、`tome-orcs.lua`、`tome-ashes-urhrok.lua`；名称类按用户指示采用 Gemini 3.8 Flash 结论；术语库未改；无跨组件同键兄弟（`check_siblings` 0）。Ashes/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修改 56 条 → REVIEW(0) r0a1（GPT-6 Sol）唯一 ISSUE 驳回 → FINAL(0) f0a2（Opus 5.5）2 条确认（科技法师进阶说明的蒸汽工具配方与技能树名；梅塔什对话漏译与增译，见 `publication/HOST-NOTE-f0a2-scope.md`）→ execute-02 → RE_REVIEW(1) r1a1 2 条确认（less than ashes；米诺陶 lore 的 eons 与 rejuvenated）、2 条驳回（Archmage 职业名“元素法师”；死亡描述模板）→ execute-03 → RE_REVIEW(2) r2a1 通过（死亡描述驳回）→ FINAL(2) f2a2 2 条确认（亡灵猎手指南署名统一；华丽抛枪后续技能多余换行）→ execute-04 → RE_REVIEW(3) r3a1 1 条确认（梅塔什光束打穿岩层露出天空）→ execute-05 → RE_REVIEW(4) r4a1 通过 → FINAL(4) f4a2 56/56 OK，cycle 4 收敛（max_cycles 5）。

死亡描述 `f6cc31f278` 被 GPT-6 Sol 连报五次，均按模板“%s而死”（`mod-tome.lua:1413`、`1416`）与待审 #18 用户裁决驳回。r1a1 的终端快照曾以占位时间戳生成后重建，见 `publication/HOST-NOTE-r1a1-terminal-capture.md`。

## Advisory

- `9af7773a4c` 的 A.P.E. 缩写本库一贯不译。
- `f5f092ac5d` 歌词 ogre/over 双关（47a 转入）。

## 门禁与标识

门禁 17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

- 译文提交：`a10222b7e4a6650d289ed90120e8d2acb867ed53`
- 新 catalog：`580d8c9600d40dc4a19547e3f797e8efaeb5191416177fb9bf71b293af469e65`
- migration：`2e88ba7a55900439acf3edb9f216e2b20fd272c338f3a4307dc8ba0d0c3d0809`

## 后续

56 个 successor 必须重新审核，不继承旧 done。

本 publication child 待宿主归档。
