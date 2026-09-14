# 翻译审核流水线交接说明（截至第 132 批）

写于 2026-09-14，交接时基线 `7758a2b6f610b8c64de14bd829caab3c5fcbb364`（分支 `develop`）。

本文承接 `docs/review-handoff-20260914.md`（截至第 127 批）。**那份仍然有效**，本文只写第 128–132 批期间新增或**被推翻**的内容。凡本文与旧文冲突的，以本文为准，冲突处都标了「更正」。

---

## 1. 交接时的状态

| 项 | 值 | 核对命令 |
|---|---|---|
| 分支 | `develop` | `git branch --show-current` |
| HEAD | `7758a2b` review: complete batch 132 evidence with nine repair findings | `git rev-parse HEAD` |
| 活动批次 | 无 | `python3 -B tools/i18n production batch show` → `{"active": false, "ok": true}` |
| 工作树 | 只有 `?? .ai/consult/` | `git status --porcelain` |
| contextual 暂存槽 | **已清空**（第 132 批的已归档进 `batch133-orchestration/prior-batch-runtime-scratch/`） | `ls -A .artifacts/i18n/production-review-v2-lite/contextual/` |
| 队列 meta evidence_head | `7758a2b`，与 HEAD 一致，无漂移 | 见 §2 的命令 |
| 引擎工作树 | `/workspace/t-engine4` HEAD == 固定 commit `624a673…ae63`，已跟踪文件改动数 0（另有 5 个未跟踪项，无关） | `git -C /workspace/t-engine4 status --porcelain \| grep -vc '^??'` |
| 已提交批次证据 | 170 个批次目录，累计 12887 条 entry 结果 | |
| 累计裁决 | 1139 条：confirmed 891、advisory 163、refuted 56、pending 29 | |
| 第 133 批脚手架 | 已搭好在 `.artifacts/i18n/batch133-orchestration/`，10 个文件已改名、无残留批次号 | |

**接手后第一件事不是 `git rev-parse HEAD`，是同时比对队列 meta。** 见下节。

---

## 2. 接手时必查：队列 meta 与 HEAD 的漂移（新增，我在第 128 批栽过）

上一任宿主写完交接文档的那条 docs 提交也让 HEAD 前进了。按旧文第 13 节四项前置条件核对**全部通过**，`batch start` 仍然直接退出码 1 报 `queue database meta/catalog/evidence-head drift`。

交接文档里写的「HEAD 应为 X」通常是**写文档时**的 HEAD，文档自身的提交在那之后。所以：

```bash
python3 -c "import sqlite3,sys;sys.path.insert(0,'tools');from pathlib import Path;\
from i18nlib import production_review_v2_lite_queue as q;\
print(sqlite3.connect(str(q.database_path(Path('.')))).execute('select * from meta').fetchall())"
git rev-parse HEAD
```

meta 第 4 列 ≠ HEAD 就先 `python3 -B tools/i18n production queue rebuild`（第 128 批实测 111.9 秒），再开批。

失败的 `batch start` **不会**开出批次，`batch show` 仍是 `{"active": false}`，可以安全重跑；但 `run-host-phase.py` 会因日志已存在而拒绝，先把旧日志连根因 NOTE 挪进 `$D/failed-attempts/`。

**本次交接我已经替你处理了**：文档提交会让 HEAD 从 `7758a2b` 前进一位，所以接手后**先跑一次 `queue rebuild` 再开第 133 批**，不要跳过。

---

## 3. 对旧文的更正

### 3.1 长阶段的起法（旧文 §11 第 1、2 条作废）

旧文写「长阶段用 `nohup ... &` 起，再在有界循环里轮询产出文件」。**这是本次交接期间两次流水线停摆的直接原因。**

`nohup ... &` 放在前台 Bash 里，进程跑完**不会通知宿主**——它静悄悄结束，没有任何东西唤醒我继续。第 129 批因此空转约 36 分钟，第 130 批约 2 小时 40 分钟，四条 lane 一直停在 `prepared`。

正确做法：长阶段用 **Bash 工具的 `run_in_background: true`**，不套 `nohup`。它会在进程退出时重新唤起宿主。旧文第 2 条「不要在 `run_in_background` 里再 nohup 一条链」仍然成立——不要套，直接用。

停摆的另一半原因是流程性的：派发需要 MCP 调用（`create_agent` / `get_agent_status` / `archive_agent`），只有宿主能做。**不要把回合结束在派发或裁决边界上**，那里没有任何后台任务能把你唤回来。

### 3.2 命令名更正

