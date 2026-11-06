# Lore 整篇重译（2026-11-06，Gemini 4 Argon）

用户 2026-11-06：「交给gemini 4进行重译」。

- 对象：lore-screen-20261105/retranslate-list.md 的 16 条，加上 0391 盲审中局部修改后仍报意思错误而升级的 909a001617bd（elvala 第五章），共 17 条。
- 每条一个独立的 antigravity/gemini-4-argon agent，逐个串行运行（run.sh）；输入为英文原文、现有译文（只参考专名）和自动整理的专名表（prep.py，人工去除了误匹配的普通词）。每个目录保存 prompt.md、glossary.tsv、out.txt 与 previous-translation.txt。
- 写回前由宿主核对：换行数与空行位置、#{italic}# 等标记、[i]/[b] 标记、无残留英文；写回后核对英文 source 全部不变，并通过严格 lint 与 runtime collision 检查。
- tome-orcs 1c73f145ab27 是游戏内「倒写」手札，按行把 4ca4e02e13e6 的新译文倒序并镜像括号与 [b] 标记生成（mirror.py）。同一方法对现有原文和现有译文都能逐字复现两者之间的对应关系。
- 盲审：lite 批次 0392（mod-tome）与 0393（cults／orcs）。
