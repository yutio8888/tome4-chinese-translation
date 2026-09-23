---

## rem-13 只读交叉审核报告

已核对冻结批次的 **20 条译文、C01–C07 全部疑点**，以及对应的上下文、术语和公开 DLC 源码。结论：**4 项 confirmed、3 项 advisory；无 pending 或新增译文问题。** 以下结论只适用于本次冻结材料，未作修改。

下文证据路径以仓库根目录为起点：

- `S`＝`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
- `D`＝`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data`
- `T`＝`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`

### C01 | entry-03939 | advisory

原译“`%s抵抗了震慑打击！`”与紧邻的 *stunning blow* 共用“打击”，未体现此处 *shock* 是扩散冲击。最强等价读法是两句都在报告抵抗震慑，玩家仍能理解结果；故仅建议改为“震慑冲击”。证据：`S:5183–5195`；`D/talents/steam/heavy-weapons.lua:720–738`。

### C02 | entry-03940 | confirmed

原译“`%s击中了某物`”容易读成主动击打，且丢失 *solid*。这里 `%s` 是被击退后撞上障碍物的目标。最强等价读法是“击中”也可宽泛表示碰撞，但在该战斗日志中仍不足以交代撞墙情境。建议“`%s撞上了坚固的物体`”。证据：`S:5208–5217`；`D/talents/steam/heavy-weapons.lua:965–990`。

### C03 | entry-03946 | advisory

原译“`所有技能冷却时间减半`”可通俗表达冷却更快；源码实际是在驾驶效果期间每回合额外减少一次冷却值，并跳过 `fixed_cooldown` 技能，不是改写基础冷却时间。为避免误读，建议“技能冷却速度加快一倍”。英文自身的 *all* 也比实现宽泛，不把这部分算作中文新增错误。证据：`S:5318–5320`；`D/talents/steam/mecharachnid.lua:690–700`；`D/timed_effects/other.lua:442–452`。

### C04 | entry-03950 | confirmed

原译“`使用灵晶射击`”未沿用同节技能名“金属灵晶”；“`与灵晶碎片建立……联系`”遗漏碎片仍留在目标体内；“`范围（当前 %d）的两倍`”又把已经乘二的显示值写成还需再乘二。等价读法可把“灵晶射击”理解为动作描述，却无法消除后两处信息损失。建议按“发射金属灵晶”“残留在目标体内的碎片”“两倍半径（当前 %d 格）”改写。证据：`S:5369–5381`；`D/talents/steam/mechstar.lua:22–45,64–81`。另须区分源码行为：状态在距离**达到**阈值时即断开，而英文及中文都写“超过”；这是沿袭英文的机制描述问题，不计中文新增错译。证据：`D/timed_effects/physical.lua:742–750`。

### C05 | entry-03951 | advisory

原译“`制造药剂、附着物等道具`”以例子解释 *tinkers*，没有必然错误；但它将类别名改成不完整的举例。冻结术语记录为“蒸汽工具”，状态是 `existing`，不强制统一。建议如需明确类别，写“制造蒸汽工具”。证据：`S:5402–5403`；`D/talents/steam/other.lua:125–142`；`T:1521`。

### C06 | entry-03953 | confirmed

原译“`射击是远程攻击将会触发弹药特效`”遗漏 *melee*，使特殊的远程近战攻击看似普通远程攻击，也抹去了“虽属近战攻击，仍触发弹药远程特效”的转折。建议明确写“远程近战攻击，但也会触发弹药的远程特效”。原译“沃瑞钽钢”也与本次 `preferred` 术语“沃瑞钽”不符，可在同条修正。证据：`S:5414–5417`；`D/talents/steam/other.lua:332–360`；`T:1609`。源码按技能等级决定额外射击，英文却称由沃瑞钽材质决定；中文沿袭英文，此机制不一致**不计中文新增错误**。证据：`D/talents/steam/other.lua:315–320,344–359`。

### C07 | entry-03960 | confirmed

原译“`修复机械生物`”漏掉 *other*。最强等价读法是读者会从施法语境推知治疗别人，但文字仍未排除自身；源码明确要求 `act ~= self`。建议“修复**其他**机械生物”。证据：`S:5482–5485`；`D/talents/steam/other.lua:839–840,853–864,907–912`。

### 完整条目映射

| Entry ID | 判定 | 依据 |
| --- | --- | --- |
| entry-03939 | 仅建议 | C01 |
| entry-03940 | 存在问题 | C02 |
| entry-03941 | 未发现问题 | 名称与相邻蒸汽产生说明相符；`S:5225–5228` |
| entry-03942 | 未发现问题 | 击碎投射物及占位符相符；`S:5245–5250`，`D/talents/steam/magnetism.lua:96–103` |
| entry-03943 | 未发现问题 | 链接召唤者语义相符；`S:5274–5275`，`D/talents/steam/mecharachnid.lua:68–79` |
| entry-03944 | 未发现问题 | 自爆、范围、主人死亡条件相符；`S:5276–5279`，`D/talents/steam/mecharachnid.lua:81–107` |
| entry-03946 | 仅建议 | C03 |
| entry-03949 | 未发现问题 | 负生命存活与修复期限制未见新增偏差；`S:5338–5341` |
| entry-03950 | 存在问题 | C04 |
| entry-03951 | 仅建议 | C05 |
| entry-03952 | 未发现问题 | 无弹药提示相符；`S:5415`，`D/talents/steam/other.lua:349–351` |
| entry-03953 | 存在问题 | C06 |
| entry-03954 | 未发现问题 | 召唤空间不足提示相符；`S:5419` |
| entry-03956 | 未发现问题 | 碾压、定身及数值占位符相符；`S:5435–5441` |
| entry-03957 | 未发现问题 | 拉近、伤害、命中后定身相符；`S:5442–5444` |
| entry-03958 | 未发现问题 | 锥形伤害、疾病几率与属性三选一相符；`S:5469–5474` |
| entry-03959 | 未发现问题 | “挖开沙墙”可表达穿碎沙墙；`S:5475–5477` |
| entry-03960 | 存在问题 | C07 |
| entry-03961 | 未发现问题 | 技能名称相符；`S:5486–5489` |
| entry-03963 | 未发现问题 | 致盲范围、时长和蒸汽强度相符；`S:5506–5512` |

**实际读取范围与版本限制：**读取了指定入口、`RULES.md`、`batches/rem-13.md`、`reports/gemini-rem-13.md`、`source-access.json`、`terms.json`、本批涉及的 `snapshots/tome-orcs.lua` 同节上下文，以及 `D` 下相关的 `heavy-weapons.lua`、`inscriptions.lua`、`magnetism.lua`、`mecharachnid.lua`、`mechstar.lua`、`other.lua`、`timed_effects/other.lua`、`timed_effects/physical.lua`。上述八个 DLC 文件的 SHA256 均与 `source-access.json` 记录匹配。**orcs DLC 的源码仓库 commit 和最终目标版本未固定**；这些判断是对冻结源码快照的核验，不能称为已核验 1.7.4 实际版本。
