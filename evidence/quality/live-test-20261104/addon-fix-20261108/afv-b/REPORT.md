# afv-b 实机验证报告（余烬怒火 / Embers of Rage）

- 测试员：`afv-b`，显示 `:132`（1600×900），GPU 渲染（`TL_GPU=1`），60 fps 帽
- 游戏：T-Engine 1.7.6 + `tome-chn-mod.teaa`（0.3.8，MD5 `d75e5cb37878cb7394cbfa8f82de3c84`）+ orcs / ashes-urhrok / cults
- 角色：`AFVB1`，兽人 狂战士，难度「简单」，模式「冒险模式」，战役「兽人战役：余烬怒火」
- 会话时长：约 80 分钟（含创建角色与职业树巡检）
- 结果汇总：**PASS 3 / FAIL 0 / NOT_REACHED 8**（另有 1 条清单外 FAIL 级观察）

## 逐项结果

| # | 项目 | 结论 | 屏幕证据 |
|---|------|------|----------|
| 6 | 锁定职业描述 | NOT_REACHED | `shots/005055-warrior-tree.png`、`shots/005313-tinker-tree3.png`、`shots/010123-c7.png`、`shots/010403-c12.png` |
| 15 | 开局日志无「角色控制切换至 player」 | PASS | `shots/011032-in-game.png`、`shots/011130-game1.png` |
| 5 | 对话立绘名牌 | NOT_REACHED | —（未触发对话） |
| 1 | 商店标题 | NOT_REACHED | —（未到达商店） |
| 2 | 平民喊话 | NOT_REACHED | —（未到达蒸汽商场） |
| 11 | 盾牌名括号全角逗号 | NOT_REACHED | 参考 `shots/015340-inv-armor3.png` |
| 13 | 「+N% 全部」 | NOT_REACHED | —（无此类物品） |
| 16 | 人偶标签「材质、关键词」 | NOT_REACHED | `shots/011909-inv1.png`、`shots/012316-char-equip3.png` |
| 12 | 角色面板装备组切换 | PASS | `shots/012316-char-equip3.png`、`shots/012418-char-equip4.png`、`shots/012634-char-q.png` |
| 10 | 存档战役名「余烬怒火」 | PASS | `shots/013609-save-node.png`（+裁图 `_c600_90_800x170.png`） |
| 4 | 成就分类列中文 | NOT_REACHED | `shots/014043-achiev.png`、`shots/014211-achiev2.png` |

### 6 锁定职业描述 —— NOT_REACHED（已查证原因）

本机 profile 预置了职业/种族解锁：角色创建页标题为「角色创建（已解锁: 20/20 职业，4/4 种族技能，11/26 其他，0/2 外观）」。
逐一展开全部 12 个职业系并核对：战士系（狂战士/盾战士/弓箭手/奥术之刃/格斗家）、盗贼（盗贼/影舞者/掠夺者/散兵）、
法师系（炼金术士/元素法师/死灵法师）、野性系（召唤师/龙战士/软泥使）、天空系（太阳骑士/星月术士）、
堕落系（收割者/腐化者/毁灭使者/恶魔使者）、痛苦系（被诅咒者/末日使者）、时空系（时空法师/时空守卫）、
灵能系（心灵杀手）、冒险家（冒险家）、疯狂系（蠕動者/熵教徒）、工匠系（链锯屠夫/快枪手/灵能射手/毁灭者）。

**所有条目图标均为彩色、无锁标记/灰显**，悬停任意条目（如链锯屠夫 `shots/005423-hover-sawbutcher.png`、
恶魔使者 `shots/010022-hover-demon.png`）都显示完整职业说明与属性修正，从未渲染 `Once freed, twice shy.`。
因此本次无法通过「悬停被锁定职业」触发该描述，判定 NOT_REACHED 而非 PASS/FAIL。

源码侧已核验（只读，`/tmp/chk` 解包 addon 副本）：
- `data/chn_supplement.lua`：`t("Once freed, twice shy.", "一朝获释，再难轻信。", "_t")`
- `hooks/load.lua`（110–123 行）：对 Orcs 在描述符创建后才替换的 `locked_desc` 函数再次包装 `_t(res)`
- `superload/engine/Birther.lua`：`newBirthDescriptor` 对字符串/函数两种 `locked_desc` 都 `_t`
即机制存在，但本次没有可达的锁定职业可验证。

### 15 开局日志 —— PASS

