# 翻译审核当前交接

更新时间：2026-09-28（第357批已 finalize，窗口48积压 6 条，继续审核第358批）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。历史交接正文见本文件的 git 历史
（`git log -p -- handoff.md`），当前会话授权优先。

## 一、当前状态

- 审核已闭合至第 **357** 批（`batch-06020dfb9cbf406a4526`）：80 条（主游戏 65 条、Ashes 15 条），74 done / 6 repair_required。
  主游戏 65＋Ashes 15 混合批（窗口47a/47b successor 首批）：surface 两组 8 lane；contextual 两个 run 一次通过；逐条裁决。窗口48积压 6。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `077d182af2b57ee621efbbacf57932e876b3841b` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **47b**：B 组单条措辞与名称 48 条及窗口 47a 转入 8 条（三个 Lua 文件）已修复；译文提交 `a10222b7e4a6650d289ed90120e8d2acb867ed53`；migration `2e88ba7a…` 的 56 个 successor 须重新审核，不继承旧 revision 的 done 状态；窗口 47a 的 77 个 successor 同样待审。第357批起审核其 successor（133 个，第357批已审 80）。
- 修复窗口 **27** 已完成 273–277 五批共 28 条确认问题的修复、复审、17 项门禁、译文提交、
  catalog/migration 发布及证据提交。证据提交 `351c6724d60221ffc1656ff1d97db2eecb2d0e02` 后的
  queue rebuild 通过；新 catalog 与 28 条待重新审核的 successor 均已核对。
- 窗口 27 译文提交为 `defcc44d6d01a1329d83b37b0dcbb83c56e4b631`；新 catalog 为
  `cdc76147d080c57a246273344897b397c53eded5051d701a3d7974dcb1f9e0f8`，migration 为
  `b8289b4f700157310fc4a583dab34cbd726be7c2a55895b4d24a942b607f8c63`。28 个 successor 必须重新审核，
  不继承旧 revision 的 done 状态。
- 2026-09-24 早些时候已提交并推送工具维护与文档整理，内容见第四节。
- 近六批结果：

