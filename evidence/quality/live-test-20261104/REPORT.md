# 实机测试（2026-11-04）

## 环境
- 官方 ToME 1.7.6 Linux 版（te4.org，tarball sha256 eff68d02099657452d94e25c876a789fedff8a18df5d91a9d9c16f4ba6eff772），Xvfb＋Mesa 软件渲染，用户态解包，未用 root。
- 插件：汉化 0.3.7（发布包 5ea7f7e5…）与三个 DLC（由 /workspace/tome4-dlcs 公开检出打包，来源未固定）；自带 addon-dev、items-vault、possessors、remote-designer 移出 addons 目录。
- 测试员：Opus 5.5 ×3（core / orcs / ashcults）约 30 分钟后因额度改为 Sonnet 接手（core、ashcults 实际为 sonnet-5，orcs 为 sonnet-5-5）。原始发现与报告在 testers/，截图未入库（本机 ~/tome-live/testers/*/shots）。

## 结果
67 条发现，处置见 disposition.json：fixed 32、engine 覆盖修复 4、发布仓库修复 3、部分修复 2、待插件代码 17、advisory 5、启动菜单不处理 4。

## 修复
- 译文：楼梯限制语病、永久性地、力量来源/制造者、混乱日志、击杀全角感叹号、恢复效果、管理物品栏、角色创建标题、类型：、合计伤害、能量消耗、药剂名空格、治疗数值、配方说明、背带、马基·埃亚尔（DLC/engine/boot 同步）、技能名空格、！。、治疗量、“文明人”、括号与逗号等。
- 名称（Gemini 4 Argon）：Unending Frenzy＝不休狂热；Gunslinger/gunslinging＝快枪手（首轮建议「枪手」与 steam giant gunner 撞名，补充事实后改判）。
- %-8.8s 按字节截断致乱码：去掉宽度说明符（与官方相同），i18n/policy.json 逐条放行。
- 发布：engine 差异条目进插件（见 ENGINE-OVERLAY.md）；发布仓库 null_translation.lua 删除 21 条遮蔽主/官方 locale 的条目。

## 待决
- 17 条硬编码英文需 superload／钩子：H.Key、按键分组、成就分类、对话头像名（The Eidolon、Metash）、Birther 种族列表、Steam:、战役名 Orcs、自动探索中断原因、快捷栏翻页对话框。
