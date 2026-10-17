# 裁决:不采纳(按提案原文形态);性能问题走 §6 的 B+C+D

回答人:Claude Fable 5(claude-fable-5),2026-09-11。
核验方式:全程只读(`git show`/`sed`/`grep` + 源码阅读)。未跑 165s 级实测重放——生产工作区不便占用,且 3575d72 提交信息里独立记录的 160.6s/160.4s(117 批规模)已与 brief 的 164.8s 互相印证。行号与事实核验结果见文末「6. 核验记录」;与 brief 不符之处均已列出。

---

## 1. 裁决

**不采纳**「当 `meta.evidence_head == HEAD` 且 `meta.catalog_id` 匹配时直接信任 SQLite overrides、跳过重放」。理由浓缩成三句:

1. **提案的事实前提在它想优化的场景里不成立。** 批次进行期间,`state_override` 表里并不"逐行存着" Git 投影的 overrides:queued 模式下它混着活动批次的行(`_check_projection` 818-825 的容忍分支就是为此存在);retry_blocked 模式下,被选行的 committed blocked winner 在 `start` 的 `INSERT OR REPLACE`(batch.py:1209)时**已被覆盖销毁**,而 `_validate_mode_prior`(783-786)、attempt 推导(1012)、phase-tuple 接受集(954-957)恰恰需要读这些 winner。"直接从 SQLite 读"对最需要独立佐证的数据无从读起——提案不是"简单地换个读取来源",而是一个 brief 及其 §4 支持理由都没意识到的、带模式分叉的重构。
2. **它换掉的东西比省下的时间贵。** 批中重放-比对买到的不是"重放结果会变"(HEAD 钉死,结果是纯函数,3575d72 已利用这一点),而是"**SQLite 在两次打开之间没被外带写过**"。这正是 §1.3 保留的威胁模型(漂移与误操作)的核心场景——今晚的 evidence_head 漂移、§27 事故、§36.3 的两个读错门禁的坑,全是误操作类,且本工作区常态跑 bypassPermissions 的子 agent。采纳后,外带写坏在批中不再被发现,而是在 finalize 的 `_replace`(batch.py:1706-1707)被**无声抹掉**——不是晚点报警,是永远不报警。
3. **长期算术上它输给 B+C+D。** 提案只能砍掉批中 4-6 次 preflight 重放,对它必须保留的重放(start 锚点、finalize 新提交校验、status/check、migration plan/check/apply、修复 worktree 的 rebuild)无能为力——这些保留项的成本和 1.9s/批的斜率原样保留,273 批后仅 start+finalize 就是 2×~730s/批。B(内容寻址校验回执)则加速**每一次**重放并把斜率主项归零。两个方案省时相当时,一个要重划信任边界,另一个只是把 §37/3575d72 已确立的原则("同一纯函数别对同一份字节重算")推广到磁盘——选后者。

注意一个容易混淆的类比:本提案**不是** 3575d72 的自然延伸。3575d72 复用的是*本进程刚从 Git 算出、无人可染指的内存值*;本提案信任的是*一个任何进程都写得到的可变文件在若干分钟到几小时后的内容*。前者的正确性由"纯函数 + 同一 commit"闭环保证;后者还需要"这段时间没人碰过这个文件"这一无法从 key 推出的额外假设。

---

## 2. 理由:对 §4、§5 逐条回应

### §4(支持采纳)

- **4.1(批次期间 HEAD 钉死)成立**,已核验:每个批中子命令都强制 `value["base_commit"] == queue._head(root, "HEAD")`(batch.py:1018)。但它只证明"重放结果不会变",不证明"SQLite 没被碰过"。前者已被 3575d72 兑现;后者才是每次重放-比对真正买到的东西。此条支持的是"批中重放是冗余计算",不支持"批中可以免验 SQLite"。
- **4.2(commit sha 密码学锚定)成立但击不中要害。** sha 锚定的是 Git 侧。`meta.evidence_head` 只是 SQLite 里一行普通数据,与 `state_override` 的行之间没有任何绑定(无整表摘要、无行级校验值)。"key 相同即内容相同"对不可变对象成立,对可变文件不成立。若为补此洞给 meta 加整表 sha256,那就是在造第二套证据机制——§1.3 明言不做"用一套额外系统复制 Git 职责"的事。
- **4.3(`_replace` 写入前自检)成立**(queue.py:863、884)。这恰好界定了争议:SQLite 在**写入时刻**是受信的,争议全在"写入后到下次读取前"的窗口。现行设计把这个窗口压到零(每次读前重验),提案把它拉长到整个批次并撤掉读前验证。
- **4.4(收益巨大)方向对、数字过时且偏高。** "14-18 次投影 ≈ 45-50 分钟"疑为 3575d72 之前的口径。按现行代码数:start 连做 **3 次**完整重放(preflight 内 `_restore_orphans`:808 一次 + `strict_check`:1184 一次,start 自己 1195 再来一次;retry 模式 1202 还有第四次),批中子命令各 1 次(surface-export/import、adjudicate、prepare-evidence,深审加 contextual 两次),finalize 在新提交上 1 次,`queue status` 每叫一次 1 次——快乐路径约 9-11 次 ≈ 25-30 分钟。提案只砍得掉其中批中的 4-6 次(≈ 11-16 分钟/批),砍不掉 start/finalize/status。"能把线性斜率压掉大半"不成立:保留项的斜率原封不动。
- **4.5(§1.3 已排除恶意同用户)同意前提,反对推论——方向用反了。** §1.3 排除的是攻击者;现行"永不信 SQLite"防的正是 §1.3 **保留**的威胁:漂移与误操作。"缓存被伪造"不在模型内,"缓存被误写/写坏"恰恰在模型内。拿排除恶意来论证可以免验,是把这条不变量最常兑现的场景论证掉了。

