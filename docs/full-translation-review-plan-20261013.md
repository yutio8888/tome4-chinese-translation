# 面向汉化版本发布的全量复核计划

日期：2026-10-13。执行更新：2026-10-22 UTC。状态：**M3第四十阶段已闭合；有效2463A／1496B，已验证2495A／1528B；16条局部修复待执行，16条source/runtime pending不计完成。全轮、最终候选与游戏验收尚未完成**。当前证据见[执行状态](../evidence/full-review/release-20261013/STATUS.md)。

用户已明确：**以发布汉化版本为主，Engine 文本也必须输出**。主交付是包含 Engine 译文、可安装且可验证的汉化包，附简明质量说明及证据索引。推荐采用 **A 遍全量语境审读＋B 遍高风险独立复核＋修复后验收＋实际候选包验证**。包外仓库组件与长篇研究报告列为后续。Engine 已是本轮明确范围，不再作为待授权的范围扩展；当前 M2 连续执行，后续执行与外部发布按当前授权及 [AGENTS.md](../AGENTS.md) 进行。

## 1. 范围：全量审什么

[此前评估](translation-quality-assessment-20261013.md)的静态检查、定向核查和 72 条样本，不能代替新一轮全量语境覆盖。旧 WP2-Lite 的 surface OK、历史 done 和打包成功也不能折算为本轮已审。

先清点全部 11 个规范译文文件，再按实际发行链路冻结范围。以下出现次数用于清点，不直接当作发行必审分母：

| 组件 | 当前有效 `t()` 出现次数 | 本轮处理 |
| --- | ---: | --- |
| 主游戏 | 21,688 | 核心发行文本全量审读，覆盖 addon 覆盖项及官方继承项 |
| Ashes／Cults／Orcs | 849／2,043／3,904 | 三 DLC 发行文本全量审读，包含被过滤后实际继承的文本 |
| Engine | 1,061 | 发行必审与必输出：全量审核 engine.lua 及适用 copy 内容，构建并纳入实际发行产物，验证修改后的译文生效 |
| Boot | 283 | 核查官方继承及加载关系；本次明确要求输出 Engine，不据此自动扩大到 Boot 全文件输出 |
| Possessors／Items Vault | 258／69 | 现有 publish 不输出，列包外后续 |
| addon-dev／两个示例模块 | 101／26／26 | 现有 publish 不输出，列开发／示例后续 |
| **合计** | **30,308** | 每项有发行必审、包外后续或有证据的不适用去向 |

[publish.py](../tools/i18nlib/publish.py) 当前只输出核心 delta 与三 DLC overlay，读取 engine／boot 官方 locale 用于运行键过滤，尚未满足 Engine 输出要求。[manifest](../i18n/versions/tome-1.7.6.json)已为 Engine 定义 full_output，现有 [full 构建](../tools/i18nlib/build.py)可生成其完整语言资源。M1 必须将该资源接入发行组装与加载验收；不能因 addon_eligible=false 或现有 publish 不支持而排除 Engine。

分开登记“包内写入集合”与“发行功能实际使用的文本集合”。后者还包含官方继承、`.copy.lua`、动态拼接及发布仓库保留层。不能用 delta 条数代替全量，也不能只证明继承键存在而不审核发行范围内实际生效的译文。Engine 以本仓库审核后的输出为交付依据，并核对核心／DLC 同键覆盖结果。

冻结“目标源码可见文本 → 规范译文或官方继承 → 实际运行键与生效译文 → 包或运行环境”的映射。新增缺译项也进入清单；缺失当前 `t()` 不能成为漏审理由。分别统计出现次数、审核单元和运行键数。仅在 source、target、参数、来源身份及全部使用语境均等价时共享审核证据，每个出现位置仍须能回溯；同英文异 section、tag、说话者或加载环境不能直接合并。

纯格式串、已证实不可达文本可登记“不适用语言审读”，保留定位及理由；包外后续单独计数，不冒充已审。全量指上述冻结范围，不承诺绝对无错或穷尽所有游戏状态。

## 2. M0：基线、来源和可执行性探针

执行开始时完成一次有界清点：

1. 冻结工作树基线，纳入已有 [11 条修复](../evidence/translation-audit/quality-assessment-20261013/repair-notes.md)及 [P01 单条修改](../evidence/translation-audit/quality-assessment-20261013/p01-harness-repair.json)，保留用户其他改动。采用明确提交或受审计补丁，不要求清空整个工作树。
2. 核心沿用 [manifest](../i18n/versions/tome-1.7.6.json) 的 ToME 1.7.6 与 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；冻结提取器、规则、术语正文及 LuaJIT／LPeg 环境，不用本机 HEAD 替代。
3. DLC 优先核定公开来源及 commit；仍未固定时，如实保留 `unpinned`，逐文件记录实际公开源码哈希、引用和与 manifest 提取基线的对照，版本适用性未证实部分保持待确认。不默认要求取得需账号访问的分发包，不因“未固定”这一状态单独阻断已有证据支持的审读。
4. **实际基线失败须另行解决。** [已有检查](../evidence/translation-audit/quality-assessment-20261013/scope-and-checks.json)中 Ashes 提取快照与 manifest 不一致，组合命令随后停止，不能视为三 DLC 提取通过。先做有界诊断，区分环境、内容版本和基线变更；不得仅写已知限制、改 hash 或降低门禁来放行。来源缺口与具体门禁失败分开记录。
5. 做 publish dry-run、Engine full 构建与加载路径核对、运行键去向检查、隔离候选包及游戏自动化能力探针。固定源码 engine/init.lua 在引擎初始化时加载 `/data/locales/engine/<locale>.lua`，engine/Module.lua 另行加载模块及 addon locale；必须验证 Engine 资源在需要的时点生效，不假定放入 addon 后能覆盖所有引擎界面。能否启动、加载、操作并观察关键界面要实际验证；当前尚无已验证的端到端 GUI 驱动。

