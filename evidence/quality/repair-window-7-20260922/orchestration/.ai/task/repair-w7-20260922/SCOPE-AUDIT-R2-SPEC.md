# 修复窗口7：253批8条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线e103379a5e809923401aa0099cfbdc9f104725ca。用户持续授权审核、修复、提交与推送；本窗口因LF/TAB不变量问题提前修复。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的8个target及evidence/quality/repair-window-7-20260922/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/special/printf/markup保持不变。唯一格式例外e882cc8d4e必须恢复原文3LF/6TAB（现译4LF/8TAB）；其他条目的LF/TAB保持基线。

8条REVIEW按v2四成员分片，FINAL_REVIEW独立full。MCP创建会自动启动首轮，因此四组首轮只执行冻结briefing中的启动前置检查；宿主完成全部4个live绑定后才一次性发布预定字节的只读启动凭据，随后允许实质审核，同一run不结束续跑。凭据精确路径及SHA在冻结briefing中提前声明，不包含译文、finding或宿主裁决；max_cycles默认3，旧窗口加轮授权不沿用。按适用契约收敛。LuaJIT全记录比较恰8个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，闭合后按用户2026-09-22最新指令暂停并更新handoff.md，不启动254。

spinneret仅修本工作集所含未鉴定物品名的器官含义，不全局替换giant spider spinneret等兄弟行。Daze=眩晕术语保持；e85e只修盾牌属性加成范围。排除其他advisory/旧Archmage/回忆录pending/RW1-SIB-01/02/已有blocked或其他repair，不扩大范围。

## e80304576e38d38aec618a843b469085df4579f12be32b6c69f4bfb7de87395e

section: mod-tome/data/talents/corruptions/plague.lua
source_tag: tformat

source: Make your target's diseases burst, doing %0.2f blight damage for each disease it is infected with.
		This will also spread any diseases to any nearby foes in a radius of %d with a minimum duration of 6.
		The damage will increase with your Spellpower.

target: 使目标的疾病爆发，每种疾病造成 %0.2f 枯萎伤害。
		同时会向 %d 码半径范围内任意敌人散播衰老、虚弱、腐烂或传染性疾病，疾病的持续时间最少为6回合。
		伤害受法术强度加成。

确认依据：plague.lua:20–38 按 e.subtype.disease 枚举全部疾病，Cyst Burst:128–168 逐项传播；译文额外限定四种疾病缩小适用范围。

## e82dab7a290c55e9305c34057ac1a5bb958fbcd6e09b771370c96b6d4944b453

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: Time and Space seem to warp and bend around the massive tip of this stave.

target: 法杖的尖端时空似乎陷入了扭曲。

确认依据：world-artifacts.lua:2770–2776 Gravitational Staff 的实物外观明确 massive tip；译文仅尖端，遗漏粗大这一独立形态信息。

## e83a05187461932d0e24968427a2ca0412bbb3d024934baf7b7f76d1d10e57b8

section: mod-tome/data/talents/chronomancy/timeline-threading.lua
source_tag: logSeen

source: #LIGHT_BLUE#%s never existed, this never happened!

target: #LIGHT_BLUE#%s 不存在，也不会发生！

确认依据：timeline-threading.lua:do_instakill 在抹除后日志 this never happened，紧接死亡处理；过去从未发生被译成也不会发生，改变时间方向。见 HOST-SOURCE-ADDITIONAL。

## e85e4d885532dd2a1e0eb55069514b010ed3bee7ef2b98e4178a999ca3ef5e5e

section: mod-tome/data/talents/techniques/agility.lua
source_tag: tformat

source: Leap onto an adjacent target with your shield, striking them for %d%% damage and dazing them for 2 turns, then using them as a springboard to leap to a tile within range %d.
The shield bash will use Dexterity instead of Strength for the shield's bonus damage.
At talent level 5, you will immediately enter a blocking stance on landing.

target: 用盾牌踩在临近目标上，造成 %d%% 伤害并眩晕 2 回合，之后将其做为跳板跃向 %d 格内的空地。
盾袭将使用敏捷代替力量决定盾牌伤害。
技能等级 5 时，你将在落地后立刻进入格挡状态。

确认依据：本观察并非surface的Daze状态名争议。agility.lua:130–136 将 shield_combat.dammod.str 转入 dex，只替换属性伤害加成；源文明确 bonus damage。译文省略加成而称决定盾牌伤害，未保留适用部分，确认有界补回属性加成。保留既定Daze=眩晕术语。

## e882cc8d4ef163f98acffe86f7c50ff2ebff8d56a483ae9c1659a6713ea13b2d

