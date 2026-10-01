1. 修复 44 条：第375批 1c38f759ab 与第376批 4e496adf1d、5c0dc6d9d2、6a7d1cc720 四条确认问题，以及 2026-10-01 三方讨论（用户同意）统一的 21 个名称在 40 条译文中的引用；按 SPEC 表格把 21 行术语改为 preferred；冻结 workset、源码锚点与译文基线；setup 后跑 check_siblings.py。
2. 唯一 EXECUTOR 先改术语库，再按 SOURCE-CLAIMS 定向修改译文，给出验证。
3. 宿主核验精确 target diff 与术语行 diff，冻结 review 输入，独立 REVIEW/full 与 FINAL_REVIEW/full，必要时有界修复。
4. 17项门禁、DONE_VERIFIED、译文提交、queue/catalog/migration、证据发布与推送。
5. 审核按用户要求仍暂停；successor 待恢复审核时复审。
