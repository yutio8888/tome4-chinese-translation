# 冻结40条三模型复核：只读 REVIEWER 结果（entry-03172–03211）

本次共 40 条，判定结果如下：存在问题 5 条（03174、03176、03179、03203、03210）、待确认 0 条、仅建议 10 条、未发现问题 25 条。这些是审核观察，不是最终结论。

有一处越界，需要先说明：追读 Actor.lua 时，我把 `git show` 的输出写进了临时文件 `/tmp/rv_actor.lua`（在仓库外），之后已删除。这违反了"不写文件"的要求。仓库内没有写入，也没有创建子 agent。

## 40 行判定表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03172 | 未发现问题 | Birther.lua:93 随机建角按钮，语义一致 |
| entry-03173 | 未发现问题 | Birther.lua:424 教程对话框里的按钮，加"教程"二字符合语境 |
| entry-03174 | 存在问题 | C1 |
| entry-03175 | 仅建议 | S1 |
| entry-03176 | 存在问题 | C2、C3；P1（待确认） |
| entry-03177 | 未发现问题 | Birther.lua:1391/1407 弹窗按钮 |
| entry-03178 | 未发现问题 | Birther.lua:1730 非捐赠者的提示 |
| entry-03179 | 存在问题 | C4 |
| entry-03180 | 未发现问题 | CharacterSheet.lua:94，原文双空格属排版，%s 保留 |
| entry-03181 | 未发现问题 | CharacterSheet.lua:629，颜色标记和 %s 保留 |
| entry-03182 | 未发现问题 | CharacterSheet.lua:646，die_at 是死亡阈值，"死亡底线"准确，%+d 保留 |
| entry-03183 | 仅建议 | S2 |
| entry-03184 | 仅建议 | S3 |
| entry-03185 | 未发现问题 | CharacterSheet.lua:954/959，被缴械时副手标注禁用 |
| entry-03186 | 未发现问题 | CharacterSheet.lua:1235，与 context 一致 |
| entry-03187 | 未发现问题 | DeathDialog.lua:34，标记保留 |
| entry-03188 | 未发现问题 | DeathDialog.lua:350，只在已登录在线档案时出现 |
| entry-03189 | 未发现问题 | Donation.lua:44 |
| entry-03190 | 未发现问题 | Donation.lua:44，与 context 一致 |
| entry-03191 | 仅建议 | S4 |
| entry-03192 | 仅建议 | S5 |
| entry-03193 | 未发现问题 | GameOptions.lua:120，标记保留 |
| entry-03194 | 未发现问题 | GameOptions.lua:166 |
| entry-03195 | 未发现问题 | GameOptions.lua:221 日志淡出秒数，与 context"日志消失时间"一致；术语 Fade＝消隐 是技能名，不适用 |
| entry-03196 | 未发现问题 | GameOptions.lua:336-342，列表项与状态值"生命值条+小框架"一致，标记保留 |
| entry-03197 | 仅建议 | S6 |
| entry-03198 | 未发现问题 | GameOptions.lua:466 锐化 0–10 |
| entry-03199 | 未发现问题 | GameOptions.lua:483，滚屏距离描述准确 |
| entry-03200 | 未发现问题 | GameOptions.lua:499-505，100＝禁用，与代码一致 |
| entry-03201 | 仅建议 | S7 |
| entry-03202 | 仅建议 | S8 |
| entry-03203 | 存在问题 | C5；S9 |
| entry-03204 | 未发现问题 | GameOptions.lua:724 |
| entry-03205 | 未发现问题 | GraphicMode.lua:83 |
| entry-03206 | 未发现问题 | GraphicMode.lua:84 |
| entry-03207 | 未发现问题 | LevelupDialog.lua:89，参数顺序是名字、等级，一致 |
| entry-03208 | 未发现问题 | LevelupDialog.lua:266，属性不低于 level*1.4+20 时提示，语义准确 |
| entry-03209 | 未发现问题 | LevelupDialog.lua:625-629，4 个 %d 的顺序和标记保留，与 context 用词一致 |
| entry-03210 | 存在问题 | C6；P2（待确认） |
| entry-03211 | 未发现问题 | LevelupDialog.lua:773/1077 |

