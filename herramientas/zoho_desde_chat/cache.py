# Construye cache.json con las llamadas a Zoho Suite hechas en este chat (desde la transcripción)
import json,re,os,sys
F='/root/.claude/projects/-home-user/d31d6c59-019f-5e35-92c4-4a675a8a9318.jsonl'
since=sys.argv[1] if len(sys.argv)>1 else ''
uses={};res={}
for line in open(F):
    try:o=json.loads(line)
    except:continue
    if o.get('timestamp','')<since:continue
    c=o.get('message',{}).get('content')
    if not isinstance(c,list):continue
    for b in c:
        if b.get('type')=='tool_use' and b.get('name','').startswith('mcp__Zoho_Suite__'):
            uses[b['id']]=(b['name'][len('mcp__Zoho_Suite__'):],b['input'])
        elif b.get('type')=='tool_result' and b.get('tool_use_id') in uses or b.get('type')=='tool_result':
            cc=b.get('content');t=cc if isinstance(cc,str) else ''.join(x.get('text','') for x in (cc or []) if isinstance(x,dict))
            res[b.get('tool_use_id')]=(t,b.get('is_error'))
cache={}
for i,(tool,inp) in uses.items():
    if i not in res or res[i][1]:continue
    t=res[i][0]
    m=re.search(r'(/root/\.claude/projects/[^\s"]+tool-results/[^\s"]+?\.txt)',t)
    if m and os.path.exists(m.group(1)) and ('too large' in t.lower() or 'saved' in t.lower()):
        t=open(m.group(1)).read()
        try:
            j=json.loads(t)
            if isinstance(j,list):t=''.join(x.get('text','') for x in j if isinstance(x,dict))
        except:pass
    inp=json.loads(json.dumps(inp))
    qp=inp.get('query_params') or {}
    if isinstance(qp.get('CONFIG'),str):
        try:qp['CONFIG']=json.loads(qp['CONFIG'])
        except:pass
    cache.setdefault(tool+'|'+json.dumps(inp,sort_keys=True,separators=(',',':'),ensure_ascii=False),[]).append(t)
json.dump(cache,open('cache.json','w'),ensure_ascii=False)
print(len(cache),'llamadas en caché')
