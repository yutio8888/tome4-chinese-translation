# 勘误：审核272 surface 裁决中的 LF 计数

`batch-54be748f9582a3f09434` 的 HOST-SURFACE-DECISIONS（证据提交 594fbd4f）对 `fc3dc9f6`（写给威斯曼的信 (1)）写了“LF 10→9”，数字有误。

实测（LocaleLoader 读取冻结 workset 的 source/target）：原文 8 个 LF、9 行，空行下标 1、3、5、7；现译 9 个 LF，第二段被拆成两段，署名“罗尔夫”前缺空行。

裁决不变：LF 结构不一致属一级换行不变量，仍为 confirmed、repair_required。窗口26 SPEC 按实测的 8 个 LF 下达。已提交的证据不可改写，勘误记于此处。
