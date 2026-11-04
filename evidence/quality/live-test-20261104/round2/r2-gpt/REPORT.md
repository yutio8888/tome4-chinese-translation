# ToME4 第二轮实机测试报告：r2-gpt

测试员：`r2-gpt`；显示：`:85`，1600×900。开始：2026-11-04 03:23 UTC；收尾记录：2026-11-04 05:29 UTC。实际操作约两小时，包含截图复核、只读源码定位和报告整理；因返回城镇与收尾略超出两小时。环境按本轮提供的 ToME4 1.7.6、汉化插件 0.3.8 和三个官方 DLC 测试；日志确认加载 Modified Chinese Translation。未启用其他测试用插件或作弊。

角色：科纳克人影舞者，主游戏马基·埃亚尔卓越纪战役，普通/冒险模式，升到 2 级。角色名因首次输入串接误操作变成 `r2-gptmousemove211281clic`，不将这一测试操作结果列为翻译问题。

## 结果

- 新问题：1 条，`awkward / minor`，已查证。见 [findings.jsonl](findings.jsonl)。
- `r2-gpt-01`：野性纹身说明中的「对…效果每类各解除你随机一个」语序错误。局部放大和 `mod-tome.lua:25912` 均已复核；机制以固定源码 `624a67329fe2` 的 inscriptions.lua:157–158 为依据，逐类型解除一个负面效果的机制本身正确。
- 未检出文字相关 Lua 错误；对 game.log 搜索 `Lua Error` 与 `stack traceback` 无匹配。
- 已对照第一轮 disposition 和 findings 去重，已知的启动旧译、硬编码英文、名牌英文等不重复报告。商品长名称未选中时截短、选中后滚动显示完整，未据此登记缺陷。OCR 漏字已通过局部放大或库内原文排除。
- 只在本测试目录写入报告、截图及游戏自身配置/存档，未修改 `/workspace` 文件，未修复译文、未提交。

## 实际覆盖及未完成项

完成了巨魔沼泽第一层探索、第二层部分探索，完成「护送：迷路的战士」并领取活力奖励，阅读任务接受/完成消息、两类任务日志、NPC 求助与奖励对话；实际升级、分配属性和技能点，查看刻印位扩展确认；回到德斯草药馆检查商品、出售确认、出售后金币变化和购买金币不足反馈。出售了一根法杖，未成功购买高价纹身。

按不同说明面板/对话内容计，下面索引记录 **52 项**；同一地图的反复移动、重复截图及重复技能提示未重复计数。满足至少 40 个不同界面或文本面板的覆盖目标。

**覆盖不足，不能视为全范围通过：**

- 临时状态详细悬停只完成 **8/20**：痛苦压制、纹身饱和、符文饱和、招架、再生、中毒、卑劣攻击、震慑。另读潜行技能说明及影之格斗持续技能提示，不将这些充作新增临时状态数量。
- 手札仅 **1/5**：《残破的纸片（巨魔沼泽）》，全文见 035249 截图。其余手札未读，不以源码浏览代替实机阅读。
- 未完成起始区域 Boss、深层区域、神器/稀有物品说明覆盖；已读的是普通附魔装备。未完成城市任务 NPC 的深入对话；NPC 对话主要来自实际完成的护送任务。
- 角色未死亡，未覆盖死亡、墓志铭、艾德隆或死亡读档流程。
- 购买仅覆盖金币不足分支，未覆盖购买成功及新纹身铭刻替换流程。

操作中短促输入和目标选择/地图模式造成数次误触，树林阻挡与发现物品也中断行走，减少了深层内容覆盖；这些不列为翻译缺陷。以上缺口如实保留，不用重复界面凑状态或手札数量。

## 面板与截图索引