| 批次 | batch id | 结果 | surface（gpt-6-sol） | contextual（opus-5-5） | 裁决 |
| --- | --- | --- | --- | --- | --- |
| 273 | `batch-5e69946bed52ed5a5cbc` | 78 done / 2 repair | 71 OK / 9 ISSUE | 8 OK / 1 ISSUE | 3 confirmed / 7 refuted |
| 274 | `batch-c03b7552b4059d697ec0` | 75 done / 5 repair | 69 OK / 11 ISSUE | 8 OK / 3 ISSUE | 8 confirmed / 6 refuted |
| 275 | `batch-54d2d16b94c511082107` | 74 done / 6 repair | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 10 confirmed / 5 refuted |
| 276 | `batch-f8d6c02a3294c168f104` | 72 done / 6 repair / 2 blocked | 69 OK / 11 ISSUE | 6 OK / 5 ISSUE | 10 confirmed / 3 refuted / 3 pending observations |
| 277 | `batch-a2538cac10c65873a661` | 70 done / 9 repair / 1 blocked | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 13 confirmed / 1 refuted / 1 pending observation |
| 278 | `batch-2dd6d21e34b360ebb6d9` | 73 done / 6 repair / 1 blocked | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 10 confirmed / 4 refuted / 1 pending observation |
| 279 | `batch-99f8a711d02012a6de19` | 73 done / 7 repair | 70 OK / 10 ISSUE | 4 OK / 6 ISSUE | 11 confirmed / 3 refuted / 2 advisory |
| 280 | `batch-76f9078d25a218ccbe79` | 69 done / 11 repair | 61 OK / 19 ISSUE | 13 OK / 6 ISSUE | 16 confirmed / 6 refuted / 3 advisory |
| 281 | `batch-6b0d756f5c05a40663fd` | 73 done / 7 repair | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 11 confirmed / 6 refuted / 2 advisory |
| 282 | `batch-523380060ecba03a1855` | 72 done / 8 repair | 64 OK / 16 ISSUE | 11 OK / 5 ISSUE | 13 confirmed / 3 refuted / 5 advisory |
| 283 | `batch-ecdac9654ed6a7ed78eb` | 73 done / 6 repair / 1 blocked | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 10 confirmed / 5 refuted / 2 advisory / 2 pending |
| 284 | `batch-2693c7d9d6bb6b335806` | 72 done / 7 repair / 1 blocked | 68 OK / 12 ISSUE | 7 OK / 5 ISSUE | 10 confirmed / 4 refuted / 2 advisory / 1 pending |
| 285 | `batch-fa1ef950617bf0290a74` | 75 done / 5 repair | 71 OK / 9 ISSUE | 4 OK / 5 ISSUE | 7 confirmed / 2 refuted / 5 advisory |
| 286 | `batch-5ce6060013cbbb517e2c` | 67 done / 11 repair / 2 blocked | 62 OK / 18 ISSUE | 10 OK / 8 ISSUE | 18 confirmed / 3 refuted / 3 advisory / 2 pending |
| 287 | `batch-de7c2c3d32f752f42784` | 70 done / 8 repair / 2 blocked | 65 OK / 15 ISSUE | 9 OK / 6 ISSUE | 14 confirmed / 4 refuted / 1 advisory / 2 pending |
| 288 | `batch-fbefc4aef1a281aee013` | 74 done / 6 repair | 70 OK / 10 ISSUE | 4 OK / 6 ISSUE | 10 confirmed / 4 refuted / 2 advisory |
| 289 | `batch-69f00dcf5db5ae40631c` | 71 done / 9 repair | 69 OK / 11 ISSUE | 3 OK / 8 ISSUE（refreeze） | 15 confirmed / 4 refuted |
| 290 | `batch-41762084bcf428db6c44` | 74 done / 6 repair | 68 OK / 12 ISSUE | 8 OK / 4 ISSUE | 8 confirmed / 6 refuted / 2 advisory |
| 291 | `batch-6da096d4813ef282276a` | 72 done / 8 repair | 71 OK / 9 ISSUE | 2 OK / 7 ISSUE | 14 confirmed / 1 refuted / 1 advisory |
| 292 | `batch-92e9dabe8523a9675217` | 75 done / 5 repair | 72 OK / 8 ISSUE | 2 OK / 6 ISSUE | 10 confirmed / 2 refuted / 2 advisory |
| 293 | `batch-a5f999f9d09ac32f56d6` | 73 done / 7 repair | 70 OK / 10 ISSUE | 5 OK / 5 ISSUE | 12 confirmed / 2 refuted / 1 advisory |
| 294 | `batch-37852a9bef8a75bb4c44` | 73 done / 7 repair | 67 OK / 13 ISSUE | 6 OK / 7 ISSUE | 13 confirmed / 6 refuted / 1 advisory |
| 295 | `batch-9af99942882ed4c5cb18` | 74 done / 6 repair | 69 OK / 11 ISSUE | 6 OK / 5 ISSUE | 11 confirmed / 2 refuted / 3 advisory |
| 296 | `batch-65e59046c4f9480d483f` | 74 done / 6 repair | 70 OK / 10 ISSUE | 7 OK / 3 ISSUE | 9 confirmed / 1 refuted / 3 advisory |
| 297 | `batch-8553828be64ba67f2632` | 78 done / 2 repair | 72 OK / 8 ISSUE | 6 OK / 2 ISSUE | 2 confirmed / 6 refuted / 2 advisory |
| 298 | `batch-fddb88b07b599a5e41c8` | 76 done / 4 repair | 72 OK / 8 ISSUE | 5 OK / 3 ISSUE | 7 confirmed / 2 refuted / 2 advisory |
| 299 | `batch-0dad341e579abd2a2943` | 73 done / 7 repair | 69 OK / 11 ISSUE | 5 OK / 6 ISSUE | 13 confirmed / 3 refuted / 1 advisory |
| 300 | `batch-ecb36bb9015065be5656` | 73 done / 7 repair | 69 OK / 11 ISSUE | 5 OK / 6 ISSUE | 13 confirmed / 2 refuted / 2 advisory |
| 301 | `batch-153eb9d93371e710a533` | 69 done / 11 repair | 65 OK / 15 ISSUE | 6 OK / 9 ISSUE | 19 confirmed / 3 refuted / 2 advisory |
| 302 | `batch-4f83e2380a274e472806` | 76 done / 4 repair | 72 OK / 8 ISSUE | 7 OK / 1 ISSUE | 5 confirmed / 2 refuted / 2 advisory |
| 303 | `batch-3990108296cb406fa158` | 75 done / 5 repair | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 10 confirmed / 4 refuted / 5 advisory |
| 304 | `batch-d3c1ad725b3e20176046` | 74 done / 6 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 8 confirmed / 1 refuted / 5 advisory |
| 305 | `batch-cb5e672c5ec0a450c4b4` | 74 done / 6 repair | 67 OK / 13 ISSUE | 8 OK / 5 ISSUE | 11 confirmed / 1 refuted / 6 advisory |
| 306 | `batch-da14fcfb8e992e06a51e` | 75 done / 5 repair | 72 OK / 8 ISSUE | 3 OK / 5 ISSUE | 9 confirmed / 3 refuted / 1 advisory |
| 307 | `batch-0ddb6472afc8da3cb0a3` | 76 done / 4 repair | 71 OK / 9 ISSUE | 6 OK / 3 ISSUE | 7 confirmed / 3 refuted / 2 advisory |
| 308 | `batch-919843e97b237942c8e1` | 75 done / 5 repair | 70 OK / 10 ISSUE | 5 OK / 5 ISSUE | 10 confirmed / 5 refuted |
| 309 | `batch-a04cd9783cf93c0e6527` | 73 done / 7 repair | 70 OK / 10 ISSUE | 3 OK / 7 ISSUE | 12 confirmed / 4 refuted / 1 advisory |
| 310 | `batch-c1080b675d02cd2c3588` | 75 done / 5 repair | 71 OK / 9 ISSUE | 7 OK / 2 ISSUE | 7 confirmed / 3 refuted / 1 advisory |
| 311 | `batch-b6a6a747b3fa260bc4d4` | 76 done / 4 repair | 69 OK / 11 ISSUE | 5 OK / 6 ISSUE | 7 confirmed / 6 refuted / 4 advisory |
| 312 | `batch-dfd4251b605b613e8c59` | 76 done / 4 repair | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 8 confirmed / 3 refuted / 4 advisory |
| 313 | `batch-956938150e4478686ed4` | 75 done / 5 repair | 72 OK / 8 ISSUE | 3 OK / 5 ISSUE | 9 confirmed / 2 refuted / 2 advisory |
| 314 | `batch-0a22d3e718c78608ca2e` | 73 done / 7 repair | 69 OK / 11 ISSUE | 5 OK / 6 ISSUE | 12 confirmed / 5 refuted |
| 315 | `batch-99739a89bb8dd600573a` | 74 done / 6 repair | 66 OK / 14 ISSUE | 10 OK / 4 ISSUE | 10 confirmed / 4 refuted / 4 advisory |
| 316 | `batch-598a0ead226a12acb790` | 76 done / 4 repair | 67 OK / 13 ISSUE | 10 OK / 3 ISSUE | 7 confirmed / 4 refuted / 5 advisory |
| 317 | `batch-f1bba7a4ed46912b5a75` | 77 done / 3 repair | 72 OK / 8 ISSUE | 5 OK / 3 ISSUE | 5 confirmed / 3 refuted / 3 advisory |
| 318 | `batch-5f6096df2cd705ed56e7` | 75 done / 5 repair | 62 OK / 18 ISSUE | 13 OK / 5 ISSUE | 8 confirmed / 10 refuted / 5 advisory |
| 319 | `batch-23e1c4938bb6155d1b29` | 74 done / 6 repair | 68 OK / 12 ISSUE | 5 OK / 7 ISSUE | 12 confirmed / 4 refuted / 3 advisory |
| 320 | `batch-b4a672d30e9d08428a7e` | 76 done / 4 repair | 66 OK / 14 ISSUE | 11 OK / 3 ISSUE | 6 confirmed / 8 refuted / 3 advisory |
| 321 | `batch-2d7befa2545967c13bf0` | 76 done / 4 repair | 68 OK / 12 ISSUE | 6 OK / 6 ISSUE | 8 confirmed / 8 refuted / 2 advisory |
| 322 | `batch-966a30f506c5616356f4` | 71 done / 9 repair | 65 OK / 15 ISSUE | 10 OK / 5 ISSUE | 14 confirmed / 2 refuted / 4 advisory |
| 323 | `batch-c754292cac5215570ec1` | 72 done / 8 repair | 69 OK / 11 ISSUE | 3 OK / 8 ISSUE | 16 confirmed / 1 refuted / 2 advisory |
| 324 | `batch-26cbd9e0dd11f97a3bb2` | 73 done / 7 repair | 70 OK / 10 ISSUE | 5 OK / 5 ISSUE | 12 confirmed / 3 refuted |
| 325 | `batch-6a31f7c0db522a0aebcc` | 77 done / 3 repair | 72 OK / 8 ISSUE | 5 OK / 3 ISSUE | 6 confirmed / 2 refuted / 3 advisory |
| 326 | `batch-39099d09ceaf3dba860e` | 74 done / 6 repair | 68 OK / 12 ISSUE | 9 OK / 3 ISSUE | 9 confirmed / 3 refuted / 3 advisory |
| 327 | `batch-ce57ffd564611fd19267` | 75 done / 5 repair | 69 OK / 11 ISSUE | 6 OK / 5 ISSUE | 10 confirmed / 4 refuted / 2 advisory |
| 328 | `batch-ce732f19626519bd62bc` | 78 done / 2 repair | 73 OK / 7 ISSUE | 3 OK / 4 ISSUE | 4 confirmed / 5 refuted / 2 advisory |
| 329 | `batch-dd7c9f57b4d10b8580df` | 77 done / 3 repair | 75 OK / 5 ISSUE | 2 OK / 3 ISSUE | 6 confirmed / 1 refuted / 1 advisory |
| 330 | `batch-a56cdce9f90a044bdd63` | 73 done / 7 repair | 71 OK / 9 ISSUE | 2 OK / 7 ISSUE | 14 confirmed / 1 refuted / 1 advisory |
| 331 | `batch-4d2f8031e94dec5144e8` | 75 done / 5 repair | 68 OK / 12 ISSUE | 7 OK / 5 ISSUE | 10 confirmed / 4 refuted / 3 advisory |
| 332 | `batch-e163d4f972b4339fa63d` | 75 done / 5 repair | 68 OK / 12 ISSUE | 9 OK / 3 ISSUE | 8 confirmed / 4 refuted / 3 advisory |
| 333 | `batch-4d284ce485ea0c143bf4` | 79 done / 1 repair | 75 OK / 5 ISSUE | 3 OK / 2 ISSUE | 2 confirmed / 5 refuted |
| 334 | `batch-252ef3e5a545f45b02aa` | 73 done / 7 repair | 69 OK / 11 ISSUE | 4 OK / 7 ISSUE | 14 confirmed / 1 refuted / 3 advisory |
| 335 | `batch-81fb42df237b10690b28` | 77 done / 3 repair | 74 OK / 6 ISSUE | 4 OK / 2 ISSUE | 5 confirmed / 2 refuted / 1 advisory |
| 336 | `batch-4febd4ec8c5db6217763` | 78 done / 2 repair | 70 OK / 10 ISSUE | 8 OK / 2 ISSUE | 4 confirmed / 3 refuted / 5 advisory |
| 337 | `batch-f9aceac9a97f5fe7f20e` | 77 done / 3 repair | 70 OK / 10 ISSUE | 6 OK / 4 ISSUE | 6 confirmed / 5 refuted / 3 advisory |
| 338 | `batch-e4fe7a44fc32bf6f4d91` | 73 done / 7 repair | 66 OK / 14 ISSUE | 7 OK / 7 ISSUE | 12 confirmed / 6 refuted / 3 advisory |
| 339 | `batch-039763ae7e35cbc42c5e` | 72 done / 8 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 10 confirmed / 2 refuted / 2 advisory |
| 340 | `batch-35b99737bcb15a9d73bc` | 75 done / 5 repair | 72 OK / 8 ISSUE | 4 OK / 4 ISSUE | 9 confirmed / 1 refuted / 2 advisory |
| 341 | `batch-55dfe3590ba5584a8f1c` | 74 done / 6 repair | 72 OK / 8 ISSUE | 3 OK / 5 ISSUE | 11 confirmed / 2 refuted |
| 342 | `batch-309f974ce42949994c6f` | 74 done / 6 repair | 68 OK / 12 ISSUE | 6 OK / 6 ISSUE | 12 confirmed / 3 refuted / 3 advisory |
| 343 | `batch-f53abe84eebb72eb0f37` | 78 done / 2 repair | 69 OK / 11 ISSUE | 9 OK / 2 ISSUE | 4 confirmed / 2 refuted / 7 advisory |
| 344 | `batch-e878f97bb5160a9024e6` | 73 done / 7 repair | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 12 confirmed / 2 refuted / 5 advisory |
| 345 | `batch-d43220638712024b72e4` | 77 done / 3 repair | 73 OK / 7 ISSUE | 3 OK / 4 ISSUE | 6 confirmed / 2 refuted / 3 advisory |
| 346 | `batch-85a38f3abc94fd9f6478` | 79 done / 1 repair | 77 OK / 3 ISSUE | 2 OK / 1 ISSUE | 2 confirmed / 2 refuted |
| 347 | `batch-6ba3aed2c3dec5c72216` | 74 done / 6 repair | 73 OK / 7 ISSUE | 2 OK / 5 ISSUE | 11 confirmed / 1 refuted |
| 348 | `batch-cb782c29f8583a6e6046` | 75 done / 5 repair | 69 OK / 11 ISSUE | 4 OK / 7 ISSUE | 10 confirmed / 3 refuted / 5 advisory |
| 349 | `batch-e03c72d3df594510acce` | 78 done / 2 repair | 74 OK / 6 ISSUE | 4 OK / 2 ISSUE | 3 confirmed / 2 refuted / 3 advisory |
| 350 | `batch-d4cf75fd2ee85585d522` | 71 done / 9 repair | 65 OK / 15 ISSUE | 5 OK / 10 ISSUE | 16 confirmed / 7 refuted / 2 advisory |
| 351 | `batch-afcff7cb54b3816378ca` | 73 done / 7 repair | 71 OK / 9 ISSUE | 6 OK / 3 ISSUE | 10 confirmed / 2 advisory |
| 352 | `batch-d6c5b26ceae7fdd04bb7` | 74 done / 6 repair | 68 OK / 12 ISSUE | 6 OK / 6 ISSUE | 12 confirmed / 1 refuted / 5 advisory |
| 353 | `batch-8382beda5373e4b7b515` | 74 done / 6 repair | 70 OK / 10 ISSUE | 4 OK / 6 ISSUE | 11 confirmed / 2 refuted / 3 advisory |
| 354 | `batch-cae8d8bde9f429a45a88` | 76 done / 4 repair | 70 OK / 10 ISSUE | 7 OK / 3 ISSUE | 7 confirmed / 3 refuted / 3 advisory |
| 355 | `batch-fbcd32274a9a90faab4a` | 25 done / 5 repair | 22 OK / 8 ISSUE | 4 OK / 4 ISSUE | 8 confirmed / 1 refuted / 3 advisory |
| 356 | `batch-4a7dd7135bbe1a68607d` | 19 done / 1 repair | 18 OK / 2 ISSUE | 1 OK / 1 ISSUE | 1 confirmed / 2 advisory |
| 357 | `batch-06020dfb9cbf406a4526` | 74 done / 6 repair | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 12 confirmed / 6 refuted / 1 advisory |

