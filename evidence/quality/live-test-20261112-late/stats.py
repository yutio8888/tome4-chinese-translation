# Read-only per-tester stats: cumulative image base64 bytes, image count, tool calls, max line.
import json,glob,os,sys
PI='/home/paseo/.pi/agent/sessions/--workspace-tome4-chinese-translation--/'
CL='/home/paseo/.claude/projects/-workspace-tome4-chinese-translation/'
PI_IDS={'d6b2':'01a1d086-2c25-74d0-908c-0e4b6b83cb48','d6a2':'01a1d07c-0e1b-70e1-b374-6d20c115b6de','d6a':'01a1d063-050d-7335-97da-fc78f92cd526','d6b':'01a1d063-113a-734a-86e0-2f318a530a0c'}
def claude_file(name):
    for f in sorted(glob.glob(CL+'*.jsonl'), key=os.path.getmtime, reverse=True)[:40]:
        with open(f,'rb') as h:
            head=h.read(4000)
        if f'run-20261112-late/{name}.md'.encode() in head: return f
def stats(f):
    imgs=ib=tools=maxl=0
    for line in open(f,'rb'):
        maxl=max(maxl,len(line))
        try: r=json.loads(line)
        except Exception: continue
        st=[r]
        while st:
            x=st.pop()
            if isinstance(x,dict):
                t=x.get('type')
                if t=='image':
                    imgs+=1; ib+=len(x.get('data','') or (x.get('source') or {}).get('data','') or '')
                if t in ('toolCall','tool_use'): tools+=1
                st+=list(x.values())
            elif isinstance(x,list): st+=x
    return imgs,ib,tools,maxl
for name in ['o6a','d6a','o6b','d6b','o6b2','o6b3','o6a2','o6b4','d6a2','o6b5','d6b2']:
    f = glob.glob(PI+'*'+PI_IDS[name]+'*.jsonl') if name in PI_IDS else [claude_file(name)]
    f=[x for x in f if x]
    if not f: print(name,'no-session-file'); continue
    i,b,t,m=stats(f[0])
    print(f"{name} images={i} image_b64_MB={b/1e6:.1f} toolCalls={t} max_line_MB={m/1e6:.2f} file={os.path.basename(f[0])[:48]}")
