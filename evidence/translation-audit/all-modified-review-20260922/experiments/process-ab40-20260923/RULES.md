# 冻结审核规则
本轮为用户授权的只读研究旁路，非正式生产审核。只返回观察，不宣称 DONE_VERIFIED。不得写文件、创建子代理、读取其他报告或遍历仓库。入口中列出的 files 是唯一文字输入；source-access.json 明列的源码和已读文件明确引用的单一额外源码可读，必须核哈希；禁止替代缺失组件。

1. 审完整句段、指代及运行消费，不逐词计漏译。每项问题给精确原译短引、具体意义变化、最强上下文反证、证据位置及影响。非直译不等于错译；reasonable equivalent readings mean no confirmed defect without further evidence.
2. 术语同时核对大小写、source_tag、category/notes、status 和 scope。existing 不强制改名。global/multi 覆盖所有；dlc=ashes-urhrok,cults,items-vault,orcs,possessors；core 排除这五个；addon=addon-dev,items-vault,possessors。词形出现不证明语境匹配。使用本包 terms.json，不追读旧规则。
3. 无类型限制的“增加伤害”或“受到额外伤害”可以表达全伤害/全来源；代码 all 不要求中文逐字出现“所有”。须有实质范围变化才判错。
4. 保持参数消费、有效标记和信息结构，不机械比较空格、空行、标点和大小写强调。动态拼接检查空/非空后缀；静态渲染不等于游戏测试。
5. 用户定标的三个边界：主句已限定造成伤害时的“攻击的第一个生物”、文明人→普通人、受到熵能反冲概括施加与增强，列 needs clarification/advisory，不计确认错译；不泛化到其他不同语境。
6. 正确性与修复优先级分开。低影响但有充分证据的语义偏差仍可 confirmed；高影响猜测仍 pending。纯措辞偏好 advisory。不得因风味文字不影响机制就自动抹去明确数值、关系或事件变化。
7. 分别说明 text_status、snapshot_fact、target_applicability、impact。纯文本偏差可确认；依赖未固定 DLC 机制或目标版本的判断保留适用性缺口。忠实沿袭上游的问题单列，不算译文新增。
8. 报告没有最低问题数。OK 不等于推荐措辞。只按本轮明确证据判断，不预测其他审核者。

输出中文：先按输入顺序给完整 entry-ID | ISSUE/PENDING/OK | claim编号或简短依据 表；再列原子 C01... 观察，每项含 entry-ID、精确短引、意义变化、最强反证及处理、confirmed/pending/advisory、证据、影响与版本限制。最后列实际读取文件。记录每项影响为机制/操作、叙事事实、表达建议之一；不要把影响标签当成正确性判定。报告尽量紧凑，但不得为凑字数漏条目或证据。