范围内工作可按依赖推进，不因某一组件暂缺来源停掉其他组件。M0 的进入下一阶段条件是基线与范围可追溯、发布通路已核对、已知缺口有明确处理路径；具体失败仍按适用门禁阻断其依赖项。

隔离候选包复用现有核心／DLC 发布及 Engine full 构建能力，补齐必要的发行组装：

- 选定并记录发行仓库基线 commit，用 `git archive` 将其干净树展开到本仓库 `.artifacts/i18n/release-candidate/<id>/addon/`。保存基线身份及文件清单，副本内不能残留指向正式仓库的可写链接。
- 将 `TOME_ADDON_ROOT` 设为该副本的绝对路径；按工具规则检查变化后的环境，先运行 `python3 -B tools/i18n publish`，再以相同环境运行 `python3 -B tools/i18n publish --apply`。这是本地隔离副本写入；确认目标路径后才执行，不带 `--commit`，不改正式发布仓库。
- 运行 `python3 -B tools/i18n build --profile full --component engine`，取得构建报告指定的 `full/game/engines/default/data/locales/engine/zh_hans.lua` 及哈希，连同适用 copy 内容进入隔离发行目录。默认按 addon 加 Engine 语言资源交付；M0 验证目标游戏的实际资源挂载和安装位置，M1 固化可重现的组装、安装及回退步骤，不能只把生成文件留在缓存里。
- 按 [i18n 打包说明](../i18n/README.md)在 addon 副本中使用 `zip -r -0`，使 `init.lua` 位于 `.teaa` 包根，按 `for_module-short_name.teaa` 命名。最终发行须同时包含 Engine 资源及其安装说明，单个现有 `.teaa` 不算完整交付。记录版本标记、完整文件清单、构建输入与各产物 SHA-256；保存最终被测发行包，后续分发同一字节产物。具体封装步骤在试运行中验证，当前未执行。

M0 的包是通路探针；M4 用最终译文重新生成验收候选，两者输入不同，不能互相抵数。

## 3. M1：最小覆盖记录与入口

[旧 catalog](../evidence/production-review-v2-lite/catalog/manifest.json)有 30,308 条，旧范围纳入 29,828 条；排除 480 条是旧六组件策略，非质量结论。[现有 contextual-export](../tools/i18nlib/production_review_v2_lite_batch.py)只选 `deep_required`，不能直接用来对所有历史条目重新深审。需要一个有界适配入口和可校验台账，不把通用队列平台或双遍新契约研发作为发布前提。

| 最小能力 | 验收条件 |
| --- | --- |
| 新轮覆盖表 | `round_id` 与条目 revision 分开；每项记录定位、source／target／tag／args、来源、运行去向、A 状态及 B 适用原因，旧 done 不抵数 |
| 全量语境派发 | 所有适用条目均可进入既有 `translation_contextual_v2` 的 `review_only/full`；不伪造 surface ISSUE，不重置旧队列 |
| Engine 发行接入 | 将 Engine full 产物纳入发行清单、组装和安装／回退路径，核对 copy、初始化加载时点及核心／DLC 同键优先级；缺少 Engine 产物或实际加载验证时拒绝发行完成 |
| 结果与修复映射 | 绑定精确候选、task／dispatch、raw、裁决、当前 revision；source、target、参数或相关源码变化时重审受影响项，无关术语行变化不重置全库 |
| 完成检查 | 原始、补充、排除、修复后继和最终运行键守恒；拒绝缺项、重复计数、借用旧版本及未归档 child |
| 有界恢复 | 验证中断恢复、重复导入、输入漂移、错误 hash、部分结果拒收；涉及旧消费者的改动才加相应兼容验证 |

优先用受跟踪 JSON／表格和小型适配、检查脚本，复用加载器、identity、envelope、结果验证与生命周期。人工判断和不可重生成锚点保存在 `evidence/full-review/<round_id>/`，缓存放 `.artifacts/`。离线入口和不可变 evidence 格式已在 M1 实现并经定向测试；正式 ledger 与分母由 ORCHESTRATOR 冻结，M1 初始交付时未产生生产条目覆盖，当前执行状态见本文件顶部。

