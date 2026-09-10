# 对外公布方案（release plan）

> 状态：最近一次获授权的 P3 集成已于 2026-08-20 完成。规范/工具链仓库的
> `develop` 已 push 到 `origin`（`42aae69`）；发布仓库
> [`tome4-chn-mod`](https://github.com/yutio8888/tome4-chn-mod) 已同步并 push
> addon 0.2.7（`9cdbd30`）。`develop → master` PR 与正式 GitHub Release／teaa
> 发布尚未完成，仍需维护者另行决定。
>
> 本文件记录发布状态和可选流程，不授权新的 push、外部仓库修改或正式发布。

## 一、当前发布基线

| 仓库 | 内容 | 已推送基线 |
|---|---|---|
| `tome-chn-mod`（汉化插件） | 主 locale：核心 tome 3,488 + DLC 5,461；另含 nullpack 464（独立文件）、hooks/superload/overload 与 GPL v3 声明 | `9cdbd30`（addon_version 0.2.7） |
| `tome4-chinese-translation`（规范/工具链） | 规范译文 30,308 条 + 工具链 + 门禁 | `develop` @ `42aae69`；后续本地维护不自动获得 push 授权 |

主 locale 共 8,949 条。DLC 分量为 Ashes of Urh'Rok 743、Cults of Entropy 1,569、
Embers of Rage 3,149；Nullpack 的 464 条由独立文件加载，不计入主 locale 总数。

## 二、尚待决定的发布动作

### `develop → master` PR

PR #1 已以 merge commit `232960a` 合入 `master`，PR #2 已以 merge commit `f6b23ed`
完成第二轮整合。最近一次 P3 尝试创建新 PR 时，fine-grained PAT 缺少
`pull_request:write`，维护者选择暂缓。后续可以：

- 手动打开
  [master...develop 比较页](https://github.com/yutio8888/tome4-chinese-translation/compare/master...develop)
  创建 PR；或
- 更新 token 权限后重新运行非交互式 `gh pr create --base master --head develop`。

不得强制推送、rebase、squash 或改写已推送历史。研究原始 artifact 和项目外 A-core
归档不提交到源码仓库。

### teaa／GitHub Release／平台发布

目前没有制作或上传 teaa，也没有创建 GitHub Release、te4.org 或 Steam 创意工坊发布。
若维护者另行授权，标准流程是从已验证的发布仓库目录打包 `init.lua`、`data`、`hooks`、
`superload` 与 `overload`，再用 `unzip -l` 和 `tools/smoke_release.py` 校验内容与加载链。

### 目录安装（玩家自用）

将 `tome4-chn-mod` 仓库内容复制到 `<游戏目录>/game/addons/chn-mod`，启动游戏后在
addons 菜单勾选 `chn-mod`。

## 三、最近一次 P3 验证

- [x] `tools/ci-gates.sh` 全部 12 项通过（doctor、strict lint、单测、运行键扫描、术语审计、构建）
- [x] `tools/smoke_release.py` 16 项全 PASS（加载链 + 一致性）
- [x] 发布仓库同步为主 locale 8,949 条，addon_version 0.2.7
- [x] GPL v3 声明、上游版权与 Nullpack 独立加载链保持有效
- [x] 发布提交 `9cdbd30` 已 push

测试数量会随工具链增长，不在常驻发布文档中固定；以对应门禁日志和退出码为准。

## 四、发布说明模板

```markdown
# chn-mod v0.2.7 — ToME 1.7.6 汉化补充插件

基于 GPL v3 发布的 ToME4 中文本地化覆盖层：
- 核心 tome 译文 3,488 条（覆盖/新增）
- 官方 DLC 译文：Ashes of Urh'Rok 743 / Cults of Entropy 1,569 / Embers of Rage 3,149 条
- Nullpackreloaded 支持（464 条 + 特殊物品挂钩）
- 安装：放入 game/addons/，勾选 chn-mod；需官方中文 locale 配合
- 许可：GNU GPL v3 or later（见 init.lua 头部）
```

## 五、持续有效的决策

1. 已推送分支不得强制改写；后续整合继续通过 `develop → master` PR。
2. addon 0.2.7 的 Git 仓库同步已经完成，但这不等于已创建正式 GitHub Release 或平台发布。
3. 新的 push、发布仓库修改、teaa／平台上传仍需维护者明确指示。
4. Facts 研究保持冻结：不启动新 F 臂、holdout 或 provider campaign，不上传项目外 A-core
   原始归档。
