# 独立复核结果（只读）

复核对象：两条实机发现。证据来源：
`/workspace/tome4-chinese-translation/mod-tome.lua`、`tome-orcs.lua`；
`git -C /workspace/t-engine4 show 624a67329fe2:game/modules/tome/class/Object.lua`（下文 Object.lua 均指该固定 commit）。

引擎拼接机制（判定前提，已核实）：`desc:add()` 只是把参数依次追加（`game/engines/default/engine/utils.lua:1566` `tstring:add`），
`true` 才产生换行（`tstring:toString`，同文件 1661 起）。因此 `{"color","YELLOW"}, 标签, {"color","LAST"}, 说明, true`
中标签与说明之间**没有任何自动分隔符**，英文标签自带的尾随空格就是唯一间隙；中文若保留该空格，就是多出半个字宽的间隙，
若不保留，"："与说明直接相接，符合中文排版。

---

## 发现 A：Embers「飞行背包」提示中「避免压力陷阱： 」冒号后多保留一个半角空格

**结论：成立**（格式缺陷，轻微；但"只改这一条"不够，应族内统一）

依据：

1. `mod-tome.lua:958` `t("Avoid Pressure Traps: ", "避免压力陷阱： ", "_t")`：译文在**全角**冒号后又保留了一个 ASCII 空格。
   该键唯一消费者是 `Object.lua:1932`，与 `Object.lua:1932` 的说明句直接拼接，故显示为「避免压力陷阱： 该物品可防止装备者触发压力式陷阱。」
   （冒号与"该物品"之间多半个字宽间隙）。
2. 同一提示框内其他标签不保留该空格：`mod-tome.lua:918` `"Movement speed: "→"移动速度："`，
   以及 917/919/920/921（`Global/Combat/Casting/Mental speed`）均去掉尾随空格；这些同样经 `Object.lua:1852-1856` 的 `compare_fields`
   直接与数值拼接（英文靠该空格分隔数字，中文不需要）。发现 A 所举的对照例子属实。
3. 同族（`Object.lua` 中 `{"color","YELLOW"}, _t"标签: ", {"color","LAST"}, _t"说明"` 这一构造）共 5 个键，现状不统一：
   - `mod-tome.lua:766` `Crushing Blows: ` → `毁灭打击：`（无空格，Object.lua:1122）
   - `mod-tome.lua:956` `Quick Weapon Swap:` → `快速切换武器：`（源文本身无尾随空格，Object.lua:1928）
   - `mod-tome.lua:951` `Blind-Fight: ` → `心眼： `（**保留空格**，Object.lua:1916）
   - `mod-tome.lua:953` `Lucid Dreamer: ` → `清晰梦境： `（**保留空格**，Object.lua:1920）
   - `mod-tome.lua:958` `Avoid Pressure Traps: ` → `避免压力陷阱： `（**保留空格**，Object.lua:1932）
4. 库内既有惯例与文档一致：`docs/review-operations-guide.md:265` 明确「ego 前后缀、冒号标签的尾随空格：中文按本库拼接不保留空格」；
   全库形如「： 」的译文仅 12 处（`grep -c '： "'`），其余数千条冒号标签均已去掉空格。
5. 无门禁阻碍：`tools/i18nlib/lint.py` 无"保留源文空白"一类校验（相关检查只有 `format-mismatch`、
   `format-invalid-percent`、`talent-placeholder-spacing`、`format-shape-difference`），去掉该空格不会挂 strict lint。

修复范围建议：**族内统一，不止 958 一条**。951/953/958 是同一构造、同一提示框区域的同一个缺陷，只改 958 会让
「心眼：」「清晰梦境：」与「避免压力陷阱：」继续不一致（同一件装备可同时带多个此类标签）。
但**不要做全局替换**：其余 9 处「： 」分属不同语境（如 `mod-tome.lua:42381-42389` 调试菜单条目源文本身带前后空格、
`2324` `Linked by: `、`9225` `Winter Storm: `、`41969/41972`、`42561`），不在本发现范围内，需各自按语境另判。
即：A 成立，修法为 3 条一并改为「心眼：」「清晰梦境：」「避免压力陷阱：」，不动其他条目。

---

## 发现 B：「便携式自动材料提取仪」说明正文以英文缩写「APE」开头

**结论：成立**

依据：

1. `tome-orcs.lua:1140-1142`：物品名为 `Automated Portable Extractor → 便携式自动材料提取仪`（`tome-orcs.lua:1138`），
   而说明正文译作「APE 是一个多功能工匠工具箱，……」，正文首词是无处解释的英文缩写。
   说明文本由物品定义直接展示，紧接着物品名，玩家看不到任何「APE＝便携式自动材料提取仪」的对照。
2. 同一物品的相邻界面文本都已不用缩写：`tome-orcs.lua:1145`「立刻熔解**提取仪**内的所有物品」、
   `1146`「便携式自动材料提取仪设置为默认物品转化选项」、`1147/1149` 用全称。发现 B 对该范围的描述属实。
3. 术语表已有定论且无 APE 缩写条目：`terminology/items.tsv:76`
   `Automated Portable Extractor	便携式自动材料提取仪	T.GAME.ENTITY	items	entity name	preferred	dlc`，
   notes「对话标签同用此名」。保留裸「APE」不在术语记录支持范围内。
4. 缩写在别处同样没有"合法身份"：`tome-orcs.lua:1153` 的 `t("APE","APE","_t")` 位于 `--[==[ ]==]` 注释块内
   （`1152` 标注 `-- untranslated text`），即该键并未启用；正文里的 APE 也不是英文名对应的中文缩写
   （便携式自动材料提取仪的首字母并非 APE）。
5. 相关事实（在本发现范围之外，但影响修法选择）：`tome-orcs.lua:8233`
   `"When you close the inventory window, all items in the APE will be melted." → "……所有APE里面的物品都会被分解。"`
   仍留 APE。若只改说明正文，同一物品族里仍会有 APE 出现。

改法建议：**优先用「提取仪是……」**（与 1145/1147/1149 的既有用词一致，中文句子自然，且不引入玩家无从对应、别处也不显示的英文缩写）。
不建议在正文首次出现处写「便携式自动材料提取仪（APE）」：这会新造一个"带英文括注"的写法，而本库同族文本与术语表都倾向不用缩写，
也会与 1145/1147/1149 的新写法再次不一致；若确要保留全称，应直接写全称「便携式自动材料提取仪是一个多功能工匠工具箱……」，
仍不引入 APE。无论选哪种，`8233` 的「APE」建议同批按同一用词处理，否则本主张要解决的"玩家无法对应"问题仍残留一处。

---

## 汇总

- A = 成立（格式缺陷，轻微；应 951/953/958 三条族内统一，不做全局替换，不涉其他「： 」条目）
- B = 成立（正文首词 APE 无对应、与相邻条目及术语表不一致；建议改「提取仪是……」或全称，并同批处理 `tome-orcs.lua:8233`）
- 未复核、未改动任何文件；除上述引用外未扩展到其他条目。
