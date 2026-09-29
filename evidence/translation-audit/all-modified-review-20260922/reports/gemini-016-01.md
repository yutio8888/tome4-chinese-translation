### batch-016 译文复核报告

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-016.md`
- **文件 SHA-256 核验**：`f34eeedb2968039c0628792d3ab4c25de6689062a2705bb61b45e89a093c3dba`（已核验一致）
- **源码基线**：公开源码 `t-engine4` 固定 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4)；本批条目全部归属 `mod-tome` 模块。
- **条目范围**：`entry-00601` 至 `entry-00640`，共 40 条，已全部逐条覆盖。

---

### 逐条复核记录

#### entry-00601
- **位置**：mod-tome.lua:5894（`mod-tome/data/chats/shertul-fortress-butler.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应管家对话选项 `{_t"I have come upon a strange thing indeed. #LIGHT_GREEN#[tell him about Melinda]", jump="cure-melinda", ...}`。夏·图尔管家为远古构装生物，译文将代词转指为“告诉它梅琳达的事”符合语境；专有名词“梅琳达”（Melinda）符合术语库；`#LIGHT_GREEN#` 颜色标记与方括号格式完整保留。

#### entry-00602
- **位置**：mod-tome.lua:5934（`mod-tome/data/chats/shertul-fortress-butler.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应管家介绍堡垒功能的长对话。术语“弑神者”（Godslayers）、“探索用远行传送门”（exploratory farportal）、“转化之盒”（Transmogrification Chest）均严格匹配术语库 preferred 规范；“emergency containment field”（紧急遏制力场）、“remote storage”（远程储藏）、“power core”（能量核心）翻译准确；省略号与破折号转换规范，段落结构 1:1 对齐。

#### entry-00603
- **位置**：mod-tome.lua:5949（`mod-tome/data/chats/shertul-fortress-butler.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应探索远行传送门开启说明。术语“夏·图尔”（Sher'tuls）、“探索用远行传送门”（exploratory farportal）、“回归之杖”（rod of recall）严格匹配术语库 preferred 规范；45 点能量消耗数值准确；4 段说明层层对应，标点与警示语气准确传达。

#### entry-00604
- **位置**：mod-tome.lua:5978（`mod-tome/data/chats/shertul-fortress-butler.lua`）
- **结论**：细微观察
- **可核验依据**：源码为管家全息投影更换选项 `{_t"Can you try for a human female appearance please?", ...}`。原文为礼貌疑问句，译文“请试着变成人类女性的外形？”将祈使词“请”与句末问号混用，略显翻译腔（中文更习惯“你能试着变成人类女性的外形吗？”或“请试着变成人类女性的外形吧”），但选项意图明确，不影响玩家理解。

#### entry-00605
- **位置**：mod-tome.lua:5979（`mod-tome/data/chats/shertul-fortress-butler.lua`）
- **结论**：细微观察
- **可核验依据**：源码为管家全息投影更换选项 `{_t"Can you try for a human male appearance please?", ...}`。同 entry-00604，译文“请试着变成人类男性的外形？”祈使与问号混用略带生硬，但语义清楚无歧义。

#### entry-00606
- **位置**：mod-tome.lua:5994（`mod-tome/data/chats/shertul-fortress-caldizar.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为卡尔蒂扎尔（Caldizar）发现玩家持有吸收之杖时的惊怒对话。样式标记 `#{normal}#` 与 `#{italic}#` 位置和闭合与源码完全一致；截断句 `"How di-"` 译为 `"你怎——"` 符合中文标点习惯；“staff”（法杖）符合术语库；语气强烈逼真。

#### entry-00607
- **位置**：mod-tome.lua:6006（`mod-tome/data/chats/shertul-fortress-caldizar.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为被卡尔蒂扎尔轰飞并抹去记忆后的过场文字。前后 `#{italic}#` 与 `#{normal}#` 样式标签闭合无误；“farportal”（远行传送门）符合规范；叙事文学性优秀，破折号与分号运用规范。