每批证据摘要在 `evidence/quality/production-batches/<batch>-host-evidence/summary.md`。

## 二、授权与节奏（用户指示）

- 2026-09-23：先做工具维护，然后持续推进审核，不需逐批确认；有争议的条目列入 pending，等用户集中审阅。
- 2026-09-24：修复先记录，**积压达到 20 条或以上再一并修复**，取代原来每批审核后接一个小修复窗口的 1:1 节奏。
- 每批（或每个窗口）完全收口后 push；批次进行期间不得提交任何东西。
- 用户随后明确要求推进新批次，暂停已解除。第 276 批的 DLC reviewer 边界修复与按原模型重派也已获明确授权。
- 2026-09-25：第278批后的暂停已由用户明确解除（“验收完毕后合入主开发区，然后让主开发区空闲的 opus5.5 agent
  继续推进审核工作”）。主持由 Opus 5.5 接手，从第279批起按既定顺序连续推进；停止条件照常生效。
- 无需再次询问审核外发或 push 授权；现有授权继续有效。
- 2026-09-25 用户：后续将审批轮次放宽到5次（修复窗口 max_cycles 默认 5，STATE 须同时写
  `max_cycles_user_authorized=true`）。
- 审核模型：surface `codex/gpt-6-sol`（medium，auto-review），contextual `claude/claude-opus-5-5`（medium，auto）；
  修复 EXECUTOR `codex/gpt-5.6-sol`。

