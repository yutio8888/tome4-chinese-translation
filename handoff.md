# 翻译审核主编排者 —— 交接说明

最后更新：2026-09-11（第 87 批后）· 分支 `develop`

接手前请先读完本文，再读 `docs/baseline-batch-runbook-2026-09-06.md`（详细操作手册）
与两份契约 `docs/paseo-translation-surface-screen-v1-contract.md`、
`docs/paseo-translation-context-review-v2-contract.md`。本文只写手册里没有、
或者踩过坑才知道的部分。

---

## 1. 角色与常驻授权

维护者（yutio8888）已授权**连续主持**，不必逐批确认：

- 每批 80 条，完成 finalize + 修复 + push 后**立即开下一批**
- 跨批次的专名／术语记为 `pending` 返回给维护者，但**不阻塞推进**
- 「一并修改发现的同类问题」是常驻指令
- 全库清扫另开**有界维护窗口**，不混进正常批次的修复

> **当前状态：运行中。** 维护者 2026-09-10 指示「从 77 批开始接手主持」，
> 连续主持授权恢复；第 77–79 批已完成并推送，随时可开第 80 批。
>
> 维护者本轮新增指令：**交叉复核后仍无法从源码判定如何处置的条目，记 `pending`
> 交回维护者人工裁决**（`pending` 会把队列状态置 `blocked`，保证日后重新浮出）。

---

## 2. 现在停在哪

| 项 | 值 |
|---|---|
| 最后完成批次 | 第 87 批 `batch-9762ac4184dbef00478c`（已 push，evidence `d7b5cf4`／修复 `770a145`） |
| 累计批次证据 | `evidence/production-review-v2-lite/batches/` 共 125 个 |
| 当前 catalog | `0d057aef…`（29828 条目 / 480 排除 / 30308 occurrence） |
| 最后 migration | `abf9e56f…`（revision_changed 10） |
| 活动批次 | **无**（可以安全提交） |
| 工作树 | 干净，仅 `.ai/consult/` 未跟踪（三模型咨询存档，未入库是有意的） |

审核进度（第 85 批后 `queue rebuild` + `queue check`，2026-09-11，`ok: true`）：

| 项 | 条数 |
|---|---|
| 条目总数 | 29828 |
| 尚未覆盖（`implicit_queued`） | 21274 |

按 80 条一批算，剩余约 **266 批**。

> 队列数不是简单的「减 80」。第 85 批 21498 → 21420 = −80 + 2：80 条审完出队，
> 其中 2 条需修复、以后继重新入队；同批另有 14 条被维护者裁定改动的条目**本就在队列里**，
> 它们的后继是**替换**原条目，净增 0。
> 第 86 批 21421 → 21342 = −80 + 1（`Foursaw` 修复在开批前把队列从 21420 推到 21421）。
> 第 87 批 21345 → 21274 = −80 + 9：migration 产生 10 条后继，其中 9 条是本批刚审过、
> 因修复重新入队（净增 9）；第 10 条（`and offered to her dark Master`，同类变体）
> 本来就在队列里未审，后继是替换，净增 0。
> **差值必须能被独立算式导出**，「少了 71」本身不含信息。

> ✅ **容量阻塞已解除（2026-09-11，`b3da9f8`）。** 上限由 128 MiB 改为带版本的
> 512 MiB 政策，第 86 批后已用 **23.0%**、余量 **394 MiB**，够约 **479 批**，
> 而剩余待审 267 批。详见 §13。

> **工作区是与一个优化者 agent 共享的**（`2577f8ff-95f4-432a-9b1e-68ae9559570c`，
> opus 5）。它在 `/workspace/tome4-opt-1`（分支 `perf/merge-cli-steps`）的 git worktree
> 里开发流水线提速，**只在批次间隙回主工作树做验收+合并**。协议见 §12。
> 每批开始／关闭都要主动给它发消息划出只读窗口——批次期间它一提交，批次就锁死。

**恢复工作的第一步**永远是 `queue rebuild` + `queue check`，确认没有漂移。

---

## 3. 一个批次的完整顺序（顺序错了会锁死）

```bash
B=$(python3 -c "import json;print(json.load(open('.artifacts/i18n/production-review-v2-lite/active-batch.json'))['batch_id'])")

python3 -B tools/i18n production queue rebuild && python3 -B tools/i18n production queue check
python3 -B tools/i18n production batch start --limit 80
TOME_ENGINE_ROOT=/workspace/t-engine4 TOME_DLC_ROOT=/workspace/tome4-dlcs \
  python3 -B tools/orchestration/freeze_workset.py $B          # 必须 80/80
python3 -B tools/i18n production batch surface-export
python3 -B tools/orchestration/stage_surface.py $B --out /tmp/plan-$B.json
python3 -B tools/surface_screen_manifest.py check .ai/task/$B/SURFACE-SCREEN-GROUP-group-000.json
python3 -B tools/orchestration/dispatch_surface.py /tmp/plan-$B.json /tmp/kids-$B.json
#   …等 4 个 child 全部 idle…
python3 -B tools/orchestration/harvest_reviews.py /tmp/kids-$B.json /tmp/raw-$B
git status --short                                             # 证明 reviewer 未写入
python3 -B tools/orchestration/close_review_tasks.py surface /tmp/plan-$B.json /tmp/kids-$B.json /tmp/raw-$B
python3 -B tools/orchestration/build_import_index.py surface /tmp/raw-$B /tmp/idx-$B.json
python3 -B tools/i18n production batch surface-import --input /tmp/idx-$B.json
#   有 ISSUE 才继续：
python3 -B tools/i18n production batch contextual-export
python3 -B tools/orchestration/stage_contextual.py $B --out /tmp/ctx-$B.json
python3 -B tools/orchestration/dispatch_contextual.py /tmp/ctx-$B.json /tmp/ctxkids-$B.json
#   …等 child idle…
python3 -B tools/orchestration/harvest_reviews.py /tmp/ctxkids-$B.json /tmp/ctxraw-$B --key verdicts
python3 -B tools/orchestration/close_review_tasks.py contextual /tmp/ctx-$B.json /tmp/ctxkids-$B.json /tmp/ctxraw-$B
python3 -B tools/orchestration/build_import_index.py contextual /tmp/ctxraw-$B /tmp/ctxidx-$B.json
python3 -B tools/i18n production batch contextual-import --input /tmp/ctxidx-$B.json   # 必须在 adjudicate 之前
python3 -B tools/orchestration/make_adjudication.py /tmp/spec-$B.json /tmp/adj-$B.json
python3 -B tools/i18n production batch adjudicate --input /tmp/adj-$B.json
python3 -B tools/i18n production batch prepare-evidence                                # 内含 17 项门禁
cp -r .artifacts/i18n/production-review-v2-lite/prospective/evidence/production-review-v2-lite/batches/$B \
      evidence/production-review-v2-lite/batches/$B
git add … && git commit                                        # evidence commit
python3 -B tools/i18n production batch finalize --commit <上一步的完整 40 位 sha>
#   —— 到这里批次才算关闭，之后才允许改译文和提交别的东西 ——
<应用修复，先不提交>
bash tools/ci-gates.sh
python3 -B tools/i18n production authoritative-catalog build --output .artifacts/i18n/authoritative-catalog-<N> --json
python3 -B tools/i18n production queue rebuild                 # HEAD 前进过就必须做，否则 plan 报漂移
python3 -B tools/i18n production migration plan  --candidate-catalog <上面的目录> --output .artifacts/i18n/migration-<N>.json
python3 -B tools/i18n production migration check --input <migration json> --candidate-catalog <目录>
python3 -B tools/i18n production migration apply --input <migration json> --candidate-catalog <目录>
cp <目录>/evidence/production-review-v2-lite/catalog/{entries.jsonl,exclusions.jsonl,manifest.json} \
   evidence/production-review-v2-lite/catalog/
cp .artifacts/i18n/migration-<N>.json evidence/production-review-v2-lite/migrations/<migration_id>.json
bash tools/ci-gates.sh
git add … && git commit                                        # 单条修复提交
python3 -B tools/i18n production queue rebuild                 # 唯一校验 migration↔catalog 绑定的环节
git push origin develop
```

### 顺序上最容易犯的三个错

1. **`contextual-import` 必须在 `adjudicate` 之前**，否则 `make_adjudication.py`
   报「spec 缺这些观察的裁决」。
2. **批次进行期间（`batch start` 到 `finalize` 之间）不得向 develop 提交任何东西**，
   连纯文档也不行。HEAD 一旦不等于冻结的 `base_commit`，
   `surface-import`／`contextual-import`／`adjudicate` 甚至 `batch abandon` 全部报
   `active batch catalog/base commit drift`，批次锁死。
   （唯一例外是 evidence commit，它在 adjudicate 之后、finalize 之前，是流程的一部分。）
3. **任何让 HEAD 前进的提交之后都要 `queue rebuild`**，否则下一步报
   `queue database meta/catalog/evidence-head drift`。

### 一次事故换来的规矩

`bash tools/ci-gates.sh` 的 **17 项门禁不校验 migration 与 catalog 的绑定关系**。
曾经出现过：改了 addon 组件
→ 重建 catalog → 只 diff 了 `entries.jsonl` 就以为 migration 不受影响 →
用新 catalog 覆盖了 `exclusions.jsonl`，`catalog_id` 变了而 migration 里的
`new_catalog_id` 还指向旧值。**17 项全绿，问题完全没被发现**，而且**无法用后续提交修复**。
所以每次修复提交后的 `queue rebuild` 不能省。

