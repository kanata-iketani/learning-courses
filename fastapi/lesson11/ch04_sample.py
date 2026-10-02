# lesson11 ch04: def と async def の使い分け
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/double/{n}")
def double(n: int):
    # 同期ライブラリを使う処理・迷ったときは def
    # (FastAPI が別スレッドで動かすので全体は止まらない)
    return {"result": n * 2}

async def calc_triple(n: int):
    return n * 3

@app.get("/triple/{n}")
async def triple(n: int):
    # await を使いたいときだけ async def にする
    result = await calc_triple(n)
    return {"result": result}

# どちらの書き方でも、呼び出す側から見た動きは同じ
client = TestClient(app)
for path in ["/double/4", "/triple/4"]:
    r = client.get(path)
    print(r.status_code)
    print(r.json())
