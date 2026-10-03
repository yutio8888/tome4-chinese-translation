# Gemini扫描产出恢复与核对

已从原始工具记录恢复第二次Gemini运行的20条候选位置，并由主代理核对当前Lua原始文本和LuaJIT读取结果。两次运行均没有最终SCOUT JSON，但超时不等于没有产出：第二次的第91步已形成清单，第92步成功验证20/20条存在。此前“没有可交付有效结论”的说法过于绝对，现予更正。

结果：13条确认存在英文外的机制扩写或突兀解释，3条仅建议精简，4条有英文依据而排除。confirmed只指文本扩写/风格证据，不证明新增机制正确或错误；本次没有重新调查游戏代码，也没有修改译文。

扫描是对30308条记录的关键词、括注、结构差异检索及候选上下文阅读，不是逐条语义深审，也不保证没有其他问题。四个辅助文件与当前组件译文分开处理。两次child均已确认归档。

## 确认的文本扩写

|编号|位置|现象|
|---|---|---|
|SCAN-01|[tome-cults.lua:3712](../../../tome-cults.lua#L3712)|将每回合概率改写为进度、抵抗减半、阈值及扣除100而非清零的流程说明；英文无这些细节。|
|SCAN-02|[tome-cults.lua:3769](../../../tome-cults.lua#L3769)|括注一层实际降低、二层起增加以及暴击始终增加；直接在正常增益描述中追加例外。|
|SCAN-03|[tome-ashes-urhrok.lua:1287](../../../tome-ashes-urhrok.lua#L1287)|动态半径占位符后插入实际触发固定4格、不随显示数值变化的纠正式括注。|
|SCAN-04|[tome-orcs.lua:6193](../../../tome-orcs.lua#L6193)|新增半径3、宿主友好关系、未感染、抵抗以及死亡必定/每回合25%的传播过程。|
|SCAN-05|[tome-cults.lua:3728](../../../tome-cults.lua#L3728)|重复限定非其他类，并追加不影响其他类效果的括注，暴露内部分类且重复。|
|SCAN-06|[tome-cults.lua:3815](../../../tome-cults.lua#L3815)|新增其他类效果除外的分类括注。|
|SCAN-07|[tome-cults.lua:3826](../../../tome-cults.lua#L3826)|新增其他类效果除外的分类括注。|
|SCAN-08|[mod-tome.lua:27881](../../../mod-tome.lua#L27881)|意志/体质段三处括注基础值10与低于10反向效果，打断玩家说明。|
|SCAN-09|[mod-tome.lua:27892](../../../mod-tome.lua#L27892)|同一基础值10及反向效果补充重复出现。|
|SCAN-10|[mod-tome.lua:27904](../../../mod-tome.lua#L27904)|同一基础值10及反向效果补充重复出现。|
|SCAN-18|[mod-tome.lua:36547](../../../mod-tome.lua#L36547)|由随机敌人改为反击施加者，并补充来源不是生物时回退随机目标的实现分支。|
|SCAN-19|[tome-orcs.lua:6456](../../../tome-orcs.lua#L6456)|新增两把枪各自选敌、可重复选中以及被缴械，英文无这些细节。|
|SCAN-20|[tome-ashes-urhrok.lua:1497](../../../tome-ashes-urhrok.lua#L1497)|新增自然到期/吸收耗尽、敌方限定、三回合灼烧与总伤害的展开说明。|

## 仅建议精简与排除项

- SCAN-11，mod-tome.lua:3671：英文明确包含其他种族获得等级以及a class and a generic；各1点属于数量澄清，不作为生硬机制追加。
- SCAN-12，mod-tome.lua:22920：英文已有in addition to the usual increase based on Willpower，括号说明有直接依据。
- SCAN-13，mod-tome.lua:27164：否则没有衰减为中文追加理由；可压缩，但没有形成复杂机制补丁，仅advisory。
- SCAN-14，mod-tome.lua:27520：英文已有mind damage only in the second case；中文单列注打断句子，可融合，仅advisory。
- SCAN-15，mod-tome.lua:28598：英文明确写spell save rather than physical save；非物理豁免括注不是擅加说明。
- SCAN-16，mod-tome.lua:31156：英文已说不检查/触发Block冷却；冷却中仍可获得与前文重复，可精简，仅advisory。
- SCAN-17，mod-tome.lua:31356：英文明确区分已有但锁定与缺少技能树，括号组织正常，不作为追加问题。

## 与刚完成撤回的关系

全部20条均与本轮修正前提交 `bfde8c53d50b065837ff34dc08639f7dbc5816f5` 的对应target相同。因此，这些现象在刚才撤回所采用的基线中已存在，不属于该有界撤回漏掉的新改写。此次扫描扩大到了当前项目存量文本，后续若修正应单独确定范围。

## 证据

- [逐条中英对照与宿主核对](ADJUDICATION.json)
- [从工具参数恢复的20条清单](RECOVERED-CANDIDATES.json)
- [Gemini执行的候选校验命令](CANDIDATE-VERIFICATION-COMMAND.json)
- [候选存在性校验原始输出](CANDIDATE-VERIFICATION-OUTPUT.txt.gz)（gzip 保存原始字节，避免原始终端空白影响文本门禁）
- [两次原始记录核验摘要](RECOVERY-PROOF.json)

首轮无最终清单；第二轮工具参数中的候选清单是可用中间产出，不伪装成Gemini最终报告。此报告是主代理普通只读核对交付，不声称正式review contract或生产批次DONE。
