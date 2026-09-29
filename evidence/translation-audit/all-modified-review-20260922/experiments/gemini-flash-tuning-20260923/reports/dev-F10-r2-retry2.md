```json
{
  "entries": [
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "技能数值、条件与加成效果翻译准确"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "召唤失败日志翻译准确"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "怪物外貌描述与术语准确传达"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "身体储存复制机制与减额折算合理等价"
    },
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "将万幸短暂统治误译为仁政"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主副手装备需求说明准确"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C02",
        "C03"
      ],
      "brief_reason": "违反西方天灾术语规范且误译候选筛选描述"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "烟幕吸收伤害与潜行增益表达清晰"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "调查书章节标题残缺格式对应正确"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "将拉入前早已着火误译为突然起火改变时序"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "遗漏召唤持续数回合及随意召唤条件"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C06"
      ],
      "brief_reason": "错译极化机制筛选条件并遗漏回复至最大值"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C07"
      ],
      "brief_reason": "遗漏主动取消技能同样触发伤害的条件"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避反击射击机制与消耗说明准确"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "新手职业机制警告说明准确"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C08"
      ],
      "brief_reason": "遗漏占据形态时方可执行吞噬的前置条件"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "mercifully brief reign",
      "target_quote": "短暂的仁政",
      "change": "将副词修饰语“mercifully brief”（万幸短暂）误译为“短暂的仁政”，反转了叙事态度。",
      "context_counter": "上下文及misc.lua明确指出特拉格拉玛统治令所有人深感尴尬，短暂属万幸，绝非施行仁政。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "Obviously, the mercifully brief reign of King Traglamar is an exception"
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 142,
          "quote": "aside from a brief period under King Traglamar, which Kasyros would only tell me \"was deeply embarassing for all involved\""
        }
      ],
      "text_status": "mistranslation",
      "snapshot_fact": "源码文本表明特拉格拉玛王统治因尴尬荒唐而万幸其短暂。",
      "target_applicability": "1.7.4",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "the Scourge from the West",
      "target_quote": "西方灾星",
      "change": "专有名词违背术语库preferred规范，误译为“西方灾星”。",
      "context_counter": "术语库society.tsv明确规定统一为“西方天灾”，且备注特别强调“不写作‘灾星’”。",
      "evidence": [
        {
          "path": "dev/terms.json",
          "line": 675,
          "quote": "{\"source\": \"Scourge from the West\", \"target\": \"西方天灾\", \"category\": \"T.PN.PERSON\", \"status\": \"preferred\", \"scope\": \"dlc\", \"notes\": \"Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”\"}"
        }
      ],
      "text_status": "terminology_violation",
      "snapshot_fact": "DLC术语规范统一个体名女性为西方天灾。",
      "target_applicability": "1.7.4",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "deeming many failures",
      "target_quote": "面对无数的困难",
      "change": "将主语艾德隆筛选主角时的判定“视许多备选为失败者”误译为主角“面对无数的困难”。",
      "context_counter": "原句主语为It，述及考虑多种候选、淘汰失败者并最终选中一人，非主角面对困难。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 104,
          "quote": "It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen."
        }
      ],
      "text_status": "mistranslation",
      "snapshot_fact": "叙事描述艾德隆挑选故事主角的筛选过程。",
      "target_applicability": "1.7.4",
      "impact": "narrative"
    },
    {
      "id": "C04",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire",
      "target_quote": "突然着火了",
      "change": "将过去完成时状态“早已着火”误译为突发动作“突然着火了”，歪曲了事件时序。",
      "context_counter": "原句强调纸条从异界拉入前就已起火，因此仅来得及看标题；并非拉入时才突然起火。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "mistranslation",
      "snapshot_fact": "时空异常拉入纸条前纸条已处于燃烧状态。",
      "target_applicability": "1.7.4",
      "impact": "narrative"
    },
    {
      "id": "C05",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "for a few turns at will",
      "target_quote": "具有召唤他的能力",
      "change": "遗漏“for a few turns at will”，未体现随意见面召唤且仅持续数回合的机制限定。",
      "context_counter": "源码中约翰召唤具有明确持续时间（john.summon_time = 12），并非永久召唤。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 74,
          "quote": "john.summon_time = 12"
        },
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 117,
          "quote": "The ring is now able to summon him for a few turns at will.*"
        }
      ],
      "text_status": "omission",
      "snapshot_fact": "约翰被召唤后的生存时间被设定为12回合。",
      "target_applicability": "1.7.4",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值",
      "change": "将仅百分比更高的一方朝最大值回复，错译为正负能量均用更高百分比恢复，且遗漏向最大值回复。",
      "context_counter": "源码do_polarize明确判断占比更高的单侧能量朝最大值回复，另一侧向静止值消退。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
          "line": 64,
          "quote": "if (self:getPositive() / self:getMaxPositive()) >= (self:getNegative() / self:getMaxNegative()) then"
        },
        {
          "path": "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
          "line": 124,
          "quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max instead of its normal resting value"
        }
      ],
      "text_status": "mistranslation",
      "snapshot_fact": "极化机制仅使当前百分比更高的单侧能量正向回复至上限。",
      "target_applicability": "1.7.4",
      "impact": "mechanism"
    },
    {
      "id": "C07",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "broken or cancelled",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时",
      "change": "遗漏“or cancelled”（主动取消），未说明玩家手动关闭维持技能同样会触发周身伤害。",
      "context_counter": "技能为持续模式（mode=\"sustained\"），源码deactivate表明主动关闭同样触发爆炸伤害。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 27,
          "quote": "mode = \"sustained\","
        },
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 67,
          "quote": "deactivate = function(self, t, p)"
        },
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 90,
          "quote": "When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you."
        }
      ],
      "text_status": "omission",
      "snapshot_fact": "锯轮在手动关闭或被攻击/技能打断时都会执行deactivate伤害。",
      "target_applicability": "1.7.4",
      "impact": "mechanism"
    },
    {
      "id": "C08",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form",
      "target_quote": "吞噬一具储备的身体，用来补充现在的身体。",
      "change": "遗漏前置触发条件“When you assume a form”（当你占据形态时），使触发时机不明。",
      "context_counter": "英文首句明确吞噬是在占据形态时方可执行的操作，译文直接省略该条件句。",
      "evidence": [
        {
          "path": "dev/entries-r2.json",
          "line": 214,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "omission",
      "snapshot_fact": "附身系技能吞噬为占据形态时可选择执行的操作。",
      "target_applicability": "1.7.4",
      "impact": "mechanism"
    }
  ],
  "read_files": [
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F10-r2.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P1.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r2.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/engineering.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/uber/mag.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/gem/npcs.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/pocket-time.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/physical.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/misc.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/chats/john-surrender.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/gunslinging.lua"
  ],
  "limitations": [
    "Orcs DLC源码属于白名单指定哈希快照，未固定DLC仓库commit及发行版本；",
    "Possessors DLC源码缺失（source_pinning为unavailable），附身系条目仅依纯文本可证事实进行审核，不作未核验机制推断。"
  ]
}
```