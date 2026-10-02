from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# async def で定義した関数は await で呼べる(本来は DB 問い合わせなど)
async def fetch_price():
    return 480

@app.get("/price")
async def read_price():
    # await は async def の中でだけ使える
    # 待っている間、FastAPI は他のリクエストを処理できる
    price = await fetch_price()
    return {"price": price}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/price")
print(r.status_code)
print(r.json())
