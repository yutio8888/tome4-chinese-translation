# 翻译审核主编排者 —— 交接说明

最后更新：2026-09-10（第 77–79 批后）· HEAD `b7f85ef` · 分支 `develop`

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
| 最后完成批次 | 第 79 批 `batch-bd59b69afb97e21dd4c1`（已 push） |
| 累计批次证据 | `evidence/production-review-v2-lite/batches/` 共 117 个 |
| 当前 catalog | `67b5b973…`（29828 条目 / 480 排除 / 30308 occurrence） |
| 最后 migration | `fdc71d7a…`（revision_changed 2） |
| 活动批次 | **无**（可以安全提交、可以开新批） |
| 工作树 | 干净，仅 `.ai/consult/` 未跟踪（三模型咨询存档，未入库是有意的） |

审核进度（`queue check`，2026-09-10，`ok: true`）：

| 项 | 条数 |
|---|---|
| 条目总数 | 29828 |
| 已过表层筛查 | 7954（其中条目另有交叉复核） |
| 尚未覆盖 | 21873 |
| `done` 显式置位 | 7954 |
| `blocked`（pending 裁决占位） | 1 |
| `historical_revision_invalidated` | 618 |

按 80 条一批算，剩余约 **273 批**。

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
只有 `queue rebuild` 会走 `_validated_migration_edges`。曾经出现过：改了 addon 组件
→ 重建 catalog → 只 diff 了 `entries.jsonl` 就以为 migration 不受影响 →
用新 catalog 覆盖了 `exclusions.jsonl`，`catalog_id` 变了而 migration 里的
`new_catalog_id` 还指向旧值。**17 项全绿，问题完全没被发现**，而且**无法用后续提交修复**。
所以每次修复提交后的 `queue rebuild` 不能省。

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

### 每批都会被重报、需另开有界窗口处理的四项

`honey tree`（蜜蜂树，字面是 bee tree）、`Warden's Focus`（专注守卫，中心词颠倒）、
`farportal`（远古传送门，Far 被当作 ancient，全库 83 处）、
`Kryl-Feijan`（卡洛·斐济，「斐济」是 Fiji 的固定译名，跨两个组件）。
**未授权前不要动**，每批照常裁决即可。

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

| 步骤 | 耗时 |
|---|---|
| `preflight`（每个 batch 子命令都跑一遍） | >4 min |
| `authoritative-catalog build` | ~3 min |
| `queue rebuild` | 157 s（每批两次） |
| `bash tools/ci-gates.sh` 17 项 | 82 s（每批两次） |
| 表层筛查 4 个 child | 约 1 min |
| 交叉复核 1 个 child | 80–100 s |

门禁里真正扫全库的几项（06 碰撞扫描、08 术语静态审计、12 addon 构建）**全在 1 秒内**，
80% 时间是两个 Python 单元测试组（`03-toolchain` 26 s、`05-production-shadow` 33 s），
与库规模无关。**要压时间应该动 `preflight` 和 catalog build，不是门禁。**

---

## 7. 挂起中，等维护者裁定

1. **`Foursaw the Clown` 墓志铭** —— 是否为韵文对换行规则破例；是否重造
   `Foursaw`/`saw` 的双关（要改一个 lore 角色名并重写墓志铭）。
2. **标记内多余空格清理** —— 已排期又被叫停，且**结论需要修正**（见下）。
3. **是否立项优化** `preflight` / `authoritative-catalog build`。

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