- `batch start` 的参数是 `--limit`，**不是** `--size`。写错会在 argparse 阶段退出码 2，不开批。
- CLI 入口是 `tools/i18n`，**不是** `tools/i18n_cli.py`。后者不存在，退出码 2。

### 3.3 阶段顺序更正（旧文 §3.2 的列表顺序正确，但容易被文件名误导）

`stage_surface.py` 读 `checkpoint['surface']`，`stage_contextual.py` 读 `checkpoint['contextual']`，这两个字段分别由 `surface-export` / `contextual-export` 填充。**未跑 export 就 stage 会炸 `TypeError: 'NoneType' object is not iterable`。**

我在第 131 批同一个错误栽了两次（两层各一次），根因是照着上一批目录里的**文件名**推顺序，而文件名没有先后信息。要复现顺序就读时间戳：

```bash
python3 -c "import json;print(json.load(open('<batch>/<phase>-result.json'))['started_at'])"
```

正确顺序：`batch-start → freeze-workset → surface-export → stage-surface → dispatch-surface-prepare → …（四路）→ close-surface → surface-index → surface-import → contextual-export → stage-contextual → dispatch-contextual-prepare → …（一路）→ close-contextual → contextual-index → adjudication-chain → 发布 → commit → finalize`。

### 3.4 create 事件的响应必须逐字完整

`submit-event.py create` 传的响应文件要是 `create_agent` 返回的**完整对象**，包含末尾那条 `guidance` 字段。我在第 131 批截掉它，被 `LIFECYCLE_FAILED: unknown create payload` 拒绝。拒绝不改状态，补全后重提即可。

---

## 4. lane 覆盖不全：不能只重跑一路（新增，第 132 批实战）

第 132 批第一次派发时，`lane-000-3` 只返回了 20 条中的 19 条（漏 `56197c2085`），顺序无误、无多报，`harvest` 判 `output_valid=false`。

**结论：单路无法重试，任何重试都等于重跑全部四路。** 依据：

- `review_lifecycle.py:691` 要求 `len(members) == 4` 且 `lane_index` 恰为 {1,2,3,4}；
- `:689` 要求四路共享同一 `attempt`/`cycle`/`review_kind`/`task_id`，`:692` 要求同一 `lane_group_identity`；
- `:704` 要求 `attempt == max(attempt)`，`:705` 要求每个成员 `output_valid is True`；
- 而 `stage_surface.py:81` 把 `cycle` 硬编码为 0、没有重试模式，走 attempt-2 就得**手写**带哈希身份的不可变分组清单。

仓库里唯一的重试先例是第 90 批的 contextual `full-001`（`retry_of` 指向 `full-000`），但 `full` 派发根本没有分组清单，不适用于 lane。

既然重新派发的子体数量两条路一样，就走只用既有命令的那条：

```bash
# 四个子体全部先归档（两条路线都需要这一步）
python3 -B tools/i18n production batch abandon      # 实测 225.3 秒
python3 -B tools/i18n production batch show          # 应回到 {"active": false}
```

`abandon` 会把 `prior_effective_state == "queued"` 的条目的 state_override 删掉、清掉 surface/contextual scratch 与 checkpoint。本批未跑 `surface-import`（无 accepted）也未跑 `prepare-evidence`（无 prospective），所以**不需要** `--discard-uncommitted-results` 或 `--restore-evidence`；这两个标志出现就说明状态比你以为的更靠后，先查清楚。

**批次号会复现。** batch_id 由选中条目集派生，abandon 把同样 80 条放回队列后重开，`batch start` 返回的还是同一个 id。所以：
- `evidence/quality/production-batches/$BID-source-workset.json` 不是废弃残留，重开后仍是本批的 workset（第 132 批实测 sha256 前后一致，为 `1a0c4e6b…`）；
- 旧的 `batch<N>-orchestration` 目录要整个改名（我用 `batch132-attempt-1-abandoned/`）并附 `ABANDON-NOTE.json`，否则 `run-host-phase.py` 会因日志已存在拒绝一切阶段。

**预防**：收割完四路、进归档**之前**，先逐路把返回的 identity 序列与该 lane 的 envelope 比对：

```python
exp=[e['entry_revision_identity'] for e in json.load(open(f'.ai/task/{B}/SURFACE-SCREEN-ENVELOPE-{did}.json'))['payload']['entries']]
got=[r['entry_revision_identity'] for r in json.loads(raw.read_text())['results']]
assert exp == got          # 逐位相等，不只是条数相等
```

我在作废那轮是四路都收割完才发现少一条。

