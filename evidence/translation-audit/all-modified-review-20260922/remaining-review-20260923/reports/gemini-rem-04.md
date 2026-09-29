# rem-04 译文审核报告

## 逐条审核汇总表

| entry-ID | 判定状态 | 疑点编号及简要依据 |
| :--- | :--- | :--- |
| `entry-03860` | 存在问题 | C01（confirmed: formally endorsing 误译为“隆重推出”）；C02（advisory: Marshall 职位内文“团长/队长”不一致）；C03（advisory: mental skills 精神技能翻译腔） |
| `entry-03861` | 存在问题 | C04（confirmed: 擅自注入富文本标记 `[b]...[/b]`）；C05（advisory: show sb what-for 俚语“难堪”偏软） |
| `entry-03864` | 存在问题 | C06（confirmed: not blame 追责问责误译为“抱怨”）；C07（confirmed: first order of business 议程术语误拼为调查步骤）；C08（advisory: As far as I am concerned 主观立场误译为知情界限） |
| `entry-03865` | 存在问题 | C09（confirmed: DESTRUCTICUS 违背受控术语库译为“毁天灭地”）；C10（confirmed: spells inadequate 法术效力不足误译为“不准”）；C11（advisory: dispose of 处置消灭轻译为“赶走”） |
| `entry-03871` | 仅建议 | C12（advisory: High Paladin 头衔用字建议对齐术语库“高阶太阳骑士”） |

---

## 原子疑点清单

### C01 | entry-03860 | confirmed
短引：原文“formally endorsing the board game”译为“隆重推出桌面游戏”。
差异：endorsing 意为公开背书、正式支持或推荐；前文已交待选拔机制为公民公投决定决选竞技项目，该局是呼吁选民投票支持该桌游作为选拔方案，而非自己开发或发行该游戏（后文已明言该游戏已上市一年且有6.0大众版）。译文错为主体推出产品，扭曲政治公投请愿性质。
等价反证：若视作推广宣传，中文“推出”特指首发上线，与后文“已推出了一年”自相矛盾，不可等价。建议改为“正式推荐/公开支持”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L38](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L38)。来源：DLC orcs（来源未固定）。

### C02 | entry-03860 | advisory
短引：段2原文“Marshall of the City Guard”译“城市卫兵团长”，段4原文“Marshall's election”译“选出卫兵队长时”。
差异：同一篇文献中前后两处指代同一市政职位的名词，分别被译为“团长”与“队长”，存在篇内专名与官职称谓不一致。
等价反证：虽“Marshall”在不同军事层级可灵活意译，但在同一公告短文内属于同一选举事件与职位实体，割裂译名易令读者误以为两个不同层级官职。建议统一为“卫兵队长”或“卫兵长”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L38-L42](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L38-L42)。来源：DLC orcs（来源未固定）。

### C03 | entry-03860 | advisory
短引：原文“mental skills”译为“精神上的技能”。
差异：原文语境系承接上文的慎思远见、决断急智、知人善任与说服能力，指领导者所需的智力与心智素养。在 ToME4 奇幻语境中，“精神技能”极易与灵能、意志属性或精神伤害混淆，存在翻译腔。
等价反证：字面直译虽不完全算错，但脱离心智素质语境并产生机制歧义。建议优化为“心智素养”或“脑力才能”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L36](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L36)。来源：DLC orcs（来源未固定）。

### C04 | entry-03861 | confirmed
短引：末尾原文“VOTE FISTICUFFS”译为“[b]请投肉搏战[/b]”。
差异：原文为全大写纯文本口号，无任何富文本标记；译文擅自添加了原文不存在的 BBCode 粗体标签 `[b]...[/b]`。违反了 markup 标记、格式控制符必须忠实保持不变量的门禁要求。
等价反证：即便游戏富文本引擎能正常解析渲染，汉化条目也不得无端向纯文本注入未定义标签，破坏词条格式对齐与回编译规范。处理：移除 `[b]` 与 `[/b]` 标签，保留“请投肉搏战”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L52](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L52)。来源：DLC orcs（来源未固定）。

### C05 | entry-03861 | advisory
短引：原文“show that old geezer what-for”译为“让那个老东西难堪”。
差异：“show sb what-for”为英语固定俚语习语，意为“给某人点颜色瞧瞧/严厉教训收拾某人”，带有强烈的肉体或政治打击意味；译为“难堪”偏向使其尴尬出丑，弱化了煽动性海报痛击对手的火药味。
等价反证：政见羞辱虽含难堪成分，但“肉搏战（FISTICUFFS）”语境下该口号强调的是以力量制裁教训老议长。建议调整为“给那个老东西点颜色瞧瞧”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L50](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L50)。来源：DLC orcs（来源未固定）。

### C06 | entry-03864 | confirmed
短引：原文“not blame”与“don't want blame because...”译为“而不是抱怨”及“不想要抱怨”。
差异：blame 在议会事故调查与争吵语境中确指“推卸责任/指责归咎/追究罪责”（下文紧接“这是你的错”），而“抱怨”对应 complain。译文将核心定责与政治问责错译为情绪发泄类的“抱怨”，严重软化并扭曲了议员间相互推诿决策责任的对抗实质。
等价反证：日常口语中指责偶有抱怨含义，但在飞艇坠毁、战事失利的官方会议记录中，双方交锋的是事故责任归属（blame vs fault），非口角牢骚。建议改为“指责/追责”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L139-L141](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L139-L141)。来源：DLC orcs（来源未固定）。

