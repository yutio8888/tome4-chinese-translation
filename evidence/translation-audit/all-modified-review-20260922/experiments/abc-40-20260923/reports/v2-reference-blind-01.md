---

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03172 | 未发现问题 | 随机创建按钮，含义一致 |
| entry-03173 | 未发现问题 | 位于教程选择框，“教程”符合语境 |
| entry-03174 | 存在问题 | C01：泛指解锁说明被改成当前选项的具体类型 |
| entry-03175 | 未发现问题 | 保留背景不协调、仍可选择及可能错过任务的信息 |
| entry-03176 | 存在问题 | C02–C05：指代改变、信息遗漏及作者态度误述 |
| entry-03177 | 未发现问题 | 按钮打开捐赠对话 |
| entry-03178 | 未发现问题 | 捐赠者外观功能提示，含义一致 |
| entry-03179 | 存在问题 | C06：装备所属角色被译成观看者 |
| entry-03180 | 未发现问题 | 参数为排序方式；空格变化无损 |
| entry-03181 | 未发现问题 | 参数为流浪者种子 |
| entry-03182 | 未发现问题 | 显示生命值死亡阈值，保留有符号整数格式 |
| entry-03183 | 未发现问题 | 显示生命回复乘治疗系数后的数值 |
| entry-03184 | 未发现问题 | 双手武器标签，与后续武器类别拼接 |
| entry-03185 | 未发现问题 | 用于被缴械时的副手状态 |
| entry-03186 | 未发现问题 | 对应伤害亲和数值列表 |
| entry-03187 | 未发现问题 | 死亡对话标题及颜色标记一致 |
| entry-03188 | 未发现问题 | 打开包含聊天功能的日志对话 |
| entry-03189 | 未发现问题 | 探索模式复活不扣除生命次数 |
| entry-03190 | 未发现问题 | 物品外观变化及幻化语义一致 |
| entry-03191 | 仅建议 | S01：局部中文表达不够顺畅 |
| entry-03192 | 仅建议 | S02：弹窗标题可以更明确地体现移动语境 |
| entry-03193 | 未发现问题 | 对应移动和攻击时的小幅抖动效果 |
| entry-03194 | 未发现问题 | 对应经典HUD日志显示行数 |
| entry-03195 | 存在问题 | C07：开始淡出的时间被表述为消失时间 |
| entry-03196 | 未发现问题 | 四种显示模式及快捷键信息保留 |
| entry-03197 | 未发现问题 | 前句已限定WASD，方向键组合语境成立 |
| entry-03198 | 未发现问题 | 锐化设置范围为0至10，0关闭 |
| entry-03199 | 存在问题 | C08：“始终居中”沿袭上游过度概括 |
| entry-03200 | 未发现问题 | 生命损失警告阈值及100禁用规则一致 |
| entry-03201 | 未发现问题 | 保留角色状态展示、重启及未使用Discord时无效的信息 |
| entry-03202 | 未发现问题 | 保留角色信息副本、非完整存档及分享链接的信息 |
| entry-03203 | 存在问题 | C09：不检查新版本被改为不能更新版本 |
| entry-03204 | 未发现问题 | 对应斗篷兜帽替代头部装备图像 |
| entry-03205 | 未发现问题 | 括注明确纸娃娃显示装备的功能 |
| entry-03206 | 存在问题 | C10：地形过渡被表述为渐变 |
| entry-03207 | 未发现问题 | 两个参数依次为角色名称、等级 |
| entry-03208 | 未发现问题 | 对应按角色等级计算的属性加点上限 |
| entry-03209 | 未发现问题 | 四类剩余点数、顺序和格式均保留 |
| entry-03210 | 存在问题 | C11、C12：扩槽操作误述及高等级点数信息遗漏 |
| entry-03211 | 仅建议 | S03：按钮数值为剩余属性点，标签可更明确 |

以下源码行号均对应 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。为缩短引用，`D/` 表示 `game/modules/tome/dialogs/`，`M/` 表示 `game/modules/tome/`，`E/` 表示 `game/engines/default/engine/`。

- **C01｜entry-03174｜已确认，翻译新增。**  
  原文泛指“locked campaigns, races and classes”，译文变成“解锁**这个**战役，种族，职业”，把一般说明收窄成对当前选项的类型指认。`D/Birther.lua:826、838` 的 `generateDifficulties()` 将同一说明附在锁定的难度选项上；`:858、870` 又用于死亡模式。因此当前选项不一定属于译文指认的三种类型。