共享流程、身份、证据或发布链路的行为变化，仍按[验证矩阵](agent-workflow.md#验证矩阵)执行完整门禁与相关验证，普通及高级 reviewer 独立交叉复审；角色／契约变更另加契约检查和语义核对。不为节省 B 遍成本改写现有正式批次的门禁语义。

## 4. A 全量审读与 B 定向复核

A 遍覆盖全部发行适用审核单元，读完整原译及必要语境，核对忠实与完整、中文表达、角色语气、术语、运行与呈现。B 默认覆盖：**含机制陈述、长对话／长文、A 提出 observation 的条目**；集合、判定规则与适用原因在派发前冻结。试运行按类别统计 B 独有的 confirmed 收益后，再决定是否值得向全量扩展；扩展为新的用户范围决定，不预先将成本翻倍。

每条都保留源码定位、语境和适用性结论。机制陈述逐项绑定实际源码，每个数值占位符至少记录 index 和 quantity kind，无法分类时记 unknown。涉及 damage／heal／shield、同句数值与 duration、译文新增范围／时序／触发限定、数值经过 DamageType／timed effect／projector 等运行层，或 reviewer／lint 提出 scope 冲突时，按[机制核验规则](agent-workflow.md#机制-claim-与运行时组合)建立 directional value-flow。纯标签核实实体及使用位置，无机制项不建立无用的数值链。仅找到英文字符串不算机制核验完成；深查程度可以按风险调整，逐条源码核验不能省略。

每个 A 工作集使用既有 v2 `review_only` task、单个 `full`；B 将适用项组成自己的有界 task，也使用单个 `full`。每个正式 task 完成现有闭环，不把同一门禁 receipt 挪给另一 task。A、B 使用不同 fresh child；为同一 revision 做 B 时选择不同精确模型，尽量分离 provider，按规则核验作者身份。B 不读取 A 的 raw、finding 或裁决，只收到中性冻结输入。预先已知的 B 风险项可与 A 并行；因 A observation 才纳入的 B 在 A 收获后派发。

同一 revision 的应做 A/B 完成并归档后才合并裁决、进入修复。主代理检查最强反证，将 observation 分为 `confirmed`、`pending`、`advisory`；只有 confirmed 自动修复。OK 仍需核对声明覆盖、实际读取与源码记录；收获审计包含判 OK 时实际查询的源码，长文共同未报错项仍检查主体、数量、时间、条件和因果。按 AGENTS 的重复实质分歧等停止条件处理，不以模型投票代替源码。

历史决定只转换为获授权、中性的冻结规则，不给 reviewer 灌输预期答案。[P01](../evidence/translation-audit/quality-assessment-20261013/p01-harness-repair.json)按用户指定将残片 `arness` 理解为 `harness`、译作“利用”；保持“用户裁决”属性，不宣称发现了未遮蔽原文，不据此补造其他残片。

先做约 **240 条**试运行，覆盖 Engine、核心和三 DLC、短标签、长文、机制、拼接、官方继承及过滤边界，并验证 Engine 修改从规范译文到发行资源再到游戏界面的通路。短文本建议每组 40—80 条，长文／机制 10—25 条，再按字节数、源码跨度与完整场景缩小；不凑条数。完成 A、适用 B、实际发现触发的修复闭环及恢复验证；无问题时不为凑修复演练制造改动，可用隔离测试夹具验证恢复。

记录各类别耗时、无效输出率、confirmed、B 独有发现及修复成本，再估算全轮预算。若 A 有 N 个单元、B 有 H 个，理想下限为 `ceil(N/80) + ceil(H/80)` 次 full，实际还要计入长文拆组、重试与修复复审。分母冻结前不报准确工期。合格试运行可计入本轮；协议变化只重跑受影响项。推进顺序：机制／运行拼接 → 对话长文 → 名称界面，顺序不改变 A 的全量覆盖。

## 5. 修复、证据与连续运行

正式执行采用 Paseo：主代理 ORCHESTRATOR，EXECUTOR 唯一写任务内容，REVIEWER 只读；按需用 SCOUT／SENIOR_REVIEWER。每批冻结、preflight，收获后立即归档；保留 SPEC／PLAN／SCOPE／STATE、逐条源码 workset、完整门禁、适用构建、`DONE_VERIFIED`、证据提交／finalize 与重放。完整入口已覆盖的检查不再另跑一遍。

建议完成三个 A 工作集及其适用 B，或积累 20 个可修 confirmed revision 时，在先到的安全边界开修复窗口；运行错误和会影响后续统一用词的问题可提前修。尾批也闭合。修复使用 schema 5 及以上 v2 implement，默认 `max_cycles=3`，按契约执行修复／closure 与覆盖整个工作集的 `FINAL_REVIEW/full`；修改前的 A/B 不抵修改后验收。

保持 source、source_tag、args_order、special、placeholder、markup、newline 不变量；有意结构变动单列依据与验证。严格 proposal、lint、运行键检查、术语审计及适用构建由正式门禁覆盖。已授权连续范围内直接推进，不逐批等待用户；新增高复用术语、跨批统一策略、包支持扩展等超出授权的决定才提交用户。非阻断 advisory 不开无限修复轮。

## 6. 全局与发行验收

M1 从冻结术语记录、源码实体／技能树／任务定义与运行键关系生成关系组清单，由主代理补核动态引用和同词异义后冻结。最终做有界交叉检查，覆盖清单中的名称、单位、角色称谓及技能—状态—日志—物品之间的表述关系；不增加第三遍逐条全量审读，也不把批内 FINAL_REVIEW 当成已覆盖所有跨批关系。

自动检查覆盖所有适用条目，运行用例覆盖明确列出的格式／拼接族与分支。核对实际渲染结果、参数类型、视角、颜色和换行。最终 publish dry-run、Engine full 构建、包含 Engine 的隔离候选包和生效文本映射均须通过；每个被过滤／去重项有正确继承或已修复的结果。验证 Engine 译文在引擎界面、模块启动前后及 addon 加载后仍按预期生效，安装／升级／回退不会遗漏该资源。DLC 无单组件官方基线时，使用实际适用的组合发布与来源覆盖检查，不伪造基线，不以“组合包生成成功”代替缺译核验。

游戏实测采用最小冒烟矩阵：**核心无 DLC、三个 DLC 全部启用**；单 DLC 组合仅在加载差异、明确依赖或已知问题要求时追加。用最终候选完成干净安装、启动与语言选择、角色创建、代表性技能／物品／状态／日志／对话、存读档；若声称支持旧版升级及旧档，增加一个冻结的上一公开版本升级／旧档用例。配置与场景按风险组合，不做所有项目的笛卡尔积；记录兼容边界，不承诺未测模组组合。

M0 探针证明能自动驱动和观察的场景由 AI 完成。仍不能自动实测的项目，待候选包及其余验证完成后一次性交付最小操作清单、环境与预期结果，请用户实测或明确决定是否接受“未测”的发布限制。AI 不自行豁免测试，实际失败与未测分开，已知缺陷仍按验收标准处理；“未测”不能计入通过数。

## 7. AI 自主边界与发布完成

| 类别 | 本方案中的工作 |
| --- | --- |
| 可在执行授权内连续完成 | 清点、公开源码核验、A/B 派发与裁决、常规修复、门禁、证据、隔离打包及说明文档 |
| 必须先验证环境 | DLC 对应来源与提取、候选包实际加载、游戏自动操作与界面观察、旧档测试资源；缺口不自动等同需要人工，也不假定已经具备 |
| 需要用户决定或授权 | 超出现有范围的术语／策略与支持范围、规则规定的异常停止、无法自动完成的最终冒烟或未测发布取舍、尚未授权的外部写入与发布 |

因此，方案适合 AI 长时间独立推进主体工作，**目前不能承诺从审读到游戏实测、公开发布完全无人参与**。先验证能力，实际遇到无法自行闭合的节点再一次性提出具体决定；不增加逐批人工批准。

交付安装包、支持版本／DLC 清单、安装升级回退说明、变更及已知问题、源码／许可对应关系、校验和与简明质量说明。分别公布 A 覆盖率（100% 为完成要求）、B 适用集合覆盖率（100%）、机制证据、当前 revision 验收、运行通过／失败／未测、产物覆盖及包外后续；不合成一个含义不明的总审核率。发现统计分问题组和受影响条目，按条目去重，不把发现率说成系统检出率或绝对真实错误率。

发布标准是：冻结发行范围覆盖闭合、Engine 已审核译文实际输出并纳入交付、confirmed 修复完成、无阻断性 pending、适用门禁及包验证通过、必要游戏场景已测通过（或用户明确接受相应未测限制）、所有 child 已归档、证据可从提交重放。DLC `unpinned` 如实披露；实际版本冲突、基线失败和缺译不能仅靠披露关闭。

先完成全部可本地完成的成果，再按已有授权执行或请求最终外部发布授权；正式发布仓库写入、push、PR、平台发布不由本规划自动授权。保留上一公开包及版本对应关系，发布后回下载核对同一候选哈希。长篇报告可随后整理。

## 8. 执行顺序

| 阶段 | 主要成果与转出条件 |
| --- | --- |
| M0：范围与能力 | 基线、11 组件清点、发行／包外范围、来源缺口、隔离包与游戏能力探针；已知失败有有界诊断路径 |
| M1：最小入口 | 覆盖表、派发适配、Engine 发行接入与完成检查，独立复审和适用门禁通过；能够拒绝虚假覆盖与缺少 Engine 输出的发行 |
| M2：约 240 条试运行 | A 全量、B 适用项、裁决与必要修复／恢复闭环；给出成本数据和 B 扩展建议 |
| M3：全量推进 | 连续审核与分窗修复，当前 revision 覆盖及源码证据闭合 |
| M4：发行候选 | 关系检查、自动验证、最小游戏冒烟、最终包和说明；解决剩余实质决定 |
| M5：发布 | 授权范围内外部发布、回下载验包；包外仓库复核和长报告另行推进 |

M0 提交 `74b81c8b4`，M1 提交 `299c1acd5`，首个机制切片与修正提交 `d5dd1fd85`。
M2 当前后继清单为 `evidence/full-review/release-20261013/round-v8/`；当前有效 A=243、B=137，
最终分母未冻结。旧 round-v1 至 round-v6 均为不可变前版；R7 精确迁移继承 141A/98B。此前 R6 迁移继承 107A/77B，
窗口-05 三条新 revision 按 Ashes 1／Cults 2 分组，四个独立生产 task 新增 3A/3B。
四处最小修复已 DONE_VERIFIED；旧宿主 key 漂移中止链及 fresh 收尾链证据均保留。
p08s2 图片标题及说明已新增 2A/2B，无待修；原有237单元及6条必要别名的适用A/B已齐。
历史 done 不抵本轮 A/B；下一阶段范围按当前授权另行冻结。

p09s1 已闭合：本批新增 11A/11B，确认待修 revision=0；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

p10s1-bound 已闭合：本批新增 18A/5B，确认待修 revision=2；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

窗口-06 两条成就计数说明已修复并 DONE_VERIFIED；实现复审不计生产覆盖，待 R7 精确迁移及 fresh2A/2B 后继续 p11s1。

window06r 已闭合：本批新增 2A/2B，确认待修 revision=0；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

p11s1 已闭合：本批新增 18A/5B，确认待修 revision=3；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

p12s1 已闭合：本批新增 20A/8B，确认待修 revision=2；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

p12s2 已闭合：本批新增 26A/8B，确认待修 revision=1；
源码裁决、生产 A/B 自身完整门禁、DONE／归档／导入均见本轮切片闭合证据。

窗口-07 七条 UI 译文已修复并 DONE_VERIFIED；实现复审不计生产覆盖，待 R8 精确迁移及按来源分组 fresh3A/3B 与4A/4B 后继续 p12s3～p12s5。

R8 继承207A/121B；七条修复按实际来源分为Orcs3和Engine4重新复审。旧R1～R7均冻结。

window07rorcs 已闭合：本批新增 3A/3B，确认待修 revision=0；
源码裁决、生产自身完整门禁、DONE／归档／导入均见本轮闭合证据。

window07rengine 已闭合：本批新增 4A/4B，确认待修 revision=0；
源码裁决、生产自身完整门禁、DONE／归档／导入均见本轮闭合证据。

p12s3 已闭合：本批新增 9A/2B，确认待修 revision=0；
源码裁决、生产自身完整门禁、DONE／归档／导入均见本轮闭合证据。

2026-10-15保留指定GPT6.1Sol后恢复成功，补齐七条B并新增7A/7B；两组各自完整门禁、DONE、归档、导入与源码裁决已闭合。原13条独立合并A不重复计数。本次不扩展B或进入无界M3。见[恢复与M2审读闭合](../evidence/full-review/release-20261013/m2/checkpoints/20261015-sol-recovery-01/REPORT.md)；先前429和成本记录保留。

三个 DLC 的 inner-root 配置更正后均精确通过原 manifest 提取基线（999/2444/4493），
旧“无法归因／需旧快照／停止 DLC”诊断已撤回，来源 commit 仍 unpinned。
隔离官方 1.7.6 的 prototype Engine 早期 locale、CJK 标题和精确回退能力已核验，
不计最终候选或三 DLC 玩法验收；M4 仍须实际加载最终候选。

从当前版本恢复：`python3 -B tools/full_review.py check --directory evidence/full-review/release-20261013/round-v74`。
完整 task-gates 使用已验证的 `PATH=/usr/local/bin:$PATH` 与 `TOME_PASEO_WORKSPACE` 环境，
当前按绝对 directory 调用；相对路径回执返回问题已有有界归因，待小型入口修正。
执行记录、门禁和迁移核验见 [当前状态](../evidence/full-review/release-20261013/STATUS.md)。

2026-10-15 用户明确要求继续推进全量审核。M3 phase01 按三个有界源码切片完成48A／24B，指定模型各task独立门禁、构建、DONE、归档和导入闭合，新增有效40A／16B至283A／153B。11个确认问题点涉及8条target，按边界合并window-08修复；名称建议不扩展为改名。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-01/REPORT.md)。完成修复及新revision生产A/B后连续选择下一有界切片；最终分母、补充项及候选游戏验收仍开放。

window-08八条法术说明、十一项已确认问题修复已DONE_VERIFIED；初审的一项距离单位意见保留advisory，正确编号fresh终审8OK，执行者及宿主最终完整17项含构建通过。宿主终态编号冲突与恢复证据完整保留，未归因为模型或门禁故障。实现复审不给生产覆盖，待R10精确后继及fresh8A/8B后连续推进下一有界切片。见[修复与闭合](../evidence/full-review/release-20261013/repairs/window-08/ORCHESTRATION.json)。

2026-10-15续：窗口-08八条新revision的fresh生产A8/B8及各自完整17项／构建、DONE、归档与导入已闭合，当前round-v10有效291A/161B，待修队列为空。按既有连续授权推进fire/wildfire、water/ice、earth/stone三个有界M3切片，保持Opus5.5/GPT6.1Sol。最终发行分母与游戏场景验收仍未完成。

2026-10-15 M3phase02完成55A／25B，各task指定模型独立门禁、构建、DONE、归档及导入，新增有效50A／20B至341A／181B。5项确认机制问题涉及4条target合并window-09修复；净化之焰显示／运行1条显式pending，不改游戏代码或formatter。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-02/REPORT.md)。随后fresh生产A/B并连续选择下一个有界切片；最终分母、补充项及游戏验收仍开放。