### §5(反对采纳)

- **5.1(991-993 注释是有意设计)属实,但这是我最不倚重的一条。** 设计决定可以修订;要紧的是它护的不变量在哪里承重。我的核对结论:在**静默路径**(start 前的 preflight、recover、migration 三处 strict_check)它是对 SQLite 的唯一真实校验,跳过等于让被评审者自证清白,绝不可动;在**批中路径**它是纵深防御,护的是"外带写入的检测时延",不是证据完整性——我逐流核对过,durable 证据字节全部源自 checkpoint + sha256 绑定的 raw 文件 + Git 目录(`prepare_evidence`:1540-1663、`_evidence_rows`:1366-1408),批中的 SQLite committed 基线只喂 fail-closed 交叉检查,不进任何证据字节。所以拒绝本提案不必靠"作者当初就是这么定的"。
- **5.2(17 项门禁不查绑定)属实但表述不准,且对本提案杀伤力有限。** 不止 `queue rebuild`:**每次 `_projection` 都走 `_validated_migration_edges`**(queue.py:661→1048),批中 preflight 同样在查。真正的空档是 ci-gates 不查。而绑定破坏(§27 那类)必然伴随新提交,HEAD 移动 → 提案守卫本来就回落到完整重放。这条事故的正确教训是"**重放的场合一个都不能少**"(所以静默路径与新 HEAD 必须重放),它不直接否决"批中同 HEAD 复用"——否决后者的是 5.3。
- **5.3(是否存在 evidence_head 匹配而内容错误)——存在,三类,已在源码落实:**
  1. **`migration apply` 的前置戳窗口**(migration.py:832-838):apply 原地改库后把 meta 戳成 `(new_catalog_id, base_commit)`,此刻 `evidence_head == HEAD` 而库内容是"迁移改写",**不是** HEAD 的重放(HEAD 上还是旧 catalog)。提案的 catalog_id 守卫挡得住它——但**必须对着 Git 现读的 manifest 比**(批中由 batch.py:996+1018 现成提供),不能对 checkpoint 或 SQLite 自己比。好在该窗口被 `_quiescent` 强制静默,批中不会出现。这个案例的价值在于证明:**"meta 说 X 就是 X" 在本代码库里已经有一个由自家代码制造的反例**,meta 不是重建专属的印章。
  2. **meta 不动、行被外带写入/写坏**:守卫完全不挡。现行设计在下一个子命令即报 `active batch changed a non-selected committed override` / `unrelated override`(batch.py:941-945);提案下这两个检查退化为"SQLite 对比 SQLite"的同义反复,腐坏一路存活到 finalize 被 `_replace` 无声覆盖。**检查还在代码里但什么都验不到,比删掉它更糟——留下覆盖率的错觉。**
  3. **值级位腐坏**:`PRAGMA integrity_check`(queue.py:786-788)只保结构,页内值翻转不报错——效果同第 2 类。
- **5.4(不变量 6 退化)是 §5 里最弱的一条,我不倚重。** 采纳后 start 与 finalize 仍每批各演练一次完整重建,"重建能力退化只在下次 rebuild 暴露"的潜伏期实际最多一个批次,不是无限期。

---

## 3. 如果我错了

**我的裁决是"不采纳"。我错 = 其实应该采纳(风险担忧过度、B+C+D 不足)。**