> **本文原先在此处写的「只有 `queue rebuild` 会走 `_validated_migration_edges`」是错的**
> （2026-09-11 证伪，另见 runbook §41）。该函数在 `_projection_contents:661` 无条件执行，
> 而 `_projection` 被 `strict_check`（`queue.py:958`）、`rebuild`（:925/:936）、
> `check`（:966）共同调用——**每个 batch 子命令的 preflight 都会走它**。
> 错的只是「只有它」这半句；「17 项门禁不查这层」仍然成立，事故本身也确实发生过。
> `queue rebuild` 不能省的真正理由是 `meta/catalog/evidence-head` 漂移：
> HEAD 前进而 `queue.sqlite3` 没跟上，下一个 writer 一来就报错。

---

## 4. reviewer 派发

| 轮次 | 契约 | 模型 | thinking | mode | 并发 |
|---|---|---|---|---|---|
| 表层筛查 | `translation_surface_screen_v1` | `codex/gpt-6-astra` | `xhigh` | `auto` | 4 lane × 20 |
| 交叉复核 | `translation_contextual_v2` | `claude/claude-opus-5` | `xhigh` | `bypassPermissions` | 1 lane，只跑 ISSUE |

2026-09-10 维护者裁定的配置。三个开关都可用 `--provider/--thinking/--mode` 覆盖。

**换 provider 就必须换 mode**：`auto` 是 codex 侧模式名（Paseo 归一为 `auto-review`：
workspace-write、无网络、符合条件的审批交给 auto-reviewer 子 agent 而不弹给编排者）；
claude 侧对应 `bypassPermissions`。claude 默认的 `default`（Always Ask）会让 child
首次用工具时弹权限框并**无限挂起**，编排者只看到 status 长期不变。

**不要用 codex 的 `full-access`**：该模式的说明含「访问网络」，`batch-4fec420d`
的 reviewer 据此 `curl` 了 GitHub 上 tome-base 的 master 分支取源码，
而不是钉住的 1.7.6，属违约，该次输出作废重发。

### 等待 child 的正确姿势

CLI 直派**拿不到** Paseo 的权限通知（MCP `create_agent` 才有）。凡是可能弹窗的模式，
等待器必须自己轮询 `paseo agent inspect` 的 `PendingPermissions` 字段
（注意：文本输出才有该字段，`--json` 是另一套结构，没有这个键）。
`/tmp/wait_agent.sh` 是这个用途的脚本，**不在仓库里**，接手后需要自己重建：

```bash
AID="$1"; MAX="${2:-3600}"; T=0
while [ $T -lt "$MAX" ]; do
  OUT=$(paseo agent inspect "$AID" 2>&1)
  ST=$(echo "$OUT" | awk '/^Status/{print $2}')
  PERM=$(echo "$OUT" | sed -n 's/^PendingPermissions *//p' | tr -d ' ')
  if [ -n "$PERM" ] && [ "$PERM" != "[]" ]; then
    echo "PERMISSION_BLOCKED after ${T}s: $PERM"; exit 2
  fi
  case "$ST" in idle|closed|completed|error|failed) echo "STATUS=$ST after ${T}s"; exit 0;; esac
  sleep 10; T=$((T+10))
done
```

**不要**写 `while pgrep -f "<命令片段>"` 这种等待循环——`pgrep` 会匹配到等待循环
自己的命令行，形成自死锁。用文件里出现的哨兵字符串判断，或者用上面的 agent 轮询。

---

## 5. 裁决标准

`disposition` ∈ `{confirmed, pending, advisory, refuted}`：

- `pending` → 队列状态置 `blocked`，保证以后还会浮上来
- `advisory` **不会**重新入队，等于一次性放过
- 其余两个进入正常后继

### 第 23 条：两轮各自独立复现同一主张才算 confirmed

「同一主张」指理由也相同。两轮都报 ISSUE 但理由不同 ⇒ advisory。

**两轮一致是升级门槛，不是核实豁免。** 第 76 批就有实例：两轮都说
`Escort: %s (level %s)` 漏译了 `level` 标签，但查源码发现 `level_name` 由兄弟条目
`t("%s of %s", "%s的第%s层", "tformat", {2,1})` 渲染，运行时输出
「护送：炼金术士 (巨魔沼泽的第3层)」，标签根本没丢，补译反而冗余 → 判 `refuted`。

### 单轮也可以 confirmed 的情形

机械／客观事实，且有强独立证据：标点、标记与占位符绑定、句法主语、量词依附、
明确限定语的漏译。语义／风格判断则必须两轮都有。

### 已生效的裁定（不要重复上报）

| 项 | 裁定 |
|---|---|
| `yeek` | 保留「夺心魔」，**不再重复上报** |
| `delving` | 「挖掘之」 |
| orcs-lore `herbal infusions` | 「草本纹身」 |
| `Arcane Combat` | 「奥术格斗」 |
| `The Deep Bellow` | 「深渊咆哮」 |
| `Ritch Flamespitter` | 「喷火里奇」 |
| `force` | 「威能」 |
| `damage affinity` | 「伤害亲和」（护盾吸收的 10 处仍作「伤害吸收」） |
| `Damage Shield` | 「伤害护盾」 |
| `Zemekkys` | 「泽梅基斯」 |
| `Animated Sword` / `Distorted Animated Sword` | 「活化之剑」／「扭曲活化之剑」 |
| `Rimebark` | 保持「召唤：雾凇」，**不修改** |
| 召唤系技能 | 统一前缀「召唤：」 |
| `zone` / `level` | 「地图」／「楼层」 |
| `%d%%` / `%0.2f` | 武器基础伤害百分比／固定点数 |
| 换行结构不镜像 | **一律 advisory** |
| 顶层单引号 | 译作「" "」，嵌套用「' '」 |
| UI 选项名 | 保留 ASCII 引号 |
| 纯中文括号 | 全角 |

### 原「每批复现的四项」已全部落地（2026-09-11 核实，此前本文档在此处是陈旧信息）

`honey tree`→「蜂蜜树」、`Warden's Focus`→「守卫者专注」、`farportal`→「远行传送门」
（全库「远古传送门」**0 处**）已由 `fbcf0aa` 改完；`Kryl-Feijan`→「克里尔·费扬」
由 `07e8656` 改完。**四项都不再是挂起项，不要按旧表复述。**

> 我在第 84 批照旧表复述过一次才发现表是过期的。凡引用本节的表，**先 `grep` 现状再说话**。

### 全库术语项 `Warden`：维护者已裁定**不调整**（2026-09-11）

第 84 批交叉复核提出 Paradox Plane 语境下 Wardens 应作「守望者」。
维护者裁定**保持现状**——`Warden` 在 `mod-tome.lua` 共 31 处，继续作「守卫」／「时空守卫」。
**这条已结案，reviewer 再提就照此判，不要重新上报维护者。**

---

## 6. 关键机制（踩过坑才知道的）

### engine/I18N.lua 的 tag 语义

`set(table, key, tag, value)` 会**同时**写 `table[tag][key]` 和 `table["nil"][key]`；
`get()` 先试 `table[tag][key]`，取不到就回落 `table["nil"][key]`。

推论：**tag 不匹配、文件归属过时都不会让条目失效**，只有源串不同才会。
判定死键的唯一标准是「源文本在钉住的源码树里找不到」。

### 钉住的源码树

- 本体 `/workspace/t-engine4` @ `624a67329fe2ad440c5b344785a9c73fcf22ae63`（1.7.6）
- DLC `/workspace/tome4-dlcs`
- 搜索必须同时覆盖 `.lua` **和 `.chat`**，并排除 `locales/` 目录

### 组件集合

catalog 的 6 个：`engine.lua`、`mod-boot.lua`、`mod-tome.lua`、
`tome-ashes-urhrok.lua`、`tome-cults.lua`、`tome-orcs.lua`。

**全库清扫必须覆盖 11 个**，另加 `mod-example.lua`、`mod-example_realtime.lua`、
`tome-addon-dev.lua`、`tome-items-vault.lua`、`tome-possessors.lua`。
漏掉 example 组件会被 `06-runtime-collision-scan` 拦下——这个错犯过两次。

### 修复必须跨组件同步

同一个 runtime key 可能同时存在于 `mod-tome.lua` / `tome-cults.lua` / `tome-orcs.lua`。
**改之前先全仓库 grep**，只数 mod-tome.lua 内的副本会漏。

### 死键登记

`evidence/production-review-v2-lite/known-dead-keys.json` 登记了 26 个死键
（29828 条扫描而得；另有 86 条 `.always_merge`、50 条运行期拼接、
24 条宿主生成键判定为可达而排除）。维护者裁定「保留，但登记为失效，不再审核」。

注意实际效果的边界：**流水线没有把指定的活条目移出审核轮转的机制**，
这份登记的真实作用是「不要再修这些」，不是「不要再审这些」。

### 单批耗时构成（2026-09-10 实测）

**已于 2026-09-11 优化，下表为第 81 批实测的现值：**

| 步骤 | 优化前 | 现值 |
|---|---|---|
| `surface-export` / `surface-import` | 320 s | **161 / 162 s** |
| `contextual-export` / `contextual-import` | 327 / 344 s | **161 / 162 s** |
| `adjudicate` / `finalize` | 同上量级 | 162 / 163 s |
| `batch start` | 528 s | **~175 s**（`263aa42` 后，见下） |
| `prepare-evidence`（含 17 项门禁） | — | 243 s |
| `queue rebuild` | 157 s | 161–163 s（未动，每批两次） |
| `bash tools/ci-gates.sh` 17 项 | 82 s | 77 s（每批两次） |
| 表层筛查 4 个 child | 约 1 min | 约 1 min |
| 交叉复核 1 个 child | 80–100 s | 150–240 s |