---

## 5. 工具边界审计 A–F 的两次修补（新增）

旧文 §7 的 A–F 定义不变。第 128–132 批期间脚本本身被修了四次，每次都是**误报**先出现、修完又暴露出**真缺陷**。现行 `audit-ctx-tools.py` 在 `batch133-orchestration/` 下，带 `--self-test`（14 例），**每批跑审计前先跑自检**。

累计的误报与修法：

| 批次 | 检查 | 误报 | 根因与修法 |
|---|---|---|---|
| 128 | A×8 / B×1 / D×1 | 10 | A：排除路径 `':!*/locales/*'` 自身含 `locales/`。B：子体观察正文里的「以 git grep 排除 locales 后」被当成命令。D：我自己的占位符 `<<HEREDOC-BODY-ELIDED>>` 含 `>>`。修法：扫描前先剥离 heredoc 正文，占位符改成方括号形式 |
| 129 | E×6 | 6 | 脚本沿用了上一批硬编码的批次号，读**本批自己**的输入信封被当成越界。修法：批次号改从同目录 `BID` 文件读——脚手架的 `sed` 只改目录名、**从不改批次号** |
| 130 | D×1 | 1 | Python 里的 `'=>'` 命中重定向正则。修 lookbehind 后暴露**真漏洞**：`2>file` 一直没被检出；再修又让 `2>&1` 误报。终态 `(?<![<=\-])>(?![>=&])` |
| 131 | A×1 | 1 | `grep -v '/locales/'` 的**排除模式**被当成读取。修法：`reads_locale` 先剥离 `grep -v` 参数 |
| 132 | C×10 | 10 | 子体用缩写 commit `624a67329f`，检查只比 40 位全写。缩写也是固定，改为用 `git rev-parse --verify <tok>^{commit}` 实际解析。**第一次改法用子串包含，自检当场抓出真缺陷**——已接受的短前缀 `624a673` 会在**错误** sha `624a67329e` 里命中，等于放行指向别的 commit 的读取。终态：按整词提取 7–40 位十六进制 token，要求**全部**解析到固定 commit 且至少有一个 |

两条教训值得记住：

1. **排除语法为了把东西挡在外面，必然要提到那个东西。** A 和 B 的误报都是这个形状：检查会把「守规矩的证据」本身当成违规。
2. **每次修完检查都补反例自检。** 三次真缺陷（`2>file` 漏检、`2>&1` 误报、短前缀子串命中）全是自检抓的，不是眼睛看出来的。

**B 检查要如实报「有没有样本」。** 第 131 批子体 `git grep` 次数为 0（改用 `git show`/`ls-tree` 加管道 grep），那批 B=0 只说明无样本可拦，不等于拦截生效——我在审计文件里写明了。第 132 批有 3 次 git grep、全部带排除，那才是真样本。

**F 检查的裁量**（旧文已有，第 132 批第一次大规模用到）：contextual 判 OK 而 surface 判 ISSUE 的条目，看它的调用记录判断查没查过。第 132 批 3 条 F（`55dd97e6f9`、`561831ce8e`、`56409ebb77`）全是**裸 OK**（无理由、无出处），按「漏看的 OK 可以直接不采」一律不采。后两条我有独立代码证据，维持 confirmed 并修复；`55dd97e6f9` 另有代码支持中文，按 §6 裁 advisory 不修——**不采 contextual 的 OK 不等于采信 surface 的 ISSUE**，两件事要分开判。

---

## 6. 上游英文与实现矛盾：样本增加到 4 个（对应旧文 §8 第 1 项）

这仍是**第一号未决问题**，不要自行定政策。本次新增三个样本，其中一个是我自己判错后走回来的：

| 批次 | revision | 情况 |
|---|---|---|
| 129 | `5217778cce` | **我先判错。** 我说 `half_talents_cooldown` 让冷却更快、中文「冷却速度减半」写反了。实际链条：`Actor.lua:652` 调 `cooldownTalents(0.5)`，`ActorTalents.lua:1096-1107` 每回合从每个 `talents_cd` 减去该值——每回合只减一半，冷却**持续两倍时长**。中文准确，英文才是不精确的一方。已在裁决结论与提交信息里写明这次走回 |
| 132 | `558ee4ab00` | surface 说中文「命中敌人的远程攻击」凭空加了命中条件；`agility.lua:268` 就是 `if hitted and …`。中文准确 |
| 132 | `55dd97e6f9` | surface 说 `in radius 1` 只限定照亮；`LITE_LIGHT_BURST`（`damage_types.lua:4271`）名字就叫 "Lite Light Burst (radius 1)"，projector 是 `radius=1` 的 ball，先照亮再对范围内敌对单位施加 LIGHT。中文准确 |

