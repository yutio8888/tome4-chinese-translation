第396批：冻结11条（主游戏 1 条、Orcs 8 条、Ashes 1 条、Cults 1 条；为修复窗口65迁移 e437cb51 排入的 successor），逐条核验11/11：主游戏、引擎与启动按 manifest 固定 commit 624a673 核验，DLC 按本批公开源码文件SHA核验、来源仓库和commit未固定。surface 4组（gpt-6.1-sol）7 个 child：主游戏 1（full）、Ashes 1（full）、Cults 1（full）、Orcs 2×4，10 OK、1 ISSUE；各 child 只读自身 envelope 与契约。contextual 一个 run（Opus 5.5）1 条 deep，首轮通过：1 OK、0 ISSUE。全部 child 已确认归档，原生读取边界已逐条核对。

宿主裁决1个观察：{'refuted': 1}；预计11条完成、0条待修复。无新增修复。驳回 1：4209c5bc6f 雷鸣榴弹“震慑强度受蒸汽强度加成”，源码以蒸汽强度作施加震慑的 apply_power，与同树致盲粉、痒痒粉同族译法一致，contextual 判 OK。宿主补充建议 1：20f6aff19f 爆矢枪空行缺行尾 \t\t，按门禁 11 先例只记 advisory。修复窗口66积压为0，未达20。