## 三、窗口 27 已修历史（28 条）

下表是窗口 27 已完成的冻结修复范围，仅作历史记录，不再是当前待修积压。

| 来源批次 | revision（前 8 位） | 修复内容 |
| --- | --- | --- |
| 273 | `fcb8219f` | “反魔法”提示第三行“拒绝使用法术”→无法使用法术与奥术驱动的装备（forbid_arcane 是硬限制） |
| 273 | `fd267689` | 领袖的皇冠描述整句（许多人而非大部分、秩序与纪律、效忠皇冠、称呼统一为“皇冠”、纳格尔领土而非大陆） |
| 274 | `fd89fad0` | 裂解：每目标每回合可各除一项物理和一项魔法增益；补回物理伤害→物理、时空伤害→魔法的对应关系 |
| 274 | `fd9c72bf` | 技能名 Unstoppable Nature“自然世界”→“势不可挡的自然”一类 |
| 274 | `fda88c96` | 技能名 Reflex Defense“闪避神经”→“反射防御”一类（机制是减伤与降低受暴击倍率） |
| 274 | `fdff442a` | 粘液：友方单位条件“经过”→处在粘液中 |
| 274 | `fe42c359` | 半身人炼金术士对话末句：恢复“越晚回来”与“冒烟的弹坑” |
| 275 | `fe5a84a1` | 燃烧之手：补“（及武器）”，体力回复改“每次命中” |
| 275 | `fe90619e` | 恶魔空间：补“每回合”、持续光环、“法术结束时” |
| 275 | `fec0939b` | 黑暗者古尔莫特墓志铭拆回三行（LF 6→5 实测） |
| 275 | `ff47fb86` | 回复纹身加载提示整句（预判伤害、提前准备；物品名统一“回复纹身”） |
| 275 | `ff585d0b` | 任务名 From bellow, it devours 与 mod-tome.lua:38225 对齐为“来自深渊，吞噬四方” |
| 275 | `ff658fab` | wispy purple cloak“脆弱的”→“缥缈的” |
| 276 | `ffb21dd4` | `seems less dangerous`：“平静了下来”→威胁降低 |
| 276 | `ffe80f4c` | 传送门描述补回 `strange` 的“奇异”限定 |
| 276 | `fff84873` | 石傀儡 `can become unstoppable`：改为可进入该状态，不写成永久不可阻挡 |
| 276 | `0523b499` | Ashes 灼热土地平台分裂的时序与意象，避免写成醒后已分离 |
| 276 | `0c22616d` | `treacherous road` 改为险途，保留世界之巅与引号 |
| 276 | `0ed56881` | `Most simply run` 改回逃跑，`destruction's engines` 不添战争机器 |
| 277 | `10419e2e` | black flame 恢复黑色，避免误作邪恶火焰 |
| 277 | `119af893` | extracting / willing 的斜体强调位置与原文对齐 |
| 277 | `120d3d48` | 水晶记忆对白恢复踏板、束缚装置及被删时序，不添“思维”限定 |
| 277 | `12c3c45f` | 3 arms 改“三条手臂”，非“三只手” |
| 277 | `1be82f2f` | primary ambush 改首轮伏击，并写明已脱身 |
| 277 | `218c180b` | 乌鲁洛克认可库马纳的心智、同条专名一致、锦标赛错字及体能耐力 |
| 277 | `21d89ecd` | 堡垒停在兵工厂上方而非主动瞄准；修复“怀着／所拥有”等错字和增译 |
| 277 | `28ea9897` | fiery display 恢复炽烈/火焰意象，不用闪电 |
| 277 | `295b84f0` | 恶魔形态说明后续行恢复两个制表符缩进；“半径”有机制依据，保留 |

