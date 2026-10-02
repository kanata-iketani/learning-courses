from fastapi import FastAPI
from fastapi.testclient import TestClient

# この3部構成 (アプリ定義 → TestClient → print) が全演習の定型です。
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok"}

# TestClient にアプリを渡すと、サーバを起動せずにリクエストを送れます。
client = TestClient(app)

# r.json() はレスポンスの JSON を Python の辞書に戻して返します。
r = client.get("/")
print(r.status_code)
print(r.json())