提速来自 `3575d72`：`preflight` 原本把整段证据历史重放**两遍**
（`_reconcile_checkpoint` 一次，`_reconcile_phase_tuples → queue.strict_check` 又一次），
现在 `strict_check` 接受调用方已算出的投影，复用前用 `_head` 重解析证据提交，
不同就照旧完整重放。**`_validated_migration_edges` 在 `_projection_contents:661` 内部，
复用的投影本身已跑过它，是不重复跑而非跳过**——这一点接手时值得自己再验一遍。

`batch start` 原先是例外（481–530 s）：它在入口处没有 active checkpoint，该路径上有
**三次**完整重放（`_restore_orphans` 的 `_projection`、`preflight` 尾部与 `start` 自身的
两次 `strict_check`），`retry_blocked` 再加一次。`263aa42` 让 `preflight` 只重放一次，
经新增的 `projection_out` 交给同进程里继续的 `start`。同环境对照实测
528.1 s（replays=3）→ 173.3 s（replays=1）。

`authoritative-catalog build` 实测两次各 **3 s**（本文原记 ~3 min，是错值）。
我一度猜是缓存命中，已证伪：该命令不跑投影，且 `git_evidence_reader.projection_scope`
每次新建 reader、退出即清空 blobs/trees/derived（`git_evidence_reader.py:41-52`），
不存在跨调用缓存。

门禁里真正扫全库的几项（06 碰撞扫描、08 术语静态审计、12 addon 构建）**全在 1 秒内**，
80% 时间是两个 Python 单元测试组（`03-toolchain` 26 s、`05-production-shadow` 33 s），
与库规模无关。**要压时间应该动 `preflight` 和 catalog build，不是门禁。**

---

## 7. 挂起中，等维护者裁定

1. ~~**`Foursaw the Clown` 墓志铭**~~ —— 维护者 2026-09-11 选定方案 A
   （小丑先觉／我们笑着／直到察觉／笑话已经结束），已落地并 push。**已结案。**
   附带结论：换行**不需要破例**，同墓园其它墓志铭本就逐行镜像，只有这条压成一行。
2. ~~**标记内多余空格清理**~~ —— 真正有视觉后果的 2 条高亮范围错位
   **已于 2026-09-11 获授权并修复**（`b2180f8`）。其余「291 处」的结论本就站不住（见下）。
   此项**已结案**。
3. **工具链：跨进程投影记忆**（第 5 项）—— 维护者已**批准**两项不新增信任的算法修正
   （第 6 项，2026-09-11）；这一项仍未裁定。详见 §13 末节。
4. ~~**`crypt` 译名**~~ —— 三方交叉咨询后维护者 2026-09-11 裁定**统一为「地宫」**，
   全库 25 处已改并 push（`41b819f`）。**已结案**，详见 §17。
5. **交叉复核的 `OK` 是否要求附理由**（2026-09-11，第 87 批引出）——
   契约下 `ISSUE` 必须带 `observation`，`OK` 只有 `revision_key` + `verdict` 两个字段。
   后果是**一个无理由的 `OK` 可以单向否决一条有证据的表层观察**。
   第 87 批 `22c6b53397` 已因此判 advisory，未修复。详见 §18。

> 原第 3 项「是否立项优化 `preflight` / `authoritative-catalog build`」已由优化者
> 落地三项（`3575d72` / `263aa42` / `208a42f`），不再挂起。

### 关于「标记内多余空格」，我先前的报告是错的

初次统计说「全库 291 处、闭标记侧 0 处、系统性单向错误」。逐条核实后：

- 291 处 → 与源文同位置比对后只剩 **93 处**（其余源文同名标记后本来就有空格）
- 93 处里 **42 处在闭合标记**（`#WHITE#`/`#LAST#`）后，那是中西文间隔空格，**本来就对**
- 剩 51 处在开标记后（16 条条目），但**着色的空格与不着色的空格渲染完全一样**，
  运行时没有任何视觉差异

所以「291 处系统性错误」站不住。真正有视觉后果的是**高亮范围错位**
（高亮短语的一部分漏在标记对之外），全库扫描只找到 **2 条**：

| revision | 组件 | 问题 |
|---|---|---|
| `d653c5ae9b` | `mod-tome.lua` | `#GOLD#special skeleton talents#WHITE#` → `#GOLD# 骷髅#WHITE# 技能`，「技能」漏在高亮外且漏译 `special` |
| `e15a6a3018` | `tome-orcs.lua` | `#LIGHT_GREEN#Undead Drake talents#LAST#` → `#LIGHT_GREEN#亡灵龙系#…#`，「技能」漏在高亮外 |

这两条与第 76 批已修的 `1613f08b`（食尸鬼版本）是同一个 bug 家族。
**扫描脚本没有入库**，逻辑见本文档 git 历史或重写（要点：按标记切分，
区分开标记与复位标记，并与源文同位置比对，不能只做模式匹配）。

维护者 2026-09-10 指示「先暂停修改同类问题」，故这两条未修。

---

## 8. 杂项

- `.ai/consult/` 下是三模型（Gemini / GPT / Fable 5.1）咨询的**冻结证据包**，
  刻意不含任何既往 finding，以免污染独立判断。未跟踪入库是有意的。
- 咨询用的 Fable 5.1 agent 共 3 个，均已 `closed`，无残留。
- `.pi/agent/models.json` 会被 provider 目录同步自动改动，与翻译无关，
  遇到时**单独成一条提交**，不要混进批次提交。
- 维护者纠正过我一次：Robert Zemeckis 的通用译名是「罗伯特·泽米吉斯」而非「泽梅基斯」；
  但游戏里的 `Zemekkys` 拼写不同，最终裁定仍取「泽梅基斯」。

---

## 9. 第 77–79 批完成记录（2026-09-10，接手后第一轮）

每批 80 条、4 lane 表层筛查（`codex/gpt-6-astra` xhigh `auto-review`）＋ 1 个交叉复核
child（`claude/claude-opus-5` xhigh `bypassPermissions`）、源码工作集 80/80、
17 项门禁两次全绿、evidence commit + finalize + 单条修复提交 + `queue rebuild` + push。
15 个 child 全部有效并已确认归档。

| 批次 | 来源 | evidence | 裁决 | 修复（migration） |
| --- | --- | --- | --- | --- |
| 77 `batch-e4b82b57…` | tome 80 | `33e7fbf` | confirmed 4、advisory 2、refuted 1 | 2 条（`e787a4ac`） |
| 78 `batch-cbe7e6c7…` | tome 80 | `4ab9bf0` | confirmed 10、advisory 1 | 11 条（`ad66c2c6`） |
| 79 `batch-bd59b69a…` | tome 78 + engine 1 + boot 1 | `de9a385` | confirmed 4 | 2 条（`fdc71d7a`） |

修复内容：77 批删掉 Misdirection 里源文不存在的增写句并把「周围」改回「相邻」、
改正毒物系说明；78 批巨魔 hide 归属与 warty、沉眠 suddenly、维网灵晶感知动词、
巫妖面具漏译 lichdom、兽人 harsh tongue 共 11 条（含 boot/engine 跨组件同步）；
79 批 Repulsion 技能名改「盾牌排斥」（原「盾牌猛击」与 Shield Pummel 的抗性日志撞字）、
Epoch 外观描述。

本段新增判例：

- **跨组件同 runtime key 在修复阶段才会暴露**：巨魔 desc 同时存在于 `mod-tome.lua`／
  `engine.lua`／`mod-boot.lua`，只改一处会被 `06-runtime-collision-scan` 拦下——
  这说明「先全仓库 grep」必须在改之前真的执行。
- **同型条目的同步**：`mumbles in a harsh tongue` 在本库 6 处，其中 2 处已作
  「刺耳的语言」；修复时把剩下 4 处（同一缺陷）一并同步，属「同类问题一并修改」，
  不视为全库清扫。
- **两轮一致但不与源码相符仍可 refute**：77 批 `#CADET_BLUE#Equipping %s with %s` 被
  表层报「语义颠倒」，但源码 `artifice.lua:49` 为 `player.artifice_tools[chat_tid] = tid`
  （工具被装入 artifice 槽），译文「将 [工具] 装备至 [artifice]」方向正确 → `refuted`。

---

## 10. 第 80 批完成记录（2026-09-11）

`batch-fa5522f26b0d131bec00`，tome 80 条单来源（1 run，`task_id == batch_id`）。
表层 4 lane × 20（`codex/gpt-6-astra` xhigh `auto`）报 4 条 ISSUE；交叉复核 1 child
（`claude/claude-opus-5` xhigh `bypassPermissions`）判 3 ISSUE + 1 OK。
源码工作集 80/80、17 项门禁两次全绿、5 个 child 全部有效。
裁决 confirmed 6（3 条 × 两轮）、advisory 1；修复 3 条（migration `441a4500`）。