section: mod-tome/data/talents/psionic/discharge.lua
source_tag: tformat

source: Unleash your subconscious on the world around you.  While active, you fire up to %d bolts each turn (one per hostile target) that deal %0.2f mind damage.  Each bolt consumes 5 Feedback.
		Feedback gains beyond your maximum allowed amount may generate extra bolts (one bolt per %d excess Feedback per target), but no more than %d extra bolts per turn. 
		This effect is a psionic channel, increasing the range of Mind Sear, Psychic Lobotomy, and Sunder Mind to 10 but will break if you move.
		The damage will scale with your Mindpower.

target: 将你的潜意识释放到周围的世界。当此技能激活时，每回合你最多射出 %d 个灵能值球（每个敌方目标一个），造成 %0.2f 精神伤害。每个灵能值球消耗 5 点反馈值。
		当获得的反馈值超出最大值时，你会产生额外的灵能值球（每个目标每超出 %d 反馈值产生 1 个灵能值球），但是每回合产生的额外灵能值球数量不会超过 %d。
		此技能运用了灵能通道，所以当你移动时会中断此技能。
		特别地，当你开启此技能时，心灵灼烧、心灵脑叶切除和碾碎心灵的攻击范围将变为10格。
		受精神强度影响，伤害按比例加成。

确认依据：discharge.lua:54–81 发射 MIND 弹体并扣除 Feedback；灵能值球误引入资源值含义。原文3LF/6TAB、译文4LF/8TAB，额外一段及缩进违反格式不变量。修复同时恢复客观格式，见 HOST-FORMAT-COMPARISON。

## e8959a83e245e295592ddf1bc4abd37fd204cdb87b7f1b16e20df58c52602477

section: mod-tome/data/talents/celestial/dirge.lua
source_tag: tformat

source: Sing a song of decay and defiance and sustain yourself through spite.
							Each time you suffer a detrimental effect, you gain a shield with strength %d, that lasts as long as the effect would.  This will add to and extend an existing shield if possible.
							This can only trigger once every %d turns

target: 为腐败和暴乱轻唱一曲来支持仇恨中的你。
							每次你受到负面状态时你获得 %d 的护盾，持续时间与那个状态的持续时间相同。这可以强化你已有的伤害护盾。
							这一效果每 %d 回合只能触发一次。

确认依据：dirge.lua:175 现有护盾 power 累加、dur=max(existing,eff.dur)，可增加护盾持续时间；译文仅强化，遗漏延长持续时间及适用条件。
dirge.lua:175 现有护盾 power 累加、dur=max(existing,eff.dur)，可增加护盾持续时间；译文仅强化，遗漏延长持续时间及适用条件。 同时确认首句defiance为抗争/不屈而非暴乱；sustain yourself through spite为以怨恨支撑自身，不是支持仇恨中的你。依据源文语义恢复首句，不更名技能或全局术语。

## e895fea0305d1be76d12a9fd52beca51c2a94cc217eaeef64bf8df6cf8ea16d5

section: mod-tome/data/general/objects/elixir-ingredients.lua
source_tag: _t

source: spinneret

target: 丝腺

确认依据：elixir-ingredients.lua:153–162 明确 spinneret，带吐丝孔的巨蛛摘取部位。Australian Museum 将 spinnerets 与 silk glands 区分；丝腺误指产丝腺体，应恢复吐丝器官语义。主来源及固定源码见 HOST-SPINNERET-REFERENCE、HOST-SOURCE-SUPPLEMENTAL；不在本裁决授权全局替换相关名称。

## e8bc936f6d6cb89e131fdddb68b357e4550d4ad593b0fd30247357dad567ca55

section: mod-tome/data/damage_types.lua
source_tag: _t

source: eviscerated

target: 被掏心

确认依据：damage_types.lua:778 将 eviscerated 列为物理死亡描述；词义指取出内脏/剖腹，不限定心脏。译文被掏心错误缩窄受创器官，应恢复剖腹/内脏意象。

## Cycle 1 bounded refinement
Host confirmed ADJUDICATION-R0.json findings on the same selected two entries. Permit disease quantifier and Vault opening action repairs in addition to initial eight-target scope; all other constraints remain.

## Cycle 2 bounded refinement
ADJUDICATION-R1 confirms only e882 excess-feedback bolt-count quantifier against Actor.incFeedback and Mind Storm; repair this second-line relationship within existing target. Spinneret sibling consistency is advisory/declined_scope; no sibling changes. Default max_cycles=3 unchanged.
