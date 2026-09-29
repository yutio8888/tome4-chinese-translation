```json
{
  "entries": [
    {
      "id": "entry-03775",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "译文准确，占位符与战斗日志代词拼接正常"
    },
    {
      "id": "entry-04080",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "信件物品描述翻译准确简洁"
    },
    {
      "id": "entry-03766",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "市场摊位搜刮提示准确，保留换行符"
    },
    {
      "id": "entry-04089",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "NPC描述翻译贴切自然"
    },
    {
      "id": "entry-04138",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "力场盾机制说明完整，占位符匹配"
    },
    {
      "id": "entry-03771",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "实体类型匹配术语库preferred规范"
    },
    {
      "id": "entry-03843",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "总体分析长文本叙事翻译准确完整，专名符合设定"
    },
    {
      "id": "entry-03908",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "漏译even through walls，遗漏穿墙感知关键机制"
    },
    {
      "id": "entry-03889",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "暮光回响机制描述准确，7个占位符均匹配"
    },
    {
      "id": "entry-03909",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "科技法术描述准确，占位符与属性加成对应无误"
    },
    {
      "id": "entry-03763",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "战斗日志拖拽效果描述准确，占位符一致"
    },
    {
      "id": "entry-03842",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "行动记录叙事翻译完整，专名术语符合DLC作用域规则"
    },
    {
      "id": "entry-04111",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "工匠配方学习日志准确，术语符合dlc preferred规范"
    },
    {
      "id": "entry-03774",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "神器特技描述简洁准确"
    },
    {
      "id": "entry-04083",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "巢穴进入弹窗翻译准确，格式与强调标签完整"
    },
    {
      "id": "entry-04013",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "火箭锁定效果区分闪避值与躲闪效果，占位符正确"
    },
    {
      "id": "entry-03935",
      "status": "OK",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "重装武器战技机制表达完整，伤害/攻击措辞略欠精确"
    },
    {
      "id": "entry-03899",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "星界领域技能说明完整，范围与持续时间占位符一致"
    },
    {
      "id": "entry-03746",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "卡托尔对话语气传神，商人戏谑与恐吓口吻等价达意"
    },
    {
      "id": "entry-03884",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "雪人援军召唤剩余次数描述准确，占位符一致"
    },
    {
      "id": "entry-03917",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "金属狂怒技能与战斗喊话翻译准确，占位符匹配"
    },
    {
      "id": "entry-04142",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "附身效果专名克里尔·费扬符合既有译名"
    },
    {
      "id": "entry-03936",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "爆矢枪攻击效果与酸伤、蒸汽恢复数值对应无误"
    },
    {
      "id": "entry-03911",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "死亡天降技能描述准确，3个百分比占位符顺序与类型正确"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03908",
      "status": "confirmed",
      "source_quote": "even through walls in radius %d",
      "target_quote": "感知半径 %d 码内的生物",
      "change": "译文漏译“even through walls”，遗漏了感知可穿透墙壁的关键机制说明。",
      "context_counter": "源码第139行赋予EFF_SENSE且actor=1，能无视视线穿墙感知生物，原文明确注明该穿墙特性。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
          "line": 172,
          "quote": "In addition for 5 turns you can sense creatures beyond your sight, even through walls in radius %d."
        }
      ],
      "text_status": "divergent",
      "snapshot_fact": "源码第139行赋予EFF_SENSE(actor=1)，在有效半径内穿透墙壁探测生物。",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C02",
      "entry": "entry-03935",
      "status": "advisory",
      "source_quote": "All shockstaff attacks will also make a shield slam",
      "target_quote": "所有电击棒伤害也会附加一次盾牌攻击",
      "change": "原文“attacks”译作“伤害”，语境中为电击棒攻击附带盾击，表达略欠精确。",
      "context_counter": "句意为电击棒近战攻击触发附加盾击，后半句已说明伤害机制，未造成实质机制误导。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
          "line": 316,
          "quote": "All shockstaff attacks will also make a shield slam for the same damage as lightning."
        }
      ],
      "text_status": "divergent",
      "snapshot_fact": "电击棒近战攻击时附带副手盾击并造成等量闪电伤害。",
      "target_applicability": "applicable",
      "impact": "expression"
    }
  ],
  "read_files": [
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/INPUT-F00-r1.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P0.md",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/source-access.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/entries-r1.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/terms.json",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/context.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/general/objects/boss-artifacts.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/internment-camp/objects.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/general/events/merchant-stall.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/sunwall-outpost/npcs.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/dominion-port.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/crepescula.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/spells/occult-technomancy.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/damage_types.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/ritch-hive/zone.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/other.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/void.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/butchery.lua",
    "evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/artillery.lua"
  ],
  "limitations": [
    "Orcs组件源码仅哈希固定，未绑定具体版本提交；已对登记源码快照进行核对。",
    "Possessors组件源码未包含在白名单镜像中，相关条目严格依据上下文及纯文本事实核验。"
  ]
}
```