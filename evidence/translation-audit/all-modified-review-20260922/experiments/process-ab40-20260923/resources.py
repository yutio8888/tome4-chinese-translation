"""Report provider observations without inventing comparable aggregate token counts."""
import json,datetime
from pathlib import Path
P=Path(__file__).resolve().parent
def dt(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def main():
    stages={}
    for st in ['P','A2','B2','B3']:
        start=json.loads((P/f'dispatches/runtime-initial-{st}.json').read_text())['structuredContent']['snapshot']
        end=json.loads((P/f'dispatches/terminal-{st}.json').read_text())['structuredContent']['snapshot']
        archive=json.loads((P/f'dispatches/archived-status-{st}.json').read_text())['structuredContent']['snapshot']
        assert not end['activeTurn'] and archive['archivedAt']
        a=start['activeTurn']['startedAt'];b=end['updatedAt']
        stages[st]={'agent_id':end['id'],'configured_model':end['model'],'runtime_info':end['runtimeInfo'],'thinking':end.get('effectiveThinkingOptionId'),
         'started_at':a,'terminal_updated_at':b,'run_window_seconds':(dt(b)-dt(a)).total_seconds(),'creation_to_start_seconds':(dt(a)-dt(start['createdAt'])).total_seconds(),
         'provider_last_usage_raw':end.get('lastUsage'),'reported_cost_usd':(end.get('lastUsage') or {}).get('totalCostUsd'),'archived_at':archive['archivedAt']}
    secs={k:v['run_window_seconds'] for k,v in stages.items()}
    cost={k:v['reported_cost_usd'] for k,v in stages.items()}
    ca=cost['A2'];cb=cost['B2']+cost['B3'] if cost['B2'] is not None and cost['B3'] is not None else None
    ratio=cb/ca if cb is not None and ca else None
    at=secs['P']+secs['A2'];bt=secs['P']+secs['B2']+secs['B3'];tr=bt/at
    r={'stages':stages,'measurement_limits':['run_window_seconds is active-turn start to terminal updatedAt, including model and tool time; no separate reliable breakdown available','provider lastUsage fields are preserved without assuming identical cross-provider billing semantics','P charged once per counterfactual arm, once in real experiment; common P fee unavailable if provider did not report it','host audit time is common and includes orchestration; not human gold or measured human labor'],
       'A_agent_minutes':at/60,'B_agent_minutes':bt/60,'real_agent_minutes':sum(secs.values())/60,
       'A_secondary_cost_usd':ca,'B_secondary_cost_usd':cb,'secondary_cost_ratio_B_over_A':ratio,'agent_time_ratio_B_over_A':tr,
       'near_resource_criteria':{'cost_0_8_to_1_25':None if ratio is None else 0.8<=ratio<=1.25,'time_at_most_1_25':tr<=1.25},
       'A_observed_critical_window_minutes':(max(dt(stages[s]['terminal_updated_at']) for s in ['P','A2'])-min(dt(stages[s]['started_at']) for s in ['P','A2'])).total_seconds()/60,
       'B_observed_critical_window_minutes':(dt(stages['B3']['terminal_updated_at'])-min(dt(stages[s]['started_at']) for s in ['P','B2'])).total_seconds()/60,
       'B2_to_B3_harvest_archive_dispatch_seconds':(dt(stages['B3']['started_at'])-max(dt(stages[s]['terminal_updated_at']) for s in ['P','B2'])).total_seconds()}
    (P/'RESOURCES.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