#### entry-00608
- **位置**：mod-tome.lua:6122（`mod-tome/data/chats/sorcerer-end.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应堕落日曜使者（Distant Sun patron）结局对话。唯一格式化占位符 `%s`（传入大写玩家名 `p.name:upper()`）保留完好；叙述块标记 `<<<...>>>` 分布位置完全对应；颜色控制标签 `#YELLOW#`、`#CRIMSON#` 与 `#LAST#` 均准确对齐；尾部换行完全匹配。

#### entry-00609
- **位置**：mod-tome.lua:6142（`mod-tome/data/chats/sorcerer-end.lua`）
- **结论**：未发现问题
- **可核验依据**：源码调用 `player:die(player, {special_death_msg=("sacrificing %s to bring the fiery wrath of the Distant Sun"):tformat(string.his_her_self(player))})`。占位符 `%s` 接收玩家自称代词（如“他自己”/“自己”），传入 `PartyDeath.lua` 拼接为特殊死因描述；译文“牺牲了%s，引来遥远太阳炽烈的怒火”语序通顺，参数类型与位置正确。

#### entry-00610
- **位置**：mod-tome.lua:6167（`mod-tome/data/chats/sorcerer-end.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为夺心魔族通关献祭结局长对话。首三行 `#LIGHT_GREEN#*...*#WHITE#` 旁白标签完全对齐；第四行占位符 `%s`（传入 `_t"sister"` 或 `_t"brother"`）位置恰当；术语“维网”（The Way）、“夺心魔”（yeek）、“埃亚尔”（Eyal）、“远行传送门”（farportals）均严格匹配术语库规范；末尾换行格式一致。

#### entry-00611
- **位置**：mod-tome.lua:6202（`mod-tome/data/chats/sorcerer-end.lua`）
- **结论**：未发现问题
- **可核验依据**：源码调用 `special_death_msg=("sacrificing %s to stop the Way"):tformat(string.his_her_self(player))`。占位符 `%s` 接收反身代词，术语“维网”（The Way）准确；代入死因描述通顺无误。

#### entry-00612
- **位置**：mod-tome.lua:6212（`mod-tome/data/chats/sorcerer-end.lua`）
- **结论**：未发现问题
- **可核验依据**：源码调用 `special_death_msg=("sacrificing %s for the sake of the world"):tformat(string.his_her_self(player))`。占位符 `%s` 接收反身代词，代入死因日志为“为了世界牺牲了自己”，语义准确自然。

#### entry-00613
- **位置**：mod-tome.lua:6282（`mod-tome/data/chats/tannen.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应向坦能出示笔记的选项 `{_t"I do. [Show him Zemekkys's scribbled notes]", jump="east_portal3"}`。人名“泽梅基斯”（Zemekkys）一致，动作方括号完整。

#### entry-00614
- **位置**：mod-tome.lua:6283（`mod-tome/data/chats/tannen.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应坦能阅读笔记后的回应。旁白标签 `#LIGHT_GREEN#*...*#WHITE#` 匹配；术语“血符仪式匕首”（Blood-Runed Athame）严格遵循 preferred 规范，“共鸣钻石”（Resonating Diamond）一致；句意准确连贯。

#### entry-00615
- **位置**：mod-tome.lua:6287（`mod-tome/data/chats/tannen.lua`）
- **结论**：细微观察
- **可核验依据**：源码为坦能借走多元水晶球的台词。术语“多元水晶球”（Orb of Many Ways）与“时空法师泽梅基斯”（Chronomancer Zemekkys）翻译准确。首句将 "hold onto the Orb of Many Ways while you search" 意译扩充为“暂时保管多元水晶球并加以研究”，与后句“如果我要重复他的工作我必须得花些时间研究这些内容”在相邻句之间产生了“研究”的轻微词义重复，但剧情表达准确，不构成机制或理解障碍。

