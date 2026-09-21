1. 核对checkpoint refs与三条envelope。
2. SCOPE preflight后准备并派发fresh full REVIEWER。
3. 通知后核验只读边界、原生日志、严格schema及来源，确认归档。
4. 发布DONE_VERIFIED，将有效raw交批次消费者；由宿主裁决，不在此修改译文。
