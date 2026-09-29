```json
{
  "entries": [
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "技能数值、盲目条件、占位符与加成阶梯描述准确。"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "召唤失败日志翻译准确，标点差异不构成错误。"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "雪人描述、材质与蒸汽链锯专名翻译准确，首句意译未违背事实。"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "身体复制数量与高阶生物使用次数惩罚表述准确。"
    },
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": ["C01"],
      "brief_reason": "将庆幸统治短暂（mercifully brief）误译为“仁政”，叙事态度颠倒。"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主手武器与副手灵晶装备要求描述准确。"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": ["C02", "C03"],
      "brief_reason": "违反术语库使用已排除译名“西方灾星”，且将判定候选失败误译为面对困难。"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "伤害吸收几率与潜行强度占位符及效果对应无误。"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "调查卷次标题与残缺专名音译保留准确。"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": ["C04"],
      "brief_reason": "将异界纸条此前已着火的时序状态误译为卷入时突然起火。"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": ["C05"],
      "brief_reason": "漏译永久绑定与戒指可随心所欲召唤数回合的关键机制信息。"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": ["C06"],
      "brief_reason": "将高百分比能量朝最大值恢复的互斥机制误译为两者均以更高比例恢复。"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": ["C07"],
      "brief_reason": "漏译主动取消技能触发伤害的条件，误将伤害限定于攻击或施法中断。"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避触发反击射击机制、武器伤害比例与频次限制完整准确。"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "职业特征警示与新手提示准确，格式控制符完整保留。"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": ["C08"],
      "brief_reason": "漏译技能生效前提“处于附身形态时”，丢失关键触发条件限制。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "the mercifully brief reign of King Traglamar",
      "target_quote": "特拉格拉玛王短暂的仁政",
      "change": "将修饰统治短暂令人庆幸的副词mercifully brief误译为“仁政”，叙事态度颠倒。",
      "context_counter": "上下文及同卷48章均说明该统治对所有当事人极度尴尬，非肯定政绩，排除等价读法。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 165,
          "quote": "which Kasyros would only tell me \"was deeply embarassing for all involved\""
        }
      ],
      "text_status": "文本语义与叙事态度可证",
      "snapshot_fact": "源码及关联文本均证实该统治为负面历史",
      "target_applicability": "适用",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "the Scourge from the West",
      "target_quote": "西方灾星",
      "change": "违反术语库明确规定，将preferred专名“西方天灾”误写为已明确排除的“灾星”。",
      "context_counter": "术语库notes明确规定“统一为‘西方天灾’，不写作‘灾星’”，属于dlc生效范围。",
      "evidence": [
        {
          "path": "terminology/society.tsv",
          "line": 34,
          "quote": "Scourge from the West\t西方天灾\tT.PN.PERSON\tsociety\t_t\tpreferred\tdlc\tEmbers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”"
        }
      ],
      "text_status": "专名术语库冲突可证",
      "snapshot_fact": "DLC范围内preferred术语唯一规范",
      "target_applicability": "适用",
      "impact": "expression"
    },
    {
      "id": "C03",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "deeming many failures",
      "target_quote": "面对无数的困难",
      "change": "将艾德隆筛选候选人时“认定多数人选为失败者”误译为主角“面对无数的困难”。",
      "context_counter": "主语为艾德隆评估options，与前句options及后句one to be finally chosen呼应，非叙事动作面对困难。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 104,
          "quote": "It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen."
        }
      ],
      "text_status": "文本句法与叙事动作可证",
      "snapshot_fact": "文本描述艾德隆挑选主角决策过程",
      "target_applicability": "适用",
      "impact": "narrative"
    },
    {
      "id": "C04",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire when the paradox anomaly pulled it in",
      "target_quote": "当时空异常从另一条世界线拉入这条纸条的时候，这张纸条突然着火了",
      "change": "将纸条此前在异界已着火的时序状态误译为被拉入时突然起火，歪曲叙事时序。",
      "context_counter": "原文过去完成时had already说明着火先于拉入，非拉入导致的突发起火事件。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "时态时序偏差文本可证",
      "snapshot_fact": "异时空纸条在卷入前已处于燃烧状态",
      "target_applicability": "适用",
      "impact": "narrative"
    },
    {
      "id": "C05",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "binding John to it forever. The ring is now able to summon him for a few turns at will.",
      "target_quote": "将约翰绑定到戒指上。戒指现在具有召唤他的能力。",
      "change": "漏译永久绑定（forever）以及戒指可随心所欲召唤数回合（for a few turns at will）。",
      "context_counter": "召唤持续时间与随意激活条件是戒指机制核心，漏译致使玩家无法获知临时召唤限制。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 116,
          "quote": "binding John to it forever. The ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "机制参数与条件遗漏可证",
      "snapshot_fact": "对话赋予玩家戒指召唤约翰数回合功能",
      "target_applicability": "适用",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代",
      "change": "将百分比更高的一方朝向最大值恢复的互斥机制，误译为两者均以更高比例恢复，丢失二选一与朝向最大值目标。",
      "context_counter": "源码do_polarize严格对比二者百分比仅使较高者正向恢复且朝向max，译文机制彻底颠倒。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
          "line": 64,
          "quote": "if (self:getPositive() / self:getMaxPositive()) >= (self:getNegative() / self:getMaxNegative()) then"
        }
      ],
      "text_status": "机制条件与数值目标扭曲可证",
      "snapshot_fact": "技能极化机制仅使高百分比能量朝最大值增长",
      "target_applicability": "适用",
      "impact": "mechanism"
    },
    {
      "id": "C07",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "When this effect is broken or cancelled",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成",
      "change": "漏译主动取消该技能（cancelled）触发伤害的条件，将伤害误绑定为仅攻击或施法中断时生效。",
      "context_counter": "该技能为持续技能，主动关闭（deactivate）同样触发周围伤害，译文排除了主动取消途径。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 67,
          "quote": "deactivate = function(self, t, p) ... if p.charges then self:project ... end"
        }
      ],
      "text_status": "操作条件遗漏可证",
      "snapshot_fact": "sustained技能无论被打断或主动关闭均结算伤害",
      "target_applicability": "适用",
      "impact": "mechanism"
    },
    {
      "id": "C08",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form you may cannibalize a body",
      "target_quote": "吞噬一具储备的身体，用来补充现在的身体。",
      "change": "漏译技能生效前提“处于附身形态时”（When you assume a form）。",
      "context_counter": "附身系技能吞噬储备身体仅在附身形态下可用，漏译前置条件使玩家误以为本体形态可吞噬。",
      "evidence": [
        {
          "path": "tome-possessors/data/talents/psionic/body-snatcher.lua",
          "line": 88,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "前置触发条件遗漏可证",
      "snapshot_fact": "附身技能必须在assume a form形态下执行",
      "target_applicability": "适用",
      "impact": "mechanism"
    }
  ],
  "read_files": [
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F11-r2.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P1.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r2.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/evidence-cards.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua"
  ],
  "limitations": [
    "Possessors源码缺失，所有判定仅基于冻结文本、上下文及机制声明进行纯文本可证性核查。",
    "Orcs源码哈希固定，但DLC仓库commit及目标版本未固定，机制解释依据公开固定快照。"
  ]
}
```