范围与源码依据：273 见 `.ai/task/batch-5e69946bed52ed5a5cbc/WINDOW27-REPAIR-DECISION.json`，274–277 见各自
`.ai/task/<batch>/REPAIR-BACKLOG-DECISION.json` 与 `HOST-FINAL-DECISIONS.json`。
本窗发布记录见 [`evidence/quality/repair-window-27-20260924/PUBLICATION.md`](evidence/quality/repair-window-27-20260924/PUBLICATION.md)。

## 四、本轮工具维护与文档整理（2026-09-24）

- `queue.rebuild` 在 carry scope 内把完整重放交给后续步骤复用（仍每次完整重放）。
- 新增 `run_batch_steps.py rollover-chain --limit N`：关闭后的 queue rebuild + 下一批 start，只重放一次历史（约省 4 分钟）。
- 新增 `run_repair_steps.py publish-chain`：译文提交后的 queue rebuild + catalog build + migration plan/check/apply，
  只重放一次历史（每个窗口约省 4 分钟）。
- 新增 5 个回归测试；完整门禁 17/17 通过（含严格构建）。
- 新增 [审核操作指南](docs/review-operations-guide.md) 与 [宿主辅助件模板](docs/review-operations/templates/README.md)；
  删除过期的 `docs/baseline-batch-runbook-2026-09-06.md`、`docs/handoff-history-through-20260919.md`、
  `docs/review-handoff-20260918-batch192.md`，其中仍生效的裁决已并入指南第六节；引用处已改指向指南。
