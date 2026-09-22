# 第一轮合并修复

只修复下列主代理确认项，先读SPEC-REV1.md与SCOPE-REV1.json。旧SPEC/冻结候选不要改。

1. R1/HOST-02：契约不能把两个字段误当唯一正文来源；WP2-Lite terminology_snapshot是摘要，实际正文在bounded_context的source_facts_v1.fact.terminology。role/两份契约/总契约/README应一致允许envelope内真实冻结正文；仅哈希不代表可据其打开当前术语库。surface无术语正文时不得仅因此报错。不变更schema或生产输入构造。
2. HOST-01：tools/contextual_lane_manifest.py与tools/surface_screen_result_check.py的PROMPT_TEMPLATE/render_dispatch_prompt仍旧模板。共用review_prompts的canonical模板/渲染，同时保持原公开API与各自ContractError异常类型。检查导入路径兼容直接CLI/测试/不同模块加载方式，避免重复模块导致异常类型漂移。ai_state_check及manifest调用者无需改逻辑。测试须覆盖这两个真实入口以及最长合法路径、超限拒绝、既有manifest/STATE重放兼容。
3. HOST-05：将新test_review_prompts.py登记到tests/i18n/test_groups.json的合适既有组（contract-suite），运行test_groups.py --check。不要登记两次或弱化registry。
4. HOST-04：input_path含CR/LF或其它splitlines()认可的Unicode/控制字符行分隔符时当前builder可生成四行。拒绝全部行分隔符并测试（含\n、\r、\v、\f、\x1c/1d/1e、\x85、\u2028、\u2029），保持普通路径与UTF8字节门禁。
5. HOST-03：授权说明把9月12日源码补查授权与9月22日本次完整契约/术语边界修订分开写，避免历史归因错误。

范围是13个允许文件；tests已有文件可以扩充，不新建其他测试文件。优先运行prompt、surface result/manifest、contextual lane、review lifecycle相关测试；最后完整CI由宿主执行。不得改任务记录、stage/commit、创建agent。报告实际结果。
