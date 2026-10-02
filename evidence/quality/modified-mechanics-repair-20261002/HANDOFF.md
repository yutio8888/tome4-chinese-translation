# 当前恢复入口

原修正包001—013及前序附属任务已完成，累计125/169个原confirmed claim、13/18包。第013包已DONE_VERIFIED并提交 `0c739d7f`；第014包尚未建task或派发。用户无关文档和其他未跟踪内容保留。持续授权至既定18包完成或真实停止条件，无push/PR/发布授权。

更新时间：2026-10-02；按用户本轮“请你更新handoff”记录当前交接。全部第013包child已确认归档，当前无运行中的EXECUTOR／REVIEWER。本轮未创建第014包；既有连续范围与停止条件保持，不从本次交接新增push、PR、发布或术语修改授权。

第013包证据：[摘要](package-013/SUMMARY.md)、[DONE验证](package-013/done-verification.txt)、[冻结状态](package-013/task/STATE.json)、[Erase消费者校准](package-013/task/HOST-CONSUMER-CALIBRATION-013.json)。

# 第013包机制修正

完成10条译文及10个原始claim的核验与修正，覆盖灰烬和禁忌邪教DLC：暴击率加成的例外、毁灭者实际冷却公式及原始等级口径、恶魔使者职业描述、Jinx连续失去视线计数、疾病免疫对疯狂值获取的限制、背叛预言的累积触发、战斗中非瞬间主动法术反冲、虫群伙伴额外1回合冷却缩减、空无目标的可见性条件及Erase消费者。

Erase原finding及初始宿主探针只确认了局部减伤公式。执行者追踪调用链后提出疑点，宿主独立核验固定Actor.takeHit：伤害先结算，随后调用callbackOnDealDamage且忽略返回值。因此撤回“局部计算即实际施加减伤”的推断，译文保留显示系数并明确这项减伤未生效；按负面魔法效果数造成时空伤害仍有效。旧冻结finding和原始报告保留，当前裁决见HOST-CONSUMER-CALIBRATION-013。新LuaJIT调用片段探针9组均证明返回数值不影响已结算扣血，不宣称完整游戏集成测试。

初始执行9条修改；首次复审前fresh补完两处（Erase及毁灭者原始等级）。宿主指定的Erase补完文本遗漏ASCII空格导致strict lint一次失败，已准确归因并由另一fresh EXECUTOR仅补一个空格后通过。没有无效dispatch，也没有重置复审轮次。首次whole-workset REVIEW/full与FINAL_REVIEW/full在同一冻结identity下均10 OK，源码/角色边界审计通过，全部5个child归档确认。

29个原始锚点、19份执行报告源码文件SHA及精确摘录由宿主核验；补完涉及6份源码再次验证。核心固定commit624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC以实际文件SHA为证，但仓库来源、commit及发布版本未固定。原始消费者探针覆盖Jinx、背叛8组序列、Erase12组局部计算、反冲16组资格组合、毁灭者及伙伴冷却各5组；局部Erase探针不能证明实际减伤，其限制已明确校准。

全部target经LuaJIT字段核验、严格proposal和全文件字节遮罩/反向证明；source/source_tag/args_order/special及placeholder/markup/newline/tab和范围外字节保持。完整门禁通过：30308条译文0错误0警告、运行键冲突0、重复分类A1711/B0/C0、严格核心addon完整构建、真实DLC消费者dry-run通过且applied=false、语义claim检查和空白检查通过。未push或发布。


下一步按 [packages.json](packages.json) 推进第014包 `mmrfix-20261002-014`，10条target／10个claim，涉及 `tome-cults.lua` 和 `tome-orcs.lua`。候选索引：1194、1202、1205、1210、1228、1424、1425、1428、1431、1436。剩余第014—018包共43条target；总数169含尚待术语决定的MMR-026，不应把待决项算作已修复。 每包唯一EXECUTOR写Lua，宿主核验，冻结whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL/full、门禁、归档、DONE与提交。结束child不续跑，MCP实时profiles/author与lineage核验，canonical prompt≤800UTF8字节，raw先原样保存后严格解析。无须逐包询问。

第010包bowman同revision跨轮OK/ISSUE曾触发WAIT_USER，用户已明确回复“同意”，批准源码支持的召唤时获得技能/等级取决于当时召唤者等级的单句修订及继续；USER-DECISION-BOWMAN保留，不重复征求该决定。第009包旧task因恢复父级变化STOP_VERIFIED，同范围接续task完整DONE，证据package-009-resume，旧记录不改。第004包毒箭终审疑点已被用户撤销，不重开。MMR-026共享术语决定仍待既有答复，不重复问、不扩大术语/全局策略授权。


恢复时先核对当前 `AGENTS.md`、[范围](SCOPE.md)、[计划](PLAN.md)、[进度](progress.json)与 `packages.json`。根目录 `handoff.md` 下半部分为旧第382批生产队列历史，不将其中旧push授权或旧模型配置套用于本修正任务。若换了ORCHESTRATOR身份，已DONE的旧task保持历史，不改写其lineage；第014包用新的父级身份新建。

环境与源码：Lua 5.1／LuaJIT及LPeg0.10.2；核心工作树HEAD不同于固定commit，必须读固定Git对象或本包冻结副本。DLC路径由工具环境发现，并按组件/公开路径核对SHA，不宣称固定DLC发布版本。后续包的derived门禁脚本须覆盖实际修改的DLC文件哈希，不能只校验 `mod-tome.lua`。每次变更后保留严格proposal、字段与字节证明、完整复审和适用门禁。

用户既有改动保留：`docs/README.md`、`.ai/consult/`、两份未跟踪文档、15份旧production source-workset及 `recipe`；不要为清空工作树而修改或提交它们。当前交接维护只涉及根handoff、此handoff和progress元数据，不改第013包冻结证据。