- 2026-09-25 工具优化（已合入 `d6dc518e`，随第279批一并推送）：A 门禁测试 fixture 隔离父进程缓存变量，
  父 shell `I18N_PROJECTION_CACHE=on` 可直接跑 prepare-evidence 与完整门禁，不再需要 unset（第279批已实测 17/17）；
  B 单次投影内复用完整相同行字节的已成功 catalog 行校验，cache-off 完整投影中位 251.99→87.58 s（实测），
  峰值 RSS +13.5%。磁盘缓存仍默认关闭；门禁运行期间不要编辑 `tools/`。详见
  [`docs/review-tool-speed-results-20260925.md`](docs/review-tool-speed-results-20260925.md)。
- 尚未实施的提速项：把 `surface-import` 与 `contextual-export` 合成一次调用（需放宽 `prepare_contextualN.py`
  的 phase 断言到 `deep_ready`），见指南 4.3 节。

## 五、下一步

1. 继续审核第 **358** 批（默认 80 条，连续推进）；用 `.artifacts/i18n/continuation-20260923/bd.sh` 驱动（`N=<批号>; source bd.sh` 须分两句；第299批起只需 `N=<批号>`，S、PT 默认取上一批）（派生后核对 snapshot 脚本里的 chain 日期）（混合批用 290/287 的 stage/snapshot/close，单组件批用 288/294 的；
   `prepare_contextual290` 起已按每个 run 的组件写 SPEC）。修复积压达 20 再开下一窗口（模板 `setup_window47b.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w47b-20260928/wd.sh`、`/tmp/w47b-*.sh`；setup 后先跑 `check_siblings.py`）。
