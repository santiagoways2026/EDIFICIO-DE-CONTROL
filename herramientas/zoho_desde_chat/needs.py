import json,glob
seen=set()
for f in sorted(glob.glob('need_*.json')):
    for x in json.load(open(f)):
        if x['k'] in seen: continue
        seen.add(x['k']);print('##',f[5:-5],x['tool']);print(json.dumps(x['args'],ensure_ascii=False))