| 条目 | 问题 | 处置 |
| --- | --- | --- |
| 祭坛腐化心脏日志 | shakes 误作「跳动」、丢失 vibrating／new、增写「最终被腐化」的完成结论 | confirmed，改「心脏干瘪、抖动，因新的堕落力量而震颤」 |
| `arcane powered` 任务目标 | 能量来源属性误作强度「强力」 | confirmed，统一为同任务已有的「充满奥术力量的神器」 |
| Nightsong 外观 | 漏译 `unadorned`、`tendrils` 抹平为「黑暗」、增写「无尽」 | confirmed，改「没有任何纹饰……黑暗的触须攀附其上」 |
| `#Target# is less protected.` | 比较级被译作绝对的「不再被保护」 | **advisory**，见下 |

本段新增判例：

- **「运行时无事实错误」不足以 refute，「两轮不一致」才是 advisory 的依据。**
  `less protected` 是 `EFF_STONE_LINK` 的 `on_lose`，该效果把目标所受全部伤害重定向给
  施术者（`physical.lua:3692-3705`），效果结束时保护确实完全消失，故「不再被保护」
  运行时不假；但源文的比较级与同块 `STONE_LINK_SOURCE` 的 `"no longer protecting
  anyone."`（本库作「不再保护任何人」）构成有意对照，译文把 `less` 与 `no longer`
  同归「不再」，抹平了该对照——表层的主张本身**成立**，只是没被第二轮复现。
  claim 成立但未获两轮复现 ⇒ `advisory`；只有源码**反证** claim 时才 `refuted`
  （对比第 76 批 `Escort: %s (level %s)` 与 77 批 artifice 两例）。
- **同库既有译法是交叉复核最有用的独立证据。** 本批 2 条 confirmed 的决定性依据
  都不是词典义，而是库内不一致：`arcane powered` 在同一任务函数上一行已作
  「充满奥术力量的神器」；`tendrils` 在 `mod-tome.lua:12539-12544`／`24120-24121`
  一律作「触须／卷须」。这类证据可机械复核，比语感判断可靠得多。
- **术语改动不搭便车。** 本条心脏日志所在事件簇里 `corrupted` 一律作「腐化」
  （`mod-tome.lua:39107/39109`），而本串的 `corrupt forces` 作「堕落力量」
  （术语表 `corruption`→堕落）。两者不算冲突，且**没有任何一轮报过**，
  故修复时原样保留——「一并修改同类问题」指同一缺陷的其他实例，
  不是给同一条串附加未经裁决的改动。

---

## 11. 第 81 批完成记录（2026-09-11）

`batch-887b6eab00682b1aa283`，tome 80 条单来源。表层报 7 条 ISSUE，交叉复核 5 ISSUE + 2 OK。
源码工作集 80/80、17 项门禁两次全绿、5 个 child 全部有效。
裁决 confirmed 10（5 条 × 两轮）、advisory 2；修复 5 条（migration `1a8a3e85`）。

| 条目 | 问题 | 处置 |
| --- | --- | --- |
| `insignia ring`（Exiler 未鉴定名） | insignia 是徽记／纹章，误作「荣誉」，且未鉴定外观名被写成神器式命名 | confirmed →「徽记戒指」 |
| Exotic Weapons Mastery | 漏译 `weapon` 限定，被读成全局伤害加成 | confirmed →「增加 %d%% 武器伤害」 |
| 阳光烈焰致盲范围 | 丢掉作为圆心的 `the target`，`everyone` 错限为「敌人」 | confirmed →「目标及其周围半径 2 以内的所有单位」 |
| 时空法师 `locked_desc` | 祈使指引被改写为第三人称陈述，`outside` 译反 | confirmed → 重译两句 |
| Blighted Summoning 解锁条件 | `may`／`more` 的不确定限定被绝对化 | confirmed →「更为持久的召唤物可能会被计为多于 1 个」 |
| `has survived the set up` | 「恢复了平衡」未表存活义 | **advisory**（交叉判 OK，见下） |
| kor-pul lore 多一处换行 | 换行总数 4 → 5 | **advisory**（既有裁定） |

本段新增判例：

- **「效果自身的 long_desc」可以为译文背书。** `#Target# has survived the set up.` 是
  `EFF_SET_UP` 的 `on_lose`，而该效果 `long_desc` 开篇即 `The target is off balance…`
  （`physical.lua:1631-1640`），故「恢复了平衡」与运行时状态相符，不是事实错误。
  与第 80 批 `less protected` 同型：**单轮 ISSUE + 交叉 OK + 源码不反证 ⇒ advisory**。
  这类「译文换了视角但仍锚定同一机制」的情形，去 `long_desc` 找锚点比查词典有用。
- **投射目标的 `friendlyfire` 缺省值决定描述范围。** 阳光烈焰的 `target2` 只写了
  `selffire=false`，**没写** `friendlyfire=false`，所以除施法者外队友与召唤物都会被致盲，
  原文的 `everyone` 是字面准确的。审 AoE 描述时要连 `friendlyfire` 一起看，
  只看 `selffire` 会把「所有人」误判成「敌人」。
- **解锁条件类文本要去数源码的写入点。** `More permanent summons may count as more than 1.`
  的真假取决于 `summoned_times` 的全部写入点：全库仅三处，魔像计 99、暗影与巫妖各计 1。
  绝对化译法之所以 confirmed，不是因为丢了 `may`，而是因为**与源码计数直接矛盾**。

### 一条本该早就套用的规矩

第 80 批收尾那条**纯文档提交**（handoff 更新）之后没有补 `queue rebuild`，
`queue.sqlite3` 的 `evidence_head` 就停在了上一个提交，下一个 writer 一来就报
`meta/catalog/evidence-head drift`。§3 的第 3 条写的是「任何让 HEAD 前进的提交之后」，
**文档提交也算**——别把它当成只适用于批次流程内的步骤。

---

## 12. 第 82 批完成记录与「共享工作区」协议（2026-09-11）

`batch-21c7c16c405ef0b9bc35`，tome 80 条。表层 7 ISSUE，交叉复核 6 ISSUE + 1 OK。
裁决 confirmed 11、advisory 1、**pending 1**；修复 6 条（migration `473d5cf8`）。

修复：诱饵说明（`is very durable` 漏译、`some` 丢失并增写「自动」、
`check individual trap descriptions` 误作「可鉴定」）、`Arcane Might`→「奥术伟力」、
Sanctity 法阵作用对象「敌人」→「其他所有生物」并统一「阵法」为「法阵」、
Kryl-Faijan 遭遇 `door`→「活门」改回「门」、Master Jeweler 成就「使用利米尔」
与任务名「失落的知识」、女武神盾整句重译。

### 本批的 pending（等维护者裁定）

`underground crypt` 译作「地窖」。词义上确实丢了墓葬义，但全库对 `crypt` **已经有两套
译名**：「地窖」（`mod-tome.lua:7157`／`:7194`）与「地穴」（`:7395`）。单改一条只会
让不一致更碎，要改得跨条目统一——属专名裁定，故 `pending`。

### 判例

- **同一条目两轮报不同理由时，仍可对其中一条单独 confirm。** 本批 `1d8c741e15`
  表层报 `crypt`→地窖，交叉报 `door`→活门，是两个不同主张。第 23 条的
  「理由不同 ⇒ advisory」管的是**同一主张**能否升级，不意味着整条作废。
  `door`→「活门」属机械客观事实且有强独立证据（「活门」是本库为另一遭遇 `trap door`
  保留的译名；**同一遭遇的下一句** `:7193` 已正译为「这扇门」），按单轮可 confirm 处置；
  `crypt` 那条另记 pending。
- **改译名前先数库内分布。** 本批三处决定都靠计数落地：`crypt` 有两套译名（→ pending）、
  「马基·埃亚尔大陆」10 处 vs「世界」1 处（→ 改）、「法阵」19 处 vs「阵法」2 处（→ 改）。
  `might`→「伟力」也是先找到库内先例（`:4779` 泰勒斯的伟力）才定的。
- **不给同一条串附加未经裁决的改动。** 诱饵说明里 `attracts all creatures` 也被译作
  「敌人」，与本批已 confirm 的 Sanctity 缺陷同型，但**两轮都没报**，且我未能从源码
  确认 Taunt 是否分阵营，故未改。

### 共享工作区协议

工作区与优化者 agent 共享，靠消息对时不可靠（我第 80 批收尾的文档提交让它报的 HEAD
当场过期，`queue.sqlite3` 又漂移一次）。现行协议：

1. 它在 `git worktree add -b perf/… /workspace/tome4-opt-1 develop` 里开发
2. **验收与合并只能在「第 N 批已关闭」到「第 N+1 批已开始」之间**
3. 合并后由它自己补 `queue rebuild`（规矩对谁都一样）
4. 不要从 worktree 用 `--root` 指回主工作区跑写操作
5. worktree 里 `.artifacts` 是空的，首次 rebuild 从零重放；**但投影是证据提交的纯函数，
   两边算出的 8 个字段应当逐字节相同——不同本身就是发现**（已实测通过，可当免费的
   环境一致性检查）

### 尚未裁定：`queue rebuild` 之后的 `queue check` 是否冗余

优化者提出：`rebuild` → `_replace` 在原子替换并 fsync 之后已用同一投影对落盘的库跑过
`_check_projection`（`queue.py:885`），`check` 相对它只多「活动 writer 时的
`_fallback_report` 分支」和「在新进程里独立重算一次投影再比对」，而按流程跑这步时没有
活动 writer。省约 165 s/批。

**我的意见是保留**，理由是 `check` 的独立重算与新进程重读是最后一道闸，而这条流水线
换来的教训恰恰是「17 项全绿、问题完全没被发现、且无法用后续提交修复」。这是**删验证
步骤**而非性能改写，须维护者裁定。**裁定前照旧两条都跑。**