2. 窗口 47b 已完成（B 组：用户 2026-09-27 裁决的单条措辞与名称，待审第 3、6、8–14、17、18、20–29、31–35、38、39、41 项共 48 条，加窗口 47a 转入 8 条：“火魔婴”→“火焰小鬼”6、“物品黑暗麻木”→“物品暗影麻木”1、雕像名“莎西·凯希”1；名称类按用户指示采用 Gemini 3.8 Flash 结论；术语库未改）。复审另确认并修复 workset 内旧缺陷：科技法师进阶说明的蒸汽工具配方与“蒸汽科技/物理系”“蒸汽科技/化学系”、梅塔什对话两条（漏译半岛各处/为了我们、增译“算了”、光束打穿岩层露出天空）、米诺陶 lore（漫长岁月、精神焕发）、亡灵猎手指南署名统一、华丽抛枪后续技能多余换行；死亡描述 f6cc31f278 被 GPT-6 Sol 连报五次，均按模板“%s而死”与待审 #18 裁决驳回。四次修复后 cycle 4 FINAL 56/56 OK（max_cycles 5）；门禁 17/17。advisory：9af7773a4c 的 A.P.E. 缩写本库一贯不译；f5f092ac5d 歌词 ogre/over 双关（47a 转入）。下一步审核窗口 47a（77）与 47b（56）的 successor（第357批起）。窗口外宿主补充项待下个窗口按 revision 核实后纳入：“stack of herbs”同族四条“一束植物”→“草药”（advisory，跨条）；Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）；`95496f3e7a` 等：区域名“太阳堡垒观星台”与 lore 分类名“太阳堡垒瞭望台”（术语 existing，tome-orcs.lua:2494）不一，随待审第 37 项 Sunwall 译名一并统一；第337批 advisory `9a75f2d93d`（精神雄蜂 bores into）、`9af7773a4c`（A.P.E. 缩写）；第342批 advisory `b6e17ee9e4`（Crimson Templar John“深红骑士约翰”，本库另有“深红圣武士”“赤红守卫”，Templar 译名待统一）、`b437b99574`（铜制护目镜附言“自爱的工匠”翻译腔）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`，并从 PATH 去掉 `/opt/agents/bin`（2026-09-27 重启后新增的 shell 包装器会遮蔽真实 pi，致门禁 04 失败；`bd.sh` 已处理）；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window47b.py`（全部宿主补充、无批次 preflight）、`.artifacts/i18n/repair-w47b-20260928/wd.sh` 与 `/tmp/w47b-*.sh`；开窗 setup 后先跑 `.artifacts/i18n/repair-w46-20260927/check_siblings.py <WORKSET>` 列跨组件同键兄弟并写 RUNTIME-SYNC（窗口 35、40 都因漏列在门禁 06 失败）；每轮复审 harvest/归档后须立即跑 `publish.py` 发布 stage 记录（窗口 39 漏跑、事后补发，见 HOST-NOTE-LATE-PUBLICATION.md）。
   窗口 48 积压 **6** 条（第357批，主游戏+Ashes）：`ba5e371016`（艾伦尼恩回忆录第一章四处）、`dc3200b76d`（次元浮岛抛入虚空）、`175effe253`、`196ce36308`（Ashes 开场陨石/世界之间/水晶）、`3626a66415`（莎西·凯希 lore 限定词）、`6a71689b25`（水小鬼雕像 lore；water imp 按用户指示咨询 Gemini 3.8 Flash 定为“水小鬼”，与火焰小鬼对仗，开窗先加术语行再全库 4 行同步：mod-tome.lua:7997、tome-ashes-urhrok.lua:127/519/520）；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。
   第357批计时（实测，投影缓存 on）：start 122.3 s；adjudication chain（含 17 项门禁）167.5 s；finalize 126.3 s。
