# 第八轮实机测试裁决（2026-11-06）

测试员 r8-opus（Opus 5.5）：主战役，半身人星月术士 Opus8，简单／冒险，9 级；巨魔沼泽→卡·普尔→德斯镇→古老森林 1–4 层（击败水晶树精）→纳尔湖 1 层；约 120 个界面。圣诗切换增益（圣诗专家）已实际触发并核对；法阵系在 9 级前尚未解锁，未测（留待 10 级后补测）。7 条发现，均为 minor。

修改前均先检索同类问题（见各条）。

- r8-opus-01 confirmed（用户 2026-11-06「同意采用C」）：前缀词缀按 `ego_always_prefix`（官方 zh_hans/zh_hant 同样设置，Zone.lua:541 拼接 `display .. _t(e.name)`）总是拼在基础名前，「一袋铁制子弹」会变成「电弧的一袋铁制子弹」。10 个弹药基础名去掉量词：榆木/白蜡/紫杉/精灵木/龙骨箭矢，铁制/钢制/矮人钢/斯莱特/沃瑞钽子弹。同类检索：其余「一袋…」均为炼金材料或固定物品（pouch of crystallized ice 为神器），不会带词缀，未改。
- r8-opus-02 confirmed，延后（插件代码）：盾牌 add_name「 (#ARMOR#, #SHIELD#)」在 class/Object.lua:593 直接 gsub 拼接，不经 `_t`，本库无可译条目。
- r8-opus-03 confirmed：logCombat「#Source# misses #target#.」「没有命中」→「未命中」，与近战同句一致；同类检索其他 misses 变体已一致。
- r8-opus-04 confirmed：区域名 Derth「德斯」→「德斯镇」；同类检索：逐一对照各城镇区域名与「(Town)」世界地图条目，只有 Derth 不一致。
- r8-opus-05 confirmed：商店日志「Bought/Sold: %s %s for %0.2f gold.」改为「已购买：%s%s，花费 %0.2f 金币。」「已出售：%s%s，获得 %0.2f 金币。」（Store.lua 第一个 %s 为数量或空串，去掉孤立空格与直译「价格」）。
- r8-opus-06 confirmed：世界地图地形 Old forest「远古森林」→「古老森林」，与区域名一致；同类检索 wilderness/grids.lua 地形名与区域名，另将 Unremarkable cave「不显眼的山洞」→「不起眼的洞穴」（区域名 Unremarkable Cave）。「name」一项为误报。
- r8-opus-07 confirmed：圣诗专家「每次你结束旧的圣诗时，你将获得圣诗提供的增益效果。」改为「此外，每当你结束一首圣诗时，你将根据所结束的圣诗获得相应的增益效果：」（hymns.lua deactivate 中按圣诗设置效果）；同句坚毅圣诗行统一为「获得强度 %d 的伤害护盾，持续 %d 回合。」。同类检索：赞歌专家说明与实现（chants.lua doCure 按类型解除）一致，未改。

## 第二段（2026-11-06 15:16–18:44，agent 2b4e911c，同一角色 Opus8）

12 级（目标 13 级未达成），死亡 1 次，剩余生命 3 条；路线：纳尔湖 1→古老森林→德斯镇→迷宫 1–3→黑暗之心 1–3→岱卡拉 1–2。法阵系已解锁（未解锁圣印），四个法阵说明与 circles.lua 核对一致，暗影之阵实战施放；圣诗三种切换增益实测；日蚀系、光之洗礼说明核对一致。复核：03、05、07 与弹药改名已生效；04 区域名在旧存档中仍显示「德斯」，测试员判断为持久化 zone 的存档内名字，待新角色复核。新增 2 条：
- r8-opus-08 confirmed：吞噬者「咬牙切齿」日志「咬 @Target@」去掉占位符前空格。同类检索（单行 t 条目中名字占位符与汉字之间的半角空格）另修 6 处：三头连枷、枯萎毒素注入、尝试吞噬、虚空的疯狂、爆炸后被灼热光线覆盖、「%s 绞杀 #Target#」→「%s绞杀了#Target#！」。
- r8-opus-09 confirmed：伤害类型 healing light「治疗之光」→「治愈之光」，与技能名一致。同类检索（damage_types.lua 中以技能命名、且只由该技能使用的伤害类型）另对齐 7 处：ice storm 冰雪风暴、glacial vapour 寒霜冰雾、congeal time 时间凝固、caustic mire 腐蚀之地、static net 静电网络、pestilent blight 致命枯萎、smokescreen 烟雾弹。flameshock（多个技能共用）、phase pulse、judgement（未对上单一技能）及 lightning/darkness/freeze 等通用类型未改。
