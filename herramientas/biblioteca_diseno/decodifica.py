import json,glob,base64,pathlib,os
TR='/root/.claude/projects/-home-user-edificio-de-control/a0fab205-7478-5c8e-9d58-24aacc1f812e/tool-results'
out=pathlib.Path('/tmp/claude-0/-home-user-edificio-de-control/a0fab205-7478-5c8e-9d58-24aacc1f812e/scratchpad/fotos')
n=0
for f in glob.glob(TR+'/mcp-Google_Drive-download_file_content-*.txt'):
    try: d=json.load(open(f))
    except Exception as e: print('no json',f,e); continue
    i=d.get('id'); c=d.get('content')
    if not i or not c: continue
    p=out/f'{i}.jpg'
    if p.exists(): continue
    raw=base64.b64decode(c); p.write_bytes(raw); n+=1
    os.remove(f)
print('decodificadas',n); 
