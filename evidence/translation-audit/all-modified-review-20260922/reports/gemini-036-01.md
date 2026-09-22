# batch-036 译文复核报告

## 批次与环境核验
- **批次编号**：batch-036
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-036.md`
- **文件哈希**：`f15232b71d57ee54dbc6ab5ae63914cdfa67a6cefc3e033e8ce5383cb1535ae1`（SHA-256 核验一致）
- **条目范围**：`entry-01223` 至 `entry-01223`，共 1 条
- **固定公开源码基准**：t-engine4 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/lore/elvala.lua`）
- **译文基准**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua:15168`）

---

## 条目详细复核

### entry-01223
- **位置**：`mod-tome.lua:15168`
- **Section**：`mod-tome/data/lore/elvala.lua`
- **Source Tag**：`_t`
- **占位符 / 格式控制**：
  - 格式控制符 `#{italic}#`、`#{bold}#`、`#{normal}#` 开闭正确，无占位符遗漏或错位。
  - 段落划分（33 段）与换行结构与原文保持一致。
- **复核结论**：**存在疑点**

#### 可核验依据与问题详列：

1. **代词与主谓指代严重倒错（影响叙事逻辑与事实）**
   - **第 23 段原文**：
     > “If **this human’s** tale is to be believed then we are in very grave danger! Scout reports suggest there is a body of humans coming here from the north as we speak. From what **this human** says **they** seek retribution - they wish to slaughter us all.”
   - **当前译文**：
     > “如果**有关人类的事情**是真的话，那么我们现在已经处在非常危险的境地了！在我们说话的时候，就有哨兵向我们报告，一群人类正在从北方向我们这边过来。**那些人类说**他们要寻求复仇——他们要杀光我们！”
   - **核验事实**：
     - 原文中在场的单数代词短语 `this human` 两次均明确指代站在莱娜尼尔身边的年长人类信使崔岚（Cuilan），`this human's tale` 指崔岚刚刚述说的特塞尔（Turthel）之死及人类叛乱始末。译文将其望文生义译为“有关人类的事情”，脱离了语境。
     - 原文后半句 `From what this human says they seek retribution` 中，主语 `they` 指代从北方赶来的人类队伍（a body of humans），全句为佩里萨基于崔岚的证词做出的推断（“根据这个人类[崔岚]所说，他们是来寻求报复的”）。译文误将 `this human` 理解为北方的人群，错译为“那些人类说他们要寻求复仇”，造成主客体混淆。

2. **时间指代与叙事逻辑倒错**
   - **第 8 段原文**：
     > “But **none of this I knew** as I lay weeping in the aftermath, cradling in my lap the one life I cared about.”
   - **当前译文**：
     > “然而，在我在灾难之中抱着我生命中最重视的人的身体，放声痛哭的一刻，**我还不知道之后所发生的那些无尽的困难**。”
   - **核验事实**：
     - 本篇为艾伦尼恩的回忆录，第 3 至 7 段作者以全知回忆视角详述了魔法大爆炸席卷整个大陆的宏大灾难（五百万人死亡、山河移位、星辰倾斜）。第 8 段句首的 `none of this` 承前指代上述刚刚描述的整场世界浩劫，意在对比“彼时彼刻怀抱垂死爱人的我，对外部世界天翻地覆的灾难一无所知”。
     - 译文将前指代词倒错为“之后所发生的那些无尽的困难”，不仅凭空增添了原文不存在的内容，且将前向追述彻底颠倒为后向未卜先知，违背原叙事逻辑。

3. **关键情节遗漏（漏译）**
   - **第 22 段原文**：
     > “He handed me his ring, **saying to seek you out in Elvala**, and then stepped outside to face the crowds.”
   - **当前译文**：
     > “他把他的戒指交给了我，然后一个人走了出去，直面了外面的人群。”
   - **核验事实**：
     - 原文中特塞尔走向暴民前对崔岚的关键遗命嘱托 `saying to seek you out in Elvala`（交代我到埃尔瓦拉来寻找你）在译文中被整句漏译。该句是解释崔岚为何会跨越地域专程赶赴埃尔瓦拉将戒指交予莱娜尼尔的重要情节枢纽。
   - **第 32 段原文**：
     > “What few made it through the smoke and arrows **I took on**, tearing Mooncutter through their flesh with little resistance.”
   - **当前译文**：
     > “只有几个人能够躲过烟雾和箭雨的夹击，我的斩月剑可以十分轻松地穿透那些仅存的人的血肉。”
   - **核验事实**：
     - 原文中艾伦尼恩主动接战的主谓动作 `I took on`（少数突破烟雾和箭雨冲过来的敌人由我亲自接战）被漏译，译文弱化为了纯客观陈述。

4. **标点与断句缺陷**
   - **第 28 段**：原文 `“But your wounds-” I tried to object.` 译为 `“但是你的伤口——”我试图反对`，句末漏句号。
   - **第 29 段**：译文出现重叠标点 `“来吧，崔岚，我们必须离开这个地方。”。`（引号内已有句号，引号外多出一个句号）。
   - **第 32 段**：原文 `As the peasants stumbled in confusion archers started firing from our walls.`，译文断句为 `当那些农民陷入混乱的时候。弓箭手们开始从城墙上向下射击。`，从句后误用句号导致前半截成为缺少主谓的残句。
   - **第 22 段**：开头 `昨天，也就是可怕的魔法大爆炸之后的一天。我们本来准备开始重建工作...`，时间状语从句后误用句号断裂。

5. **细微观察与语感偏差**
   - **第 10 段**：`worried she might relapse, and at the back of my mind scared of that empty look she had given me` 译为“但又对她的虚弱状态感到担忧。而且，她刚才看向我时空洞的眼神让我心如刀割”。
     - `relapse` 指旧伤复发/伤情恶化，译为“虚弱状态”弱化了濒死复发的紧迫性。
     - `scared` 指因莱娜尼尔那空洞眼神而内心生畏（承接后文害怕她不肯原谅自己在灾难中的过失），译为“心如刀割”改变了人物的情感指向（将畏惧转为哀伤）。
   - **第 9 段**：`Her gaze at me was empty` 译为“她望向我的目光空灵无物”。“空灵”带有褒义与出尘脱俗之意，此处莱娜尼尔身受重创、失魂落魄，应为“空洞/呆滞”。
   - **第 4 段**：`white stone cracking` 译为“磐石也被其撕裂”。在 ToME 设定中，夏·图尔传送门及遗迹的标志性材质为“白石”（white stone），意译为“磐石”弱化了这一世界观特征。
   - **第 33 段**：`dealings with the outside world` 译为“和外界的一切交易”。`dealings` 语境下指与外界的一切“往来/接触”，译为商业层面的“交易”偏窄。