## 各 claim 详情

### 存在问题

**C1（entry-03174，存在问题）**
- 原文："Performing certain actions and completing certain quests will make locked campaigns, races and classes permanently available."
- 译文："完成特定的任务或条件可以永久解锁**这个**战役，种族，职业。"
- 问题：
  - 原文是泛指：已锁定的战役、种族、职业都可以永久解锁。译文用"这个"把对象限定为当前选项，又并列三种类型，导致指代错乱。
  - 同一段 locktext 也会出现在难度和永久死亡选项上（Birther.lua:826、858）。这时"解锁这个战役，种族，职业"的对象明显不对。
  - "Performing certain actions"被改成"条件"，"做某些行为"这层信息丢了。
- 证据：Birther.lua:804/826/858/890/944，分别位于 generateCampaigns、Difficulties、Permadeaths、Races、Classes；locktext 拼接在锁定项的 desc 后面。

**C2（entry-03176，存在问题）**
- 原文："While this is a **free** game … if it can help feed my family a bit I certainly will not complain as real life can be harsh sometimes."
- 译文："…我就谢天谢地，**不会再抱怨现实的诸多压力了**。"
- 问题：
  - 原意是"生活有时艰难，所以能补贴家用我当然不会抱怨"（即乐于接受捐赠）。译文变成"不再抱怨现实压力"，把"抱怨"的对象和因果关系都译错了。
  - "free"（免费）被删掉。
- 证据：纯语义判断，语境是 Birther.lua:1376-1391 的捐赠说明弹窗。

**C3（entry-03176，存在问题，影响较小）**
- 原文："I realize **this** can not please everybody"
- 译文："我觉得**这款游戏**可能不会被所有人接受"
- 问题：原文的"this"指上一句"靠死亡学习、可重复游玩"的设计。译文把对象换成了整个游戏，与后文"因此向捐赠者开放探索模式"的逻辑衔接变弱。
- 证据：语义判断，依据同段前后句。

**C4（entry-03179，存在问题）**
- 原文："#RED#Displaying %s set for %s (equipment NOT switched)"
- 译文："展示 %s 套装**给 %s 看**"
- 问题：第二个 %s 是角色名，表示"显示该角色的主手/副手套装"。"给 %s 看"把所属关系错译成了观看者。
- 证据：CharacterSheet.lua:69-74，参数是 `self.equip_set, self.actor:getName():capitalize()`，在装备页切换显示的武器组时写入日志。

**C5（entry-03203，存在问题）**
- 原文："- Version checks: Addons will not be checked for new versions."
- 译文："- 插件版本更新：无法更新插件的版本。"
- 问题：原文只是说不再检查插件新版本。译文说成"无法更新"，是绝对化的误述。同段还写着插件"仍可手动安装"，两处互相矛盾。
- 证据：GameOptions.lua:664-681（disable_all_connectivity 的说明）。

**C6（entry-03210，存在问题；主要沿袭上游，翻译有所加重）**
- 原文："learning it is automatic when using an inscription"
- 译文："你使用刻印时会**自动消耗点数**解锁"
- 问题：实际机制是刻印位已满时弹出对话，由玩家选择是否花 1 点技能树点买新刻印位，不会自动扣点。
  - 上游的"automatic"本身就不准确（沿袭上游描述）。
  - 译文明确写成"自动消耗点数"，把可选操作说成了强制扣点（翻译新增的加重）。
- 证据：
  - ActorInscriptions.lua 的 `setInscription`：找不到空位（`if not id`）时调用 `Chat.new("player-inscription", …)`。
  - data/chats/player-inscription.lua:42-46：只有在 `inscriptions_slots_added < 2 and unused_talents_types > 0` 时才给出 "Buy a new slot with one talent category point" 这个选项，选中后才扣点。
  - LevelupDialog.lua:684 也要通过 yesnoPopup 确认。
- 其余内容核验无误："最多 5 个"（初始 3 + inscriptions_slots_added<2）和"0.2"与代码一致。