窗口-09五条候选（四条修复及矮人同运行键同步）已 DONE_VERIFIED，独立Opus5.5初审／终审均5OK，执行者与宿主完整17项含构建通过。初始漏列共享键导致的失败门禁及STOP任务保留于[可重放闭合证据](../evidence/full-review/release-20261013/repairs/window-09/ORCHESTRATION.json)；fresh收尾仅同步一条，保留原修复及报告。实现复审不给生产覆盖，待R12精确后继及fresh5A/5B后连续推进下一有界切片。净化之焰显示／运行问题1条继续显式pending，最终分母、补充项和游戏验收仍开放。

2026-10-15续：窗口-09五条新revision（含矮人共享条目）fresh生产A5/B5及各自完整17项／构建、DONE、归档和导入闭合；round-v12有效346A/186B，普通target修复队列为空，净化之焰显示／运行1条显式pending仍未计完成。保持Opus5.5/GPT6.1Sol，按连续授权推进下一有界切片。最终分母、补充项和游戏验收仍开放。

2026-10-15 M3phase03完成52A／22B，六个task分别完成full17/build、DONE、归档及导入。新增有效49A／19B至395A／205B，3项确认问题涉及2条target合并window-10修复；凝固时间和净化之焰共2条source/runtime pending，不改游戏代码或formatter。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-03/REPORT.md)。之后fresh生产A/B并连续选择下一有界切片，最终分母、补充项及游戏验收仍开放。

