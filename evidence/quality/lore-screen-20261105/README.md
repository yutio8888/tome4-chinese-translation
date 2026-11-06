# 长篇 Lore 单独审核（2026-11-05～06）

用户 2026-11-05「请将篇幅较长的Lore和其他文本区分开，对Lore进行一轮单独的审核，判断有哪些Lore需要整体重译」。

- 范围：`data/lore/` 各 section 中英文 ≥300 字符的条目，共 410 条（约 90 万英文字符）；更短的 lore 多为标题，不计入。texts/（开场、解锁、教程）等其他文本不在本轮。`prepare.py` 按文件顺序切成 16 批（每批约 6 万英文字符）。
- 方法：每批两条独立盲审 lane（A＝Opus 5.5，B＝GPT-6.1-Sol，规则 `reviewer-rules.md`），每篇评 OK / LOCAL（1–3 处明确问题）/ RETRANSLATE（问题遍布全文），附流畅度、忠实度与问题清单；`dispatch.sh` 派发并校验。
- 裁决：A、B 均 RETRANSLATE → 重译；仅一方 RETRANSLATE 的 18 条交第三方 Gemini 4 Argon（C，`batch-tie.json`/`result-tie-C.json`）按同一规则复评，C 判 RETRANSLATE 才重译，否则按 LOCAL 处理。C 明显偏宽（8 条判 OK 且未列问题，而 A/B 均列出具体问题），因此这 17 条仍按 LOCAL 修复 A/B 列出的问题。
- 结果（`summary.json` 的 `final`）：RETRANSLATE 16、LOCAL 169、OK 225。重译清单见 `retranslate-list.md`。
- 注意：tome-orcs.lua 2592（倒序文本）与 2615 是同一篇的正反写，重译须同步。