- **C02｜entry-03176｜已确认，翻译新增。**  
  “I realize **this** can not please everybody”承接通过犯错、死亡学习的设计，译成“**这款游戏**可能不会被所有人接受”后，评价对象扩大为整个游戏。证据为 `D/Birther.lua:1379–1380` 的连续语境，属于指代和语义范围变化。

- **C03｜entry-03176｜已确认，翻译遗漏。**  
  “try as much as you want **without restarting**”只剩“无限多的尝试次数”，遗漏不必重新开始角色的区别。`D/Birther.lua:1381` 明说此条件；`D/DeathDialog.lua:174–185、340–345` 显示探索模式走原角色复活流程，并且不扣生命次数。无限次重新创建角色与无限次原角色复活并不等价。

- **C04｜entry-03176｜已确认，翻译遗漏。**  
  “While this is a **free game** that I am doing for fun”译成“尽管这只是我自娱自乐所做的一款游戏”，遗漏免费这一事实陈述。证据为 `D/Birther.lua:1384`；该信息不能由“自娱自乐”替代。

- **C05｜entry-03176｜已确认，翻译新增。**  
  “I certainly will not complain as real life can be harsh sometimes”表达作者欢迎游戏收入补贴家用，并解释现实生活有时艰难。译文“不会**再抱怨现实的诸多压力**了”改成收到帮助后停止抱怨现实，并新增过去一直抱怨的意味。证据为 `D/Birther.lua:1384` 的完整条件句；这不是单纯语气润色。

- **C06｜entry-03179｜已确认，翻译新增。**  
  “Displaying %s set **for %s**”被译成“展示 %s 套装**给 %s 看**”。`D/CharacterSheet.lua:71–74` 先切换面板展示的 `main/off` 装备组，再传入 `self.actor:getName()`；第二个参数是装备所属角色，不是观看者。“装备未切换”保留正确，但不能抵消所属关系错误。

- **C07｜entry-03195｜已确认，翻译新增。**  
  “Fade time”译为“消失时间”，混淆开始淡出与完全消失。`D/GameOptions.lua:217–227` 明确这是日志开始淡出前的秒数，并调用 `enableFading(qty)`；`E/LogDisplay.lua:270–274` 在经过设定的 `t` 秒后才开始降低透明度，到 `2t` 秒才完全不可见。例如设置3秒并不是3秒后消失。术语快照中的技能名“Fade”不适用于此处，判定不依赖该术语行。

- **C08｜entry-03199｜已确认，沿袭上游描述。**  
  “always center on the player”与“始终以人物为中心”都没有说明地图边界限制。`M/class/Game.lua:726` 把玩家坐标和滚屏距离传给 `moveViewSurround()`；`E/Map.lua:899、909` 在边距足够大时计算居中坐标，但 `:929` 随后调用 `checkMapViewBounded()`，`:935–943` 会按地图边界修正，较小地图还会直接居中整张地图。因此靠近地图边缘等情况下，不能保证人物始终居中。译文没有新增此错误。

- **C09｜entry-03203｜已确认，翻译新增。**  
  “Version checks: Addons will not be **checked for new versions**”译成“插件版本更新：**无法更新插件的版本**”，把版本检查改成更新操作，并扩大了禁止范围。`D/GameOptions.lua:671–672` 同时保留手动安装途径，又明确这一项说的是新版本检查；这两种操作不能混为一谈。依据是该选项说明内部明确区分的操作语境，不是对网络变量名的推测。

- **C10｜entry-03206｜已确认，翻译新增。**  
  “transitions”译成“渐变”，未准确表达这里的相邻地形过渡拼接。`D/GraphicMode.lua:84–89` 将选项写入 `tiles_custom_adv`；`M/class/Game.lua:633` 将其用于 `Map.tiles.nicer_tiles`。`M/class/NicerTiles.lua:77–80、684–721` 实际检查相邻地形类型，并选择边缘、外角和内角贴图，`:725–730` 用于水、草地和沙地等地形的衔接。这里涉及地形交界的贴图选择，而不是泛指颜色渐变。未另将“大型贴图”计为一个已证实的机制缺陷。

- **C11｜entry-03210｜已确认，沿袭上游描述，译文进一步明确了自动扣点。**  
  原文“learning it is automatic when using an inscription”，译文“使用刻印时会**自动消耗点数解锁**”，与实际玩家操作不符。`M/class/interface/ActorInscriptions.lua:66–85` 找不到空位时打开 `player-inscription` 对话；`M/data/chats/player-inscription.lua:42–49` 只有玩家选择购买新槽的答案后才扣点、增加槽位并安装刻印，`:52` 明确允许取消。另有 `D/LevelupDialog.lua:684–690` 的确认购买流程。因此使用刻印不会无条件自动扣点扩槽。

