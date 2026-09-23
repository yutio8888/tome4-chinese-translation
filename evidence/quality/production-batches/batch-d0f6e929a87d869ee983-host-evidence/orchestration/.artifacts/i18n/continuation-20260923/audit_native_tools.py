import json,sys,hashlib,pathlib
# usage: audit_native_tools.py children.json outdir  -> writes NATIVE-TOOLS-<dispatch>.json, prints each call input
children,outdir=sys.argv[1],pathlib.Path(sys.argv[2])
for r in json.load(open(children)):
    sid=r['terminal_capture']['snapshot']['persistence']['sessionId']
    import glob
    L,=glob.glob(f'/home/paseo/.codex/archived_sessions/*{sid}.jsonl')+glob.glob(f'/home/paseo/.codex/sessions/2026/09/23/*{sid}.jsonl')
    calls=[]
    for line in open(L):
        o=json.loads(line)
        p=o.get('payload',{})
        if o.get('type')=='response_item' and p.get('type') in ('custom_tool_call','function_call','local_shell_call'):
            calls.append(p)
    out=outdir/f"NATIVE-TOOLS-{r['dispatch_id']}.json"
    out.write_text(json.dumps(calls,ensure_ascii=False,indent=2)+'\n')
    print('==',r['dispatch_id'],len(calls),hashlib.sha256(out.read_bytes()).hexdigest())
    for c in calls: print('   ',json.dumps(c.get('input',c.get('arguments')),ensure_ascii=False)[:400])
