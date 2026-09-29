# 独立参考与匿名核验安排

## 第一阶段：盲审参考

不参赛的全新 REVIEWER 只接收和三臂相同的 INPUT 与读取边界，逐条全40作同样分类；不能接触任何v1/v2实验臂报告或统计。先原样收获并冻结参考报告，再归档确认。

## 第二阶段：匿名claim核验

将v2实验臂及盲审参考的全部问题、建议和未决观察提取到统一的 entry/claim 表；去除模型、provider、dispatch名字，按entry及claim文字排序。语义去重不能由宿主擅自裁决，保留相似观察，由核验REVIEWER建立每条的canonical defect IDs；同条同义重复仅算一个缺陷，不同遗漏分开。每条claim保留原始文本与原报告偏移映射在宿主专用文件，核验者不可读取映射。

fresh REVIEWER仅见统一规则、相同冻结材料、匿名观察，依固定源码裁定 confirmed/refuted/pending/advisory，明确每个canonical defect属于哪个entry、哪些匿名claims命中它，并逐条判定40条（包括没有任何模型报错的条目）。不得用重复次数或观点一致替代证据。每个confirmed/refuted必须短引或源码锚点；缺证据的pending，不把未发现新问题称为彻底无错。

模型核验后，宿主只做机械映射和计数。若盲审/核验间出现实质争议且证据未充分消解，保留pending并报告影响，不强迫单一答案。明确说明该参考由独立模型构建、非人工金标准；同系列裁决偏差是限制。

所有报告先存raw再提取；创建前写pending_dispatch及prompt/input SHA256，核验lineage；终态归档前递增archive_attempts_started，最多两次，live archivedAt才记确认。新的参考角色仍为REVIEWER purpose=translation_contextual_v1，沿用本campaign的自然语言研究例外，不宣称严格contract DONE。
