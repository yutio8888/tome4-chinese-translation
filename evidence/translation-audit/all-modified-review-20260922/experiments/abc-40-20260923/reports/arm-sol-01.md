---

按 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/INPUT.md) 的分类，40 条均已逐条复核：**未发现问题 29 条、存在问题 5 条、待确认 0 条、仅建议 6 条**。以下仅列有问题的 claim；“仅建议”均不作为缺陷。

| 条目 | 判定 | 原文、译文对照与依据 |
|---|---|---|
| 03172 | 未发现问题 | `Random!` →「随机！」；随机创建按钮，见 Birther.lua:93。 |
| 03173 | 未发现问题 | `Basic Gameplay (recommended)` →「基本游戏教程（推荐）」；按钮启动 `Basic` 教程，见 Birther.lua:424。 |
| 03174 | 存在问题 | 锁定选项说明中的动作及解锁对象被改写，见下方 claim。 |
| 03175 | 仅建议 | `does not make much sense lore-wise` →「不符合剧情」语气更绝对；特殊任务提示仍保留，见 Birther.lua:967。 |
| 03176 | 存在问题 | 探索模式说明漏掉无需重新开始游戏这一点，见下方 claim。 |
| 03177 | 未发现问题 | `Donate!` →「捐赠！」，见 Birther.lua:1391。 |
| 03178 | 未发现问题 | `Cosmetic customization is a donator-only feature.` →「自定义外观是捐赠者的特权」，见 Birther.lua:1730。 |
| 03179 | 仅建议 | `Displaying %s set for %s` →「展示 %s 套装给 %s 看」略像向角色展示；实际是切换角色面板所显示的装备组，装备不切换，见 CharacterSheet.lua:64–76。 |
| 03180 | 未发现问题 | `Sort: %s` →「排序：%s」，占位符保留，见 CharacterSheet.lua:94。 |
| 03181 | 未发现问题 | `Seed: %s` →「种子：%s」，颜色标记与占位符保留，见 CharacterSheet.lua:629。 |
| 03182 | 未发现问题 | `die:%+d` →「死亡底线：%+d」；用于生命行的 `die_at`，见 CharacterSheet.lua:646。 |
| 03183 | 仅建议 | `with heal mod` →「治疗系数加成后」；系数也可能低于 1，“加成”略窄，计算见 CharacterSheet.lua:731–744。 |
| 03184 | 未发现问题 | `Two-Handed,` →「双手，」，作为武器类别前缀使用，见 CharacterSheet.lua:897。 |
| 03185 | 未发现问题 | ` (disabled)` →「（被禁用）」，前导空格保留，见 CharacterSheet.lua:954。 |
| 03186 | 未发现问题 | `Damage affinities:` →「伤害亲和：」，颜色标记保留，见 CharacterSheet.lua:1235。 |
| 03187 | 未发现问题 | `You have #LIGHT_RED#died#LAST#!` →「你已经#LIGHT_RED#死了#LAST#！」，标记保留，见 DeathDialog.lua:34。 |
| 03188 | 未发现问题 | `Message/Chat log (allows to talk)` →「消息/聊天日志（允许聊天）」，与已登录时的菜单分支相符，见 DeathDialog.lua:350。 |
| 03189 | 未发现问题 | `Exploration mode (infinite lives)` →「探索模式（无限命）」，标记保留，见 Donation.lua:44。 |
| 03190 | 未发现问题 | `Item's appearance change (Shimmering)` →「改变物品外观（幻化）」，标记保留，见 Donation.lua:44。 |
| 03191 | 未发现问题 | 捐赠说明保留免费开源、请求捐赠及附加功能的意思，`%s` 保留，见 Donation.lua:48–54。 |
| 03192 | 未发现问题 | `Enter movement speed(lower is faster)` →「设置动画速度（越低越快）」；该项控制平滑移动动画，见 GameOptions.lua:103–116。 |
| 03193 | 未发现问题 | `Twitch creatures movement and attack` →「生物移动和攻击抖动效果」，标记保留，见 GameOptions.lua:118–128。 |
| 03194 | 未发现问题 | 经典 HUD 的战斗日志行数说明准确，见 GameOptions.lua:166。 |
| 03195 | 仅建议 | `Fade time` →「消失时间」可更明确表达“开始淡出前的秒数”；说明及 `enableFading` 调用见 GameOptions.lua:217–230。 |
| 03196 | 未发现问题 | 四种战术信息显示模式及 Shift+T 均保留，见 GameOptions.lua:336。 |
| 03197 | 未发现问题 | WASD 与同时按两方向键斜向移动的说明准确，见 GameOptions.lua:452。 |
| 03198 | 未发现问题 | `From 0(disable) to 10` →「从 0（关闭）到 10」，范围与停用值相符，见 GameOptions.lua:466。 |
| 03199 | 未发现问题 | 屏幕边缘滚动距离及高值居中效果的说明准确，见 GameOptions.lua:483。 |
| 03200 | 未发现问题 | `From 1 to 99 (100 to disable)` →「从 1 到 99（100 为禁用）」，见 GameOptions.lua:499。 |
| 03201 | 未发现问题 | Discord 实时状态、重启生效及不使用 Discord 时无效果均保留，见 GameOptions.lua:634。 |
| 03202 | 未发现问题 | 在线保存的是角色信息而非完整存档，链接分享用途保留，见 GameOptions.lua:643。 |
| 03203 | 存在问题 | 断网说明中“角色备份”和“无法更新插件版本”误述功能，见下方 claim。 |
| 03204 | 未发现问题 | 穿斗篷时以兜帽图像替换头部装备图像的说明准确，见 GameOptions.lua:724。 |
| 03205 | 仅建议 | `moddable tiles` →「纸娃娃」不是直译；括号仍说明装备显示在玩家身上，勾选项见 GraphicMode.lua:83–91。 |
| 03206 | 仅建议 | `transitions, wide tiles` →「渐变，大型贴图」可能弱化“过渡”和“宽贴图”的具体含义；仅凭该勾选项不足以判为功能误述，见 GraphicMode.lua:84–92。 |
| 03207 | 未发现问题 | `Levelup: %s, level %s` →「升级：%s，等级 %s」，占位符顺序保留，见 LevelupDialog.lua:89。 |
| 03208 | 未发现问题 | 当前等级的属性上限提示准确，见 LevelupDialog.lua:266。 |
| 03209 | 存在问题 | `Category points left` 被限定成「技能树解锁点剩余」，见下方 claim。 |
| 03210 | 存在问题 | 类别点数用途与刻印位消耗时机有误，见下方 claim。 |
| 03211 | 未发现问题 | `Stats: %s` →「属性：%s」，占位符保留，见 LevelupDialog.lua:773。 |

