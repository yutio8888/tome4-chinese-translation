VERDICT: READY

未发现 blocking 问题。结论限于冻结的 3580885、配套 translation.diff、0.3.13 locale 与所列公开源码；DLC 检出没有冻结 commit，因此机制核验的来源仍属未固定。

1. [advisory] 建议将真实 I18N 查找及 Bloodstream 的 replaceFormat 调用链纳入长期回归。tests/test_dynamic_desc_fixes.lua:84-85 把 _t/tformat 简化为字典查找/string.format，未检验 tag、nil fallback、args_order/special 或真实 loadLocale；:301-335 的包装链测试只针对 Automated Repair。现有矩阵确实调用了公开 DLC 原 info 与插件 wrapper，并覆盖四组数值、低于 100% 的倍率、六种代码/locale 配对、异常回退、英文原样和 actor 不变，并非纯粹重复实现；但单靠该测试不能证明生产 I18N 集成。此次已额外用固定引擎 I18N.lua 的真实实现和插件真实 replaceFormat，在 /tmp/r7/review/check-i18n.lua 验证专用键的加载、tag/fallback、无该键 args_order/special、Bloodstream 中文路径、英文与缺译文回退，全部通过。该补充 harness 只模拟外围 class/fs/loadfilemods 与 actor，不运行游戏；原始翻译片段加载时补入 locale 头。

核验依据：

- engine/I18N.lua（核心 624a67329fe2，game/engines/default/engine/I18N.lua:42-59、67-94）：get 按 tag 查找后回退到 "nil"；set 同时写 tag 和 "nil"。_t 缺译文返回原键，故 dynamic_desc_fixes.lua:55-58 的比较对于本次专用键可靠。这检查的是有效译文存在，不承诺译文一定来自某一 tag；此处与 tformat 使用的查找语义一致。引擎不会剥离 ## 后缀，它完整参与键匹配，不影响 % 占位符格式化。专用键没有 args_order/special（补充条目只有三个参数，真实加载核验也确认缺省），四个参数顺序不被重排。
- data/chn_supplement.lua:1、82-90 明确注册 zh_hans；hooks/load.lua:4-11 先载入补充 locale，再加载修复模块，:107-111 在 ToME:load 安装。I18N.lua:97-120、129-163 对同一 locale 表累加登记，setLocale 选择对应表；不要求安装当时已经选择中文。能力检查在每次 info 调用时执行。专用键和原键内容不同，且增加 chn-mod 专用后缀；冻结输入中未见冲突。不能对未知第三方插件作绝对无冲突承诺。
- DLC data/talents/steam/sawmaiming.lua:64-66、75-86：攻击前记录 EFF_CUT，攻击后重新取值，仅 hit、was_cut、cut 且未 bloodstreamed 时延长持续时间并令 cut.power *= getDamage/100，随后投射窄锥伤害。补充中文 :86-90 与条件、一次强化限制和倍率一致；“变为原来的”可正确表达低于 100% 的数值。dynamic_desc_fixes.lua:73-78 保留武器伤害、回合数、倍率、damDesc(PHYSICAL,getDamage) 的顺序；原 info :98 则传 getDamageInc 为第三参数。tome-orcs.lua:5757 恢复“伤害增加”对应旧实参契约；它保留上游原有机制描述缺陷，是明确约定的兼容回退，不等于修复后专用中文的机制准确性。
- 核心 game/modules/tome/data/talents.lua:100-154 定义 damDesc 并导出 Talents.damDesc，插件 install():127 使用该函数；第三参数保持原始倍率而第四参数使用伤害显示换算，与原 info 结构一致。
- dynamic_desc_fixes.lua:68-82：中文且专用键有效才使用 getDamage；缺译文、非中文及新格式化路径抛错均调用捕获的原 info。新代码+新/旧 locale 且有补充键显示 getDamage 倍率文案；没有补充键显示 getDamageInc 增加文案；旧代码+新 locale 仍走原键和 getDamageInc；新路径异常也回到原键和旧实参。因此未出现约定禁止的交叉配对。英文路径直接返回原 info 的结果。
- superload/engine/interface/ActorTalents.lua:5-13 在 newTalent 时把 info 包入 helper:replaceFormat；overload/engine/i18nhelper.lua:3-25 临时替换 string.format，调用后恢复。动态修复安装在定义注册之后，捕获该包装函数作为回退；成功的新路径在外层直接 tformat，无嵌套包装依赖。额外真实引擎调用链验证通过。
- dynamic_desc_fixes.lua:61-65、84、121-131 对缺定义/缺依赖不安装，重复安装由定义标志拦截。新增操作仅替换定义 info、写定义标志和模块内一次性警告表，未写 actor、cut、eff 或存档。没有 DLC 时现有回归测试验证 install 无错。
- data/chn_supplement.lua:82-90 的 CRLF 在 LuaJIT 解析长字符串时规范化为 LF。现有测试 :151 的键存在断言已直接加载实际 CRLF 文件，额外真实 I18N harness 也确认代码键不含 CR 且能命中补充条目，不存在行尾导致的键失配。

执行结果：指定 CHN_TEST_* 环境下的 luajit tests/test_dynamic_desc_fixes.lua 退出 0，输出 ALL OK；补充真实 I18N harness 退出 0，输出 REAL I18N + Bloodstream replaceFormat chain OK。所有写入仅在 /tmp；未修改仓库、未运行游戏。