#### entry-00616
- **位置**：mod-tome.lua:6295（`mod-tome/data/chats/tannen.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为交付道具后的告别选项 `{_t"Thank you, and farewell."}`。译文“谢谢，再见。”简洁准确。

#### entry-00617
- **位置**：mod-tome.lua:6305（`mod-tome/data/chats/tannen.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为坦能交托钥匙探索泰尔玛废墟任务。术语“肖尔塔”（Sholtar）严格遵循 2026-08-25 裁定统一规范；地名“泰尔玛”（Telmur）一致；旁白标签 `#LIGHT_GREEN#*...*#WHITE#` 完好；书名号《反转与复原概率场》符合中文规范。

#### entry-00618
- **位置**：mod-tome.lua:6383（`mod-tome/data/chats/the-master-resurrect.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应恐惧王座主宰（The Master）被击败后复活的嘲讽台词。旁白标签 `#LIGHT_GREEN#*...*#WHITE#` 完好；称谓“领主”（The Master）与全篇恐惧王座语境统一；换行一致。

#### entry-00619
- **位置**：mod-tome.lua:6392（`mod-tome/data/chats/trap-priming.lua`）
- **结论**：未发现问题
- **可核验依据**：源码调用 `game.logPlayer(player, "#LIGHT_BLUE#You cannot prepare this trap: %s.", unlearnable)`。颜色标签 `#LIGHT_BLUE#` 保留，格式化占位符 `%s` 接收未满足条件的说明文本；冒号与句号标点正确。

#### entry-00620
- **位置**：mod-tome.lua:6417（`mod-tome/data/chats/tutorial-start.lua`）
- **结论**：细微观察
- **可核验依据**：源码为新手教程完成后的引导总结长文本。首部换行与段落布局完全一致；四处按键与提示颜色标记 `#GOLD#...#WHITE#` 准确无误；“Esc 键”、“保存并退出”、“埃亚尔”等表述通畅。文本中“玩的开心”宜作“玩得开心”，“勇敢的前进”宜作“勇敢地前进”（助词“得/地”使用规范），属于极细微文字观察，不影响阅读。

#### entry-00621
- **位置**：mod-tome.lua:6472（`mod-tome/data/chats/ukllmswwik.lua`）
- **结论**：细微观察
- **可核验依据**：源码为面对水龙乌克鲁姆斯维克提供单向传送门时的拒绝选项（选择后造物之殿任务失败）。原文 "death trap"（致命陷阱/送命的陷阱/绝路）译文简化为“这是个陷阱！再见。”，语气略有弱化，但该选项的功能与态度表达依然明确。

#### entry-00622
- **位置**：mod-tome.lua:6535（`mod-tome/data/chats/unremarkable-cave-bosses.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应平平无奇的洞穴中菲拉瑞尔与克罗加尔对峙场景。对话中两次出现的种族占位变量 `@playerdescriptor.race@` 均完好保留且位置对应；旁白标签 `#LIGHT_GREEN#*...*#WHITE#` 匹配；引号与角色对话格式严谨；兽人粗口“wench”译为“臭婊子”符合角色性格。

#### entry-00623
- **位置**：mod-tome.lua:6557（`mod-tome/data/chats/unremarkable-cave-fillarel.lua`）
- **结论**：存在疑点
- **可核验依据**：源码原文为 `"It was my pleasure. But may I ask a favor myself? I am not from these lands. I used a farportal guarded by orcs deep below the Iron Throne and was brought here."`。
译文为：“我的荣幸，不过我有个请求。我其实不是这个大陆的人，使用了钢铁王座地下深处，被兽人保护的远行传送门，然后就到了这里。”
在 ToME4 剧情中，雷克诺尔（Reknor）深处被兽人重兵占据，远行传送门是由敌对兽人士兵“把守/守卫/看守”（guarded by orcs），玩家一路厮杀突破方能启动。译文将 "guarded by orcs" 译作“被兽人保护的”，中文“保护”带有善意维护色彩，与兽人设伏把守关隘的剧情设定相悖，存在词义误导，宜校订为“由兽人把守的远行传送门”或“被兽人守卫的远行传送门”。