---

## 13. 证据容量：已由 128 MiB 常量改为带版本的 512 MiB 政策（2026-09-11）

### 曾经的问题

`MAX_TRACKED_BYTES = 128 MiB` 是写死的常量，超限在 `prepare-evidence` 抛错。
第 83 批后已用 **91.0%**（122,204,299 字节），实测增速 843 KiB/批 → **约 14 批后停产**，
而剩余待审 270 批。撞线发生在一批已经跑完 4 个表层 child + 1 个交叉复核 child 之后。

（更正一处我当时的说法：超限分支 `batch.py:1635-1639` 的 `rmtree` 删的是 prospective
暂存包，**checkpoint 里的裁决与 raw 输入输出保留**。代价是一次 prepare 重跑，
不是一整轮 child 白跑——前提是之后别让 HEAD 前进。）

### 现在的机制

`tools/i18nlib/capacity_policy.py`：政策以 **id + 规范文档 sha256** 双重绑定，只追加、永不改。

| 政策 | 上限 |
|---|---|
| `legacy-128mib-v1` | 128 MiB |
| `expanded-512mib-v1` | 512 MiB（当前写入政策） |

**关键性质：抬高上限不会回溯放宽旧证据的验收域。**

- gates **schema 1 / 2** 没有政策绑定 ⇒ 按构造是历史件 ⇒ **永远按 128 MiB 读**
- gates **schema 3** 自带 `capacity_policy_id` / `capacity_policy_sha256` ⇒ 按其指名政策读，
  且摘要必须与注册表文本相符，否则报 `batch gates v3 capacity policy invalid`
- 就地改一个数字会改掉摘要，旧 receipt 立刻对不上，**而不是被静默重新解释**

**四个消费者**全部接同一注册表，没有第五个自定义常量：
`evidence.py:MAX_TRACKED_BYTES`、`production_review_v2_lite.py:TRACKED_LIMIT`、
`batch.py:_committed_production_bytes`、`queue.py` 重放时对历史 `gates.json` 的校验。

> **注意这条我一度写错过，别沿用旧说法。**
> 改造**之前**，`queue.py` 读的是唯一的 `catalog.TRACKED_LIMIT`，所以「调低会让合法旧批次
> 当场失效」成立。**改造之后不再成立**——`queue.py` 对 `catalog.TRACKED_LIMIT` 的引用已是
> **零**，四处容量判断全走 `LEGACY_TRACKED_LIMIT`（固定）或 `resolve()`（按 receipt 自己
> 指名的政策），与 `CURRENT_POLICY_ID` 无关。
>
> 当前政策现在只卡**新产出**三处：`evidence.py:141/233`（prospective）、
> `production_review_v2_lite.py:27`（`prospective_occupancy`）、
> `batch.py:1767`（`_committed_production_bytes`，它量的是**整棵已提交生产树**）。
>
> 所以准确的说法是：**调低不影响任何历史 receipt，也不影响 `queue rebuild` / `queue check`；
> 它只挡住新产出。** 一旦调到低于现有总量（116.54 MiB），新批次会 finalize 不了，
> 但旧证据全部仍然有效——即调低是可逆的，代价只是新批次被挡住。
> （优化者在隔离 worktree 里把两个上限一起压到 1 MiB 跑完整重放实测：
> 重放成功、29828 条目、一条历史证据都没失效。）

### 同时做的 group 去重

`prepare_evidence` 原先给每个 surface lane 各复制一份**相同的** group manifest。
全库 612 份 17.10 MiB，批次内按内容去重后只需 153 份 4.28 MiB——**重复 12.83 MiB**。

现在 `_raw_copy_plan(checkpoint)` 一次遍历同时产出声明清单、复制任务与 ref 绑定
（`_prospective_declared_paths` 已经只是它的 `["declared"]`），目的文件内容寻址
`group-<sha256>.json`，四条 lane 绑同一份。**只共享组清单**，input/output 仍各一份，不跨批共享。
重放端零改动——`queue.py:407` 的 `present_raw != referenced_raw` 本就是集合比较。

**只作用于新批次**，已发布的 12.83 MiB 不回收。

### 当前占用（`b3da9f8`）

```
已提交生产证据 122,204,299 字节 = 116.54 MiB
512 MiB 下 22.8%，余量 395.46 MiB → 按 843 KiB/批约 480 批
```

每批开始前仍应跑一次占用统计：

```bash
python3 - <<'PY'
import sys,subprocess; sys.path.insert(0,'tools')
from i18nlib import capacity_policy as cp
PREF=("evidence/production-review/","i18n/quality/production-review/",
      "evidence/production-review-v2-lite/","i18n/quality/production-review-v2-lite/")
out=subprocess.run(["git","ls-tree","-r","-l","--full-tree","HEAD"],capture_output=True,text=True).stdout
tot=sum(int(p[3]) for p in (l.split(None,4) for l in out.splitlines())
        if len(p)==5 and p[3]!='-' and any(p[4].strip().startswith(x) for x in PREF))
L=cp.CURRENT_TRACKED_LIMIT
print(f"{tot:,} 字节 = {tot/1048576:.2f} MiB  {tot/L*100:.1f}%  余 {(L-tot)/1048576:.2f} MiB")
PY
```

### 裁定状态（2026-09-11）

**已批准：两项不需要新信任的算法修正**

- 发布查询快路径（~34.7s）：每次投影用一次 `git rev-list --parents --topo-order --reverse H`
  建可达图，替掉 121 次 `git log`。**守卫条件不可省**：只有当前可达图里 B 的单父 child
  恰为 `[C]` 时才走快路径；多个 sibling、shallow/replace/grafts 一律回落原算法。
  发布唯一性是**对当前可达图的查询**，不是不可变事实
  （`tests/i18n/test_production_review_v2_lite_queue.py:875` 的 merged-sibling 用例证伪过我）。
- 行摘要视图（~31s）：按构造安全——`production_review.py:187` 的 `parse_jsonl` 已强制
  `canonical_bytes(value) == line`。**实现坑**：`migration.py:_snapshots`（`:188`）按
  `entry_revision_identity` **排序**、`_build_migration` **过滤 unchanged**，
  所以按**位置**建摘要表会静默错配（29,828 个合法 sha256 挂错行，不报错）。
  摘要必须随行身份走。

合计约 65s / 167.8s = 39%；每批 11 次重放 × 65s ≈ 11.9 min，31.0 → 约 19.1 min。
（65s 实测；**11 次是从耗时表推的，不是数出来的[估算]**。）

**仍未裁定：投影的跨进程记忆**（catalog 校验 71.3s / 42.5%）

维护者问过一个关键问题：本项目只有一个写入者，防篡改的意义何在？结论是
**在本项目的威胁模型里 HMAC 基本买不到东西**：

- 它能挡的是「改缓存文件、重算普通摘要、但拿不到密钥」的污染 —— 本项目里这类是空集；
- **挡不住同 UID 运行任意代码者**（`0700/0600` 不防同用户），而派发的 reviewer child
  全部同 UID，正好落在挡不住那一类；
- **也挡不住验证器自己算错然后签名**。

（child 的只读性是用别的手段证明的：每批 harvest 后 `git status --short` 证明工作树未被写过。
这条不依赖任何密钥。）

**所以该问维护者的不是「接不接受新信任根」，而是：**

> 接不接受「写入者不再独立重导投影，而是采信一份先前的推导」——赌注是缓存 key 的完备性。

本项目的设计前提是「git 唯一权威，每个写入者改动前从 git 重导完整投影」。这一项在该前提上开口子，
而风险不是恶意，是 **key 设计漏项**。历史事故 `f5373e4` / migration `0eafbff1` 就是实例：
`new_entries_sha256` **匹配**，而 catalog_id、manifest sha、exclusions sha 三项全不匹配 ——
任何只以 entries 为 key 的缓存都会漏掉它。

**若将来启用，建议去掉 HMAC**，改为纯内容寻址（key = verifier fingerprint + 精确 blob
OID/长度/sha256）。这是否定 gpt-6 的设计选择，理由是它覆盖的类别在本项目为空，
而密钥管理是实打实的长期负担。**但去掉 HMAC 省不了多少**——真正的成本是：
verifier fingerprint 必须覆盖 `tools/**/*.py` 全部内容（**工具链动一字节缓存全冷**，
而工具链正在被持续改动）、key 覆盖面测试、历史事故夹具、merged-sibling 用例要重写成
「先暖缓存→再 merge→再检查」。

**启用门槛建议**：工具链进入稳定期之后。

### `queue check` 的冗余：保留，并升格为定义性

维护者曾裁「等容量问题解决再议」，容量已解决。结论（采纳优化者对 gpt-6 设计的硬更正）：

> `queue check` 存在的意义是回答「**在一个全新进程里，重放还能不能重现出同一个投影**」，
> 所以绕过缓存是它的**定义性质，不是可调开关**——可传的参数意味着有人能传成 `on`。

推论：**任何让 `check` 变快的缓存提案都应当直接否掉**，那正好是在拆掉唯一能证伪缓存的东西。
缓存必须可证伪：只要它撒过一次谎，下一次 `check` 就会对不上 8 字段。
代价是每次 160s、每批约 2 次 = 320s（占 1862s 的 17%），**这个冗余就是产品**。

两份并排设计在 `.ai/consult/capacity-perf-design-20260911/`（gpt-6）与
`.ai/consult/disk-memo-design-20260911/`（优化者草案），均未入库。

