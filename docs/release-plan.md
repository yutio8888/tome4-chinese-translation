# 对外公布方案（release plan）

> 状态：规范/工具链仓库的 `develop` 已通过面向 `master` 的
> [PR #1](https://github.com/yutio8888/tome4-chinese-translation/pull/1)
> 以 merge commit `232960a` 完成公开整合。运行键修复随后同步至发布仓库
> **https://github.com/yutio8888/tome4-chn-mod**（public，master @ `439d134`，
> addon 0.2.5，含 README）。各 PR 页面是对应合并状态的权威记录。

## 一、发布内容

| 仓库 | 内容 | 当前 HEAD |
|---|---|---|
| `tome-chn-mod`（汉化插件） | 核心 tome 译文 3,348 + DLC 译文 5,426 + nullpack 464（独立文件）+ hooks/superload/overload + GPL v3 声明 | `439d134`（addon_version 0.2.5） |
| `tome4-chinese-translation`（规范/工具链） | 规范译文 30,177 条 + 工具链 + 门禁 | PR #1 merge `232960a`；后续维护从该 merge commit 续接 |

## 二、公布选项

### 选项 A：Git 仓库推送

addon 仓库已经发布；规范/工具链仓库保留 `develop` 远端跟踪：

```bash
cd ~/projects/tome4-chinese-translation
git push -u origin develop
```

PR #1 已以 `master` 为 base、`develop` 为 head 合并。后续维护轮次继续先把
`develop` fast-forward 到最新 `master`，再通过新 PR 以 merge commit 合并；不得
强制推送、rebase、squash 或改写现有分支历史。根目录
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

- [x] `tools/ci-gates.sh` 全绿（doctor、strict lint、403 项 toolchain 测试、201 项 quality/Facts 测试、运行键扫描、术语审计、构建）
- [x] quality/Facts 子系统 201 项测试通过并纳入统一门禁
- [x] `tools/smoke_release.py` 16 项全 PASS（加载链 + 一致性）
- [x] 确定性发布（8,774 条，SHA-256 可复现 `f9e04517b827934b…`）
- [x] 许可证（GPL v3 依据 + init.lua 声明 + 上游版权）
- [x] nullpack 独立可加载（locale 头 + hooks 显式加载）
- [x] 发布仓库工作树干净（.DS_Store 已清理）

## 四、发布说明模板

```markdown
# chn-mod v0.2.5 — ToME 1.7.6 汉化补充插件

基于 GPL v3 发布的 ToME4 中文本地化覆盖层：
- 核心 tome 译文 3,348 条（覆盖/新增）
- 官方 DLC 译文：Ashes of Urh'Rok 743 / Cults of Entropy 1,555 / Embers of Rage 3,128 条
- Nullpackreloaded 支持（464 条 + 特殊物品挂钩）
- 安装：放入 game/addons/，勾选 chn-mod；需官方中文 locale 配合
- 许可：GNU GPL v3 or later（见 init.lua 头部）
```

## 五、已确认决策（2026-08-08）

1. PR #1 已以 merge commit `232960a` 合入 `master`；远端 `develop` 保留，并在
   后续维护轮次仅以 fast-forward 对齐 `master`。
2. 运行键修复已发布为 addon 0.2.5（`439d134`）；不制作或上传 teaa，也不创建
   GitHub Release。
3. Facts 研究冻结，不启动新 F 臂/holdout/provider 调用，不制作脱敏复现包；A-core
   原始归档继续只读私有保存，不上传源码仓库。
