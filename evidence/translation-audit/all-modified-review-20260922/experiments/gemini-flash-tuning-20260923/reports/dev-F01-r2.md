```json
{
  "entries": [
    {
      "id": "entry-03923",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "占位符类型与顺序匹配，数值加成与目盲条件逻辑忠实。"
    },
    {
      "id": "entry-03995",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "简短日志忠实无误，标点差异不构成错误，术语源标签与作用域不强制改名。"
    },
    {
      "id": "entry-04078",
      "status": "OK",
      "claim_ids": [
        "C01"
      ],
      "brief_reason": "核心叙事与装备描述准确；存在对施虐者评价的意译发挥，列advisory，整体OK。"
    },
    {
      "id": "entry-04126",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "夺舍克隆数量与降阶规则表意等价，未固定源码缺失不推测机制错误。"
    },
    {
      "id": "entry-03862",
      "status": "ISSUE",
      "claim_ids": [
        "C02"
      ],
      "brief_reason": "将形容短暂统治万幸的副词误译为“仁政”，与背景设定中尴尬混乱的统治相悖。"
    },
    {
      "id": "entry-04121",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "主副手武器装备需求提示准确，术语使用规范。"
    },
    {
      "id": "entry-03868",
      "status": "ISSUE",
      "claim_ids": [
        "C03",
        "C04"
      ],
      "brief_reason": "专名违背 preferred 术语统一定义，且将判定多数候选为失败品误译为面对困难。"
    },
    {
      "id": "entry-04039",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "吸收伤害与潜行强度数值对应正确，占位符消费正常。"
    },
    {
      "id": "entry-03857",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "未写完标题忠实截断，专名与章节数字无误。"
    },
    {
      "id": "entry-03858",
      "status": "ISSUE",
      "claim_ids": [
        "C05"
      ],
      "brief_reason": "将过去完成时本就已着火误译为拉入时突然着火，改变起火时间与因果关系。"
    },
    {
      "id": "entry-03740",
      "status": "ISSUE",
      "claim_ids": [
        "C06"
      ],
      "brief_reason": "遗漏召唤仅持续数回合且可随时召唤的关键机制描述。"
    },
    {
      "id": "entry-03891",
      "status": "ISSUE",
      "claim_ids": [
        "C07"
      ],
      "brief_reason": "将取正负能量百分比更高者单项回复，误译为两者都获得更高回复，严重歪曲技能机制。"
    },
    {
      "id": "entry-03915",
      "status": "ISSUE",
      "claim_ids": [
        "C08"
      ],
      "brief_reason": "句子合并遗漏了主动取消同样能触发伤害的机制说明。"
    },
    {
      "id": "entry-03932",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "闪避与反击射击机制、伤害加成与回合限制表达准确。"
    },
    {
      "id": "entry-04119",
      "status": "OK",
      "claim_ids": [],
      "brief_reason": "格式标记与新手警示完整，语意流畅通顺。"
    },
    {
      "id": "entry-04127",
      "status": "ISSUE",
      "claim_ids": [
        "C09"
      ],
      "brief_reason": "遗漏附身变形时方可吞噬储备身体的前置生效时机。"
    }
  ],
  "claims": [
    {
      "id": "C01",
      "entry": "entry-04078",
      "status": "advisory",
      "source_quote": "did an amazing job of pain and destruction",
      "target_quote": "它的确变成了一个恐怖的杀戮机器",
      "change": "原意指施虐者制造痛苦与毁灭干得惊人，译文发挥为主体变成杀戮机器。",
      "context_counter": "雪人被改造为半机械 Boss，意译符合其实际形象，未产生机制冲突。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/zones/gem/npcs.lua",
          "line": 94,
          "quote": "Whoever tortured and tormented this yeti did an amazing job of pain and destruction."
        }
      ],
      "text_status": "textual divergence",
      "snapshot_fact": "MECH_YETI 实体描述，装备蒸汽链锯与斯莱特装甲",
      "target_applicability": "applicable",
      "impact": "expression"
    },
    {
      "id": "C02",
      "entry": "entry-03862",
      "status": "confirmed",
      "source_quote": "mercifully brief reign",
      "target_quote": "短暂的仁政",
      "change": "将修饰 brief 的副词 mercifully（万幸／谢天谢地）误解为仁慈修饰 reign 译为“仁政”，事实完全相反。",
      "context_counter": "特拉格拉玛王统治在背景中被明确指出令所有相关者深感尴尬，绝非仁政。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/palace-fumes.lua",
          "line": 69,
          "quote": "(Obviously, the mercifully brief reign of King Traglamar is an exception, but it should be clear why this was a special case and not worthy of further consideration.)"
        }
      ],
      "text_status": "textual divergence confirmed",
      "snapshot_fact": "卡西罗斯辞职演说，背景中特拉格拉玛王统治是众所周知的荒唐特例",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C03",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "Scourge from the West",
      "target_quote": "西方灾星",
      "change": "违背术语库 dlc 范围 preferred 规范，未按明确要求统一为“西方天灾”而写作“灾星”。",
      "context_counter": "术语库 society.tsv 明确规定 Embers of Rage 统一用“西方天灾”，不得写作“灾星”。",
      "evidence": [
        {
          "path": "terminology/society.tsv",
          "line": 34,
          "quote": "Scourge from the West\t西方天灾\tT.PN.PERSON\tsociety\t_t\tpreferred\tdlc\tEmbers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”"
        },
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 110,
          "quote": "and the Scourge from the West in <?=Lore.pocket_time_winner.hisher?> legend"
        }
      ],
      "text_status": "terminology non-compliance",
      "snapshot_fact": "时空畸变扭曲时空背景文本，指代本体通关英雄传说",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C04",
      "entry": "entry-03868",
      "status": "confirmed",
      "source_quote": "deeming many failures",
      "target_quote": "面对无数的困难",
      "change": "将艾德隆考量主角时视多数备选为失败者（暗示玩家死亡重开），误译为主角面对困难。",
      "context_counter": "句子主语为艾德隆（It），宾语为 failures，与主角经历困难无关。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/pocket-time.lua",
          "line": 104,
          "quote": "It considered a few different options, deeming many failures, some potentially adequate with a few mistakes forgiven, and only one to be finally chosen."
        }
      ],
      "text_status": "textual divergence confirmed",
      "snapshot_fact": "讲述者艾德隆挑选故事主角的元叙事描述",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C05",
      "entry": "entry-03858",
      "status": "confirmed",
      "source_quote": "had already caught fire",
      "target_quote": "突然着火了",
      "change": "过去完成时表明纸条在被拉入前已起火，译为拉入时突然着火歪曲了因果时序。",
      "context_counter": "后文解释只来得及看部分标题便烧尽，正是因为被拉入前就已在燃烧。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/lore/misc.lua",
          "line": 154,
          "quote": "(This note had already caught fire when the paradox anomaly pulled it in from another timeline.  You only had time to read part of the title before it burned away completely.)"
        }
      ],
      "text_status": "textual divergence confirmed",
      "snapshot_fact": "时空异常拉入残卷的背景说明，解释标题不完整的原因",
      "target_applicability": "applicable",
      "impact": "narrative"
    },
    {
      "id": "C06",
      "entry": "entry-03740",
      "status": "confirmed",
      "source_quote": "for a few turns at will",
      "target_quote": "戒指现在具有召唤他的能力",
      "change": "完全遗漏了召唤持续时间仅数回合（for a few turns）及随心/任意（at will）的机制限定。",
      "context_counter": "该描述向玩家说明戒指召唤约翰的具体机制约束，遗漏导致持续时间信息缺失。",
      "evidence": [
        {
          "path": "sources/orcs/tome-orcs/data/chats/john-surrender.lua",
          "line": 117,
          "quote": "The ring is now able to summon him for a few turns at will.*#WHITE#"
        }
      ],
      "text_status": "omission confirmed",
      "snapshot_fact": "击败约翰后选择将其灵魂绑定至戒指所获神器的使用说明",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C07",
      "entry": "entry-03891",
      "status": "confirmed",
      "source_quote": "Whichever of your positive and negative energies is a higher percentage",
      "target_quote": "无论是你的正能量还是负能量都将用更高百分比的恢复",
      "change": "将比较二者百分比择高者的主语从句，误译为全选并列结构，歪曲了单向极化机制。",
      "context_counter": "源码 do_polarize 明确按比例比较两者大小，仅对较高者设为正向回复。",
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
      "text_status": "textual divergence confirmed",
      "snapshot_fact": "极化技能 passive 机制，两类能量二选一向最大值回复",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C08",
      "entry": "entry-03915",
      "status": "confirmed",
      "source_quote": "or cancelled",
      "target_quote": "攻击或者使用其他技能的动作都会中断效果，同时冲击力对周围的敌人造成",
      "change": "合并句子时遗漏了 or cancelled，漏译了主动关闭持续技能同样能造成武器伤害的触发方式。",
      "context_counter": "技能 deactivate 回调无论被动作打断还是主动取消均触发 melee 伤害投影。",
      "evidence": [
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
      "text_status": "omission confirmed",
      "snapshot_fact": "锯轮技能注销时无论打断或取消均造成突变伤害",
      "target_applicability": "applicable",
      "impact": "mechanism"
    },
    {
      "id": "C09",
      "entry": "entry-04127",
      "status": "confirmed",
      "source_quote": "When you assume a form",
      "target_quote": "吞噬一具储备的身体，用来补充现在的身体",
      "change": "遗漏技能前置时机“When you assume a form（当你占据/拟态形态时）”，使玩家误以为随时可用。",
      "context_counter": "附身系技能吞噬专用于拟态变身时消耗储备身体回复，前置时机为关键限制。",
      "evidence": [
        {
          "path": "dev/entries-r2.json",
          "line": 214,
          "quote": "When you assume a form you may cannibalize a body in your reserve to replenish your current body."
        }
      ],
      "text_status": "omission confirmed",
      "snapshot_fact": "附身系吞噬技能描述，前置触发条件为 assume a form",
      "target_applicability": "applicable",
      "impact": "mechanism"
    }
  ],
  "read_files": [
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/INPUT-F01-r2.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/COMMON.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/P0.md",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/FREEZE.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/entries-r2.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/context.lua",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/terms.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/source-access.json",
    "/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/gemini-flash-tuning-20260923/dev/evidence-cards.json"
  ],
  "limitations": "Orcs 源码仅哈希固定，DLC 仓库 commit 及目标发行版本未固定；Possessors 源码缺失，相关判定仅依据冻结原文与纯文本逻辑；本审查严格遵循只读权限与限定输入范围，未访问宿主记录或其他实验组文件。"
}
```