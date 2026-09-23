# 本轮外部参考

查阅日期：2026-09-23。外部资料只用于实验设计和价格说明，不进入译文审核子代理的证据。

- [Google提示词设计指导](https://ai.google.dev/gemini-api/docs/prompting-strategies?authuser=14)：采用清晰任务、具体边界、正反例和必要上下文作为待测变量。这些建议并不证明在本仓库有效，必须用留出结果验证。
- [Gemini 3.8 Flash型号说明](https://ai.google.dev/gemini-api/docs/latest-model)：型号页提供low/medium/high思考配置。本轮固定已有profile要求的high，避免同时改变思考强度造成混杂。
- [Google Gemini API价格](https://ai.google.dev/gemini-api/docs/pricing)：当前3.8 Flash标准API介绍价为每百万输入$0.75、输出（含思考）$3.75，至2026-12-31。当前CPA路由不等于直接Google API，不能把这个价当实际账单，也不能拿未报告费用当零成本。