---

## 14. 第 84 批完成记录（2026-09-11）

| 项 | 值 |
|---|---|
| batch_id | `batch-c728d0ed87c0971376f0` |
| evidence commit | `3851dd307f8c92da7fc3cdde1960581f090257b8` |
| 修复 commit | `554889bdb87bad813b3db0f58d4dc902bbca7de2` |
| migration | `e47fd409…`（revision_changed 6 / unchanged 29822 / ambiguous 0 / unmapped 0） |
| catalog | `a9fdc7e8…` |
| 裁决 | 11 条观察（6 surface + 5 contextual），**全部 confirmed**，6 条条目需修复 |
| 队列 | 21572 → 21498 |

条目全部来自 `tome` 组件，6 处修复全在 `mod-tome.lua`，无跨组件兄弟。

### 六条修复

| revision | 位置 | 问题 |
|---|---|---|
| `1f25cdcd` | `init.lua load_tips` | `rendered extinct` → 「几乎已经灭绝」擅加「几乎」；`hidden groups biding their time` 主语与蛰伏义丢失 |
| `1f46b209` | `quests/east-portal.lua` | `about establishing a link back` → 「关于这件事」，任务指引失效 |
| `1f698194` | `timed_effects/physical.lua` | `feels a surge of adrenaline` → 「被注入了肾上腺素」，主语与语态双错 |
| `1f700213` | `talents/corruptions/plague.lua` | 同一项疾病的两个并列条件被读作先后施加两项；`enemy` 放宽为「单位」；`high` 升格为「最多」 |
| `1f9a18af` | `zones/paradox-plane/objects.lua` | `for generations` → 「数载」；`According to legend` → 「根据历史记载」；`sapling` 漏译 |
| `1fbe8466` | `lore/elvala.lua` | `Aye` 译作感叹词；`without ever dulling the blade` 删除并换成源文没有的「如同划破薄纸」；黑血喷涌换成「战斗的声响」；弃械护脸改成「抵挡呛人的烟雾」；`burning limbs flying into the air` 整句缺失 |

### 一处单轮 confirmed，理由须留痕

`1f698194` 的交叉复核轮判 **OK**，与表层轮分歧。仍判 confirmed，依据是 §5「单轮也可以
confirmed」的机械例外（句法主语与语态）**加上**引擎源码的强独立证据：
`game/modules/tome/data/timed_effects/physical.lua` 的 `ADRENALINE_SURGE` 是
`status = "beneficial"` 的自身增益，`activate` 走 `self:addTemporaryValue`，
机制上不存在外部施加者。分歧已写进裁决 conclusion。

### 两处**未**采纳的复核主张

- `1f9a18af`：`powers of both time and renewal` 译作「时空」**不改**——`Warden` 本库既有
  译名即「时空守卫」（`mod-tome.lua:18441`/`:21853`），「时空」是本库既定行文。
- `1f9a18af`：`Wardens` 应作「守望者」**本批不动**，属全库改名，见 §5 末节。

### group 去重首次真数据验收（本批 `prepare-evidence`）

四条检查项全部成立[实测]：

```
磁盘 group-*.json 份数          1
distinct group_manifest_sha256   1   ← 本批多 lane run 数 = 1
每个哈希挂的 lane 数              4
文件名 vs 重算内容 sha256         逐字节相符（group-ca73e68e…d29.json）
旧布局 *-group.json 残留          0
「group manifest reference lacks a recorded SHA-256」 0 次
gates schema_version             3
capacity_policy_id               expanded-512mib-v1
capacity_policy_sha256           4d3bf7d2… == capacity_policy.digest(CURRENT_POLICY_ID)
prospective occupancy 定点        正常收敛，无 did not converge
```

本批省 57,168 字节 × 3 份 = 171,504 字节 = 167.5 KiB。

> **本批只验到「4→1」这一个实例。** 跨 run 组字节不碰撞这条本批**验不到**
> （只有 1 个多 lane run），证据仍只有优化者在 119 个历史批次上的形态验证
> （按 sha 分组后每组恒为 4 条 lane，无 8 条）。两件事不要混为一谈。

> **12.83 MiB 是已提交在历史里的，一个字节都收不回来。** 去重只让将来不再产生新冗余。
> 算余量只能用「避免」不能用「回收」：按历史每批冗余均值 110.4 KiB × 剩余 269 批
> ≈ 29.0 MiB 可避免[估算，乘数是剩余批数]。
> 相对 395.46 MiB 余量，这 29 MiB 是锦上添花而非承重——**它以后若出问题，回退代价很低**，
> 不必为保住 29 MiB 硬撑一个有疑点的改动。真正解开容量阻塞的是抬限那一项。

### 性能实测（`263aa42` 之后）

`batch start` 160s、`surface-export` 159s、`surface-import` 160s、`contextual-export` 159s、
`contextual-import` 160s、`adjudicate` 159s、`prepare-evidence` 252s（含 17 项门禁）、
`queue rebuild` 159–162s、`migration plan/check/apply` 各 163–165s。
**每个子命令固定约 160s 的那一段就是整棵历史重放**，§13 末节的三项待裁定都针对它。

---

## 15. 第 85 批完成记录（2026-09-11）

| 项 | 值 |
|---|---|
| batch_id | `batch-37e8bcf6fcc318e68716` |
| evidence commit | `e040fad9279a55f43579fecec67161b30651fbf3` |
| 修复 commit | `b2180f8bcacc7f300702809d66606fa12a93cbbd` |
| migration | `d33c84c7…`（revision_changed 16 / unchanged 29812 / ambiguous 0 / unmapped 0） |
| catalog | `163074d8…` |
| 裁决 | 5 条观察（3 surface + 2 contextual）→ **4 confirmed / 1 refuted**，2 条条目需修复 |
| 队列 | 21498 → 21420 |

### 一条 refuted：光之印记

表层轮报「`all melee attacks against it` 未限定攻击者，译文『标记方』缩小了范围」，
交叉复核轮判 OK。**查引擎源码后判 refuted**：
`game/modules/tome/data/timed_effects/magical.lua` 的 `MARK_OF_LIGHT`（`:3248-3250`）是

```lua
callbackOnMeleeHit = function(self, eff, src, dam)
    if eff.src == src then
        src:heal(dam * eff.power / 100, self)
```

`eff.src` 是施加印记者，治疗**只在攻击者就是标记方时触发**。译文与机制一致，
反而是英文 `long_desc` 措辞偏松。与第 76 批护送任务楼层标签那条同类：
**两轮一致也好、单轮也好，都不豁免查源码。**

### 我的第 84 批修复被本批重报

`mod-tome/data/lore/elvala.lua` 的斩首句：源文 `I rushed to hew their heads off.
But as I swung my blade I was knocked to the ground from behind` 是**被打断的未完成动作**。

- 第 84 批之前：「一剑终结他们的性命」= 完成态（已错）
- 第 84 批我重写该句修「呛人的烟雾」时，改成「将他们的头颅**一一斩落**」= 完成态更重
- 第 85 批表层轮当场重报

**教训：重写整句的修复，必须把整句从头到尾与原文逐小句对照，
尤其查时态/体、转折词、方位状语——这三类最容易在改写中被抹平。**
流水线抓住了它，代价是一整批的往返。

### 两轮主张不重叠时怎么裁

`0ae390f1d4` 两轮都报 ISSUE 但**四项主张无一重叠**。第 23 条「两轮复现同一主张才 confirmed」
管的是**升级**，不适用于此；两条观察各自改依第 5 节的单轮机械例外
（句法主语 / 量词依附 / 明确限定语的漏译），逐项定性写进 conclusion。
其中一项（`wreathed in flames` 被降格为「点缀裙摆」）属语义判断、**不在机械例外之列**，
但同段内部一致性（前文 `pillar of flame`、后文 `robe in tatters`）构成独立证据，
据此一并修复并如实记录定性差异。

### 维护者裁定（2026-09-11）与执行

| 项 | 裁定 | 执行 |
|---|---|---|
| `Warden` 全库译名 | **不调整** | 保持「守卫／时空守卫」，从待办划掉 |
| `crypt` | **统一「地窖」** | 改 12 处（原「地穴」10、「洞穴」1、「墓穴」1） |
| 高亮范围错位 2 条 | **同意修改** | `special skeleton talents`、`Undead Drake talents` 的「技能」移回标记内 |
| `Foursaw` 墓志铭 | **允许破例换行、允许重造双关** | 见下，等选定方案 |

`crypt` **不在**范围的三类，已逐一核实，未改动：

- `mod-tome.lua:2828`「繁衍地穴」源文是 `breeding pits`，`:7270`「恐怖地穴」源文是
  `Intimidating Cave` —— 都不是 crypt
- `:2830`、`:43132`、`:16004` 三处 `crypt(s)` 属**整句漏译**，是漏译不是术语不一致
- 全库大量「洞穴」对应的是 `cave`，**一个都不能动**

> `Call of the Crypt` → 「地窖召唤」是照裁定执行的，但我保留意见：
> 作为死灵系技能名，「墓穴」比「地窖」贴切。要改回说一声。

### `Foursaw the Clown`：换行规则根本不需要破例

同一片墓园其它墓志铭**已经逐行镜像**（`操纵时间者／死于时间`、`玩弄烈火／终究引火烧身`、
`来自异乡的璀璨星辰／我们为你的陨落而哭泣`）。**只有 Foursaw 把三行压成一行。**
恢复三行是与邻居一致，不是破例。维护者授权的那条例外在这里用不上。

