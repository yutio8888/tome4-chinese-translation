VERDICT: READY

未发现 blocking 问题。以下 advisory 不阻断本次显示修复。

1. [advisory] 测试尚未覆盖生产包装和总安装入口。tests/test_dynamic_desc_fixes.lua:57-59 用简化 tformat，:134、:178 直接安装裸上游定义，:208 只验证 Bloodstream 缺失；未执行 M.install() 的 require 失败/无 DLC 路径，也未把真实 replaceFormat 放在内层，未注入格式化异常。建议补充这些集成/回退用例，以及移除后 compute_vals 三个槽确实为空、resists.all 恢复的断言。当前测试并非纯自证：确实加载了公开 DLC 的 activate/deactivate 与固定核心的临时值实现，但 Bloodstream 期望值仍复述显示公式，未运行 action 的条件分支。

2. [advisory] 异常回退保留原有错误数值。hooks/dynamic_desc_fixes.lua:56-58、:87-91 回到原始描述，因此异常或效果已移除时可再次显示 getDamageInc 或临时值 id；这满足安全退回上游行为，但不保证回退后中文数值准确。格式化异常有一次日志；registry 缺失的正常形态回退没有日志。无需为此改游戏状态。

核验依据：

- Bloodstream：DLC data/talents/steam/sawmaiming.lua:64-66、:75-86、:98 明确区分 getDamageInc 与 getDamage。实际倍率是 getDamage/100；锥形伤害也是 getDamage（随后 steamCrit）。修复 :49-54 使用正确倍率，且保留原始 damDesc 的物理伤害显示实参；固定核心 game/modules/tome/data/talents.lua:100-142、:154 导出该函数。中文 tome-orcs.lua:5757 的命中、攻击前存在 EFF_CUT、攻击后仍存在、bloodstreamed 一次限制与源码一致；“变为原来的”准确允许低于 100%。源码不要求攻击前后为同一 table，译文也未额外声称对象身份相同。
- 自动修复：DLC data/timed_effects/other.lua:548-551 将三个 eff 字段覆盖为 id；固定核心 Entity.lua 的 addTemporaryValue 直接将传入 v 登记到 compute_vals[id]，因此读取的是本效果登记的生命恢复增量、{all=抗性增量}、负 die_at 增量，而非 actor 总量。修复 :66-77 形态检查和负号还原正确；deactivate :557-561 经 removeTemporaryValue 清空槽，之后检查失败并退回上游。该说明显示本效果贡献，并不承诺叠加其他来源后的总死亡阈值。
- locale 与状态：修复 :47、:85 在非 zh_hans 下直接调用捕获的原函数并透传参数；英文返回值逐字节保持。修复只写共享定义的函数和幂等标记（:60、:93），描述调用不写 eff、actor、compute_vals 或存档字段；读取不到预期值不尝试补登记或修改参数。固定源码 getter 无临时值写入，异常路径亦无新增游戏状态写操作。
- 加载与包装：核心 game/modules/tome/load.lua:174-177、:267 在基础定义加载后触发 ToME:load；DLC hooks/load.lua:23 绑定 Orcs.hookLoad，其 overload/mod/class/OrcCampaign.lua:56-61 加载目标定义。按题设插件权重高于 DLC，插件 hooks/load.lua:107-111 在 DLC 回调之后安装。现有 superload/engine/interface/ActorTalents.lua:10-11、ActorTemporaryEffects.lua:5 将原函数包在 replaceFormat 中；新中文路径直接 tformat，无需再次包装，英文/回退仍经过原包装。overload/engine/i18nhelper.lua:19-22 会恢复 string.format。缺失定义或必要函数时安装无操作；标记防止重复套层。

验证：在 /workspace/tome4-chn-mod 使用指定三个 CHN_TEST_* 环境变量运行 LuaJIT 测试，Entity.lua 从核心提交 624a67329fe2 导出至 /tmp/r6/review/Entity.lua；结果 ALL OK，未运行游戏。DLC 依据所提供公开检出，未固定其 commit/版本；核心依据指定固定提交。未修改任何仓库文件。
