# 对外公布方案（release plan）

> 状态：addon 发布已完成（2026-08-04）；规范/工具链仓库的 `develop`
> 分支已推送，并通过面向 `master` 的
> [PR #1](https://github.com/yutio8888/tome4-chinese-translation/pull/1)
> 完成公开整合。本轮已授权在本地审核、完整门禁与 release smoke 全部通过后，
> 以 merge commit 合并；PR 页面是最终合并状态的权威记录。发布仓库已推送至
> **https://github.com/yutio8888/tome4-chn-mod**（public，master @ `947e624`，
> addon 0.2.4，含 README）。

## 一、发布内容

| 仓库 | 内容 | 当前 HEAD |
|---|---|---|
| `tome-chn-mod`（汉化插件） | 核心 tome 译文 3,354 + DLC 译文 5,426 + nullpack 464（独立文件）+ hooks/superload/overload + GPL v3 声明 | `947e624`（addon_version 0.2.4） |
| `tome4-chinese-translation`（规范/工具链） | 规范译文 30,177 条 + 工具链 + 门禁 | 远端 `develop`，PR #1；整合起点 `0f9c513` |

## 二、公布选项

### 选项 A：Git 仓库推送

addon 仓库已经发布；规范/工具链仓库已建立 `develop` 远端跟踪：

```bash
cd ~/projects/tome4-chinese-translation
git push -u origin develop
```

PR #1 以 `master` 为 base、`develop` 为 head；只有本地审核、完整门禁和 release
smoke 全部通过，且远端 head 与已审核提交一致时，才转为 ready 并以 merge commit
合并。不得强制推送、rebase、squash 或改写现有分支历史。根目录
`LICENSE`/`COPYING` 与 README 已纳入整合批次；研究原始 artifact 和项目外 A-core
归档不提交到源码仓库。

### 选项 B：teaa 打包发布（te4.org / 创意工坊）
ToME addon 的标准分发格式为 teaa（zip 容器 + 固定结构）。流程：
1. `cd ~/projects/tome-chn-mod && zip -r chn-mod.teaa init.lua data hooks superload overload`
2. 上传 te4.org 或 Steam 创意工坊（需要对应账号与发布授权）
3. 校验：`unzip -l chn-mod.teaa` 确认结构；`tools/smoke_release.py` 已在目录上验证过，teaa 内容相同

### 选项 C：目录安装（玩家自用）
```bash
cp -R ~/projects/tome-chn-mod <游戏目录>/game/addons/chn-mod
```
启动游戏后在 addons 菜单勾选 chn-mod。

## 三、发布前校验清单（已全部完成）

- [x] `tools/ci-gates.sh` 全绿（doctor、strict lint、401 项 toolchain 测试、201 项 quality/Facts 测试、运行键扫描、术语审计、构建）
- [x] quality/Facts 子系统 201 项测试通过并纳入统一门禁
- [x] `tools/smoke_release.py` 16 项全 PASS（加载链 + 一致性）
- [x] 确定性构建（SHA-256 可复现 `1d2d7428…`）
- [x] 许可证（GPL v3 依据 + init.lua 声明 + 上游版权）
- [x] nullpack 独立可加载（locale 头 + hooks 显式加载）
- [x] 发布仓库工作树干净（.DS_Store 已清理）

## 四、发布说明模板

```markdown
# chn-mod v0.2.4 — ToME 1.7.6 汉化补充插件

基于 GPL v3 发布的 ToME4 中文本地化覆盖层：
- 核心 tome 译文 3,354 条（覆盖/新增）
- 官方 DLC 译文：Ashes of Urh'Rok 759 / Cults of Entropy 1,661 / Embers of Rage 3,400 条
- Nullpackreloaded 支持（464 条 + 特殊物品挂钩）
- 安装：放入 game/addons/，勾选 chn-mod；需官方中文 locale 配合
- 许可：GNU GPL v3 or later（见 init.lua 头部）
```

## 五、已确认决策（2026-08-08）

1. `develop` 已推送并创建合入 `master` 的 PR #1；本轮授权在审核和全部门禁通过后
   转为 ready，并使用 merge commit 合并，保留远端 `develop` 分支。
2. 本轮不制作或上传 teaa，addon 0.2.4 保持现状。
3. Facts 研究冻结，不启动新 F 臂/holdout/provider 调用，不制作脱敏复现包；A-core
   原始归档继续只读私有保存，不上传源码仓库。