### C07 | entry-03864 | confirmed
短引：原文“The first order of business at the next session will be determining...”译为“接下来进行调查的第一部分，将会决定……”。
差异：“first order of business”为标准议事程序术语“首要议程/第一项议题”，“next session”指“下次会议/下次全会”。原文前一句动议刚通过“启动官方调查”，本句是指下次会议将首先审议纳沙尔的设备能否拔出其头颅。译文将其错拼为“调查的第一部分”，混淆了议会会期议程与调查阶段。
等价反证：议会成立调查委员会并非立即进入第一环节，此句是对下次会议日程的讽刺性动议，不可曲解为调查步骤。建议改为“下次会议的首要议程”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L135-L136](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L135-L136)。来源：DLC orcs（来源未固定）。

### C08 | entry-03864 | advisory
短引：原文“As far as I am concerned”译为“据我所知”。
差异：“As far as I am concerned”标准语义为“在我看来/就我而言/依我之见”，表达主观立场与利益取舍；而“据我所知”对应“As far as I know”，表达事实掌握界限。此处为坦塔洛斯表明其不愿将兽人视作本方防务责任的态度，非陈述知情限度。
等价反证：两者虽同属插入语，但认知事实与主观立场的混淆会略微弱化坦塔洛斯冷酷推脱责任的人设。建议改为“在我看来/依我之见”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L147](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L147)。来源：DLC orcs（来源未固定）。

### C09 | entry-03865 | confirmed
短引：原文“DESTRUCTICUS”译为“毁天灭地”。
差异：`terms.json` (line 1257) 明确登记该专名/实体名首选受控译名为“毁灭号”，且 notes 明确警示“欢呼与叙词统一为‘毁灭号’，不写作‘毁天灭地’”。原文指代武器实体（裂天者 毁灭号），译文将其望文生义意译为成语“毁天灭地”，直接违背既定术语规则。
等价反证：即便该词根源自 destruction，受控术语库已明确禁止使用四字成语意译，强制要求统一武器实体简称。处理：必须更正为“毁灭号”。
证据：[terms.json#L1257-L1266](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json#L1257-L1266)；[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L170](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L170)。来源：DLC orcs（来源未固定）。

### C10 | entry-03865 | confirmed
短引：原文“their invisibility spells were inadequate”译为“他们的隐形咒语不准”。
差异：inadequate 含义为“不够强/效力不足/不过关”（导致隐形法术未能瞒过兽人侦测）；被错译为射击或空间精度概念的“不准”（将法术威能不足曲解为施法命中率失准），逻辑不通。
等价反证：隐形法术属于状态覆盖类法术，不存在命中“准不准”，只有隐蔽效果与反隐对抗的强度差异。译文出现概念层级错置，必须修正为“隐形法术效力不足”或“法术不过关”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L172](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L172)。来源：DLC orcs（来源未固定）。

### C11 | entry-03865 | advisory
短引：原文“disposing of these barbarians”译为“把那群野蛮人赶走”。
差异：dispose of 意为“处置/除掉/消灭/解决掉”；坦塔洛斯借由忠诚者的行星穿凿伟力，其意图是彻底消灭摧毁兽人威胁，译为“赶走”程度偏轻，弱化了其残忍冷酷的灭绝性企图。
等价反证：虽然驱逐在某些战役语境中可算解决方式，但面对生死存亡的决战叙事，“除掉/消灭”远比“赶走”更契合语境力量感。建议调整为“除掉那群野蛮人”。
证据：[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L185](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua#L185)。来源：DLC orcs（来源未固定）。

### C12 | entry-03871 | advisory
短引：原文“High Paladin”译为“至高太阳骑士”。
差异：`terms.json` (line 1807) 规定太阳堡垒领袖完整头衔为“高阶太阳骑士”（High Sun Paladin Aeryn），且 notes 明确要求统一称呼不省“高阶”。正文中此处特指艾琳，译作“至高”与现有统称“高阶”出现细微偏差。
等价反证：虽“High”可意译为至高，但为保证全库阵营官职头衔严谨一致，建议对齐术语库规范，统一使用“高阶太阳骑士”。
证据：[terms.json#L1807-L1816](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json#L1807-L1816)；[.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/sunwall.lua#L37](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/sunwall.lua#L37)。来源：DLC orcs（来源未固定）。

---

## 读取路径与版本限制说明

1. **实际读取的文件路径**：
   - 批次任务输入：[`rem-04.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-04.md)
   - 审核规则契约：[`RULES.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md)
   - 访问源控制清单：[`source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json)
   - 统一受控术语库：[`terms.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json)
   - 冻结源码上下文：
     - [`.artifacts/.../orcs/tome-orcs/data/lore/palace-fumes.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua)（SHA256: `b57c1122b56037bd86ca9815e8a59700db548755d9c401e5ee17959a5cf3fc2a`）
     - [`.artifacts/.../orcs/tome-orcs/data/lore/sunwall.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/sunwall.lua)（SHA256: `e80b0cf896d7160ed3e69b411ae4a9b375a813e3b6ba61803d98e46d573d85e1`）

2. **版本限制声明**：
   - 本批次所有条目均归属于 `orcs`（Embers of Rage DLC）。
   - 根据 `source-access.json` 与 `RULES.md` 规定，DLC 源码固定方式为快照哈希锁定（`frozen_root`），其源码仓库 commit 与游戏目标版本未固定（`source_pinning: unpinned`）。
   - 本次审核仅依据快照源码核验文本一致性与叙事逻辑，不宣称已核验 1.7.4 正式运行时行为。不写文件、未派生子代理、未读取任何已归档报告。