- 故障形态:**纯时间损失,无正确性损失。** 每批多花 11-16 分钟(今天)——若 B+C+D 也没做或未达预期,按剩余 ≈273 批算,上限约 50-70 小时吞吐损失。
- 多久发现:一两个批次。runbook §4 的计时工具或任何一次批次墙钟统计都能证伪我:若做完 B+C+D 后投影占比仍是主项,我就错了。
- 能否事后修复:**完全可以,零路径依赖。** 本提案(或我在 §4 节给出的更安全等价物)随时可以在 B+C+D 之后再上;先做 B+C+D 不烧掉任何桥。

**反向错误(采纳而我列的风险成真)的形态,作为对照:**

- 外带写入批中静默存活、finalize 无声自愈,你**永久失去**"环境里有东西在写队列"的唯一警报。单看这一点损失有限(自愈后 durable 状态仍正确)。
- 真正的代价是滑坡:批中版落地后,剩余的慢点全在静默路径(start 3 次、status、migration),"同一守卫再多用一处"的诱惑极大。而静默路径一旦信任 SQLite,坏状态就能种进 selection:已 done 条目被重选重审,后批以不同结论进入证据,投影的 winner fold(queue.py:730-737)**后批无声顶掉前批,没有任何门禁报警**——这是进入已提交证据、"无法用后续提交修复"的一类(§27 已演示过一次这种历史改写的代价)。
- 发现时延:可能永远不被发现(自愈类),或在数批之后由人对账时发现(污染类);后者修复要改写历史。

两种错的代价不对称:我错 = 可恢复的分钟;反向错 = 一层检测 + 一条滑坡。**这个不对称就是裁决的核心依据。**

---

## 4. 对 §6:B+C+D 足够,且 B 是正确的架构方向,不是权宜

- **B(校验回执落盘)——最优先。** 前提已核验:`validate_catalog_files` 只吃字节,`_catalog_from_tree` 已按内容标识在进程内记忆(queue.py:190-199;每个文件仍逐个 `_ordinary_blob` 读取并校验 mode/kind,memo 只覆盖纯校验)。落盘的两个硬条件:
  1. **key 必须并入代码/schema 版本。** 这是进程内复用没有的新风险:重放逻辑修了 bug 之后,旧回执还在为旧行为放行。3575d72 的复用活不过进程,天然免疫;磁盘回执必须显式处理。
  2. **回执只做"免重验",不携带任何向前的数据**(或携带解析产物时,加载后对源字节逐次 re-hash)。这样坏回执的最大伤害是"漏掉一次对内容寻址、且历史上已验过上百遍的字节的重复校验",它**注不进**投影输出——与本提案(把可变表内容直接当 committed 基线用)在失效模式上是两个类别。
  预期 165s → ~45s 与 §37 结构一致(120s 的 validate 项归零)。**更重要的是斜率:** 每批新增的 ~1.65s 主项来自对该批 `base_commit` 的 `_catalog_from_tree`,内容命中后归零;同一模式自然延伸到 `_batch_rows` 的按批 raw 校验与 sparse migration 的 `reconcile`(44.5s,纯函数 of 两份 entries 字节)。做全之后,390 批时单次重放可望停在 ~30-60s,而不是 730s。
- **C(批量化 git)**:已测量(11183 次 spawn / 51s;`_publication_commit` 117 次 `git log` / 32.6s),机械、零语义,做。
- **D(合并进程)**:有一个立刻可拿的免费案例——**`start` 在同一进程、同一 HEAD 连做 3 次(retry 4 次)完整重放**(`_restore_orphans`:808 + preflight 的 `strict_check`:1184 + start:1195 + retry:1202),按 3575d72 同款透传手法去重,省 330-495s/批,不需要任何磁盘缓存。`abandon`(preflight + 1238)同理。
- **顺序建议**:D 的 start 去重(半天内)→ C → B(回执版)→ 实测。粗算 B+C+D 后每批投影总耗时 ~5-8 分钟且斜率被压平,批周期瓶颈回到评审本身——**本提案没有存在的必要了**。
- **若量完仍不达标**,正确的下一步也不是本提案,而是:**`start` 时把刚验证过的 committed 基线快照进 checkpoint,批中拿 SQLite 对着 checkpoint 快照比。** 同样跳过批中重放,但 SQLite 一分授信都不加、批中检查保持非同义反复、retry winner 问题顺带解决(快照发生在 1209 覆盖之前)、外带写入仍在下一个子命令被当场抓住。约 8000 行 ≈ 1-2MB,checkpoint 本来就是整写的。这才是"有条件采纳"应有的形态——而它已经不是原提案,所以我的裁决记为不采纳而非有条件采纳。

---

## 5. brief 里最可能错的陈述

**§1 的"它实际只用到这个五元组的第 4 项 overrides"。** 两处错,且都动摇提案的"实现很简单":