2026-10-15续：窗口-10两条新 revision fresh生产 A2/B2 与各自完整17项／构建、DONE、归档和导入闭合；round-v14 有效397A/207B，普通 target 修复队列为空，两条显示／运行 pending 显式保留。继续使用 Opus5.5/GPT6.1Sol，按既定连续授权推进下一有界切片；最终分母、补充项和游戏验收仍开放。

2026-10-15 M3phase04完成35A／16B，指定模型六个task各完成full17/build、DONE、归档和导入。累计427A／218B，8项确认问题合并5条target进入window-11；不改代码、formatter、术语库或既有全局命名。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-04/REPORT.md)。两条source/runtime pending、最终分母、补充项及游戏验收仍开放。

2026-10-15续：窗口-11五条新 revision 的 fresh生产 A5/B5 与各自完整17项／构建、DONE、归档及导入闭合；round-v16 有效432A/223B，普通 target 修复队列为空，两条显示／运行 pending 显式保留。继续使用 Opus5.5/GPT6.1Sol 按既定连续授权推进下一有界切片；最终分母、补充项和游戏验收仍开放。

2026-10-16 M3phase05完成27A／13B，七个任务各完成full17/build、DONE、归档和导入。累计454A／231B；8项确认问题合并5条target进入window-12。已实测导出内重复清单读取／解析开销，按[并行提效方案](full-review-parallel-efficiency-plan-20261016.md)另做有界工具维护；保留全部验证、模型与修复边界。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-05/REPORT.md)。两条source/runtime pending、最终分母、补充项及游戏验收仍开放。

