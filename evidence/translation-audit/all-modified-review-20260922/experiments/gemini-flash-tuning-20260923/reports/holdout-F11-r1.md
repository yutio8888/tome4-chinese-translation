```json
{
  "entries": [
    {
      "id": "entry-03775",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符数量与顺序完整，战斗日志主谓宾关系与机制一致。"
    },
    {
      "id": "entry-04080",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "实体信件描述简短准确，无信息偏差。"
    },
    {
      "id": "entry-03766",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "交互文本与末尾换行符格式完全匹配。"
    },
    {
      "id": "entry-04089",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "成语与种族译名准确，叙事语气自然传神。"
    },
    {
      "id": "entry-04138",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "双手武器副栏切换、单次伤害上限与反击机制描述完整。"
    },
    {
      "id": "entry-03771",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "符合entity type术语表首选译名“元素生物”。"
    },
    {
      "id": "entry-03843",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "叙事文段完整流畅，专名与反乱密谋情节逻辑吻合。"
    },
    {
      "id": "entry-03908",
      "status": "ISSUE",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "遗漏技能感知的关键机制条件“even through walls”（穿透墙壁）。"
    },
    {
      "id": "entry-03889",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "全部7个格式化占位符完整对应，光暗回响机制表达精确。"
    },
    {
      "id": "entry-03909",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "法术强度加成、反击、以太转化及工匠配方逻辑完整一致。"
    },
    {
      "id": "entry-03763",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "战斗受击位移日志简练准确。"
    },
    {
      "id": "entry-03842",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "走私报告叙事完整，专名与条款作用域规范相符。"
    },
    {
      "id": "entry-04111",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "实体与对白日志符合工匠配方（schematic）术语要求。"
    },
    {
      "id": "entry-03774",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "神器特效简述准确，回满生命与冷却机制明确。"
    },
    {
      "id": "entry-04083",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "区域弹窗提示与任务目标说明准确，着色与样式标签完整。"
    },
    {
      "id": "entry-04013",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "精准区分闪避值降低（defence）与躲闪失效（evasion）。"
    },
    {
      "id": "entry-03935",
      "status": "OK",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "机制传达清晰；attacks译为“伤害”主谓略显生硬，列advisory。"
    },
    {
      "id": "entry-03899",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "星界领域时间停滞、零重力及投射物减速机制表达准确。"
    },
    {
      "id": "entry-03746",
      "status": "OK",
      "claim_ids": [
        "C03"
      ],
      "brief_reason": "NPC对白性格鲜明；动作描写将glare译为“指向”略有微瑕，列advisory。"
    },
    {
      "id": "entry-03884",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "任务进度计数说明与占位符匹配。"
    },
    {
      "id": "entry-03917",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "近战范围伤害与蒸汽免伤概率机制对应正确，风味文本传神。"
    },
    {
      "id": "entry-04142",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "恶魔领主专属人名音译规范准确。"
    },
    {
      "id": "entry-03936",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "双重酸性武器攻击与每次命中回汽效果清晰无误。"
    },
    {
      "id": "entry-03911",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "飞行状态机动、躲闪增益与弹幕打断规则完全对应。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-03908",
      "status": "confirmed",
      "source_quote": "even through walls in radius %d",
      "target_quote": "感知半径 %d 码内的生物",
      "change": "遗漏技能感知的关键机制条件“even through walls”，未体现透视穿墙能力。",
      "context_counter": "原文该条件与超出视野并列，源码EFF_SENSE全地形透视，非可省略修饰。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
          "line": 172,
          "quote": "In addition for 5 turns you can sense creatures beyond your sight, even through walls in radius %d."
        }
      ],
      "text_status": "关键机制条件漏译",
      "snapshot_fact": "源码调用EFF_SENSE且actor=1，实际赋予无视视线与障碍物的全地形透视。",
      "target_applicability": "译文缺失穿墙判定，影响玩家对技能侦测范围与实际作战效果的理解。",
      "impact": "mechanism"
    },
    {
      "id": "C02",
      "entry": "entry-03935",
      "status": "advisory",
      "source_quote": "All shockstaff attacks will also make a shield slam",
      "target_quote": "所有电击棒伤害也会附加一次盾牌攻击",
      "change": "attacks译为“伤害”，造成“伤害附加盾牌攻击”的主谓搭配欠妥。",
      "context_counter": "同技能总纲已译为“电击棒攻击还会发动一次盾牌攻击”，建议保持一致。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
          "line": 316,
          "quote": "All shockstaff attacks will also make a shield slam for the same damage as lightning."
        }
      ],
      "text_status": "措辞主谓搭配欠妥",
      "snapshot_fact": "代码在电击棒近战判定后由hasShield触发额外的盾牌攻击。",
      "target_applicability": "建议调整为“攻击”使动宾搭配更符合机制动作逻辑。",
      "impact": "expression"
    },
    {
      "id": "C03",
      "entry": "entry-03746",
      "status": "advisory",
      "source_quote": "directs his glare toward",
      "target_quote": "指向",
      "change": "将目光怒视转向（glare）译为肢体动作“指向”，且Emporium前后用词微有不一。",
      "context_counter": "原文为面部神态而非手势，虽不影响剧情推进，建议译为“怒目瞪向”。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/kaltor-shop.lua",
          "line": 36,
          "quote": "He directs his glare toward the multiple well-armed guards staring at you and standing still on the sides of the room."
        }
      ],
      "text_status": "动作描摹略有偏差",
      "snapshot_fact": "对话舞台动作描写，无底层玩法数值交互。",
      "target_applicability": "建议调整为“目光扫向/怒视”更契合原文神态神情。",
      "impact": "narrative"
    }
  ],
  "read_files": [
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/INPUT-F11-r1.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P1.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/entries-r1.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/terms.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/source-access.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/evidence-cards.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/holdout/context.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/psionic/gestalt.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/mental.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/talents/steam/butchery.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/timed_effects/other.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/sources/orcs/tome-orcs/data/zones/ritch-hive/zone.lua"
  ],
  "limitations": [
    "Orcs 源码由快照哈希固定，但 DLC 仓库 commit 与发行版本未固定。",
    "Possessors 组件源码在环境中缺失（source_pinning 为 unavailable），仅能依据原译文本语境进行文本完整性与一致性核对。",
    "仅依据指定入口及其严格限定的白名单文件完成审查，不扩大范围至其他非分配条目或全局报告。"
  ]
}
```