# 对外公布方案（release plan）

> 状态：草案，待用户决策后执行。当前两个仓库均无 remote。

## 一、发布内容

| 仓库 | 内容 | 当前 HEAD |
|---|---|---|
| `tome-chn-mod`（汉化插件） | 核心 tome 译文 3,354 + DLC 译文 5,426 + nullpack 464（独立文件）+ hooks/superload/overload + GPL v3 声明 | `9273c35`（addon_version 0.2.4） |
| `tome4-chinese-translation-review-fixes`（规范/工具链） | 规范译文 30,177 条 + 工具链 + 门禁 | 分支 `codex/review-findings-20260802`，领先 origin/master 80+ 提交 |

## 二、公布选项

### 选项 A：Git 仓库推送（推荐）
```bash
# 发布仓库
cd ~/projects/tome-chn-mod
git remote add origin <你的仓库地址>
git push -u origin master

# 规范仓库（可选，公开工具链与规范译文）
cd ~/projects/tome4-chinese-translation-review-fixes
git remote add origin <你的仓库地址>
git push -u origin codex/review-findings-20260802
```
需要：用户提供仓库地址；确认 GPL v3 兼容（两个仓库均需 LICENSE/声明——发布仓库已含 init.lua 声明；规范仓库尚无，发布前应补）。

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

- [x] `tools/ci-gates.sh` 全绿（doctor/lint 0/0/46 测试/collisions 0/keys/审计/diff-check）
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

## 五、决策点（待用户确认）

1. 推送目标仓库地址（选项 A）？
2. 是否需要 teaa 打包（选项 B）？
3. 规范仓库是否一并公开？