2026-10-16续：窗口-12五条新 revision 的 fresh生产 A5/B5 与各自完整17项／构建、DONE、归档及导入闭合；round-v18 有效459A/236B，普通 target 修复队列为空，两条显示／运行 pending 显式保留。继续使用 Opus5.5/GPT6.1Sol 按既定连续授权推进下一有界切片；最终分母、补充项和游戏验收仍开放。

2026-10-16 M3phase06以34条关联炼金术为一批完成34A／13B，三个生产任务各自full17/build、DONE、归档及导入；累计有效489A／245B。5项源码确认问题合并4条待修target，尚未计完成。按连续审核授权继续傀儡关联切片及合并修复；两项既有runtime pending、最终分母、补充项及游戏验收仍开放。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-06/REPORT.md)。

2026-10-16 M3phase07完成傀儡关联73A／48B，各自full17/build、DONE、归档及导入；累计有效556A／287B。累计10条待修target／11项claim待合并修复，两项既有runtime pending仍不计完成。继续38条石守卫关联切片，再按三切片边界集中修复。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-07/REPORT.md)。

2026-10-16 M3phase08完成石守卫关联38A／26B，各自full17/build、DONE、归档及导入；累计有效593A／312B。待修10条target／11项claim进入修复窗口13，三条source/runtime pending排除在外。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-08/REPORT.md)。

2026-10-16续：窗口-13十条新revision的fresh生产A10/B10及各自完整17项／构建、DONE、归档和导入闭合；round-v22有效603A／322B，普通修复队列为空，三条显示／运行pending显式保留。按既定连续授权与Opus5.5/GPT6.1Sol模型对推进下一有界切片。最终分母、补充项和游戏验收仍开放。

2026-10-16 M3phase09完成28A／16B，各自full17/build、DONE、归档及导入；累计有效624A／331B。待修5条target／6项claim按三批或二十revision边界合并；5条source/runtime pending排除在外。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-09/REPORT.md)。

2026-10-16 M3phase10完成30A／18B，各自full17/build、DONE、归档及导入；累计有效652A／347B。普通修复保持5条target／6项claim，7条source/runtime pending排除在有效完成外。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-10/REPORT.md)。继续42条相关召唤法术切片，达到三批边界后合并普通修复。

2026-10-16 M3phase11完成42A／26B，各自full17/build、DONE、归档及导入；累计有效679A／358B，已验证706A／385B。普通修复合并19条target／20项claim，8条source/runtime pending排除。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-11/REPORT.md)。达到三批边界，开始window14集中普通修复。

2026-10-16续：窗口-14的19条当前revision完成fresh生产A19/B19及各自完整17项／构建、DONE、归档、导入；round-v26实测有效697A／376B，接受18完整revision。夜幕球保留原频率修复，新增敌我范围缺陷进入普通队列1条／1claim，整条不计完成；8条source/runtime pending显式保留。按连续授权继续下一39条关联切片并合并后续普通修复，最终分母、补充项和游戏验收仍开放。

2026-10-16 M3phase12完成39A／22B，各自full17/build、DONE、归档与导入；累计有效732A／394B，已验证745A／407B。普通队列3条／3claim，10条source/runtime pending排除。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-12/REPORT.md)。按三关联切片／20revision策略继续类别审核。

2026-10-16 M3phase13完成103A／55B，三个独立full17/build任务，合并B完整结果按unit并集计数；累计有效835A／449B，已验证848A／462B。普通队列3条／3claim，10条source/runtime pending排除。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-13/REPORT.md)。按既定边界集中普通修复。

2026-10-16续：窗口-15三条当前revision完成fresh生产A3/B3，各自完整17项／构建、DONE、归档、导入与源码验收。R29有效838A／452B，validated848A／462B，普通队列为空；10条source/runtime pending仍整条排除。核心法术617条已逐条审读，607条接受、10条运行待确认。继续下一有界机制切片，最终分母、补充项与游戏验收仍开放。

