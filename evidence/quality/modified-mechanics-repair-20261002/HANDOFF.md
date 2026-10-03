# 当前恢复入口

原修正包001—016及前序附属任务已完成，累计154/169个原confirmed claim、16/18包。本包已DONE_VERIFIED，准备提交；前序HEAD=937df53c。用户无关文档和其他未跟踪内容保留。持续授权至既定18包完成或真实停止条件，无push/PR/发布授权。

# 机制修正第016包

原包10条/10个原confirmed claim中，实施9条/9个claim：毒镖限定敌对单位的近战/远程命中；超载酸伤共享每目标回合内最多6次追加；静电屏障限定自己的炮台；冲撞嘲讽区分显示半径与实际单次投射；钳制不再错误要求初击命中；血链在距离达到阈值时终止；蒸汽产量按每个成功产汽目标递减70%；诱饵持续8回合；护甲电弧说明实际随机伤害及友伤。

UPSTREAM054（entry1520）保持baseline并单独留待核验。宿主追查固定版本Target.block_path与ActorProject后发现默认每段range=1；仅凭beam模式不能推出总命中人数超过工具等级。EXECUTOR独立复核DLC范围覆盖逻辑后撤回旧推论并恢复该条。原冻结输入与原报告保留，新REPAIR-INPUT-SPLIT明确9条实施范围；该holdout不计入修复完成数。范围内其他内容无需等待这一非阻断疑点。

宿主核验25处原始源码锚点及执行报告39处源码记录/39个精确摘录。LuaJIT运行实际源码片段验证酸伤80组次数/已有计数条件、蒸汽零伤害/递减/计数重置和血链距离临界条件；另运行固定引擎投射函数，在20个直线场景与中间目标反例中验证range=1执行限制。探针使用地图/FOV等桩函数，不宣称端到端游戏验证。DLC来源、commit及版本未固定，以实际公开源码SHA与精确摘录定位。

9条target的全文件反向替换恢复baseline；LuaJIT语义记录与词法字节校验均证明source/source_tag、args_order/special及范围外字节不变，placeholder/markup/newline/tab序列保持，holdout亦未变。严格proposal通过。EXECUTOR原生运行中宿主追加反证时，Paseo将进行中的provider turn中断并启动续接turn；没有续跑已结束的child。通用单turn解析器不接受该事件，宿主保存原始终态字节与完整生命周期/调用证据后单独核验；独立reviewer仍使用原有严格单次运行验收。

执行期间有一次读取当前core工作树用于查找；实际采纳的所有源码锚点均已再次由执行者和宿主从固定commit逐字核验，该工作树读取不作为裁决依据。执行报告中的“User counterevidence”实际来自ORCHESTRATOR补充侦察，并非新的用户授权。

MMR-026术语事项及UPSTREAM054 holdout继续保持独立记录。

首轮独立REVIEW/full为8 OK、1 ISSUE。宿主确认电击棒撞墙后脉冲的伤害与震慑对象是半径1内各个尚未受该次施放脉冲影响的敌人，原“震慑其”错误收窄为撞墙者；采用一条FIX明确范围内敌人及尝试震慑，并保留每敌每次施放一次的去重条件。

修正脉冲后的RE_REVIEW为8 OK、1 ISSUE，指出静电屏障末句把装备需求与伤害属性统称为“力量要求”。宿主核实该条在前后两轮source/target及固定来源身份未变，依AGENTS跨轮判定变化规则交回用户。向用户说明前轮只有裸OK，并无相反机制论证；这是有源码依据的措辞澄清，不是属性方向写反。用户在了解完整上下文后回复“同意。”，批准改为“装备盾牌时，你以灵巧代替力量满足属性需求；计算盾牌伤害时，也以灵巧代替力量。”对应USER-DECISION-STATIC-SHIELD和FIX-2保留，不追溯修改旧复审。

用户批准的静电屏障措辞已由fresh EXECUTOR落实，宿主核对6处相关源码、完整旧新target及反向字节证明；strict proposal和9条候选校验通过，holdout仍未改。cycle2 RE_REVIEW独立9 OK，原生终态/8次工具调用已核验，只读取自身冻结输入、契约与临时上下文；归档已确认。当前候选SHA对应的完整门禁通过：30308条lint零错误零警告、runtime collision 0、重复键仅A类1711/B0/C0、strict addon及真实DLC消费dry-run applied=false、空白检查通过。

