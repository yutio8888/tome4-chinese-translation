# o7d REPORT — Embers：烟雾宫殿(1) 配件与首领（v0.3.12 公开版，Opus）

停止原因：budget（读图达到 16 张提前收尾线；工具调用≈61，图片累计≈0.97 MB）。

## 覆盖（证据分类）
- debug-ui：控制台生成 3 件配件后在物品栏真实悬停提示——惊人的第二皮肤（治疗）、沃瑞钽火箭靴（机械）、沃瑞钽电力反击装置（电力），均正常（000727-tip-e-c.png / 000729-tip-f-c2.png / 000731-tip-g-c2.png）。
- debug-ui：物品栏 电力反击装置→「安装到物品」，提示「你没有可供安装它的已装备物品。」正常（000801-attach-s.jpg）。源码：galvanic retributor 只装盾牌（on_subtype shield）。
- debug-ui：控制台 makeEntityByName COUNCIL2 + addEntity 放置议员 Tormak 成功，地图悬停提示正常（combo1.jpg 右半，名称「议会成员托马克(男性)」、精英Boss、描述、持续技能 太阳风/幻象护盾/模糊视觉）。主手行「龙骨、地狱、超级守护 (95)」为短名+关键词格式，非问题。
- console：第二皮肤用 doWearTinker 附着到 库洛塔的龙鳞甲，控制台确认 A.tinker=惊人的第二皮肤；但装备提示截图失败（物品栏未打开，combo1.jpg 左半为地图），配件行显示未验收。

## 统计
- item 4（通过 3，not_reached 1），monster 1（通过 1），talent 0（not_reached），other 1（通过）。异常 0，findings 0。
- 读图 16（其中 3 张为启动/欢迎框阶段全屏缩略 800x450 jpg，计为全屏）；combo1.jpg 为两张裁切拼合成一次读取，如实说明。
- 工具调用代理计数≈61/100。

## 调试手段
控制台 makeEntityByName/identify/addObject、makeEntity(heavy armor)+wearObject、doWearTinker、COUNCIL2 放置；详见 debug-actions.md。UI 内「安装到物品」用键盘/点击导航两次失败（焦点落到地图「操作」菜单、控制台未关闭），改走控制台。

## 未覆盖（交主代理另开会话）
1. 装备提示中的配件行（龙鳞甲已附着第二皮肤，可直接 i → 悬停身体栏 (238,435) 验收）；UI 内「安装到物品」完整流程（需盾牌或身体/鞋子栏装备）。
2. 工匠/配件技能说明 1–2 条。
3. Tormak 观察详情（l）及其技能说明；Tormak 仍在地图 (11,5)，未攻击。
4. 电力反击装置 on_block 盾牌说明行。
