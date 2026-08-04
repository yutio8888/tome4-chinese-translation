# Pi 审核并发 worker 调优测试记录

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

1. **最优 worker 数 = 6**（本 provider）：墙钟 20.5min → 4.8min，约 4.2 倍加速；有效吞吐 154 → 36 s/bundle。
2. **workers=8 明显劣化**（7.6min）：provider API 并发上限约 5–6，超出后触发排队/限速，重试增加反而不划算。
3. 1→3 是最大收益段（3.3×），3→6 仍有 22% 增量；默认 `--workers` 建议从 3 调整为 **6**（本 provider 环境）。
4. 若更换 provider/账号，应重跑本矩阵校准（单次约 45 分钟）。
5. 复审场景（缓存命中）不受 worker 数影响——内容 hash 复用是更大的时间杠杆。

## 复现

```bash
# 准备 8-bundle 测试 index（内容见 .artifacts/i18n/worker-test/）
python3 -B tools/pi-review-batch.py --index .artifacts/i18n/worker-test/index.json --workers N --retries 1 --force
```
