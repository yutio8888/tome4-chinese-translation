"""Post-B3 mapping; immutable pre-B3 reference remains separately available."""
def extend(g):
    new,table,R,observations=g['new'],g['table'],g['R'],g['observations']
    new('N88','03867','confirmed','far more dangerous','可怕的多','程度补语应为可怕得多。','原文对应恐怖程度比较；属于明确错字，不是半角标点或版式偏好。','表达建议')
    new('N89','03862','advisory','My fellow councilors,','我的同僚们','空行和段落合并未改变呼语所属。','没有显示损坏或逻辑依赖证据，不能仅按23→21段认定结构缺陷。','表达建议')
    new('N90','03866','advisory','paragraph breaks','额外空行','空行数量变化本身不是翻译缺陷。','段落、模板和事件仍可辨，没有信息丢失证据。','表达建议')
    new('N91','03867','advisory','ancient, impossibly advanced Farportal','发达到让人难以置信的远行传送门','古老修饰可补充以提高清楚度。','叙述仍保留古代科技通路及其先进特征；未据遗漏一个修饰词另立事件或机制错误。')
    new('N92','03867','advisory','held up the Orb of Many Ways to activate it','手握着多元水晶球','举球激活的目的可以更明确。','该句接着描述通过作响旋转的传送门，球与通行的联系仍在，作为动作明确度建议。')
    new('N93','03874','advisory','Long before their creation','在他们被创造出来之前','可补很久以保留时间距离。','先于创造、众神尚年轻的完整历史关系保留；此处未给确定年代或数量边界。')
    new('N94','03955','advisory','newline indentation','裸换行','缩进字符差异不足确认显示缺陷。','各说明行仍完整，未给出引擎中段落层级破坏的证据。','表达建议')
    new('N95','03962','advisory','newline indentation and trailing period','全角空格及省略末尾孤立句点','等效缩进与删除英文残留句点不构成信息遗漏。','不按字符或换行计数机械判错；没有数值、目标或标记损坏。','表达建议')
    new('N96','03866','advisory','name template followed by comma','半角逗号加空格','中英文标点形式差异仅为排版建议。','不是模板闭合、参数消费或动态分支损坏。','表达建议')
    new('N97','03867','advisory','<?=Lore.pocket_time_winner.name?> refused to back down','<?=Lore.pocket_time_winner.himher?>绝不愿朝困难屈服','姓名改成同一人物的代词，完整语境指代明确。','中文无英语主宾格强制，himher实际中文短串也未获证；不能把变量种类差集当作错译。','表达建议')
    new('N98','04126','advisory','copies.','克隆体.','半角句点只需排版统一。','不改变句界、数值或运行解析，不计确认错译。','表达建议')
    new('N99','03915','advisory','Amazing!','冲锋！死亡之轮！！','感叹号数量不构成独立错译。','话语行为变化已N35确认；不把其标点差异重复计为缺陷。','表达建议')
    new('N100','03868','advisory','a few different options','各种各样的可能性','几种不同可能性可概括为各种可能性。','没有确切计量或场景数量约束，不把各种各样强解为数量很多。')
    new('N101','03868','advisory','It considered','他会综合考虑','中文会可描述人物一贯的考虑方式。','英文过去式不要求中文另设已完成标志；完整人物回顾允许此表达。')
    # Apply the same split to both source B2 and verifier B3, including refuted
    # side assertions attached to an otherwise supported compound claim.
    for o in observations:
        if o['stage']=='B2' and o['id'] in ['C33','C63']:o['id']+='.1'
    table('B2','''C33.2|c|N100
C33.3|c|N101
C63.2|c|N99''')
    # Previously unnumbered B2 observations, now given stable host U identifiers.
    # These were all advisory in the original B2 text, not newly confirmed findings.
    table('B2','''U20|a|N89
U21|a|
U22|a|
U23|a|
U24|a|
U25|a|
U26|a|N90
U27|a|
U28|a|
U29|a|N91
U30|a|N92
U31|a|
U32|a|N88
U33|a|
U34|a|
U35|a|
U36|a|
U37|a|
U38|a|N93
U39|a|
U40|a|
U41|a|
U42|a|
U43|a|''')
    # K records are deduplicated conclusions; their incoming P/B2 mappings are
    # recorded separately and never scored a second time.
    table('B3','''K01.1|c|H02
K01.2|c|N76
K02|c|N01
K03|a|
K04|c|N02
K05|c|H04
K06|c|H06
K07.1|c|H08
K07.2|c|N12
K07.3|c|N11
K08|a|N03
K09|c|H07
K10|c|H09
K11|c|N17
K12|c|N09
K13.1|c|N10
K13.2|c|
K14|a|N45
K15|c|H13
K16.1|c|H10
K16.2|c|N46
K17|a|N87
K18.1|c|H11
K18.2|c|N14
K19|a|N47
K20.1|c|N13
K20.2|c|N48
K21|a|N49
K22|c|H15
K23|c|H21
K24|c|N51
K25.1|c|H27
K25.2|c|
K26|c|H20
K27|c|N15
K28|c|N19
K29.1|c|N52
K29.2|c|N53
K30|c|H23
K31.1|c|N20
K31.2|c|N21
K32|c|H24
K33|p|N04
K34|c|N50
K35|c|N05
K36|c|N22
K37.1|c|H28
K37.2|c|N100
K37.3|c|N101
K38|c|N24
K39.1|c|H30
K39.2|c|N54
K40.1|c|H29
K40.2|c|N55
K41|c|N56
K42|c|N57
K43|c|N23
K44|c|H32
K45|c|N58
K46|c|H34
K47.1|c|N59
K47.2|c|N28
K48.1|c|N60
K48.2|c|N27
K49.1|c|N29
K49.2|c|N61
K50.1|c|N62
K50.2|c|N63
K51.1|c|N25
K51.2|c|N26
K52|a|N33
K53|c|H33
K54|a|
K55|p|
K56|c|H36
K57.1|c|H37
K57.2|c|N64
K58|c|N65
K59|c|N66
K60|c|N67
K61.1|c|H38
K61.2|c|H39
K62|a|N06
K63|a|
K64|a|
K65.1|c|H40
K65.2|c|N68
K66.1|c|N35
K66.2|c|N99
K67|a|
K68|c|N69
K69.1|a|N70
K69.2|a|N36
K70|a|
K71|a|N71
K72|a|N86
K73|a|N85
K74|c|H42
K75|c|H43
K76.1|c|N39
K76.2|c|N72
K77|c|N40
K78|a|N42
K79.1|c|N73
K79.2|a|N73
K80|a|
K81.1|c|N43
K81.2|c|N74
K82|c|N44
K83|c|N75
U01|c|N89
U02|a|
U03|p|N77
U04|a|
U05|a|
U06|c|H17
U07|c|N78
U08|a|N79
U09|p|
U10|a|N80
U11|a|
U12|c|N90
U13|p|N81
U14|c|H26
U15|a|
U16|a|
U17.1|c|N91
U17.2|c|H22
U17.3|c|N92
U18|a|
U19|c|N88
U20|c|N16
U21|c|H25
U22|a|
U23|a|
U24|a|
U25|a|
U26|c|N31
U27|c|N82
U28|c|N30
U29|a|N32
U30|a|
U31|a|N83
U32|a|N84
U33|c|N93
U34|a|
U35|a|
U36|a|
U37|a|
U38|a|
NEW01|c|H01
NEW02|c|N94
NEW03|c|N95
NEW04|c|N96
NEW05|a|H19
NEW06|c|N97
NEW07|c|N98''')
    for o in observations:
        if o['stage']!='B3':continue
        if o['id']=='K13.2':o.update(host_decision='refuted',false_cluster='F-B2-C09.2',reason='同B2:C09.2，完整本性语境允许该转述，非独立缺陷。')
        if o['id']=='K25.2':o.update(host_decision='refuted',false_cluster='F-B2-C23.2',reason='同B2:C23.2，全文已说明两位法师举行仪式。')
        if o['id'] in ['K55','U09']:
            o.update(host_decision='pending',reason='报告状态混用时保留其明确的证据缺口，不计确认发现。')
        if o['id']=='K11':o['reason']='映射表K11部分写advisory，去重表及B2:C24明确confirmed；按最终去重结论计，并披露内部不一致。'
