```json
{
  "entries": [
    {
      "id": "entry-03771",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "实体类型术语准确匹配，无错译"
    },
    {
      "id": "entry-03889",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符类型与顺序完整对应，数值与机制表述准确"
    },
    {
      "id": "entry-03917",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符对应无误，技能机制与减伤概率表述准确"
    },
    {
      "id": "entry-04111",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "配方术语与格式占位符匹配，提示信息无误"
    },
    {
      "id": "entry-04089",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "成语习语翻译地道，符合NPC描述语境"
    },
    {
      "id": "entry-04083",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "材质术语规范，挖墙机制与任务提示完整准确"
    },
    {
      "id": "entry-04080",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "物品描述简练准确，无语义偏差"
    },
    {
      "id": "entry-04138",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符与伤害上限机制对应准确，双手武器切换说明完整"
    },
    {
      "id": "entry-03936",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "重装武器射击与蒸汽恢复机制表述清晰准确"
    },
    {
      "id": "entry-04142",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "人名专名翻译符合既有习惯"
    },
    {
      "id": "entry-03884",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "雪人召唤计数占位符消费正确"
    },
    {
      "id": "entry-03909",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "多参数占位符顺序与类型准确，法术强度与魔力加成机制无误"
    },
    {
      "id": "entry-03842",
      "status": "OK",
      "claim_ids": [
        "C04"
      ],
      "brief_reason": "整体走私账目叙事完整，小段贸易报酬句式略有倒置建议澄清"
    },
    {
      "id": "entry-03908",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "遗漏穿墙感知关键机制限定（even through walls）"
    },
    {
      "id": "entry-03843",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "叙事信件事件与阵营关系翻译准确通顺"
    },
    {
      "id": "entry-03775",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "双字符串占位符正确组合代词与神器名称，日志输出正常"
    },
    {
      "id": "entry-03763",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "拖动伤害类型日志占位符匹配"
    },
    {
      "id": "entry-03766",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "弹窗事件前导文本与换行结构完整"
    },
    {
      "id": "entry-03774",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "冷却与完全治疗效果说明明确"
    },
    {
      "id": "entry-03746",
      "status": "OK",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "对话整体生动且格式控制符完整，守卫动作神态略有省略"
    },
    {
      "id": "entry-03899",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "零重力与减速星界领域机制描述准确"
    },
    {
      "id": "entry-03911",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "飞行移速躲闪及重复弹幕机制准确匹配"
    },
    {
      "id": "entry-04013",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避降低与躲闪失效状态说明符合术语规范"
    },
    {
      "id": "entry-03935",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将电击棒攻击误译为电击棒伤害，歪曲盾击触发条件"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03908",
      "status": "confirmed",
      "source_quote": "even through walls in radius %d",
      "target_quote": "超脱视线的感知半径 %d 码内的生物",
      "change": "遗漏“even through walls”（甚至穿透墙壁），未传达该感知效果可穿墙的关键机制。",
      "context_counter": "译文虽有“超脱视线”，但未明确说明可无视墙体阻挡感知生物。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
          "line": 172,
          "quote": "In addition for 5 turns you can sense creatures beyond your sight, even through walls in radius %d."
        },
        {
          "path": "sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
          "line": 139,
          "quote": "self:setEffect(self.EFF_SENSE, 5, { range = t.getSenseRadius(self, t), actor = 1 })"
        }
      ],
      "text_status": "源文明确限定“even through walls”，译文完全遗漏穿墙条件。",
      "snapshot_fact": "代码赋予EFF_SENSE效果，在半径范围内提供穿墙全向生物感知。",
      "target_applicability": "Orcs未固定仓库commit，但快照源码行为明确。",
      "impact": "mechanism"
    },
    {
      "id": "C02",
      "entry": "entry-03935",
      "status": "confirmed",
      "source_quote": "All shockstaff attacks will also make a shield slam",
      "target_quote": "所有电击棒伤害也会附加一次盾牌攻击",
      "change": "将“attacks”（攻击）误译为“伤害”，把攻击动作判定混同为伤害产生。",
      "context_counter": "后文虽提到盾牌攻击，但主语误用“伤害”会导致误解为需造成伤害才触发。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
          "line": 316,
          "quote": "All shockstaff attacks will also make a shield slam for the same damage as lightning."
        },
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
          "line": 412,
          "quote": "if shield then self:attackTargetWith(tmp_target, shield_combat, DamageType.LIGHTNING, t.getDamage(self, t)) end"
        }
      ],
      "text_status": "attacks（攻击）被误译为“伤害”，造成语义与机制偏差。",
      "snapshot_fact": "源码判定发动电击棒攻击且佩戴盾牌时即伴随盾击，非依赖电击棒造成伤害才触发。",
      "target_applicability": "Orcs未固定commit，快照源码实现明确。",
      "impact": "mechanism"
    },
    {
      "id": "C03",
      "entry": "entry-03746",
      "status": "advisory",
      "source_quote": "He directs his glare toward the multiple well-armed guards staring at you and standing still on the sides of the room.",
      "target_quote": "他指向周围和房间里那些装备良好的警卫。",
      "change": "将“怒视那些在房间两侧静立盯视你的守卫”简化为“指向周围和房间里那些警卫”，神态略有简化。",
      "context_counter": "全段整体仍传达出店主借助店内守卫武力进行言语威慑的对话意图。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/kaltor-shop.lua",
          "line": 36,
          "quote": "He directs his glare toward the multiple well-armed guards staring at you and standing still on the sides of the room."
        }
      ],
      "text_status": "动作神态与守卫站姿描写略有概括与改动。",
      "snapshot_fact": "纯文本对话叙事，无动态分支差异。",
      "target_applicability": "Orcs未固定commit，文本事实可查。",
      "impact": "expression"
    },
    {
      "id": "C04",
      "entry": "entry-03842",
      "status": "advisory",
      "source_quote": "received as payment for a product received via Iron Throne smugglers",
      "target_quote": "作为从钢铁王座的走私者那里以货物形式支付的报酬",
      "change": "将“作为通过走私者所获货物的付款”译为“以货物形式支付的报酬”，句式理解稍有偏差。",
      "context_counter": "通篇为港口走私与黑市贸易账目汇报，宏观叙事逻辑基本通顺。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/dominion-port.lua",
          "line": 60,
          "quote": "received as payment for a product received via Iron Throne smugglers"
        }
      ],
      "text_status": "介词短语修饰理解稍有偏差，但未阻断剧情理解。",
      "snapshot_fact": "纯文本lore，不影响游戏机制。",
      "target_applicability": "Orcs未固定commit，文本事实可查。",
      "impact": "narrative"
    }
  ],
  "read_files": [
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/INPUT-F00-r2.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P0.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/source-access.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/terms.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/entries-r2.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/context.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/general/npcs/hethugoroth.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/crepescula.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/butchery.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/sunwall-outpost/npcs.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/ritch-hive/zone.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/internment-camp/objects.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/quests/yeti-abduction.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/spells/occult-technomancy.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/lore/dominion-port.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/general/objects/boss-artifacts.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/damage_types.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/general/events/merchant-stall.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/chats/kaltor-shop.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/celestial/void.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/artillery.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/other.lua"
  ],
  "limitations": "Possessors DLC源码缺失（entry-04138与entry-04142标记为source_pinning: unavailable），仅凭冻结文本与通用语境核查；Embers of Rage（Orcs）源码DLC仓库commit及发行版本未固定，核验基于白名单哈希固定快照。"
}
```