- **C12｜entry-03210｜已确认，沿袭上游信息遗漏。**  
  原文和译文都只列出10、20、34级的点数来源。`M/class/Actor.lua:3959–3962` 的实际升级规则还包含 `level > 50` 且 `(level - 4) % 30 == 0` 的情况，即64、94级等继续获得点数。对于允许角色超过50级的情形，这份点数获取说明不完整；10、20、34这三个等级本身没有译错。

仅建议事项如下，均不计作缺陷，也不提供替换译文：

- **S01｜entry-03191。** “我最衷心的希望”等局部搭配略显生硬。`D/Donation.lua:48–54` 的自我介绍、捐赠请求及附加功能列表关系仍清楚，属于语言流畅度建议。
- **S02｜entry-03192。** “设置动画速度”单独看较宽泛，但冻结相邻文本明确限定为平滑生物和投射物移动；`D/GameOptions.lua:107–114` 也在这一选项下打开输入框。结合实际界面语境，没有足够依据判定其宣称控制所有动画，故只作明确性建议。
- **S03｜entry-03211。** `D/LevelupDialog.lua:773、1077` 填入的是 `unused_stats`。原文和译文都使用简短类别标签，在升级点数界面可以成立；对标签明确程度的偏好不足以认定信息错误。

实际读取范围如下。设包目录 `P` 为：

`evidence/translation-audit/all-modified-review-20260922/experiments/abc-40-20260923/protocol-v2`

冻结材料版本为本次 `protocol-v2`：

- `P/INPUT.md`
- `P/entries.json`
- `P/context.lua`
- `P/source-access.json`
- `P/sources/game/modules/tome/dialogs/Birther.lua`
- `P/sources/game/modules/tome/dialogs/CharacterSheet.lua`
- `P/sources/game/modules/tome/dialogs/DeathDialog.lua`
- `P/sources/game/modules/tome/dialogs/Donation.lua`
- `P/sources/game/modules/tome/dialogs/GameOptions.lua`
- `P/sources/game/modules/tome/dialogs/GraphicMode.lua`
- `P/sources/game/modules/tome/dialogs/LevelupDialog.lua`

七份冻结源码的SHA-256均与 `source-access.json` 一致。40条原文、译文与 `entries.json` 一致；未发现占位符、标记或元数据不变量问题。

额外源码均仅通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取：

| 实际源码路径 | 调用链或符号来源 |
|---|---|
| `game/modules/tome/class/Game.lua` | `GameOptions.lua` 的 `game:setupWASD()` 等游戏对象调用 |
| `game/modules/tome/class/Actor.lua` | `LevelupDialog.lua` 的角色方法与点数字段、`CharacterSheet.lua` 的角色字段；另获 `Game.lua` 的显式require印证 |
| `game/modules/tome/class/interface/ActorInscriptions.lua` | `Actor.lua` 显式require |
| `game/modules/tome/class/NicerTiles.lua` | `Game.lua` 显式require及实例创建 |
| `game/engines/default/engine/Map.lua` | `GraphicMode.lua`、`Game.lua` 显式require及 `moveViewSurround()` 调用 |
| `game/modules/tome/data/chats/player-inscription.lua` | `ActorInscriptions.lua` 的 `Chat.new("player-inscription", ...)` |
| `game/modules/tome/class/uiset/Classic.lua` | `Game.lua` 按HUD配置加载uiset；冻结设置列出Classic |
| `game/modules/tome/class/interface/ActorLife.lua` | `Actor.lua` 显式require |
| `game/modules/tome/class/Player.lua` | `Game.lua` 显式require，用于检查玩家升级覆盖逻辑 |
| `game/engines/default/engine/LogDisplay.lua` | `Classic.lua` 显式require并调用 `enableFading()` |
| `game/engines/default/engine/Tiles.lua` | `Game.lua`、`Birther.lua` 显式require，追查贴图处理 |
| `game/engines/default/engine/Entity.lua` | `Game.lua`、`Birther.lua` 显式require；`LevelupDialog.lua` 调用实体的 `getMapObjects()` |

没有保留待确认claim；未运行游戏，显示与机制判断基于上述静态源码及冻结语境。未越界读取，未查看实验臂报告、历史意见或其他模型输出，未写文件，未创建子agent。以上为独立审核观察，未做模型比较。