cycle2 FINAL_REVIEW返回8 OK、1 ISSUE（致命诱饵）：前轮同一冻结payload的OK未发现嘲讽范围及伤害成长两处旧描述。宿主核实Taunt半径有限且反伤比例固定30，只有生命/抗性/护甲直接随蒸汽强度成长，确认该finding。按AGENTS相同revision跨轮意见变化进入WAIT_USER，拟将“所有敌人”改为“附近敌人”、末句删除“伤害”，尚未应用。7个child全部自然结束、证据已核验并确认归档。门禁通过不等于终审通过，本包未DONE、未提交。WAIT-FATAL-ATTRACTOR保留完整候选、提案及源码证据。

用户随后明确回复“采用两处修订并继续（推荐）”。fresh FIX3仅修致命诱饵该两处，宿主对23条源码记录/摘录独立核验，逐字提案与整文件逆向还原通过；9条LuaJIT语义、strict proposal及词法范围/placeholder/markup/newline/tab校验通过。该执行者11次工具调用已逐项核验并确认归档。cycle3完整9条RE_REVIEW已派发。

cycle3 RE_REVIEW为9 OK；FINAL_REVIEW为8 OK、1 ISSUE，电击棒攻击普通未命中仍尝试击退（attackTargetWith第一返回值是速度，第二才是命中）。宿主核对DLC封装及固定core返回值，确认应避免“受击目标”造成命中前提误读，拟改为“即使攻击未命中，也会尝试将范围内的敌人击退 %d 格”。reviewer“恒成立”论断收窄：core hd.stop钩子可直接中止，不能推广到所有中止/取消攻击。当前候选与前轮完全相同且cycle3=max_cycles3，进入WAIT_USER，拟请用户批准该句并前瞻增加一轮有界cycle4，尚未应用。10个child全部确认归档；本包门禁通过但终审未通过，未DONE/提交。

用户明确批准“采用修订，额外授权1轮并继续（推荐）”。SPEC/STATE前瞻max_cycles4，原始周期历史完整保留。fresh FIX4落实唯一电击棒句；宿主核验38条来源记录/摘录、完整反向字节证明，9条LuaJIT语义及strict proposal、placeholder/markup/newline/tab序列全通过。执行者11次工具调用核验后已归档；当前cycle4全量复审。

最终结果：cycle4 RE_REVIEW/full与FINAL_REVIEW/full分别9 OK、9 OK，身份de19aeb5dac2183a09a4af6db5c2f7b9659eab8d84db98191fbd77ae9ec3d915一致。终审19次工具调用核验，仅自身输入/契约/冻结源码及本会话生成的工具结果；13个child全部确认归档，无未决accepted finding。当前候选完整门禁再次通过：lint30308/零错误零警告，runtime collision0，A1711/B0/C0，strict addon和真实DLC消费dry-run applied=false，空白通过。UPSTREAM054仍为独立holdout、MMR-026术语事项保持原待决记录，不计入本批9个原claim完成数。


提交本包后按packages.json推进第017包，保留既定10条以内有界范围。 每包唯一EXECUTOR写Lua，宿主核验，冻结whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL/full、门禁、归档、DONE与提交。结束child不续跑，MCP实时profiles/author与lineage核验，canonical prompt≤800UTF8字节，raw先原样保存后严格解析。无须逐包询问。

第010包bowman同revision跨轮OK/ISSUE曾触发WAIT_USER，用户已明确回复“同意”，批准源码支持的召唤时获得技能/等级取决于当时召唤者等级的单句修订及继续；USER-DECISION-BOWMAN保留，不重复征求该决定。第009包旧task因恢复父级变化STOP_VERIFIED，同范围接续task完整DONE，证据package-009-resume，旧记录不改。第004包毒箭终审疑点已被用户撤销，不重开。MMR-026共享术语决定仍待既有答复，不重复问、不扩大术语/全局策略授权。

收束状态校验首次发现宿主将历史含ISSUE审核统一标记为completed，导致旧终审被误判为成功终审。已按实际raw结果校正四份宿主review record为completed_with_findings，原始raw与冻结input未改；前后值记录在HOST-RECORD-STATUS-CORRECTION.json。重新校验已DONE_VERIFIED。累计16/18包、154/169个原claim完成；本包9条完成，一条UPSTREAM054独立holdout未计完成。

当前既有决定均已执行：静电屏障措辞、致命诱饵范围/成长、电击棒未命中击退及额外cycle4。不得重问这些决定。UPSTREAM054保持holdout，详见根目录HOLDOUT-UPSTREAM054.json。
