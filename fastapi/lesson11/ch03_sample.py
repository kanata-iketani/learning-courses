# lesson11 ch03: async def エンドポイント
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 非同期の部品関数。本来はここで DB や外部 API を await で待つ
async def load_message():
    return "非同期で取得しました"

@app.get("/async")
async def read_async():
    # await は async def の中でだけ使える
    msg = await load_message()
    return {"message": msg}

@app.get("/sync")
def read_sync():
    # 同期版。呼び出す側から見えるレスポンスの形は同じ
    return {"message": "同期で取得しました"}

client = TestClient(app)
for path in ["/async", "/sync"]:
    r = client.get(path)
    print(r.status_code)
    print(r.json())
