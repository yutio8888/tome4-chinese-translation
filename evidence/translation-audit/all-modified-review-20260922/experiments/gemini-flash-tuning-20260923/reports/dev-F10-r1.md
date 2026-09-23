```json
{
  "entries": [
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "将特拉格拉玛王因糟糕而幸好短暂的统治误译为仁政，颠倒叙事态度与历史语境"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "文本准确传达召唤空间不足日志，标点与source_tag差异符合规则，核验无误"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "调查文献残卷标题与断句保留完整，翻译准确无误"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "身体储备与高阶惩罚机制翻译准确，数值占位符对应无误"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "职业特性警告说明与格式控制标签完整准确，核验无误"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "烟雾掩护吸收伤害几率与潜行强度说明准确，参数消费正确"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将过去完成时拉取前已起火误译为突然着火，产生时序与状态偏差"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "遗漏首句关键机制触发条件“When you assume a form”（附身形态时）"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "将正负能量高者向最大值恢复的互斥机制误译为两者均用更高百分比恢复，逻辑颠倒"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "漏译“for a few turns at will”，遗漏戒指召唤持续时间与主动使用机制"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C06"
      ],
      "brief_reason": "未遵循DLC专用术语规范，将Scourge from the West误译为禁用的“西方灾星”"
    },
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "过热蒸汽阀技能伤害、目盲条件及蒸汽系数换算表达准确，格式符匹配"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C07"
      ],
      "brief_reason": "漏译“or cancelled”，遗漏主动取消持续状态同样触发范围伤害的机制分支"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "雪人改造生化改造描述意译合理，斯莱特/蒸汽链锯等术语准确"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "反击射击触发条件与回合限制表述准确，参数消费无误"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主副手装备限制日志表达准确，术语对应无误"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "mercifully brief reign of King Traglamar",
      "target_quote": "特拉格拉玛王短暂的仁政",
      "change": "将修饰brief的副词mercifully（幸好/谢天谢地）误译为仁政，颠倒了叙事态度。",
      "context_counter": "结合前句正史唯一反面例证及misc.lua尴尬历史，该统治实属不堪，绝非德政。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 145,
          "quote": "aside from a brief period under King Traglamar, which Kasyros would only tell me \"was deeply embarassing for all involved\""
        }
      ],
      "text_status": "文本明确叙事态度偏差",
      "snapshot_fact": "快照中特拉格拉玛王统治为负面历史个例，正史唯一不客观记录",
      "target_applicability": "Orcs快照哈希固定，文本证据充分，适用于当前目标版本",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire",
      "target_quote": "突然着火了",
      "change": "过去完成时“had already caught fire”（拉取前已起火）被误译为“突然着火了”。",
      "context_counter": "时序与状态偏差，改变了纸条在原时间线便已起火并被拉过来的既有事实。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "文本明确时序与事件状态偏差",
      "snapshot_fact": "快照文本明确表达被异常拉取前已处于着火状态",
      "target_applicability": "Orcs快照哈希固定，叙事时序偏差可直接在文本中确认",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body.",
      "target_quote": "吞噬一具储备的身体，用来补充现在的身体。",
      "change": "遗漏首句明确触发条件“When you assume a form”（附身/变身一个形态时）。",
      "context_counter": "该技能机制在附身形态时触发选择，缺失条件使人误以为可随时主动发动吞噬。",
      "evidence": [
        {
          "path": "dev/entries-r1.json",
          "line": 102,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "纯文本明确机制触发条件遗漏",
      "snapshot_fact": "Possessors源码缺失，依COMMON.md规则纯文本可证错误可确认",
      "target_applicability": "无论Possessors源码是否缺失，技能描述本身遗漏关键前置条件，全版本适用",
      "impact": "mechanism"
    },
    {
      "id": "C04",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max instead of its normal resting value",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值",
      "change": "将二选一机制“Whichever ... is a higher percentage”误译为“无论是……都将……”。",
      "context_counter": "代码do_polarize证实仅百分比更高的一方恢复至最大值，另一方消退，属排他机制。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
          "line": 64,
          "quote": "if (self:getPositive() / self:getMaxPositive()) >= (self:getNegative() / self:getMaxNegative()) then self.positive_regen = self.positive_regen_ref ... else self.negative_regen = self.negative_regen_ref ... end"
        }
      ],
      "text_status": "文本主体与机制逻辑完全颠倒",
      "snapshot_fact": "快照源码do_polarize根据两能量百分比高低互斥设定正负恢复",
      "target_applicability": "Orcs快照哈希固定，机制错误在快照中完全确证",
      "impact": "mechanism"
    },
    {
      "id": "C05",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "for a few turns at will",
      "target_quote": "戒指现在具有召唤他的能力。",
      "change": "漏译“for a few turns at will”（在需要时随意召唤他出战数回合）。",
      "context_counter": "代码设定john.summon_time=12为临时召唤，漏译导致持续回合与主动使用模式丢失。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 74,
          "quote": "john.summon_time = 12"
        },
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 117,
          "quote": "The ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "文本明确机制参数与持续时间修饰遗漏",
      "snapshot_fact": "快照源码明确召唤持续时间为12回合，为可主动使用的戒指技能",
      "target_applicability": "Orcs快照哈希固定，文本与快照实现均证明为限时主动召唤",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "the Scourge from the West",
      "target_quote": "西方灾星",
      "change": "专名术语违规：术语库dlc级preferred规范为“西方天灾”，且明确禁止“灾星”。",
      "context_counter": "术语库条目scope覆盖dlc且source_tag匹配_t，译文未按规范采用“西方天灾”。",
      "evidence": [
        {
          "path": "dev/terms.json",
          "line": 677,
          "quote": "\"source\": \"Scourge from the West\", \"target\": \"西方天灾\", \"status\": \"preferred\", \"scope\": \"dlc\", \"notes\": \"Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”\""
        }
      ],
      "text_status": "术语库明确禁止用法违规",
      "snapshot_fact": "术语库中该条目为dlc/preferred/_t，明确排他性规范为“西方天灾”",
      "target_applicability": "适用于全部DLC文本",
      "impact": "narrative"
    },
    {
      "id": "C07",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "broken or cancelled",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成",
      "change": "漏译“or cancelled”（主动取消时），仅保留动作中断效果的伤害触发途径。",
      "context_counter": "代码deactivate显示玩家手动关闭持续技能同样触发范围伤害，非仅由攻击施法中断。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 67,
          "quote": "deactivate = function(self, t, p) ... if p.charges then self:project ... attackTarget ... end"
        }
      ],
      "text_status": "文本明确机制分支遗漏",
      "snapshot_fact": "快照源码deactivate回调在持续效果中断或取消时均执行范围伤害结算",
      "target_applicability": "Orcs快照哈希固定，结算分支覆盖中断与主动取消",
      "impact": "mechanism"
    }
  ],
  "read_files": [
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F10-r1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r1.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/misc.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/physical.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/chats/john-surrender.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/engineering.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/gunslinging.lua"
  ],
  "limitations": [
    "Orcs源码仅哈希固定，DLC仓库commit及发行版本未固定；Possessors源码缺失（source_pinning: unavailable）。对Possessors条目仅依据纯文本语境及句意进行客观复核，不推断未固定的底层代码实现；Orcs机制均在公开快照源码中完成了交叉验证。"
  ]
}
```
