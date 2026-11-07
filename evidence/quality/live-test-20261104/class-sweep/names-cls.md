你是《马基埃亚尔的传说》(ToME4) 简体中文汉化的译名顾问。下面每项都是同一界面里撞名或译法不一致的技能/技能树名，请各给一个简体中文译名，写入 /tmp/gem-work/names-cls.json，格式：{"A": {"name": "...", "reason": "..."}, ...}；有两个名字的项用 {"name1": "...", "name2": "...", "reason": "..."}。只写这个文件，不做别的。
通用约束：不要和下面列出的已占用译名重名；风格与本库一致（技能名多为 2–5 字，技能树名多为 2–4 字）。已占用：闪避（Evasion 技能、Defense 属性名）、躲闪、时空守卫（职业 Temporal Warden）、石化皮肤（法术 Stone Skin）、奥术岩盾（技能 Eldritch Stone）、奥术盾击、空间跳跃（Dimensional Step）、时空折叠（技能树 Spacetime Folding）、时空（chronomancy/spacetime 系统称）。

A. 半身人种族技能 "Duck and Dodge"（被动：生命值降低时获得闪避加成）。现译「闪避」，与 Evasion 技能及闪避属性撞名。
B. 时空守卫职业的技能树 "Temporal Guardian"（防御、护盾与守护技能）。现译「时空守卫」，与职业名完全相同。
C. 灵能唯我论者的两棵技能树 "Dream Smith"（在梦境中锻造武器护甲的技能树）与 "Dream Forge"（以梦之熔炉发出冲击、护盾的通用技能树）。现译「梦境锻造」「梦之熔炉」，玩家分不清。给 name1=Dream Smith，name2=Dream Forge。
D. 矮人种族技能 "Stoneskin"（被动：受到打击后皮肤硬化，提高护甲）。现译「石化皮肤」，与土系法术 Stone Skin 同名。
E. 石之守护者的技能树 "Earthen Vines" 与其中第 1 个技能 "Stone Vines"（召唤岩石藤蔓缠住敌人）现都译「岩石藤蔓」。同树其他技能：奥术藤蔓、岩石漫步、岩石吞噬。给 name1=技能树 Earthen Vines，name2=技能 Stone Vines（可保留其一为「岩石藤蔓」）。
F. 石之守护者的技能树 "Eldritch Shield"（同树技能：奥术盾击、奥术充能、奥术连击、奥术猛击）与 "Eldritch Stone"（同树技能：奥术藤蔓、奥术岩盾等）。现译「魔力盾牌」「魔法岩石」，与树内「奥术…」技能不一致。给 name1=Eldritch Shield 树，name2=Eldritch Stone 树（注意不能与技能「奥术岩盾」重名）。
G. 时空守卫的两个技能 "Dimensional Anchor"（把目标锚定在空间中、阻止传送）与 "Spatial Tether"（用空间系绳把目标拴在某处，拉回时受伤）。现译「时空锚」「时空系绳」，但 dimensional/spatial 是「空间」，「时空」应留给 spacetime。给 name1=Dimensional Anchor，name2=Spatial Tether。