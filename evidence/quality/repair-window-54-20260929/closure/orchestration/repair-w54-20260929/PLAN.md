1. 修复第369批确认的 Orcs 信件第二段（5d4b280889，整段按原文重译）与 batch-5e2173dbfb90012ff34d 确认的 8b977dd836（spell 应为“法术”：独特技能→独特法术，按用户 2026-09-28 裁决保留“元素法师”）；冻结 workset、源码锚点与译文基线；setup 后跑 check_siblings.py。
2. 唯一 EXECUTOR 按 SOURCE-CLAIMS 定向修改，给出验证。
3. 宿主核验精确 target diff，冻结 review 输入，独立 REVIEW/full 与 FINAL_REVIEW/full，必要时有界修复；与裁决无关的既有问题记 advisory 并 carry_forward。
4. 17项门禁、DONE_VERIFIED、译文提交、queue/catalog/migration、证据发布与推送。
5. 之后审核窗口54的 successor。