|序号|阅读内容|截图|
|---|---|---|
|1|角色创建：主战役、科纳克人影舞者说明|[截图](shots/032441-shadowblade.png)|
|2|初始升级面板与属性分配|[截图](shots/032458-talents.png)|
|3|潜行技能完整说明|[截图](shots/032512-stealth.png)|
|4|卑劣攻击技能说明|[截图](shots/032526-dirtyfighting.png)|
|5|双持掌握技能说明|[截图](shots/032539-dualmastery.png)|
|6|强化命中技能说明|[截图](shots/032545-accuracy.png)|
|7|受训反应技能说明|[截图](shots/032558-movementtree.png)|
|8|强化感知技能说明|[截图](shots/032604-heightened.png)|
|9|后跳技能说明|[截图](shots/032617-disengage.png)|
|10|加点接受更改确认|[截图](shots/032623-confirmbuild.png)|
|11|科纳克人开场叙事|[截图](shots/032636-intro.png)|
|12|初始任务日志：巨魔与潮湿洞窟|[截图](shots/032657-queststart.png)|
|13|使用技能列表及快捷键说明|[截图](shots/032715-usetalents.png)|
|14|符文：法力涌动说明|[截图](shots/032727-manasurge.png)|
|15|纹身：野性说明|[截图](shots/032735-wildinfusion.png)|
|16|纹身：回复说明|[截图](shots/032749-regeneration.png)|
|17|痛苦压制状态提示|[截图](shots/032828-painstatus.png)|
|18|纹身饱和状态提示|[截图](shots/032834-infusionsaturation.png)|
|19|招架状态提示|[截图](shots/032904-runesaturation.png)|
|20|符文饱和状态提示|[截图](shots/032932-runesaturation-correct.png)|
|21|再生状态提示|[截图](shots/033027-recovery-status.png)|
|22|影之格斗持续技能提示|[截图](shots/033103-shadowcombat-status.png)|
|23|巨狼完整观察提示|[截图](shots/033212-wolfattack.png)|
|24|行为菜单与可用技能|[截图](shots/033648-trollcontext-view.png)|
|25|物品栏、装备槽及鉴定水晶球提示|[截图](shots/033912-inventory-view.png)|
|26|铁匕首属性与武器说明|[截图](shots/033929-iron-dagger.png)|
|27|粗制皮甲属性与说明|[截图](shots/033937-leatherarmor.png)|
|28|黄铜灯属性与说明|[截图](shots/033954-brasslantern.png)|
|29|鉴定水晶球物品操作菜单|[截图](shots/034001-itemaction.png)|
|30|白色蠕虫团角色面板|[截图](shots/034352-wormsheet.png)|
|31|中毒状态提示|[截图](shots/034526-poisonstatus.png)|
|32|地面手札：残破的纸片（巨魔沼泽）全文|[截图](shots/035249-lore1-read.png)|
|33|地图面板：巨魔沼泽|[截图](shots/034900-fullmap-view.png)|
|34|附带照明术的法杖完整说明|[截图](shots/041049-inventoryloot.png)|
|35|力量之铁盔说明及重甲需求|[截图](shots/041135-helmetcomparison.png)|
|36|法杖与当前武器比较差值|[截图](shots/041219-staffcomparison.png)|
|37|护送迷路战士的求助对话、接受/拒绝选项|[截图](shots/042109-actual-level2.png)|
|38|护送任务日志目标|[截图](shots/042431-escortjournal-detail.png)|
|39|敌人卑劣攻击状态提示|[截图](shots/041751-dirty-status-read.png)|
|40|敌人震慑状态提示|[截图](shots/042825-stunned-status-read.png)|
|41|观察操作和瞄准自身确认|[截图](shots/043110-levelup-menu.png)|
|42|升级后的角色面板、资源及属性变化|[截图](shots/043327-levelup2screen.png)|
|43|二级加点面板、照明术说明与遗忘限制|[截图](shots/043724-learnt-illumination.png)|
|44|新增刻印位的提示和确认框|[截图](shots/043826-inscription-panel.png)|
|45|轻甲训练说明|[截图](shots/043924-lightarmortraining.png)|
|46|护送完成消息及六种奖励选项|[截图](shots/044532-mapreturn-run.png)|
|47|护送奖励后的致谢和活力技能说明|[截图](shots/044649-escortrewardchosen.png)|
|48|世界地图与城镇入口提示|[截图](shots/051233-derthapproach.png)|
|49|德斯草药馆商品、分类、售价及付款上限|[截图](shots/052001-shop-jewelry.png)|
|50|商店法师野性纹身完整说明|[截图](shots/052131-wildshop-tooltip.png)|
|51|尖晶石装备/强化效果说明及出售确认|[截图](shots/052252-sellgem.png)|
|52|出售后金币与金币不足购买反馈|[截图](shots/052416-buying-feedback.png)|

## 证据说明

问题原文仅采用已复核的屏幕文字，JSONL 内包含英文键和库内行号。战斗/任务消息可在本目录 `game.log` 的 `[LOG]` 行复查。地图画面中的 OCR 噪声未作为问题证据。截图文件名中个别早期标签（如 `runesaturation`、`jewelry`）是操作时的暂定名称，以本报告索引实际面板名称为准。