#### entry-00624
- **位置**：mod-tome.lua:6689（`mod-tome/data/chats/zemekkys.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应泽梅基斯解释共鸣钻石成因的对话。人名“布莱亚”（Briagh）、生物“巨型沙龙”（Great Sand Wyrm）、术语“共鸣钻石”（Resonating Diamonds）均准确对应；“infused with his life rhythms”译为“灌注了生命节律”形象贴切。

#### entry-00625
- **位置**：mod-tome.lua:6715（`mod-tome/data/chats/zigur-mindstar-store.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应齐格尔灵念星核商店训练选项，执行代码为 `player:setTalentTypeMastery("wild-gift/mindstar-mastery", player:getTalentTypeMastery("wild-gift/mindstar-mastery", true) + 0.2)`。源码中实际增加的是技能树专精系数（talent type mastery），译文“增加技能树系数0.2”完全贴合底层机制，数值 0.2 与 750 金币准确无误。

#### entry-00626
- **位置**：mod-tome.lua:6727（`mod-tome/data/chats/zigur-trainer.lua`）
- **结论**：未发现问题
- **可核验依据**：源码为反魔入教剥离奥术装备时的日志 `game.logPlayer(player, "You cannot use your %s anymore; it is tainted by magic.", o:getName{do_color=true})`。占位符 `%s` 保留，指代被卸下的奥术物品；句意与机制准确。

#### entry-00627
- **位置**：mod-tome.lua:6744（`mod-tome/data/chats/zigur-trainer.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应玩家角色等级低于 10 级时尝试接取反魔任务的拒绝台词（`cond=function(npc, player) return player.level < 10 end`）。译文“你似乎跃跃欲试，但或许还太稚嫩。等你再成长一些再来吧”语气契合原义。

#### entry-00628
- **位置**：mod-tome.lua:6791（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应黑暗潜行增伤日志（`damage_types.lua:271`）：`game:delayedLogMessage(source, target, "dark_strike"..(source.uid or ""), "#Source# strikes #Target# in the darkness (%+d%%%%%%%% damage).", dark.damageIncrease)`。注意源码注释特别标注 `-- resolve %% 3 levels deep`，因此必须包含 8 个 `%` 转义符号；译文精准保持了 `%+d%%%%%%%%`，标签 `#Source#` 与 `#Target#` 无损保留。

#### entry-00629
- **位置**：mod-tome.lua:6794（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应灵能盾伤害吸收日志（`damage_types.lua:406`）：`("%s(%d to psi shield)#LAST#"):tformat(DamageType:get(type).text_color or "#aaaaaa#", lastdam-dam)`。格式化参数 `%s`（伤害颜色）与 `%d`（吸收量）顺序与数量正确，尾部 `#LAST#` 标签完整。

#### entry-00630
- **位置**：mod-tome.lua:6802（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码对应伤害反射消息（`damage_types.lua:574`）：`game:delayedLogMessage(target, src, "reflect_damage"..(src.uid or ""), "#CRIMSON##Source# reflects damage back to #Target#!")`。颜色 `#CRIMSON#`、发起方 `#Source#` 和目标 `#Target#` 保留无误。

#### entry-00631
- **位置**：mod-tome.lua:6808（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码位于物理伤害类型（DamageType.PHYSICAL）的 `death_message` 数组。消费逻辑见 `PartyDeath.lua:111`，模板为 `"%s the level %d %s %s was %s to death by %s..."`，中文模板为 `“玩家%s等级%d%s%s%s而死，杀死他（她）的是%s……”`。代入后为“受到钝击而死”，语法顺畅。

#### entry-00632
- **位置**：mod-tome.lua:6809（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码同属物理伤害 `death_message` 数组。代入死亡模板后为“被切开而死”，准确对应 "sliced"。

