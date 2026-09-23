```json
{
  "entries": [
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "将表达万幸短暂的mercifully brief误译为短暂的仁政，扭曲历史叙事态度。"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "空间不足提示翻译准确，感叹号符合原文且与logSeen术语差异属合法范围。"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "标题结构与48章体例统一，截断保留原文音节，符合着火烧毁语境。"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "躯体克隆与数量除以3表述与机制等价，占位符消费正确。"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "职业机制警告翻译准确，颜色与斜体标记完整对应。"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "伤害吸收概率与潜行值双参数顺序与类型匹配，语义准确。"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将过去完成时被拉入前已着火误译为突然着火，改变事件时序。"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "漏译附身形态前置生效条件When you assume a form，缺失关键机制约束。"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "将百分比高者单向恢复曲解为正负能量均恢复，颠倒极化核心机制。"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "漏译for a few turns at will，遗漏召唤时效限制与随意主动发动条件。"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C06",
        "C07"
      ],
      "brief_reason": "违反preferred术语统一译名，且将筛选主角判定失败误译为面对困难。"
    },
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "蒸汽冲击波伤害、致盲阈值及4个占位符匹配正确，机制无偏差。"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C08"
      ],
      "brief_reason": "漏译or cancelled，遗漏主动取消持续技能同样触发终结伤害的机制。"
    },
    {
      "id": "entry-04078",
      "status": "ISSUE",
      "claim_ids": [
        "C09"
      ],
      "brief_reason": "将评价施虐者手段彻底强行篡改为雪人自身变成杀戮机器，主谓倒错。"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避反击射击触发条件、每回合一次限制与弹药消耗说明准确。"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主手武器与副手灵晶装备限制日志翻译忠实规范。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "mercifully brief reign",
      "target_quote": "短暂的仁政",
      "change": "将表达万幸/谢天谢地很短暂的“mercifully brief”误译为“仁政”，扭曲历史评价与叙事态度。",
      "context_counter": "上下文及同卷前文明确特拉格拉玛王的统治令所有当事人深感尴尬，mercifully修饰brief表庆幸短暂，无仁政之意。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "源码为叙事lore文本，特拉格拉玛王统治在世界观中被明确视作负面尴尬特例。",
      "target_applicability": "适用于文本叙事与历史背景理解。",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire",
      "target_quote": "突然着火了",
      "change": "将过去完成时“had already caught fire”（被拉入前已着火）误译为“突然着火了”，篡改事件时序与初始状态。",
      "context_counter": "83章标题仅存Wei...正是因纸条从另一世界线被卷入时便已在燃烧，而非拉入当前世界线后突发起火。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "文本通过过去完成时描述时空异常卷入已着火物品的叙事因果。",
      "target_applicability": "适用于文本叙事与因果设定。",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form you may cannibalize",
      "target_quote": "吞噬一具储备的身体",
      "change": "完全遗漏前置生效条件“When you assume a form”（当你占据/附身某一躯体时），丢失关键机制限制。",
      "context_counter": "附身系机制中吞噬必须处于附身躯体形态方可生效（同文件日志明确要求先占据躯体），常态无法使用。",
      "evidence": [
        {
          "path": "dev/context.lua",
          "line": 1111,
          "quote": "t(\"You require need to assume a form first.\", \"你需要先占据一个身体。\", \"logPlayer\")"
        },
        {
          "path": "dev/context.lua",
          "line": 1113,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "纯文本条件从句与同文件限制日志均要求必须处于附身形态下方可发动吞噬。",
      "target_applicability": "适用于技能使用机制与限制条件。",
      "impact": "mechanism"
    },
    {
      "id": "C04",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值",
      "change": "将“正负能量中百分比更高者向最大值恢复”曲解为“无论正负能量都将用更高百分比恢复”，机制主体与极化逻辑颠倒。",
      "context_counter": "源码极化逻辑仅使百分比高的一方恢复至上限，另一方按休息值消退；译文误将二者一并设为恢复。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
          "line": 64,
          "quote": "if (self:getPositive() / self:getMaxPositive()) >= (self:getNegative() / self:getMaxNegative()) then"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "源码Polarization技能明确依据正负能量百分比比较，仅单向恢复高者，使低者衰减。",
      "target_applicability": "适用于DLC天赋技能核心运行机制。",
      "impact": "mechanism"
    },
    {
      "id": "C05",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "for a few turns at will",
      "target_quote": "具有召唤他的能力",
      "change": "漏译“for a few turns at will”（随意召唤他持续数回合），丢失召唤时效限制与主动施法条件。",
      "context_counter": "戒指赋予的是主动触发且仅持续数回合的临时召唤能力，译文删减时限与条件使技能机制不明。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 117,
          "quote": "The ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "戒指绑定剧情赋予物品主动激活且有时限的临时召唤效果。",
      "target_applicability": "适用于物品获得技能的实际效果描述。",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "the Scourge from the West",
      "target_quote": "西方灾星",
      "change": "违反preferred术语规范，将“Scourge from the West”误译为“西方灾星”。",
      "context_counter": "术语库society.tsv明确该专名scope为dlc，统一规范为“西方天灾”，且特注“不写作‘灾星’”。",
      "evidence": [
        {
          "path": "dev/terms.json",
          "line": 675,
          "quote": "{\"source\": \"Scourge from the West\", \"target\": \"西方天灾\", \"category\": \"T.PN.PERSON\", \"status\": \"preferred\", \"scope\": \"dlc\", \"notes\": \"Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”\"}"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "术语库明文强制统一该专有名称为“西方天灾”，禁止使用“灾星”。",
      "target_applicability": "适用于DLC专有名词规范。",
      "impact": "narrative"
    },
    {
      "id": "C07",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "deeming many failures",
      "target_quote": "面对无数的困难",
      "change": "将叙述者艾德隆挑选主角时“判定许多人为失败者”误译为“面对无数的困难”，扭曲主语动作与叙事含义。",
      "context_counter": "原文主语为艾德隆在综合考量候选主角（options），deem many failures指筛除不合格者，非主角面对困难。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 104,
          "quote": "It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "文本主旨为创作者视角对多名候选主角的筛选与评价。",
      "target_applicability": "适用于背景故事叙事逻辑与主体行为。",
      "impact": "narrative"
    },
    {
      "id": "C08",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "or cancelled",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力",
      "change": "遗漏“or cancelled”（或主动取消时），误将技能终结伤害仅归结为被动作打断，忽略手动关闭也能触发。",
      "context_counter": "该技能为维持技，deactivate源码表明玩家手动取消或因攻击中断均会触发周围武器伤害，手动引爆为关键机制。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 90,
          "quote": "When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "维持技deactivate回调对被打断与手动取消统一执行伤害释放判定。",
      "target_applicability": "适用于维持技能操作与终结爆发机制。",
      "impact": "mechanism"
    },
    {
      "id": "C09",
      "entry": "entry-04078",
      "status": "confirmed",
      "source_quote": "Whoever tortured and tormented this yeti did an amazing job of pain and destruction.",
      "target_quote": "虽然不知道是谁把这个雪人折磨成这样，它的确变成了一个恐怖的杀戮机器。",
      "change": "将评价施虐者残忍彻底的“did an amazing job of pain and destruction”改写为雪人自身“变成了恐怖的杀戮机器”。",
      "context_counter": "原文主语为Whoever（施虐者），强调施虐手段在造成痛苦与破坏上极其惊人，译文强行调换主谓关系。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/zones/gem/npcs.lua",
          "line": 94,
          "quote": "Whoever tortured and tormented this yeti did an amazing job of pain and destruction."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "文本为NPC Half-Mechanized Yeti的背景描述，评价折磨者的残酷手笔。",
      "target_applicability": "适用于实体叙事与描绘。",
      "impact": "narrative"
    }
  ],
  "read_files": [
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F11-r1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r1.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/evidence-cards.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json"
  ],
  "limitations": "Possessors DLC源码缺失（source_pinning: unavailable），基于冻结条目、上下文语境及同类实现逻辑完成语义与语法核对；Orcs DLC仅哈希快照固定，仓库commit及发行版本未固定，机制核对基于已核验的固定快照源码。"
}
```
