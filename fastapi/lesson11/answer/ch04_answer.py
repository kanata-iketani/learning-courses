from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/double/{n}")
def double(n: int):
    # await を使わないふつうの処理は def でよい
    # (FastAPI が別スレッドで実行するので遅くても全体は止まらない)
    return {"result": n * 2}

@app.get("/triple/{n}")
async def triple(n: int):
    # async def でも await なしで書ける。どちらもレスポンスの形は同じ
    return {"result": n * 3}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/double/5")
print(r.status_code)
print(r.json())
r = client.get("/triple/5")
print(r.status_code)
print(r.json())
