# 翻译质量试点评审指引（rubric v1）

> contract：`mqm-pilot-v1`（`method_version`）。本文件是评审协议的权威说明；
> rubric 修改必须提升 `method_version`（如 `mqm-pilot-v2`），并保留旧版本结果不重释。
> 配套权威配置：`taxonomy-v1.json`（错误码/severity/profile/复用范围）、
> `policy-v1.json`（试点与 dry-run 参数）、`schemas/*.json`（数据契约）。

## 一、评审对象与输入

每个 revision 会得到一份有界 context packet，包含：

- `source`、`target`、`component`、`section`、`source_tag`；
- `args_order`、`special` 与结构签名（printf 序列、markup/@token 多重集、换行）；
- 自动推断的 `profile` 及其置信度（`high/medium/low`）；
- 相关术语行（含 status、scope、notes）与 `domain_hints`；
- 同组 contrast 条目（`contrast_siblings`）；
- `profile_confidence != high` 时附最多前后各两条规范译文（`context_neighbors`）。

只依据 packet 内信息评价。packet 不足以形成可靠结论时，必须设置
`context_sufficient: false`，不得猜测机制后强行给出结论。

## 二、逐 revision 填写 assessment

每个 revision 输出一条 item：

| 字段 | 规则 |
|---|---|
| `revision_id` | 原样复制，不得修改 |
| `context_sufficient` | 布尔。上下文不足时为 `false` |
| `profile_confirmed` | 你确认的文本功能 profile（白名单），或 `null` 表示无法确认 |
| `findings` | 缺陷数组；无缺陷留 `[]` |
| `reuse_recommendation` | 复用范围（白名单），或 `null` |

### finding 字段

- `finding_id`：本 assessment 内唯一的短别名（如 `A-001`）。
- `error_code`：必须来自 taxonomy 白名单（37 个代码，见下）。
- `severity`：`blocker / major / minor / note`，见判定规则。
- `source_span` / `target_span`：短跨度。可用字符偏移（如 `0:5`）、参数位置
  （如 `arg1`）或直接引用术语/短语；留空表示整条。不要复制完整长文本。
- `body`：简洁、可复核的理由（1–3 句）。
- `evidence_refs`：可选引用数组。只允许：sample 内术语行、相对公开源码路径
  + 固定 commit、受审计 artifact ID。**禁止**主机绝对路径与 `..` 路径段。

### severity 判定

| severity | 标准 | 示例 |
|---|---|---|
| `blocker` | 不可运行、破坏格式、系统性错误 | Lua 加载失败、参数缺失、关键 token 损坏 |
| `major` | 实质改变含义、机制或玩家决策 | 伤害类型错误、否定反转、关键条件遗漏 |
| `minor` | 确有问题但不改变核心机制 | 局部生硬、次要术语不一致、标点问题 |
| `note` | 非缺陷的可选建议 | 两种表达均正确时的风格偏好 |

`note` 不是缺陷，不计入缺陷分。有实质缺陷 = 存在 `minor/major/blocker`
（非 `note`）finding。

## 三、错误代码速查

- **准确性 `ACC_*`**：`MISTRANSLATION` 一般错译；`OMISSION` 漏译；`ADDITION`
  增译；`UNTRANSLATED` 英文残留；`POLARITY` 否定/增减反转；`CONDITION` 条件/
  时序/比较错误；`NUMBER_UNIT` 数字/概率/回合/单位；`ENTITY_ROLE` 主客体/指代
  错位；`MECHANICS` 与固定版本机制不符。
- **术语 `TERM_*`**：`PREFERRED` 未用适用 preferred 术语；`PROPER_NAME` 专名；
  `INCONSISTENT` 同语境无理由多译。
- **流畅度 `FLU_*`**：`GRAMMAR` 语法；`WORD_CHOICE` 用词；`AWKWARD` 生硬欧化；
  `AMBIGUITY` 引入原文没有的歧义；`PUNCTUATION` 标点排版。
- **风格 `STYLE_*`**：`REGISTER` 语体；`VOICE` 口吻称谓；`NARRATIVE` 叙事风格。
- **UI `UI_*`**：`CLARITY` 不清楚；`LENGTH` 过长/截断风险；`RENDER` 渲染后不可读。
- **技术 `TECH_*`**：`FORMAT` printf 问题；`ARGS_ORDER` 参数顺序/角色；
  `MARKUP` 颜色标记；`TOKEN` @token；`LUA` 加载/编码；`RUNTIME_KEY` 覆盖冲突。
- **上下文 `CTX_*`**：`SOURCE_TAG` 错误语境；`DOMAIN` 错误领域；`ALIGNMENT`
  条目错位；`INSUFFICIENT` 上下文不足（此时同时设 `context_sufficient=false`）。
- **目录 `CATALOG_*`**：`DUPLICATE` 非法重复声明；`STALE` 旧原文/旧机制依赖。
- **原文 `SOURCE_*`**：`AMBIGUOUS` 原文有歧义；`INCORRECT` 原文与机制不符且
  译文是有证据的修正。`SOURCE_*` 不直接计为译文缺陷，但要写清理由。

## 四、评审纪律

1. **独立评价**：不看另一评审者的结论、不预设 grade。自动技术事实（gate
   signals）可以看，风险标志只是提示，不得写成既定错误。
2. **机制优先**：译文/术语/原文与机制描述冲突时，以固定版本公开源码实际行为
   为准；闭源 DLC 机制证据不足时标 `CTX_INSUFFICIENT`，不猜测。
3. **不锚定**：`note` 只表示可选建议；没有具体证据不要报 finding。
4. **span 从简**：短跨度或参数位置即可，禁止复制完整受限上下文来证明局部错误。
5. **dry-run 纪律**：dry-run 的 12 条用于检验 rubric 可理解性；冻结原始结果；
   若 rubric 需修改，提升 `method_version` 后从头重评，不得查看对方答案回写。