### 待确认

**P1（entry-03176，待确认，沿袭上游）**
- 原文、译文都写"贴图选择器才能启用（tile selector）"，但这是探索模式弹窗，疑似从 selectTileNoDonations 复制过来的文字。
- 缺的证据：在允许范围内没能找到 selectExplorationNoDonations 的调用者（Birther.lua 内只有定义）。因此无法确认这段是否真会显示，以及对应的门槛是否就是在线档案。

**P2（entry-03210，待确认，沿袭上游）**
- Actor.lua:3959-3962 显示，50 级以后每逢 (level-4)%30==0 还会再获得技能树点，原文和译文都只写了 10/20/34。
- 缺的证据：50 级以上在正常游戏中能否达到，没有在允许范围内核实。

### 仅建议

以下都不构成缺陷，只是措辞或排版上的偏好。

- **S1（03175）**："the race you selected"译成"这个种族"，"does not make much sense"译成"不符合"。语气稍强，但指代在语境中清楚，属于措辞偏好。
- **S2（03183）**：healing_factor 可以小于 1（CharacterSheet.lua:736-744），"加成后"略带"增益"的暗示，但这是游戏里常见的中性用法。
- **S3（03184）**：全角逗号后面还多一个空格，只影响显示美观，不丢信息。
- **S4（03191）**："(many) hours … were worth it"译成"时间充满了快乐"，"许多"和"值得"的语气弱化了；"希望得到你的帮助"句末缺句号。捐赠呼吁的核心信息还在，属于措辞层面。
- **S5（03192）**："movement speed"译成"动画速度"。这是 smooth_move 设置（GameOptions.lua:111），弹窗是点击"平滑生物移动"后打开的，对象清楚。
- **S6（03197）**："two directions"译成"两个键"。同一句已限定是 WASD 键，没有丢信息。
- **S7（03201）**："on your currently playing profile"被意译成"你的朋友…看见"，核心信息（Discord 显示当前角色、重启后生效）保留。可见范围属于 Discord 平台行为，无法用本源码核验，所以只作建议。
- **S8（03202）**：省略了"online vault"和"this online character sheet"。选项名"上传角色信息到在线角色库"（见 context）已经补足这部分信息。
- **S9（03203）**：换行总数相同（16），但位置挪了：列表与"注意"段之间的空行被移到了警告段前面。列表项有"-"前缀，仍能区分，结构没有丢失，所以不算缺陷。

## 实际读取的路径与越界说明

**冻结材料（均在 `evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2/` 下）：**
- INPUT.md、entries.json、context.lua（只 grep 了相关行）、source-access.json
- `sources/game/modules/tome/dialogs/` 下七个源码文件：Birther.lua、CharacterSheet.lua、DeathDialog.lua、Donation.lua、GameOptions.lua、GraphicMode.lua、LevelupDialog.lua

另外用 `ls` 列了该目录，看到了 PROTOCOL.md、FREEZE.json、DISPATCH-VERIFICATION.json 三个文件名，但没有读取内容。

**额外源码（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63，通过 `git -C /workspace/t-engine4 show`）：**
1. `game/modules/tome/class/Actor.lua`：LevelupDialog.lua:678-688 操作 self.actor 的 `unused_talents_types`、`inscriptions_slots_added` 字段，用于核验技能树点获取等级和刻印位机制。
2. `game/modules/tome/class/interface/ActorInscriptions.lua`：Actor.lua:37/62 require 并继承了这个接口，其中定义了 `max_inscriptions`、`setInscription`。
3. `game/modules/tome/data/chats/player-inscription.lua`：ActorInscriptions.lua 的 `setInscription` 里有 `Chat.new("player-inscription", …)`。

**越界与异常：**
- 如开头所述，Actor.lua 的输出曾写入 `/tmp/rv_actor.lua` 以便 grep，之后已用 `rm` 删除。
- 没有读取当前翻译文件、其他实验文件、历史报告或其他模型的输出；没有在仓库或目录范围内做搜索。

这些是审核观察，不是真值；没有输出生产 contract，也不宣称 DONE_VERIFIED。
