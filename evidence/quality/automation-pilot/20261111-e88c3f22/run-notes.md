本次候选初始干净，分支 codex/automation-pilot，HEAD=develop=121ca1c6c4f9037497bab59b68852665c5c407b3；ff-only 返回 Already up to date。领取时无其他活跃 agent，主线只有历史 .adapter.lock。无本试运行遗留；初始账本 release_required_units=29554，A/B=29554，pending_A=0，pending_B_backfill=0。本次40条为混合抽查，不是首次全库审核。

修复混乱苔藓触发条件；固定核心版本624a67329fe2。DLC来源未固定，锚点含实际文件摘要。0480维护修复；0481当前revision双盲审均OK。运行输出仅LuaJIT格式校验，未作实机通过声明；UI字体、裁切与自动换行有validation_gap。

完整门禁两次未通过；第二次16/17通过，Facts测试7项缺pi依赖。保留候选，不整合不推送。所有children均已结束、收取并确认归档。下次优先恢复本候选，解决验证环境后再执行完整门禁；不得新建重复修复或重开advisory。
