import json
c=json.load(open('cache.json'))
for k,v in c.items():
    if k.startswith('ZohoAnalytics_getExportJobDetails|'):
        ok=[x for x in v if '"1004"' in x]
        c[k]=ok[-1:] if ok else v
json.dump(c,open('cache.json','w'),ensure_ascii=False)