三条都裁 `advisory` / `repair_required: false`，理由一致：不把更贴近代码的描述改成更不准的，同时不替用户定政策。

**注意第 132 批 `558ee4ab00` 的特殊处理**：surface 的**具体主张**不成立，但该条目仍然修复——依据是 contextual 层报出的**另一处**缺陷（`excels at close combat` 译作「更适用于近战」取错义项）。两层分开裁决，surface 键 advisory、contextual 键 confirmed。这种「同一条目上一层被推翻、另一层成立」的形态以前没出现过，建议保留分开记的做法。

---

## 7. 新增的缺陷形态与观察（补充旧文 §9）

旧文六种形态不变。第 128–132 批的补充：

- **整族同错**又添两例：`lapis lazuli` 目录 4 行全作「天青石」（正确是青金石；celestite 在游戏英文里出现 0 次，不是撞名而是译错）；`over one million` 的火焰/冰冷两行都漏「超过」，而 `can_gain` 返回的是严格的 `self.nb > 1000000`。
- **「异次元」是反复出现的增译模式**：`mod-tome.lua` 中 3 处，原文均无跨次元设定。第 130 批 `530ce4f980`、第 132 批 `557ed78097` 各撞见一次。
- **跨条术语撞车**（第 132 批，contextual 发现）：同一批内「近战」同时被用于 `attacking in melee`（对）和 `excels at close combat`（错，那是近距离射击）。撞车发生在**同一批的两个条目之间**，比旧文记的「一个中文词被两个英文机制占用」更难察觉，因为两条分在不同 lane。
- **contextual 层确实在挣工钱**：第 130 批四条全部补了 surface 没看到的证据，第 131 批在 `5485c65c37` 上沿调用链上溯一层，给出比我更硬的证据（`class/interface/Archery.lua` 的 `hitted` 分支）。宿主独立研究**不能替代**它。

候选译名要**双向**查冲突，这条继续有效，第 130–132 批每条都做了。

---

## 8. 未决项（旧文 §8 的 5 项全部仍然未决）

一项没动，都需要用户拍板：

1. **上游英文与实现矛盾时跟哪边** —— 样本已增至 4 个，见 §6。
2. **gauntlets 译名是否全目录改** —— 未动。
3. **冻结 matcher 是否加全库字面量回退** —— 未动，我仍建议**不加**。
4. **Elvala 回忆录是否整篇清查** —— 未动。
5. **修改条目的归因汇总工具** —— 未做。

---

## 9. 批外清理待办（在旧文 §10 之上新增）

第 128–132 批记录、**未**清扫的：

- `mod-tome.lua:37961` —— 星辰十字军与第 128 批同一处 `a mean sword`→「华丽的剑技」错误
- `tome-cults.lua:4520` —— `A vaguely humanoid shape`→「模糊的人形生物」，是第 129 批 `526d03c9a1` 的跨组件孪生行
- `high level lure` 七行中的六行（全部漏「高级」；「高级诱饵」全目录出现 0 次），第 130 批只处理了 `mod-tome.lua:23763`
- `mod-tome.lua:27550` —— `Projection of %s` 译作「%s的投影。」，句尾多一个原文没有的句号
- `mod-tome.lua:11157` / `:11158` / `:11213` —— lapis lazuli 另外三行同样作「天青石」，第 132 批只处理了 `:11214`
- `mod-tome.lua:2862` —— Pyromancer 成就同样漏「over」
- `mod-tome.lua` 中 3 处「异次元」

---

## 10. 第 128–132 批结果

| 批次 | batch_id | commit | base | 冻结 | surface | contextual | 裁决 | 门禁 |
|---|---|---|---|---|---|---|---|---|
| 128 | `batch-fb8f4299c68d305b86b8` | `9f2f723` | `d7e41a5` | 80/80 | 74 OK / 6 ISSUE | 6 ISSUE / 0 OK | 12 键全 confirmed，6 条修复 | 17/17 `run.gj2r` |
| 129 | `batch-0c5b965877ccb598ae29` | `3ba1693` | `9f2f723` | 80/80 | 75 OK / 5 ISSUE | 4 ISSUE / 1 OK | 9 键：8 confirmed + 1 advisory，4 条修复 | 17/17 `run.ouqu16xx` |
| 130 | `batch-2a70d57717beaf7508c0` | `6fe46bb` | `3ba1693` | 80/80 | 76 OK / 4 ISSUE | 4 ISSUE / 0 OK | 8 键全 confirmed，4 条修复 | 17/17 `run.ehmc6911` |
| 131 | `batch-c43d7c15fb9b0e5ba609` | `c82a81f` | `6fe46bb` | 80/80 | 77 OK / 3 ISSUE | 3 ISSUE / 0 OK | 6 键全 confirmed，3 条修复 | 17/17 `run.0rbtj3dp` |
| 132 | `batch-1602008c843425c567df` | `7758a2b` | `c82a81f` | 80/80 | 73 OK / 7 ISSUE | 4 ISSUE / 3 OK | 11 键：9 confirmed + 2 advisory，6 条修复 | 17/17 `run.rc4x805k` |

