# 初审冻结后的旧裁决揭示与规则澄清

这是第二阶段输入，不是盲审。先前答复摘要已保存于 INITIAL-OBSERVATIONS.json；其SHA-256为 cfed9e90d9267425aa1cc135538510c3cc99c6605187ed2b436ace5cdf5bb390。不得将二阶段结果计作新测试集准确率。

## 本轮规则澄清

主代理在首轮包中附入完整TERMINOLOGY.md，却漏重申原实验INPUT的专门排版规则。这是宿主包装冲突，不能算作模型误报能力的证据。现明确：只有导致错误参数、错误显示或信息结构丢失的格式差异才算缺陷；合法排版和等价重排不算缺陷。本条优先于TERMINOLOGY.md的通用换行保留指南。请撤销仅凭换行数量变化提出的缺陷；非空后缀造成的实际病句仍须独立审查。

术语scope定义保持首轮规则，未获授权修改。DLC目标版本缺口只影响依赖该版本才能下结论的claim，不应把所有纯文本条目一律判PENDING。K10中文名映射已从合并邻文补齐，但源码支持的上游纠正对目标版本是否适用应单列残余缺口。

## 原裁决（供比较，不是答案）

### K01 / entry-03620

原条目状态：ISSUE；D03：适用机制术语。“力量”分支标签及无类型限定的“伤害”不足以另立机制缺陷。

- G12-D03: **适用术语偏差。**`global speed` 译为“整体速度”；冻结术语中匹配 `tformat`、全局行动速度机制的 preferred 行明确要求“全局速度”。`S/data/talents/misc/misc.lua:247,258` → `S/data/timed_effects.lua:2219` 写入 `global_speed_add`。

### K02 / entry-03714

原条目状态：ISSUE；D07：全部伤害的明确范围遗漏

- G14-D07: 翻译新增遗漏：`all their damage` 只剩“伤害”，失去明确的全范围限定；不据此声称译文限定为物理伤害。orc:115、125；本体 talents/misc/races:731 → timed_effects/mental:2007 的 `inc_damage={all=eff.power}`。

### K03 / entry-03627

原条目状态：ISSUE；D08、D09；另有 P03。

- G12-D08: **首次对象的选取条件改变。**`first creature hit` 变为“攻击的第一个生物”。主句虽保留造成伤害条件，括号仍可能把首次攻击但未命中的对象算作首个对象。`S/data/talents/misc/races.lua:205–209`；`S/data/timed_effects.lua:1945–1953` 在正伤害回调内处理首次触发。
- G12-D09: **补充漏项：对象范围收窄。**`can only stun a creature once per turn` 译为“每个敌人……一次”，将生物范围收窄为敌人。`S/data/talents/misc/races.lua:207`；`S/data/timed_effects.lua:1945–1953` 按 `target.uid` 限制，未在此检查敌对关系。

### K04 / entry-03729

原条目状态：ISSUE；D08–D11；另有 P02、P03

- G14-D08: 翻译新增缩窄：`lumps of metal` 变成“铁块”。aaf:47；APE:28–29 同样泛称金属及矿块。无需依赖具体各级材料名称即可确认。
- G14-D09: 翻译新增泛化：材料语境的 `herbs` 变成“植物”，丢失草药类别。aaf:47；Actor:304–308 为辅助快照证据。
- G14-D10: 翻译新增遗漏：`which are used to craft tinkers` 无对应译文。aaf:47；APE:29、PartyTinker:81–83、114–117 辅助说明制造材料的用途与消费。
- G14-D11: 翻译新增遗漏：未说明在 `when you destroy items` 的操作中选择处理工具。aaf:49 的加粗说明；前句介绍分解用途不等于保留这一操作适用条件。

### K05 / entry-03605

原条目状态：ISSUE；D13、D14；另有 P12、P13、P14

- G11-D13: **翻译新增的条件拼接语病**：非空后缀时，宿主和 entry-03606 拼成“你的触手当前属性为 ，由于副手非空，该技能暂时被禁用：〔属性列表〕”。`为` 后插入完整禁用分句，破坏属性引导句。`S/tentacles.lua:69–80`。空后缀时“属性为：〔列表〕”成立，不将该状态判错。
- G11-D14: **翻译新增的人群限定变化**：带引号的 `civilized people` 变为“普通人”，把文明社会身份改为普通／特殊之分；后面的遮掩恐魔外貌没有补回这一限定。`S/tentacles.lua:76` 及本条完整叙事语境。

### K06 / entry-03689

原条目状态：ISSUE；D17、D18；另有 P07、P08：借代术语与抗性描述范围。

- G13-D17: 遗漏 `while they are magic users` 的让步条件。`S/overload/data/texts/unlock-race_krog.lua:22–24`：符文维生背景仍在，但“尽管使用魔法，教团仍同情他们”的关系未保留。
- G13-D18: `A mastery of infusions like no others` 的独有比较程度被缩为“自然纹身的大师”。`S/overload/data/texts/unlock-race_krog.lua:33`：“大师”表达高超，未表达“其他人无法相比”。这是轻微的语义信息遗漏。

### K07 / entry-03692

原条目状态：OK；整段明确保留浮动概率；没有证实“必然触发”误述。


### K08 / entry-03595

原条目状态：ISSUE；D08；另有 P18

- G11-D08: **翻译新增的触发事件信息损失**：`applied or increased` 被概括为“受到熵能反冲”，没有区分效果新增／增强与既有效果逐回合造成伤害。`S/oblivion.lua:58`；`A/data/timed_effects.lua:803–818` 在激活、合并时调用 `do_nihil`，`:827–842` 的伤害结算没有该调用。

### K09 / entry-03596

原条目状态：ISSUE；D09，独立复核补充

- G11-D09: **独立补充；翻译新增的范围信息遗漏**：`radius 2 explosion` 变为“2 码的虚空爆炸”，丢失半径这一度量关系。`S/oblivion.lua:311–314、337`。附加的“暗影时空各 50%”有 `E/data/damage_types.lua:2864–2869` 支持，不列缺陷。

### K10 / entry-03646

原条目状态：PENDING；P07：伤害调用链支持 Sanity Warp 分支，但缺中文名称映射和目标版本证据。


## 二阶段输出请求

只读已授权盲审材料及本文件，不读其他代理报告。返回恰好10行修订状态表，再简述：与旧裁决相比哪些保留、哪些改变以及改变来自规则澄清、新证据还是语言裁定。重点给出K03首次对象／敌人范围、K05文明人／普通人及方位、K08触发语句的最强正反证；无法排除的解释保留pending，不为与他人一致而硬判。全文约2500中文字符；无需重抄全部源码路径。不要修改文件。