#### entry-00633
- **位置**：mod-tome.lua:6815（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码同属物理伤害 `death_message` 数组。代入死亡模板后为“被开膛破肚而死”，生动准确对应 "disembowelled"。

#### entry-00634
- **位置**：mod-tome.lua:6817（`mod-tome/data/damage_types.lua`）
- **结论**：细微观察
- **可核验依据**：源码同属物理伤害 `death_message` 数组。原文为 "stabbed"（被刺/被扎），译为“被刺杀”。代入死亡模板（`%s而死`）时会产生“被刺杀而死”的微量语意重叠（“刺杀”已包含致死语义），若译为“被刺”或“被刺伤”在组合时更为严谨，但当前译文仍可清晰传达死因。

#### entry-00635
- **位置**：mod-tome.lua:6818（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码同属物理伤害 `death_message` 数组。代入死亡模板后为“被刺穿而死”，准确对应 "pierced"。

#### entry-00636
- **位置**：mod-tome.lua:6821（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码同属物理伤害 `death_message` 数组。代入死亡模板后为“被击碎而死”，准确对应 "shattered"。

#### entry-00637
- **位置**：mod-tome.lua:6824（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码同属物理伤害 `death_message` 数组。代入死亡模板后为“被横扫而死”，准确对应 "swiped"。

#### entry-00638
- **位置**：mod-tome.lua:6889（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码位于光系伤害类型（DamageType.LIGHT）的 `death_message` 数组（`damage_types.lua:916`）。代入死亡模板后为“被净化而死”，准确对应 "purified"。

#### entry-00639
- **位置**：mod-tome.lua:6894（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码位于暗影伤害类型（DamageType.DARKNESS）的 `death_message` 数组（`damage_types.lua:923`）。代入死亡模板后为“被阴影笼罩而死”，准确对应 "shadowed"。

#### entry-00640
- **位置**：mod-tome.lua:6907（`mod-tome/data/damage_types.lua`）
- **结论**：未发现问题
- **可核验依据**：源码位于时空伤害类型（DamageType.TEMPORAL）的 `death_message` 数组（`damage_types.lua:1006`）。代入死亡模板后为“被一个时间克隆体取代（其他人均不会感到任何差别）而死”，契合 ToME4 时空系伤害黑色幽默风味的彩蛋死因，括号完整，翻译准确。

---

### 汇总清单

- **存在疑点（1 条）**：
  - `entry-00623`："guarded by orcs" 译作“被兽人保护的”，在剧情中兽人为把守/看守远行传送门的敌方阻碍，用词带有褒义偏离，宜订正为“把守/守卫”。
- **细微观察（6 条）**：
  - `entry-00604`：礼貌疑问句译为“请……？”，祈使问号混用略显生硬。
  - `entry-00605`：同 entry-00604，祈使与问号混用。
  - `entry-00615`：前句增译“并加以研究”，与后句“花些时间研究这些内容”有轻微词义重复。
  - `entry-00620`：“玩的开心”宜为“玩得开心”，“勇敢的前进”宜为“勇敢地前进”。
  - `entry-00621`："death trap" 简化为“陷阱”，语气略有弱化。
  - `entry-00634`：`stabbed` 译为“被刺杀”，代入模板呈现为“被刺杀而死”，略带语义冗余。
- **未发现问题（33 条）**：
  - `entry-00601`、`entry-00602`、`entry-00603`、`entry-00606`、`entry-00607`、`entry-00608`、`entry-00609`、`entry-00610`、`entry-00611`、`entry-00612`、`entry-00613`、`entry-00614`、`entry-00616`、`entry-00617`、`entry-00618`、`entry-00619`、`entry-00622`、`entry-00624`、`entry-00625`、`entry-00626`、`entry-00627`、`entry-00628`、`entry-00629`、`entry-00630`、`entry-00631`、`entry-00632`、`entry-00633`、`entry-00635`、`entry-00636`、`entry-00637`、`entry-00638`、`entry-00639`、`entry-00640`。