### 存在问题的 claim

- **03174，解锁条件与对象。** 原文是 `Performing certain actions and completing certain quests`，译文为「完成特定的任务或条件」；“采取特定行动”被改成“完成条件”。原文随后说 `locked campaigns, races and classes`，译文却说「这个战役，种族，职业」，把通用的多类锁定内容说成当前这组对象。同一段锁定说明用于不同出生选项，见 [Birther.lua:804](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/Birther.lua:804)。

- **03176，遗漏无需重开游戏。** 原文 `you can try as much as you want without restarting`；译文只说「你可以有着无限多的尝试次数」。这里的 `without restarting` 指无需重新开始游戏，属于探索模式效果的一部分，见 [Birther.lua:1378](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/Birther.lua:1378)。

- **03203，角色库被说成备份。** 原文 `Characters vault: You will not be able to upload any character to the online vault`；译文为「角色备份：不能在 te4.org 上保存你的角色信息」。相邻选项明确说上传的是角色信息表、`not the whole savefile`；“备份”容易让玩家理解为可恢复的存档备份，见 [GameOptions.lua:643](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/GameOptions.lua:643) 与 [GameOptions.lua:664](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/GameOptions.lua:664)。

- **03203，版本检查被说成版本更新。** 原文 `Addons will not be checked for new versions`；译文为「无法更新插件的版本」。原文限定的是不检查新版，译文扩大为不能更新插件，见 [GameOptions.lua:672](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/GameOptions.lua:672)。

- **03209，点数用途被收窄。** 原文 `Category points left`；译文「技能树解锁点剩余」。同一种点数除了学习新类别，还能提高已知类别精通度、购买刻印位；消费分支见 [LevelupDialog.lua:440](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:440) 和 [LevelupDialog.lua:684](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:684)。

- **03210，类别点数名称沿用同一误述。** 原文 `Talent category points allow you to either`；译文「技能树解锁点有以下作用」。其后列表自身列出提高精通度和刻印位用途，说明这些点数不限于“解锁技能树”，见 [LevelupDialog.lua:650](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:650)。

- **03210，自动消耗时机误述。** 原文括号为 `learning it is automatic when using an inscription`；译文为「你使用刻印时会自动消耗点数解锁」。源码中的类别点数扣除发生在升级界面购买刻印位、确认操作后，而不是使用刻印时自动扣点，见 [LevelupDialog.lua:678](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/sources/game/modules/tome/dialogs/LevelupDialog.lua:678)。

实际读取的实验材料为 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/dialogs/` 下的 **Birther.lua、CharacterSheet.lua、DeathDialog.lua、Donation.lua、GameOptions.lua、GraphicMode.lua、LevelupDialog.lua** 七份冻结源码。源码版本按 `source-access.json` 为 `/workspace/t-engine4` 的提交 `624a67329fe2ad440c5b344785a9c73fcf22ae63`；未读取其他模型输出或当前源码工作树，未写文件。