`game.log` 全部 `[LOG]` 行（145 行，含后续战斗日志）中 `grep "角色控制"` 结果为 **0**。
开局可见日志只有：`由于未开启在线账户，在线账户已禁用（切换至离线账户）。`、
`接受了任务“家园”！（按 J 键查看任务日志）`、`显示小血条和战术边框。`、`保存完毕。`

### 12 角色面板装备组 —— PASS

按 `C` 打开「角色面板：AFVB1」，点「装备[E]」页签 → 标题显示「装备[E]：主用武器组」，人偶持铁质大剑；
再点一次 → 标题变「装备[E]：备用武器组」，人偶武器槽清空，底部日志
`正在显示备用武器组（角色：AFVB1，装备未切换）`。按 `q` 切换武器组后再开面板并点「装备」，
首次切换同样显示中文「备用武器组」，人偶无武器。全程无英文残留、无切换失效。

### 10 存档战役名 —— PASS

保存后回主菜单 → 读取游戏 → AFVB1 存档详情：
`游戏版本：1.7.6` / `需要的插件：chn-mod, ashes-urhrok, orcs, cults` /
`AFVB1 等级1，兽人 狂战士。` / `难度：简单 / 冒险模式` / **`战役：余烬怒火`** / `正在探索克鲁克部落 第 1 层。`
旧现象 `Orcs` 未复现。

## 清单外发现（extra，FAIL 级观察，供裁决）

- 存档详情标题仍为英文且战役名不符：`Tales of Maj'Eyal: Age of Ascendancy: AFVB1`
  （截图 `shots/013609-save-node.png`）。同一窗口下方「战役：余烬怒火」已正确，故这是模块长名/硬编码层面
  的残留，不是本次清单项 10 的失败。是否属本次修复范围请裁决。

## Lua 报错情况

开局后与收尾前各执行
`grep -n -i -E "error|stack traceback|superload|chn" testers/afv-b/game.log`：

- **无任何 Lua 报错、无 stack traceback、无 ShowErrorStack 弹窗。**
- 命中的 `error` 行全部来自 ALSA 音频驱动（`snd_func_* returned error: No such file or directory`，
  与 SDL_AUDIODRIVER=dummy 环境有关），非游戏/插件错误。
- 命中 `chn`/`superload` 的行均为加载清单，显示汉化插件 superload 正常加载：
  `engine/DamageType.lua`、`engine/Birther.lua`、`engine/interface/ActorTalents.lua`、
  `engine/interface/ActorTemporaryEffects.lua`、`mod/class/Store.lua`、`mod/class/Object.lua`、
  `data/talents.lua`，以及 `[I18N] Loaded locale file: /data-chn-mod/locales/zh_hans.lua`、
  `/data-chn-mod/null_translation.lua`、`/data-chn-mod/chn_supplement.lua`。
- 运行期无红字 Lua 报错；战斗日志中的 `#UID:...`、`#{bold}##ORCHID#格挡。` 等标记均正常渲染为中文。

## 未覆盖原因（总体）

1. 开局区域「克鲁克部落（1）」正处于兽人守卫/兽人快枪手与蒸汽巨人守卫/枪手的交战带，玩家被远程
   火力压制（HP 136→122），自动探索（`z`）反复被「在西南面有敌对目标（蒸汽巨人枪手）」打断，
   无法安全穿越到营地商店/NPC 区，因此 **1、5、11、13、16** 均未取得屏幕证据。
2. **2** 需要到达蒸汽商场（Vaporous Emporium）才有男性平民喊话，本段路程不可达。
3. **4** 离线 profile 无成就记录（成就窗口三个筛选下列表均为空），无法查看「分类」列。
4. **6** 预置 20/20 职业全解锁，不存在被锁定（灰色/带锁）职业。

## 已核验的插件侧实现（只读参考，不替代屏幕证据）

- `superload/mod/class/Store.lua`：`interact` 未传 name 时用 `_t(self.name, "entity name")`（对应 1）
- `superload/engine/dialogs/ShowAchievements.lua`：`generateList` 后 `_t(item.category)`（对应 4）
- `superload/mod/class/NPC.lua`：`doEmote` 显示时 `_t(text)`，注释指明 tome-orcs vaporous-emporium 男性平民（对应 2）
- `superload/mod/dialogs/Chat.lua`（对应 5）、`superload/mod/class/Object.lua` 与 `mod/class/uiset/ClassicPlayerDisplay.lua`（对应 11/13/16）

## 文件

- `results.jsonl`：11 条清单项 + 1 条 extra，共 12 行
- `shots/`：本报告引用的全部截图（`_c*` 为放大裁图）
- `game.log`：游戏日志（`[LOG]` 145 行）
