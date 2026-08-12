# Pi 审核并发 worker 调优测试记录

> 历史适用范围：本页数据来自旧 `tome4-review-v1`、固定 50 条、flat findings
> 输出，只能说明当时 provider 的并发吞吐。translation semantic v2 改为字符预算、
> 逐 item 回执和不同输出契约；在重新测量前，不得用本页推导 v2 的分包质量、成本或
> 全量审核 bundle 数。worker=6 也只是在同 provider/账号下的历史起点。

> 测试时间：2026-08-04；provider=opencode-go / model=deepseek-v4-flash
> 测试集：8 个 tome bundle（每 50 条，内容多样），`--force` 强制重跑绕过缓存
> 工具：`tools/pi-review-batch.py`（v0.2，含 `--force` 透传）

## 测试矩阵

| workers | 墙钟 | 有效吞吐 | 相对串行加速 |
|---|---|---|---|
| 1（串行基线） | 20m30s | 154 s/bundle | 1.0× |
| 3 | 6m11s | 46 s/bundle | 3.3× |
| 4 | 5m12s | 39 s/bundle | 3.9× |
| **6** | **4m50s** | **36 s/bundle** | **4.2×** |
| 8 | 7m39s | 57 s/bundle | 2.7×（劣化） |

## 结论

1. **旧 v1 样本的最优 worker 数 = 6**（本 provider）：墙钟 20.5min → 4.8min，约 4.2 倍加速；有效吞吐 154 → 36 s/bundle；这不是 v2 默认值。
2. **旧 v1 样本中 workers=8 明显劣化**（7.6min）：当时的 provider API 并发上限约 5–6，超出后触发排队/限速；不得据此外推当前 v2。
3. 1→3 是旧 v1 最大收益段（3.3×），3→6 仍有 22% 增量；历史上曾建议该 provider 的 v1 从 3 调整为 **6**。当前 CLI 默认值和 v2 显式选择以工具帮助为准。
4. 若更换 provider/账号，应重跑本矩阵校准（单次约 45 分钟）。
5. 复审场景（缓存命中）不受 worker 数影响——内容 hash 复用是更大的时间杠杆。

## 复现

```bash
# 准备 8-bundle 测试 index（内容见 .artifacts/i18n/worker-test/）
python3 -B tools/pi-review-batch.py --index .artifacts/i18n/worker-test/index.json --workers N --retries 1 --force
```
