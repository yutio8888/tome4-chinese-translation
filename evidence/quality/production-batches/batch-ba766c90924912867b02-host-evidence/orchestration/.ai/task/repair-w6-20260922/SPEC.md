# 修复窗口6：252批两条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement。基线805b67263c3359441a4e6e12f3ebd0d2bdc5a0da。用户持续授权审核、修复、提交与推送；本窗口因换行不变量问题提前进入修复。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的两个target及evidence/quality/repair-window-6-20260922/。不改其他译文、术语、规则、工具、旧证据；初次不改handoff/catalog/migration；不stage/commit，不写.ai，不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施；独立reviewer只使用中性源码与冻结输入。全部源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。保持source/source_tag/args_order/special、printf/markup/TAB不变。唯一LF例外是e709日记恢复两处空行（3LF→5LF），全部字词不变；另一条LF保持0。

仅两条，REVIEW与FINAL_REVIEW均使用full；max_cycles默认3，旧窗口额外轮次授权不沿用。验证LuaJIT全记录比较恰两条target变动、strict lint/claims、diff check、完整门禁和构建、DONE_VERIFIED。译文commit→queue rebuild→单次catalog/migration→证据发布commit→queue rebuild→push，后继续253。

排除旧Archmage、回忆录pending、RW1-SIB-01/02和本批其他advisory/pending，不扩大工作集。

## e7091b21dcc32852f5515f5a0c9304597eb3eaef2bfe88ab9f8dad95bb5a0384

section: mod-tome/data/lore/trollmire.lua
source_tag: _t

source: You find a tattered page scrap. Perhaps this is part of a diary entry.
"...is a gorgeous glade, but I could swear that looked like a part of a human femur.

...

Saw an absolutely gigantic troll, but fortunately I threw him off my scent."

target: 你找到了一片破烂的纸页残片。也许这是某篇日记的一部分。
“……是一片美得惊人的林间空地，但我敢发誓，那东西看起来像一截人类股骨。
……
看到了一只大得吓人的巨魔，不过幸好我掩住了自己的气味，把他甩掉了。”

确认依据：只恢复省略号前后两处空行，target从3LF恢复source的5LF，全部字词保持当前译文，包括已修复的气味内容。

## e7e5e7f4e541826ba3972684d86422f723d89df27804d83798e60f787fb6aacc

section: mod-tome/data/achievements/events.lua
source_tag: _t

source: Disturbed an old battlefield and survived the consequences.

target: 踏入古战场并最终生还。

确认依据：恢复主动惊扰古战场及在由此引发的后果中幸存的含义；玩家主动挖掘触发坍塌和袭击，存活后授予成就。