3. 窗口 28 的操作教训：同一 cycle 内 `RE_REVIEW` 之后冻结 `FINAL_REVIEW` 时，逻辑 attempt 使用 2；
   长 lore 条目开窗时由宿主先逐句预检，再合并进入修复与复审。
4. 专名待用户集中审阅：[待用户集中审阅的争议条目](evidence/quality/pending-user-review.md)（当前 37 项；Osmosis Regen(eration) 同族第23/24/26项，Corruption of the Doomed 同族第22/25/29项，Armoured Leviathan 同族第21/27/28项；第 30 项 numbed→麻痹（Numbing 族）；第 31 项软蹄族／软蹄者（Soft-foot）；第 32 项 Thunder Grenade 闪电榴弹；第 33 项 Voltaic Bolt 闪电球；第 34 项 Supercharge Bullets 超速子弹；第 35 项 Awesome Toss 致命翻转；第 36 项 Gardanion 物品名未译；第 37 项 Sunwall 全库译名不一）。
5. 全 DLC 批次的操作要点：adjudication chain 一开始就传 SHA 核验的 `reviewN-source-root`；首次 contextual envelope 不含 checkout
   位置（`--ashes-checkout` 只在 refreeze 路径生效），Opus 可能自行搜寻而越界（第277、280批各一次），届时拒收并按 refreeze 重派；
   surface 某 lane 判废须整组用 `tools/surface_screen_manifest.py build --attempt 2 --group-id group-000-retry-02` 重建（envelope 字节不变）。

## 六、环境备忘

- 宿主工作目录 `.artifacts/i18n/continuation-20260923`（已 gitignore），Paseo workspace `wks_420314270844170b`，
  live profiles 快照 `$C/profiles-live-01.json`。
- 上游源码 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；子 agent 看不到这个检出，
  它们报“commit 不存在、证据不足”时由宿主自查。
- 未跟踪文件 `.ai/consult/`、`recipe` 与旧的 `evidence/quality/production-batches/*-source-workset.json`（15 个）
  是既有遗留，保持不动。
- 历史保留边界：Archmage `8b977dd836…` 仍为范围外 pending；`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 第 277 批 contextual 首轮 Opus 为找 DLC checkout 枚举 `/workspace`，输出被拒收并确认归档；重冻后单个 Opus run 读取边界通过并 DONE_VERIFIED。
- 第 276 批 contextual 原本按主游戏 6 条、Ashes DLC 5 条拆成两个 Opus run；DLC 两次旧输出因 `find /` 越界被拒收并归档。
  规则 prompt 与契约现明确禁止从 `/` 或无关目录扫描，并在新 envelope 中给出本批 DLC checkout；同 event 重冻后两路 reviewer 均通过读取边界检查与 `DONE_VERIFIED`。
