```json
{
  "entries": [
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符格式与顺序正确，技能范围、伤害、致盲持续时间与蒸汽缩放比例说明完整准确。"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "召唤空间不足日志翻译准确，保留原文感叹号，标点差异不构成错误。"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "斯莱特装甲与蒸汽链锯术语规范，完整传达半机械雪人外观特征，无事实偏差。"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "克隆体数量及高阶生物使用次数折算机制表述清晰，与附身者复制机制一致。"
    },
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "将mercifully brief（万幸短暂）误译为‘仁政’，与正史及背景中特拉格拉玛王令人尴尬的负面记录相悖。"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主手武器与副手灵晶装备前置条件翻译准确，术语符合规范。"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将Scourge from the West译为‘西方灾星’，直接违反术语库preferred条目统称为‘西方天灾’且禁止用‘灾星’的明确规则。"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [
        "C07"
      ],
      "brief_reason": "基础免伤与潜行加成数值占位符正确，仅漏译fully，建议优化但整体达意，评为OK。"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "调查报告章节标题翻译规范，保留未完整单词Wei符合纸条残缺背景，无偏差。"
    },
    {
      "id": "entry-03858",
      "status": "OK",
      "claim_ids": [
        "C08"
      ],
      "brief_reason": "时空异常背景叙事表达通顺，时态细微变化不影响事件理解，评为OK。"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "遗漏for a few turns at will，未说明戒指召唤约翰为主动且仅持续数回合的关键机制条件。"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "严重语法与机制误译：将正负能量百分比较高的一方朝最大值恢复，误译为两能量均以更高百分比替代休息值。"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "遗漏主动取消（or cancelled）同样触发范围伤害的机制，并将两侧无伤害击退误译为‘割断’。"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避触发反击射击机制、每回合限次与弹药消耗说明准确完备。"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "职业警告提示忠实完整，颜色与样式标记格式完全一致。"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C06"
      ],
      "brief_reason": "遗漏关键前提条件When you assume a form（处于占据身体形态时），影响技能实际可用条件理解。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "the mercifully brief reign of King Traglamar",
      "target_quote": "特拉格拉玛王短暂的仁政",
      "change": "将修饰brief表示万幸很短的mercifully误译为仁政，颠倒了对该统治的负面叙事评价。",
      "context_counter": "前文及misc.lua记载特拉格拉玛王的统治令所有人深感尴尬，是体制特例，绝非仁政。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 145,
          "quote": "aside from a brief period under King Traglamar, which Kasyros would only tell me \"was deeply embarassing for all involved\""
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        }
      ],
      "text_status": "text_divergence",
      "snapshot_fact": "快照中描述特拉格拉玛王统治是令人尴尬的特例，mercifully brief意为万幸短暂。",
      "target_applicability": "适用于公开Orcs源码及目标版本",
      "impact": "narrative"
    },
    {
      "id": "C02",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "and the Scourge from the West in <?=Lore.pocket_time_winner.hisher?> legend",
      "target_quote": "也欠传说中的西方灾星这个机会",
      "change": "将专名术语Scourge from the West译为西方灾星，违反术语库规范。",
      "context_counter": "dev/terms.json规定统一为‘西方天灾’，且明确注明‘不写作灾星’。",
      "evidence": [
        {
          "path": "dev/terms.json",
          "line": 675,
          "quote": "\"source\": \"Scourge from the West\", \"target\": \"西方天灾\", \"notes\": \"Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”\""
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 110,
          "quote": "and the Scourge from the West in <?=Lore.pocket_time_winner.hisher?> legend"
        }
      ],
      "text_status": "terminology_violation",
      "snapshot_fact": "术语库preferred条目要求Orcs语境统称为‘西方天灾’并禁用‘灾星’。",
      "target_applicability": "适用于Orcs DLC全部发行版本",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "The ring is now able to summon him for a few turns at will.",
      "target_quote": "戒指现在具有召唤他的能力。",
      "change": "遗漏for a few turns at will，未说明召唤是主动触发且仅持续数回合。",
      "context_counter": "游戏机制中绑定约翰赋予戒指主动技能，限时召唤协助战斗，非永久常驻召唤。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 117,
          "quote": "The ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "omission",
      "snapshot_fact": "对话奖励赋予戒指主动召唤技能，原文明确限定for a few turns at will。",
      "target_applicability": "适用于公开Orcs源码及目标版本",
      "impact": "mechanism"
    },
    {
      "id": "C04",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage regenerates towards its max instead of its normal resting value",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复替代正常的休息值",
      "change": "语法与机制错译：误将百分比较高的一方朝最大值恢复，译为两者均用更高恢复替代休息值。",
      "context_counter": "源码中Polarization仅让能量百分比较高的一方朝100%恢复，另一方维持正常静止恢复。",
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
      "text_status": "mechanic_distortion",
      "snapshot_fact": "快照中do_polarize根据两能量百分比高低单向朝max恢复，译文逻辑完全颠倒。",
      "target_applicability": "适用于公开Orcs源码及目标版本",
      "impact": "mechanism"
    },
    {
      "id": "C05",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "When this effect is broken or cancelled the sudden change in motion deals %d%% weapon damage to all foes around you.",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成 %d%% 武器伤害。",
      "change": "遗漏or cancelled触发条件，且将撞退无伤害的wrecked误译为被链锯割断。",
      "context_counter": "源码deactivate在主动关闭技能时同样触发周围伤害；路线两侧仅触发击退，无伤害。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
          "line": 46,
          "quote": "lt:knockback(self.x, self.y, 3)"
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
      "text_status": "omission_and_distortion",
      "snapshot_fact": "Saw Wheels结束时（不论中断或手动取消）均造成范围伤害，两侧仅击退。",
      "target_applicability": "适用于公开Orcs源码及目标版本",
      "impact": "mechanism"
    },
    {
      "id": "C06",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body.",
      "target_quote": "吞噬一具储备的身体，用来补充现在的身体。",
      "change": "遗漏关键前提条件When you assume a form（处于占据身体形态时）。",
      "context_counter": "附身者机制中本体无法直接使用吞噬，必须先占据形态，上下文日志明确提示须先占据。",
      "evidence": [
        {
          "path": "dev/context.lua",
          "line": 1111,
          "quote": "t(\"You require need to assume a form first.\", \"你需要先占据一个身体。\", \"logPlayer\")"
        },
        {
          "path": "dev/entries-r2.json",
          "line": 214,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "omission",
      "snapshot_fact": "Possessors源码虽未独立固定，但上下文与纯文本明确限定须处于占据形态。",
      "target_applicability": "适用于Possessors DLC全部版本",
      "impact": "mechanism"
    },
    {
      "id": "C07",
      "entry": "entry-04039",
      "status": "advisory",
      "source_quote": "fully absorb any damaging actions",
      "target_quote": "几率吸收伤害",
      "change": "未译出fully，建议补上‘完全吸收伤害’以准确反映cancel_damage_chance特性。",
      "context_counter": "Smoke Cover给予cancel_damage_chance免伤判定，‘完全吸收’比单纯‘吸收伤害’更明确。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/timed_effects/physical.lua",
          "line": 704,
          "quote": "self:effectTemporaryValue(eff, \"cancel_damage_chance\", eff.power)"
        }
      ],
      "text_status": "advisory_suggestion",
      "snapshot_fact": "Smoke Cover代码设定cancel_damage_chance免伤几率。",
      "target_applicability": "适用于公开Orcs源码",
      "impact": "expression"
    },
    {
      "id": "C08",
      "entry": "entry-03858",
      "status": "advisory",
      "source_quote": "had already caught fire when the paradox anomaly pulled it in",
      "target_quote": "拉入这条纸条的时候，这张纸条突然着火了",
      "change": "had already caught fire为完成时表示穿越前已起火，译为‘突然着火了’改变了时序感知。",
      "context_counter": "原文意指纸条被拉入时已在燃烧，故仅来得及看标题碎片即被烧尽。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "nuance_advisory",
      "snapshot_fact": "快照文本为世界线穿越设定的趣味叙事描述。",
      "target_applicability": "适用于公开Orcs源码",
      "impact": "narrative"
    }
  ],
  "read_files": [
    "dev/INPUT-F00-r2.md",
    "COMMON.md",
    "P0.md",
    "FREEZE.json",
    "dev/entries-r2.json",
    "dev/source-access.json",
    "dev/terms.json",
    "dev/context.lua",
    "sources/orcs/tome-orcs/data/talents/steam/engineering.lua",
    "sources/orcs/tome-orcs/data/talents/uber/mag.lua",
    "sources/orcs/tome-orcs/data/zones/gem/npcs.lua",
    "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
    "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
    "sources/orcs/tome-orcs/data/timed_effects/physical.lua",
    "sources/orcs/tome-orcs/data/lore/misc.lua",
    "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
    "sources/orcs/tome-orcs/data/talents/celestial/energies.lua",
    "sources/orcs/tome-orcs/data/talents/steam/battlefield-management.lua",
    "sources/orcs/tome-orcs/data/talents/steam/gunslinging.lua"
  ],
  "limitations": [
    "Orcs DLC 源码在 source-access.json 中仅哈希固定，未绑定具体 commit 或发行版本 tag；核验基于实验快照固定源码文件进行。",
    "Possessors DLC 源码不可用（source_pinning 为 unavailable），相关条目依据纯文本契约、dev/context.lua 语境以及已登记术语进行核查。"
  ]
}
```