1. **消费面不止第 4 项。** `_reconcile_phase_tuples`:987 把整个五元组传给 `strict_check`,`_check_projection`(794-830)消费全部五项:`[0][1]` 对 meta,`[2]` 做"override 必须属于当前 catalog"的成员检查(815-817),`[3]` 逐行比,`[4]` 对 reconciliation 表逐行比。若 overrides 改从 SQLite 读,这些比对沦为同义反复,strict_check 必须整体重新设计,不是"换个数据源"。
2. **反向也错:第 4 项并不"正好逐行存在表里"。** 批中 `state_override` = committed ∪ 活动行(`_check_projection`:818-825 的容忍分支即为此存在);retry 模式下被选行的 committed winner 已在 `start`:1209 被 `INSERT OR REPLACE` 销毁,批中 SQLite 里**根本没有**这份数据,而三处检查(783-786、954-957、1012)都要读它。

**验证方法**:读上列行号即可闭环;或(在下一个批次进行期间、以只读连接)`SELECT * FROM state_override` 与一次 `_projection(root, "HEAD")[3]` 求差集,会看到被选行两边不一致、retry winner 只在投影侧存在。我本次因不碰生产库,只做了代码级核验。

次候选:"一批约 14-18 次投影 ≈ 45-50 分钟"(疑为 3575d72 前口径,现行快乐路径 9-11 次,详见 §2 对 4.4 的回应)。

---

## 6. 核验记录

**核对无误**:`_projection` 639 / `_projection_contents` 646 / `_check_projection` 791 / `strict_check` 943 / `_catalog_from_tree` 175 / `_clean_evidence` 203 / `_reconcile_phase_tuples` 931 / `_reconcile_checkpoint` 990 / `preflight` 1176 / batch.py:994 调用与 997 取 `[3]` / 991-993 注释原文与 brief 引文一致 / migration `reconcile` 283、`validate_migration` 555 / queue.py:195-197 内容标识(实为 `catalog.CANDIDATE_FILES` 全集的 path:blob_id 哈希,brief 称"三份目录文件的 blob id 三元组"义近)/ §37 原文(96 批 49 迁移、314.8→125.4s、"只省掉对同一份字节重复做同一个纯函数")/ §27 事故原文(1f849ff、17 项全绿、`migration publication catalog identity drift`、只能改写历史)/ 计划 §1.2 不变量 6 与 §1.3 非目标原文 / entries.jsonl 29828 行、35.2MB / implicit_queued 21796(3575d72 提交信息)/ 斜率自洽:(164.8−125.4)/(117−96)≈1.88 s/批 / flock 排他锁(queue.py:221-238)/ `_clean_evidence` 逢投影必查(strict_check:956)。

**与 brief 不符或不准**:

| brief 陈述 | 实测 |
|---|---|
| `rebuild` 在 queue.py:928 | 实际 932 |
| `_validated_migration_edges` 在 1041 | 实际 1048 |
| 规模"117 批 / 72 migration" | 在 brief 自钉的 3575d72 上数得 **118 个批次 manifest / 73 个 migration 文件**;今日 HEAD 8381692(多了第 81 批)为 119/73。3575d72 提交信息同样写 117/72,疑为同源笔误或口径差(不影响任何结论) |
| "只用五元组第 4 项"(§1) | 错,见上文第 5 节 |
| "overrides 正好逐行存在 state_override 表里"(§1) | 仅在静默态成立;批中不成立(活动行混入、retry winner 被销毁) |
| "只有 queue rebuild 会走 `_validated_migration_edges`"(§5.2,引 runbook) | 不准:每次 `_projection` 都走(queue.py:661),含批中 preflight;真正不查的是 ci-gates |
| "14-18 次投影 ≈ 45-50 分钟"(§2) | 现行代码快乐路径约 9-11 次(start 一处就有 3 次同进程冗余);45-50 分钟疑为 3575d72 前口径 |
| "每批省约 35-40 分钟"(§4.4) | 按现行代码,提案实际可省批中 4-6 次 ≈ 11-16 分钟 |
| cProfile 表把 `reconcile` 44.5s 嵌在 `_validated_migration_edges` 之下 | `reconcile` 有两个调用面:edges 内 `validate_migration`(579-583)与 `reconciliation_rows_for_tree`(_projection_contents:666→1138);嵌套展示不完全准确,量级无碍 |

**brief 未列、但对裁决有实质影响的两个源码事实**(均已在正文使用):`start`:1209 的 `INSERT OR REPLACE` 销毁 retry winner;`migration apply`(migration.py:832-838)的前置戳 meta 窗口。