双关方案（`福萨` 全库仅 1 处，改名无外溢）：

- **A** `小丑先觉` ／ `我们笑着 / 直到察觉 / 笑话已经结束`（先知先觉 ↔ 察觉，共用「觉」）
- **B** `小丑先见` ／ `我们笑着 / 直到看见 / 笑话已经结束`（先见之明 ↔ 看见，共用「见」）

两案共同损失：`Four` 这个数字丢了（硬保留如「四觉」谐音近「死觉」）；名字由音译变意译
（但 `Foursaw` 在英文里本身就是双关造词而非普通人名，所以这是忠于差异）。**等维护者选定。**

### 一个新踩的坑：`cp -r` 重跑会改变语义

`finalize` 报 `commit parent does not equal batch base_commit`。原因：**一次被中断的工具调用
其实已经执行完了 `git commit`**，我以为没跑又跑一遍；第二遍的 `cp -r SRC DEST` 因为 DEST
已存在，变成「拷进 DEST 里面」，产生嵌套目录 `batches/<id>/<id>/…`，多出 15 个文件。

处理：`ls-remote` 确认两个提交都未推送 → 逐字节比对第一个提交与 prospective（15 个文件不符 0 个）
→ `git reset --hard` 到第一个 → finalize 通过。

- `cp -r SRC DEST`：DEST 不存在→拷成 DEST；DEST 已存在→拷进 DEST。**同一命令重跑语义不同且不报错。**
- 防法是 `cp -r SRC/. DEST/` 或先 `rm -rf DEST`，**不是「记得别重跑」**——
  我并不知道自己在重跑（工具调用报的是「已拒绝」，而 `git commit` 已经跑完了）。
- `reset --hard` 前逐字节比对是必需的，因为它不可逆。

### 一个流程写作坑：heredoc 反引号会静默掏空正文

写裁决 spec 用了不带引号的 `python3 -B - <<PY`（为了替换 `$B`），结论里的反引号被 bash
当命令替换执行，`refuted` 那条的全部引擎源码证据被掏空成「实现为 ， 是施加印记者」，
而 **`make_adjudication.py` 仍然 rc=0**（JSON 合法、条数对得上）。

**规矩（入口侧，根治）：** 自然语言正文永远不经过 shell。写文件用 `<<'EOF'`（定界符必须带引号）
或文件写入工具；传参数用 `--prompt-file` / `--input <path>` 这类读文件的选项，
不要把正文塞进命令行；变量走 `export` + `os.environ`。
判据：正文里若出现 `` ` ``、`$`、`'`、`\` 任何一个而它要经过 shell，就已经错了。

**规矩（出口侧，补网）：** 生成后读回文件，断言每条正文里**事先写死的承重片段**在场
（如 `"eff.src == src" in conclusion`）。**必须连同局限一起写**：只守住列进去的那几处；
**尤其不能用症状匹配**（如 `assert "（）" not in c`）——那会把「没检出」当成「没损坏」，
消耗掉本该用于真检查的注意力。

第 84 批的 spec 没用反引号、输出无 `command not found`，已提交证据经逐条核对完好。

### 三类「结构校验全绿而内容已错」的发现手段**不同**

| 损坏 | 靠什么发现 |
|---|---|
| 行摘要按下标配对错行 | **读回无效**——字节本身合法，只能靠理解排序与过滤的语义 |
| 正文被掏空 | 读回文件肉眼可见 |
| migration↔catalog 脱钩 | 门禁不查，只有 `queue rebuild` 查且事后无法补救 |

**不要把三者并列成一条规矩**，那会让人以为读回能解决全部；读回只解决中间一处。

### group 去重第二次真数据

```
磁盘 group-*.json 1 份 == distinct sha256 1 == 本批多 lane run 数 1，每个哈希挂 4 条 lane
文件名 group-2cf630c451c0….json 与重算内容 sha256 逐字节相符，70464 bytes
旧布局残留 0 ／「lacks a recorded SHA-256」0 次
gates: schema 3 / expanded-512mib-v1 / 4d3bf7d2…
本批省 70,464 × 3 = 211,392 字节 = 206.4 KiB（高于历史中位 108.4 KiB）
```

仍只验到「4→1」一个实例；跨 run 组字节不碰撞本批**验不到**（只有 1 个多 lane run）。

### 一个「必须 80/80」的正当例外

`freeze_workset` 报 78/80，missing 2：`gem.lua | alchemist fire opal` 与 `alchemist ruby`。
原因是 `gem.lua:83` 用 `name = "alchemist "..name:lower()` **运行时拼名**，字面串不在源文件里，
不可能字面匹配。**workset 的 `public_source_path` 仍是 80/80 齐全**，
`make_adjudication` 不会 KeyError。代价：若这类条目被判 confirmed，
证据快照里不含该字面串，结论里要改引构造式所在行。



---

## 16. 第 86 批完成记录（2026-09-11）

```
batch      batch-1c65f7e787ad7110fef5   80 条   freeze 80/80
evidence   2d7d0870d04a27ccad58a407a95eccbfb24c847e（父 f667cf5）
修复       b8019e56e7126dec6fcec5a908cd41c565ea6ad5
catalog    aa5a924741b4e51ce126b998da01300d460a519362d731a84fa80bb253754b99
migration  9b2a2a4294e380591a5644b98c1895d2b046bcca6ce32ebf62ccfa49eafac998
           revision_changed 1 / queued_successors 1
queue      21421 → 21342
```

4 条观察 → **2 confirmed / 2 pending**，修复 1 条（4 处编辑，全在
`mod-tome/init.lua` 的开场介绍）。

| 处 | 问题 | 修法 |
|---|---|---|
| E1 | `after the Age of Pyre` 译作「在烈火纪末」，把「之后」反转成「结束前」 | 改「烈火纪之后」，并补回源文的空行分段 |
| E2 | Toknor 一句主语悬空、重复指称；且凭空称 Mirvenia 为「半身人皇后」 | 重写；源文未称其为半身人，删 |
| E3 | `with the Allied Kingdoms` 窄化为「和联合王国的人类们」（与同文人类半身人共存矛盾）；`yet` 的转折被改成让步「尽管」致逻辑反转 | 复原为「与联合王国」；改回「但」 |
| E4 | 末段大段无据增译（「被遗忘的大陆、未被开发的森林」「谁也不知道最终会找到些什么」「大多数法师宁愿避开公众的视线」）；`wonders` 由「古老的力量」顶替 | 全删；`wonders` 还原为「奇观」 |

两条 pending 都落在 `0c9009638b49`（rat-lich 事件的 `Stairs seem to lead into
some kind of crypt.`）：crypt 译名 + `seem` 情态被抹除。**两条已在 §17 的
crypt 清扫中一并修复**（改为「这道楼梯似乎通向某种地宫。」）。

### 本批各子命令耗时[实测，非安静环境]

| 子命令 | wall | user | sys |
|---|---|---|---|
| `batch start --limit 80` | 153 s | — | — |
| `surface-export` / `surface-import` | 153 / 151 s | — | — |
| `contextual-export` | 153.2 | 130.4 | 20.4 |
| `contextual-import` | 154.2 | 131.2 | 20.3 |
| `adjudicate` | 151.4 | 129.7 | 20.0 |
| `prepare-evidence` | 260.1 | 203.7 | 39.7 |
| `finalize` | 154.9 | 131.8 | 20.8 |
| `queue rebuild` | 158.2 | 133.3 | 22.2 |
| `migration plan` / `check` / `apply` | 165.5 / 157.3 / 156.6 | 139.2 / 134.4 / 134.0 | 23.0 / 20.6 / 20.5 |

**这些数不能当基线**：测的时候优化者也在跑基准，两边互相污染。

> ⚠️ **一个我犯过的错，记在这里防止重犯。** 我曾拿第 84 批的 160 s 和第 86 批的
> 153 s 相减，报「6b 只省 6–7 s」。**两批的重放单元数不同**（122 vs 124），
> 所以这个减法没有意义。绝对耗时只能在**同单元数、同工作树、同 treeish**
> 之间比较。详见记忆 `perf-baseline-same-worktree-same-treeish`。

---

## 17. `crypt` 译名：三方交叉咨询与裁定（2026-09-11）

### 裁定

维护者裁定：**全部 `crypt` 统一译作「地宫」**。已落地 25 处
（`mod-tome.lua` 24 + `tome-ashes-urhrok.lua` 1）。

### 咨询过程

简报 `.ai/consult/crypt-terminology-20260911/BRIEF.md`（未入库），只给条目清单、
既有术语绑定表和约束，**不含任何倾向性结论**。三个模型独立作答：

| 模型 | 结论 | 技能名 |
|---|---|---|
| GPT-6-Astra (xhigh) | 统一为「墓室」 | 墓室之唤 |
| Grok 4.6 | 统一为「墓室」 | 墓室召唤 |
| Gemini 3.8 Flash (high) | 统一为「地宫」 | 地宫召唤 |

**三家一致：必须统一、「地窖」必须废弃。** 一致否决的候选也完全相同：
墓穴（占 `grave`/`tombs`）、地穴（占 `breeding pits`/`Intimidating Cave`）、
洞穴（占 `cave`）、墓园（占 `graveyard`）、陵墓（占 `mausoleum`）、
地下室（占 `basement`）。