2026-10-16 M3phase14完成58A／35B，两路独立full17/build，新增有效53A／30B；累计891A／482B，已验证906A／497B。5条Orcs译文／6claim集中机制修复，4项advisory；DLC来源未固定，10条旧runtime pending不计完成。见[阶段报告](../evidence/full-review/release-20261013/m3/phase-14/REPORT.md)。

2026-10-17续：窗口-16五条新revision完成fresh生产A5/B5，各自完整17项／构建、DONE、归档、导入与源码验收，六项claim闭合。R31有效896A／487B，validated906A／497B，普通队列为空；10条runtime pending仍整条排除。58条Orcs法术切片闭合，DLC来源仍未固定。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase15完成38A／23B，两路各自full17/build，新增有效33A／18B，累计929A／505B，已验证944A／520B。5条确认修复／5项advisory，10条旧runtime pending保持。实测准备瓶颈转入独立inventory递归链复用维护，见[阶段报告](../evidence/full-review/release-20261013/m3/phase-15/REPORT.md)。

2026-10-17续：窗口-17五条新revision完成fresh生产A5/B5，各自完整17项／构建、DONE、归档、导入与源码验收，五项claim闭合。R33有效934A／510B，validated944A／520B，普通队列为空；10条runtime pending仍整条排除。固定624核心／引擎源码已核验。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase16完成73A／49B，两路各自full17/build，新增有效65A／41B，累计999A／551B，已验证1017A／569B。确认8claims／7条局部修复，5项advisory，11条runtime pending保持；见[阶段报告](../evidence/full-review/release-20261013/m3/phase-16/REPORT.md)。

2026-10-17续：窗口-18七条修复及两条运行时同键同步完成fresh生产A9/B9，各自完整17项／构建、DONE、归档、导入与源码验收，八项claim闭合；Pin Down普通射击标记前提经源码确认后重新入队（1条）。R35有效1007A／559B，validated1019A／571B；11条runtime pending仍整条排除。固定624核心／引擎源码已核验。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase17完成54A／31B，两路各自full17/build，新增有效45A／22B，累计1052A／581B，已验证1073A／602B。确认7claims／7条局部修复，队列共8条；runtime pending共13条整条排除。

2026-10-17续：窗口-19八条修复（含cycle1沥青目标修正）完成fresh生产A8/B8，各自完整17项／构建、DONE、归档、导入与源码验收，九项claim闭合，修复队列清空。R37有效1060A／589B，validated1073A／602B；13条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase18完成44A／28B，两路各自full17/build，新增有效41A／25B，累计1101A／614B，已验证1117A／630B。确认2claims／2条局部修复；runtime pending共14条整条排除。

2026-10-17续：窗口-20两条修复（含cycle1格挡专家属性需求修正）完成fresh生产A2/B2，各自完整17项／构建、DONE、归档、导入与源码验收，三项claim闭合，修复队列清空。R39有效1103A／616B，validated1117A／630B；14条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase19完成41A／29B，两路各自full17/build，新增有效36A／24B，累计1139A／640B，已验证1158A／659B。确认4claims／4条局部修复；runtime pending共15条整条排除。

2026-10-17续：窗口-21四条双持修复完成fresh生产A4/B4，各自完整17项／构建、DONE、归档、导入与源码验收，四项claim闭合，修复队列清空；节奏「弓箭攻击」observation记advisory（archery类别统一译法属未授权跨批次策略）。R41有效1143A／644B，validated1158A／659B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase20完成37A／23B，两路各自full17/build，新增有效35A／21B，累计1178A／665B，已验证1195A／682B。确认2claims／2条局部修复；runtime pending共15条整条排除。

2026-10-17续：窗口-22两条修复完成fresh生产A2/B2，各自完整17项／构建、DONE、归档、导入与源码验收，两项claim闭合，修复队列清空。R43有效1180A／667B，validated1195A／682B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase21完成43A／27B，两路各自full17/build，新增有效41A／25B，累计1221A／692B，已验证1238A／709B。确认2claims／2条局部修复；runtime pending共15条整条排除。

2026-10-17续：窗口-23两条修复完成fresh生产A2/B2，各自完整17项／构建、DONE、归档、导入与源码验收，两项claim闭合，修复队列清空。R45有效1223A／694B，validated1238A／709B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase22完成40A／26B，两路各自full17/build，新增有效35A／21B，累计1258A／715B，已验证1278A／735B。确认5claims／5条局部修复；runtime pending共15条整条排除。

2026-10-17续：窗口-24五条修复（含cycle1两项）完成fresh生产A5/B5，各自完整17项／构建、DONE、归档、导入与源码验收，七项claim闭合，修复队列清空。R47有效1263A／720B，validated1278A／735B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase23完成31A／18B，两路各自full17/build，新增有效30A／17B，累计1293A／737B，已验证1309A／753B。确认1claim／1条局部修复；runtime pending共15条整条排除。

2026-10-17续：窗口-25一条修复完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，一项claim闭合，修复队列清空。R49有效1294A／738B，validated1309A／753B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-17 M3phase24完成43A／31B，两路各自full17/build，新增有效40A／28B，累计1334A／766B，已验证1352A／784B。确认3claims／3条局部修复；runtime pending共15条整条排除。

