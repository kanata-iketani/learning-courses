# 使い方: python3 check_code_grading.py <port> <講座dir> <lesson>...
# アプリの採点 API に模範解答(合格すべき)と雛形(不合格になるべき)を出して確かめる
import json,glob,sys,urllib.request
port,course=sys.argv[1],sys.argv[2]
for L in map(int,sys.argv[3:]):
  for f in sorted(glob.glob(f'{course}/lesson{L:02d}/ch*.json')):
    c=json.load(open(f))
    for i,q in enumerate(c['quiz']):
      if q.get('kind')!='code': continue
      res=[]
      for draft in (q['answer'],q['setup']):
        body=json.dumps({"lesson":L,"chapter":c['chapter'],"q":i,"draft":draft}).encode()
        r=json.load(urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{port}/api/quiz/grade',body,{'Content-Type':'application/json'}),timeout=120))
        res.append(r.get('pass'))
      print(L,c['chapter'],i,q.get('lang'),'OK' if res==[True,False] else f'NG {res}')