分歧只在**空间尺度 vs 建筑属性**：GPT-6 与 Grok 选「墓室」取其墓葬本义，
并**都主动承认**「室」是单间尺度、不合 5 层的 Kryl-Feijan 与 3 层的 Shadow Crypt；
Gemini 选「地宫」取其尺度与四字区名的工整，代价是帝陵语域偏高。

### 我漏掉的那条事实（比裁定本身更重要）

第 85 批我把 crypt 改成「地窖」时，列出了洞穴／地穴／墓穴／墓园四个已绑定词并逐一排除。
**但「地窖」自己早已绑给 `cellar`**（`tome-cults.lua:1667/1669`：活板门、酒、
蔬菜干果），所以那次改动制造了一词两指。

> **规矩：候选译名要双向查。**
> 不只查「这个候选会不会撞到别的词」，还要查「这个候选是不是已经被别的英文词占了」。
> 我上次只查了前一个方向——这是个不对称的盲区，光靠「我查过冲突了」不足以免疫。

### 25 处编辑 = 24 个 catalog 条目

`migration plan` 报 `revision_changed: 24` 而我改了 25 处，差的那一处**不是漏改**：
`lore/fun.lua` 的尸妖段（`crypts and graveyards`）与幽灵段（`windswept crypts`）
同属**一个** `t([[…]])` 块（`#{italic}#An undead hunter's guide, by Aslabor Borys#{normal}#`），
两处编辑落在同一个条目上。反之 `Shadow Crypt` 出现两次却是**两个**条目
（`entity name` 与 `_t`，kind 不同）。

> 编辑处数和条目数天然不等，**差值必须逐条解释掉**，不能当舍入误差放过——
> 「少了一条」和「某处漏改了」在数字上完全一样。

### 25 处的分类

| 类 | 处数 | 说明 |
|---|---|---|
| 区名与区内实体 | 10 | `Crypt`／`Dark crypt`／`Shadow Crypt`×2／`Forsaken Crypt`／`collapsed forsaken crypt`／入口／楼梯提示／离开日志／vault 变形日志 |
| 遭遇文本 | 3 | `maj-eyal.lua` 的入口描述、开门日志、选项「进入地宫」 |
| 任务文本 | 2 | `kryl-feijan-escape.lua` |
| 技能名 | 1 | `Call of the Crypt` → 地宫召唤 |
| 叙事 lore／对话 | 6 | 梅琳达父亲、elvala、fun×2、last-hope、misc |
| **crypt 整词漏译，补回** | **3** | 见下 |

三处漏译（与译名选择是两回事，一并修）：

- `Saved Melinda from her terrible fate in the Crypt of Kryl-Feijan.`
  旧译「从克里尔·费扬**邪教**手中……」——`Crypt` 是地点不是教派，专名整个丢失。
- `ceaselessly drifting through windswept crypts` 旧译「它们不停的随风飘荡」
  ——把 `windswept` 误读成「随风」并丢掉 `crypts`；`wanderers` 还被窄化成「生物」。
- `Dreadfell has always been shunned for its haunted crypts` 旧译「因闹鬼而为人所避讳」
  ——`crypts` 丢失；同句 `a darker and more terrible power in residence`（居于此）
  被放大成「有位……的**主人统治了**此地」，一并改回。

### 一处**有意不改**的地方

`Entrance to a dark crypt` 现译「通向**阴影**地宫之路」，字面应作「黑暗」。
保留「阴影」是因为该入口实际通向 `Shadow Crypt`，而 `Dark crypt` 是
Kryl-Feijan 区名的变体已作「黑暗地宫」——照字面改会让两个不同区域在界面上同名。
**这是明知不忠实而保留，不是漏改。**


---

## 18. 第 87 批完成记录（2026-09-11）

```
batch     batch-9762ac4184dbef00478c   80 条   freeze 80/80
evidence  d7b5cf4dec8bacfbc238216d389f5999ff2ebc3d
修复      770a14542d061d6b553401ab243fa0edf5bc0eca
catalog   0d057aeff651ada755aac2b7394f956fe9c1c772e60ea78595b30320849f4c77
migration abf9e56f3a7b69cd08645bfe67ad491b0e14254d3e7945c02544ac0bc79ac218
          revision_changed 10 / queued_successors 10
queue     21345 → 21274
```

表层 10 条 ISSUE → 交叉复核 9 ISSUE / 1 OK。裁决 19 条观察
（surface 10 + contextual 9）：**confirmed 18 / advisory 1**，repair 9 个条目，
实际 12 处编辑（一个条目可含多处；另加 1 条同类变体）。

### 表层轮只用了 90 秒，是真的

4 个 lane 各跑 60–105 秒、25–31k 输入 token、1.2–1.5k 输出，比历史的 20–40 分钟短得多。
我先按「不可能这么快」去查，结论是**它们确实做完了**：harvest 的覆盖校验报
每 lane 20/20、身份校验通过。

> **可靠的完成判据是 harvest 的覆盖数，不是 agent 的 `idle` 状态。**
> `idle` 同时代表「跑完了」和「还没开始」，等待器区分不了这两者。

### 一条 advisory，以及它引出的契约问题

`22c6b53397`（`alchemist-last-hope.lua`）：源文 `Here's a list of the creature bits
I need. Good luck with the murdering!` 中，`creature bits` 在译文「材料清单」里被泛化，
`murdering` 整个没有对应成分。我独立核对属实。

但交叉复核轮返回 `OK`，而**该判定在契约下不附任何理由**——其 verdict 对象只有
`revision_key` 与 `verdict` 两个字段。按 §23 语义判断需两轮共同支持，两轮不一致，
故判 advisory（一次性放行、不重新入队、不修复），而不是 refuted
（refuted 等于承认观察是错的，而它不是）。

> ⚠️ **待维护者裁定：交叉复核的 `OK` 是否应与 `ISSUE` 一样要求附理由？**
> 现状是**一个无理由的 `OK` 可以单向否决一条有证据的表层观察**。
> `ISSUE` 要举证而 `OK` 不用，等于把举证责任只压在「发现问题」一侧。

### 修复中的两条同类检查

修完后逐条 grep 旧文本，抓到两处残留，**一处是真同类，一处不是**：

- `mod-tome.lua:38363` `and offered to her dark Master` —— 被点名的是 `his` 版，
  这是同一句的**性别变体**，同样的错。一并修。
- `mod-tome.lua:5220` 的「镀金工艺」**不是错**。它的原文就是 `a gold plating`，
  与 `5200` 的 `magical plating` 是两个不同的英文串。同一个仪式在**英文原文里**
  就有两种叫法，逐句忠实翻译正好保留了这个不一致。

> 「同类问题」要按**英文源串**判定，不能按中文译文判定。
> 我差点把 `5220` 当成同类顺手改掉，查了原文才停手。

### 本批耗时[实测，非安静环境]

| 子命令 | wall | user | sys |
|---|---|---|---|
| `batch start` / `surface-export` / `surface-import` | 154.9 / 178.1 / 174.8 | — | — |
| `contextual-export` / `contextual-import` | 152.6 / 152.9 | 131.4 / 131.8 | 19.6 / 19.6 |
| `adjudicate` | 153.6 | 132.3 | 19.8 |
| `prepare-evidence` | 261.0 | 205.2 | 39.1 |
| `finalize` | 154.5 | 132.8 | 20.3 |
| `queue rebuild` ×2 | 152.4 / 152.8 | 131.7 / 132.2 | 19.5 / 19.3 |
| `migration plan` / `check` / `apply` | 154.8 / 155.9 / 156.8 | 133.6 / 134.2 / 135.7 | 19.8 / 19.9 / 19.7 |
| `authoritative-catalog build` | **3.8** | 3.6 | 0.15 |
| `ci-gates.sh` ×2 | 97.6 / 98.9 | 66.3 / 67.8 | 16.8 / 16.7 |

`authoritative-catalog build` 不走投影重放，只要 3.8 s，**不是优化目标**。

### 第 88 批要做的一个实验

维护者委托的 GPT-6 第二轮架构咨询读代码发现：`finalize` 内部已调 `_projection` +
`_replace`，**所以 finalize 之后紧接的那次 `queue rebuild` 可能是重复的**。

第 88 批按此顺序试：finalize → 修复 → `ci-gates` → `authoritative-catalog build`
→ **跳过 rebuild，直接 `migration plan`**。

- `plan` 报 `meta/catalog/evidence-head drift` ⇒ 这次 rebuild 必需，把理由写进 §3；
- `plan` 正常返回 ⇒ 它是重复的，砍掉，**每批省约 155 s**。

实验安全：`plan` 的 preflight 自身走 `_projection`（含 `_validated_migration_edges`），
漂移会当场报错而不是静默产出错的 migration；失败代价只是一次白跑的 `plan`。

> **修复提交之后那次 rebuild 不动。** 它是唯一校验 migration↔catalog 绑定的环节，
> 17 项门禁查不到那一层且事后无法补救（有事故记录）。
> 它不是重复生成，**它是验收**——写在这里免得下一个人看到「又 rebuild 一次」顺手砍掉。

### 实现细节：`queue check` / `rebuild` 的前置条件

两者第二行都是 `_clean_evidence(root)`：对 `evidence/production-review-v2-lite`
跑 `git status --porcelain=v1 -z --untracked-files=all`，**非空就抛
`tracked evidence worktree must be clean before queue rebuild`**。

所以证据目录一脏，**连一次投影都不会发生**。函数名叫 `_clean_evidence` 但它不清理，
它是断言干净——读代码时别被名字骗了。这也解释了为什么复制 catalog 进 `evidence/`
必须排在所有 rebuild/check 之后。