2026-10-18续：窗口-26三条修复（含经用户裁决的Exhaustion＝力竭术语）与窗口-27两条状态名／描述同步完成；三条W26当前译文fresh生产A3/B3，各自完整17项／构建、DONE、归档、导入与源码验收。灵巧防御与翻滚通过，三项claim闭合；脱离的疲劳方向表述经B路提出、宿主按固定源码确认，重新排队待窗口-28。R51有效1336A／768B，validated1352A／784B；15条runtime pending仍整条排除；W27两条仍待其切片生产复审。最终分母、补充项和游戏验收保持开放。

2026-10-18续：窗口-28一条修复（脱离疲劳方向）完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，一项claim闭合，修复队列清空。R52有效1337A／769B，validated1352A／784B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-18 M3phase25完成39A／26B，两路各自full17/build，新增有效38A／26B，累计1375A／795B，已验证1391A／811B。确认1claim／1条局部修复（待术语授权）；runtime pending共15条整条排除。

2026-10-18 M3phase26完成24A／16B（另定向B路1条），三路各自full17/build，新增有效23A／16B，用户裁决另计1A／1B，累计1399A／812B，已验证1415A／828B。确认1claim／1条局部修复；runtime pending共15条整条排除。

2026-10-18续：窗口-29一条修复（直觉射击换行）完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，一项claim闭合，修复队列清空。R55有效1400A／813B，validated1415A／828B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-18 M3phase27完成46A／20B（另定向B路1条），三路各自full17/build，新增有效45A／20B，累计1445A／833B，已验证1461A／849B。确认1claim／1条局部修复；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-18续：窗口-30一条修复（战斗训练描述）完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，一项claim闭合，修复队列清空。R57有效1446A／834B，validated1461A／849B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-18 M3phase28完成47A／28B（另定向B路1条），三路各自full17/build，新增有效44A／26B，累计1490A／860B，已验证1508A／878B。确认3claim／3条局部修复；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-19续：窗口-31三条修复（弓术检查发射器译名两条、射术类别名一条）完成fresh生产A3/B3，各自完整17项／构建、DONE、归档、导入与源码验收，三项claim闭合，修复队列清空。R59有效1493A／863B，validated1508A／878B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-20 M3phase29完成51A／31B（cunning 五个类别），两路各自full17/build，新增有效51A／31B，累计1544A／894B，已验证1559A／909B。无确认缺陷，1条上游实现advisory；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-20 M3phase30完成49A／32B（cunning 四个类别），两路各自full17/build，新增有效48A／31B，累计1592A／925B，已验证1608A／941B。确认1claim／1条局部修复；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-20续：窗口-32一条修复（致命射击日志距离加成译名）完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，该项claim闭合，修复队列清空。R62有效1593A／926B，validated1608A／941B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase31完成31A／17B（另定向B路2条），三路各自full17/build，新增有效29A／17B，累计1622A／943B，已验证1639A／960B。确认2claim／2条局部修复（用户裁决 scoundrel→无赖）；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21续：窗口-33（用户裁决 scoundrel→无赖）两条已审单元完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，两项claim闭合，修复队列清空；欺诈圣手（Tricks of the Trade）同步单元仍未审。R64有效1624A／945B，validated1639A／960B；15条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase32完成84A／59B（另定向B路1条，两组切片同轮），五路各自full17/build，新增有效82A／58B，累计1706A／1003B，已验证1723A／1020B。确认2claim／2条局部修复（剧毒打击改名、钩爪 immovable）；runtime pending共15条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase33完成123A／103B（两组切片同轮），四路各自full17/build，新增有效118A／98B，累计1824A／1101B，已验证1846A／1123B。确认4claim／4条局部修复；新增1条死键runtime pending，共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase34完成142A／81B（天体系 Sun Paladin 与 Anorithil 两组同轮），四路各自full17/build，新增有效135A／74B，累计1959A／1175B，已验证1988A／1204B。确认7条局部修复；runtime pending共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase35完成74A／48B（天体系 Fallen 与圣印两组同轮，含1条b-extra），五路各自full17/build，新增有效69A／43B，累计2028A／1218B，已验证2062A／1252B。确认5条局部修复；runtime pending共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase36完成38A／19B（天体系技能类别），两路各自full17/build，新增有效36A／17B，累计2064A／1235B，已验证2100A／1271B。确认2条局部修复；修复队列达20条，下一步开修复窗口；runtime pending共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21续：窗口-34（M3 phase32–36 共20条确认问题＋剧毒打击三处同步，复审中另修两处）21条已审单元完成fresh生产A1/B1，各自完整17项／构建、DONE、归档、导入与源码验收，20条接受、暗影临近重新入队；两条同步单元仍未审。R70有效2083A／1254B，validated2100A／1271B；16条runtime pending仍整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-21 M3phase37完成130A／86B（时空系十一个文件两组同轮），四路各自full17/build，新增有效126A／82B，累计2209A／1336B，已验证2230A／1357B。确认4条局部修复；runtime pending共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-22 M3phase38完成160A／111B（时空系十一个文件两组同轮），四路各自full17/build，新增有效155A／106B，累计2364A／1442B，已验证2390A／1468B。确认5条局部修复；runtime pending共16条整条排除。最终分母、补充项和游戏验收保持开放。

2026-10-22 M3phase39完成52A／26B（chronomancer.lua），两路各自full17/build，新增有效49A／23B，累计2413A／1465B，已验证2442A／1494B；3条局部修复入队（共13条），下一片other.lua。

2026-10-22 M3phase40完成53A／34B（other.lua），两路各自full17/build，新增有效50A／31B，累计2463A／1496B，已验证2495A／1528B；3条局部修复入队（共16条），下一片anomalies.lua。
