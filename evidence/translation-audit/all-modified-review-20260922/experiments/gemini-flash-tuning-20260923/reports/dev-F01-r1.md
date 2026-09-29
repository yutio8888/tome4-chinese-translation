```json
{
  "entries": [
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "将mercifully brief reign（幸好短暂的统治）误译为短暂的仁政，叙事定性颠倒。"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "译文准确，标点差异属非错误范畴，无机制或语义偏差。"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "截断书名Wei...保留完整，符合纸条烧毁上下文，格式一致。"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "复制克隆体及数量折算机制表述准确，数值与逻辑与原文一致。"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "职业警示描述与格式标签完全保留，表达通顺等价。"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "几率吸收伤害与潜行数值表述准确，机制表达等价。"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将拉入前已经着火（had already caught fire）误译为拉入时突然着火，时态与因果偏差。"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "漏译技能前置触发条件When you assume a form（当你进入形态时）。"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "将正负能量中较高一方回复误译为无论正负能量均提高回复，严重破坏极化机制。"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "漏译召唤持续时间与任意发动条件for a few turns at will及forever。"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C06",
        "C07"
      ],
      "brief_reason": "违反preferred术语使用了西方灾星（应为西方天灾）；且将筛选判定deeming many failures误译为面对无数的困难。"
    },
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "各项参数占位符类型与顺序一致，数值、机制与负面效果描述准确。"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C08"
      ],
      "brief_reason": "漏译or cancelled（或取消时），将主动关闭维持技能造成伤害的机制遗漏。"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "半机械化雪人描述完整，装甲与武器替换准确，无机制偏差。"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "反击射击触发条件、伤害加成与弹药消耗说明准确无误。"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主副手装备限制说明准确，符合术语及游戏机制规范。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "the mercifully brief reign of King Traglamar is an exception",
      "target_quote": "特拉格拉玛王短暂的仁政除外",
      "change": "将“谢天谢地尚算短暂的统治”（mercifully brief reign）误译为“短暂的仁政”，完全颠倒了对该历史时期的负面定性。",
      "context_counter": "上下文及同作者第48章均指出特拉格拉玛统治令人极度尴尬，mercifully修饰brief表示幸好短暂，绝非‘仁政’。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire when the paradox anomaly pulled it in",
      "target_quote": "当时空异常从另一条世界线拉入这条纸条的时候，这张纸条突然着火了",
      "change": "将拉入前“已经着火”（had already caught fire）误译为拉入时“突然着火了”，篡改了事件时态与因果先后。",
      "context_counter": "过去完成时表明纸条自另一世界线拉入时便已处于燃烧状态，非进入本世界线后才突发起火。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form you may cannibalize a body",
      "target_quote": "吞噬一具储备的身体",
      "change": "遗漏技能触发前置条件“When you assume a form”（当你进入/采用形态时），缺失关键机制时机。",
      "context_counter": "纯文本条件缺失，使玩家误以为吞噬身体可脱离附身形态随时主动发动。",
      "evidence": [
        {
          "path": "dev/entries-r1.json",
          "line": 102,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "unavailable",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C04",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值",
      "change": "将“正负能量中百分比更高的一方回满”严重误译为“无论正负能量都用更高百分比恢复”，颠倒技能两极极化机制。",
      "context_counter": "源码do_polarize判定二者百分比大小，仅高者获得正向回复且向最大值恢复，另一方消退，非双方均加速。",
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
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C05",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "binding John to it forever. The ring is now able to summon him for a few turns at will.",
      "target_quote": "将约翰绑定到戒指上。\n戒指现在具有召唤他的能力。",
      "change": "漏译“forever”（永久）及“for a few turns at will”（随意召唤数回合），缺失召唤持续回合与任意触发机制。",
      "context_counter": "源码设定戒指召唤为限时数回合的临时召唤，译文删减后易误导为永久仆从。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 116,
          "quote": "binding John to it forever.\nThe ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "the Scourge from the West",
      "target_quote": "西方灾星",
      "change": "违反DLC生效的preferred术语规则，译为“西方灾星”；术语库明确规定统一为“西方天灾”，不得写作“灾星”。",
      "context_counter": "terminology/society.tsv第34行明确标明DLC作用域下preferred为“西方天灾”，备注严禁使用“灾星”。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 110,
          "quote": "and the Scourge from the West in <?=Lore.pocket_time_winner.hisher?> legend"
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C07",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen",
      "target_quote": "面对无数的困难，有些可能允许一部分的错误，但是最终只会选择一个",
      "change": "将艾德隆对候选英雄的筛选审定“认定多数为失败者”（deeming many failures）严重误译为“面对无数的困难”。",
      "context_counter": "主语为艾德隆审视备选方案（options），deem意为评定，failures指失败者/品，非主角面临困难。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 104,
          "quote": "It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C08",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成 %d%% 武器伤害",
      "change": "漏译“or cancelled”（或取消时），将两句合并导致排除了玩家主动关闭维持技能造成伤害的情形。",
      "context_counter": "源码deactivate显示主动关闭该维持技能同样结算周围伤害，非仅被攻击/施法中断时触发。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 90,
          "quote": "When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you."
        }
      ],
      "text_status": "confirmed",
      "snapshot_fact": "hash-fixed, DLC repository/commit/target-release unpinned",
      "target_applicability": "applicable",
      "impact": "mechanism"
    }
  ],
  "read_files": [
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F01-r1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P0.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r1.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/evidence-cards.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua"
  ],
  "limitations": [
    "Possessors（附身系）源码在白名单及工作树中不可用（unavailable），相关条目仅依据冻结原译文本及语境判定纯文本可证偏差。",
    "Orcs源码仅有快照哈希固定，DLC仓库commit及发行版本未固定。",
    "本审核严格局限于dev/entries-r1.json分配的16个条目，context.lua仅作为语境参考，未审核其邻近条目。"
  ]
}
```
