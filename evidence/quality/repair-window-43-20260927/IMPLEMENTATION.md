# repair-w43-20260927 implementation

Role: Paseo EXECUTOR
Scope: `tome-orcs.lua` WORKSET 25 targets only
Source: `/workspace/tome4-dlcs/orcs` paths frozen by `SOURCE-ANCHORS.json`

## Changes

1. `a27688ff3f72672447396d04b85c27f968d541c301d2e69b937b0a814d74c6e8` — `Powered by `：改为“装备力量来源 ”，保留用于运行时拼接的末尾空格。
2. `a2aa6c921a9d503e70300e1386e304eb8090b27e85babf7ef11d9493b71c67c4` — 补回“把链锯绑在双臂上”的动作特征。
3. `a2d8aa0cb9ed8d6b879c95fffb43c4a4a159fee0be1331bb48f9b5eeb15a562f` — Explosives 说明恢复 4 行及每个续行的两个 TAB；保留已确认的学习机制表述。
4. `a3a35758bd4127b678ed0e34dd7ff8003a0571c8b4753ee5a84a5400764b84ca` — steam giant 仅挥舞战斧，删除“冲来”增译并将 battleaxe 译为“战斧”。
5. `a3cecc7f1f6f555ecfa59f86e08ca69ad7acd00bb70c44e91dfaa759469af241` — 披风说明第二行恢复两个 TAB。
6. `a49b334d447d3a4920b3b71565c9b5b7152fc4ea83ad74c2a945a9825c947f85` — 长串续行移除错误 TAB，并把 tinker crafting 统一为“插件制作”。
7. `a668705856cd7297fb89aed03e5d5d647948c81d2efba4a280d9663d3ef6d0a6` — GEM 录音全文逐句修复 posterity、all too clear、so long ago、称谓、beauty、partnership、询问语气、all are welcome、gurgling、将来奖赏、新形体/心智与录音结束等问题；18 行结构与 markup 保持。
8. `a79480d625d3593293180ae270d12e20e6ccd11ce1e4b1573b3b9ce5081882b8` — 两处单位对象改为“敌人”。
9. `a7c20343e019cce5d4df8b82cc25c868d4ba6f6257b3331ad8640c80d2b0ecf1` — 阿马克泰尔颂诗全文逐句修复 reform、is nigh、delectable、三类敌人、设计/大理石/愿景、儆戒、共同找出异端、重复书页和 new existence；26 行、空行、`%s` 与 markup 保持。
10. `a9d2942514aebb65224ae0806a4725fdcb5d5abcda0e188bb8ddc492555d5fe7` — lore 名补出 torn，改为“约翰日记中撕下的一页”。
11. `ab005d53a8a9ce237b391f31a1e77297bead08c229d1cacd3c4f5dbcf0f17c50` — 补出 petty 的轻蔑语气与“赏/推迟死亡”的因果。
12. `ac38d13dc57f0dfd674cae664fe1acfc460074be2207a9adb2b1b49d8726276a` — 补出爆裂伤害类型“物理”。
13. `ac986bd586ae5c6fe2e37037e175e03a739b6f0c7571630799cdad1d98e50cd5` — 删除“力大无穷”增译，仅保留难以阻挡与定身抗性。
14. `af09f513b941c59aeff494b425b2bb2048eb5faf7bac1c8ace34286cc29967b1` — classy goggles 改为“考究的护目镜”。
15. `afa6a8bcfdb2fd5b120a1b01a20a18b3dfc69244bc79ecbecba14a51d59a3eff` — Heartrend 附言按 spilt/heartsblood 重写并去除“像心脏一样跳动”的重复；空白行不补源文的单个行尾空格。
16. `afb30f1aafc14f8bd6f77c87487185c1a530cfee6fcd501470693effbaa99a8c` — 明确安置引爆器后须在 100 回合内撤离，否则会被炸毁。
17. `b18f5ccf7cdd8f33f933720c18371b6e6217c65df91960f96d607e0385116a98` — Voltaic Shell 补“至多 %d 名”、ammo 自指句、句末标点和全部 4 个续行 TAB。
18. `b24d120d1c6b67054879766b12648fd23fdf22bdb6c0ea3f88dee13cb813275e` — Steam Powered Armour 的 4 个续行全部恢复两个 TAB，语义不改。
19. `b2f95a8393bb06c5b3a690940e05bf2d2379808616184db36b6dfca33a02b384` — `Whatever.` 改为轻蔑语境的“无所谓。”；同源不同 `source_tag` 记录保持不变。
20. `b4989e1df22170f87b14a2fc0500bb37dd109311bdf48ab29a4b97d501047623` — Flamethrower 全句修复为燃烧装置喷射液态火焰、对敌人造成火焰伤害，复数 attacks 对齐；纯空白行不新增行尾 TAB。
21. `b4d7ff1a4001d0be91d23b12e86ebde6437657b8d2197034fcc6b45956772611` — 炮台“最大生命值增加”，superheated air 改为“过热空气”；敌人对象保持。
22. `b5c9934b1171e91a7919e1e65b3dc09abf3f0de927ce979935f7427ae2024eb1` — 恢复 you 主语与 before 顺序，secure 译为“打通道路”。
23. `b6ae150553ec66f89be082249cb66554630d1562d3e1177a9d91a43b5e30c16d` — 删除灵能之雾首句后的多余换行，只保留 Mindpower 前换行。
24. `b7d5bb68d3a17c91f0cfcb3e67b552b04034d48686f5708f74e6d2d6739b5ae6` — 补出灼烧血肉及“通过格式塔以灵能吸收蒸汽”；沿用本文件既定“格式塔”“蒸汽强度”。
25. `b8a51a2baf55814b910447d4809e55131fd85a83562d44f64d5c30ddf447b2ad` — 技能名统一为“蜘蛛机器人护盾”。

## Plan deviation

`SPEC.md` 的标题、条目清单、四批计数（8+5+6+6）和冻结 WORKSET 均为 25 条，但验证段写成“恰23个 target 变动”。本实现依用户指令和冻结 WORKSET 按 25 条执行；LuaJIT 证明恰 25 条。

## Unresolved / risk

- Orcs 源码文件 SHA 与冻结锚点全部匹配，但源码仓库和 commit 未固定；不能把本机 checkout 当作版本 pin。
- 未执行独立语言复审与正式 17 项门禁；由宿主按 PLAN 后续完成。
- 未 stage、commit 或 push；未修改 `.ai/task/`，未触碰无关未跟踪文件。