第 132 批的 11 个裁决键覆盖 7 个条目，实际修复 6 条：`55dd97e6f9` 只有 surface 一键、裁 advisory 不修；`558ee4ab00` 的 surface 键裁 advisory、contextual 键裁 confirmed 并修复（见 §6）。其余五条两层或单层均 confirmed 并修复。

核对命令（`disposition` 与 `repair_required` 都在 `adjudications.jsonl` 里）：

```bash
python3 -c "import json,collections;rows=[json.loads(l) for l in open('evidence/production-review-v2-lite/batches/<batch_id>/adjudications.jsonl')];\
print(collections.Counter(r['disposition'] for r in rows), len({r['entry_revision_identity'] for r in rows if r['repair_required']}))"
```

五批全部 80/80 无 MISS，门禁全部 17/17。第 132 批是第二次派发的结果，第一次已作废（见 §4）。

---

## 11. 提交信息里的数字要能被反查

我在第 131 批的提交信息里写了门禁运行号 `run.uz6f9pa9`——**那是编的**，实际是 `run.0rbtj3dp`。在 finalize 之前 `git commit --amend` 修掉了（父节点不变，所以对批次无影响）。

规矩：提交信息里出现的每个运行号、耗时、条数，落笔前从日志里 grep 一次：

```bash
# 编排日志里的（写提交信息时最方便）
grep -o 'run\.[a-z0-9]*' "$D/adjudication-chain.log" | sort -u

# 权威来源是已提交的 gates.json，运行号藏在每个 check 的 log_path 里
python3 -c "import json,re;ch=json.load(open('evidence/production-review-v2-lite/batches/<batch_id>/gates.json'))['result']['checks'];\
print({re.search(r'run\.[a-z0-9]+',c['log_path']).group(0) for c in ch}, sum(1 for c in ch if c['exit_code']==0),'/',len(ch))"
```

注意运行号长度不定（第 128 批就是 `run.gj2r`，只有 4 位），看着像被截断也别自己补。「17/17」的判据是 17 个 check 的 `exit_code` 全为 0，`gates.json` 里没有 `status`/`passed` 字段，别照着不存在的字段数。

同理，「合计 N OK / M ISSUE」要程序化数，不要心算——第 129 批我口头说 74/6，实际是 75/5。

---

## 12. 接手后开第 133 批的最短路径

```bash
cd /workspace/tome4-chinese-translation
git rev-parse HEAD                                        # 本文提交后会比 7758a2b 前进一位
python3 -B tools/i18n production batch show               # 应为 {"active": false}
git status --porcelain                                    # 应只有 ?? .ai/consult/
ls -A .artifacts/i18n/production-review-v2-lite/contextual/   # 应为空（第 132 批的已归档）

# 必做：本文的提交让 HEAD 前进了，先重建队列投影
python3 -B tools/i18n production queue rebuild            # 实测约 112 秒

# 脚手架已搭好，直接开批
D=.artifacts/i18n/batch133-orchestration
python3 -B "$D/run-host-phase.py" batch-start timeout -k 10s 900s \
  python3 -B tools/i18n production batch start --limit 80
# 拿到 batch_id 后写进 $D/BID，再跑一次审计脚本自检
printf '%s\n' "$BID" > "$D/BID"
python3 -B "$D/audit-ctx-tools.py" --self-test            # 应 PASS 14 cases
```

`$D` 里已备好 10 个文件（7 个脚本 + 2 个 profile 模板 + 1 份 profiles 实况快照），`prior-batch-runtime-scratch/` 已放好第 132 批的暂存与 NOTE，`failed-attempts/` 空目录已建。审计脚本要读同目录的 `BID`，所以自检必须在写入 `BID` 之后跑。

然后按 §3.3 的顺序从 `freeze-workset` 往下。
