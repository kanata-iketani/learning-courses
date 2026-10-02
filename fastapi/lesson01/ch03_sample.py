# lesson01 ch03: 演習の定型 (アプリ定義 → TestClient → print)
from fastapi import FastAPI
from fastapi.testclient import TestClient

# 1. アプリを定義する
app = FastAPI()

@app.get("/")
def read_root():
    return {"lesson": 1, "chapter": 3}

# 2. テスト用クライアントを作る (サーバの起動は不要)
client = TestClient(app)

# 3. リクエストを送り、結果を print する
r = client.get("/")
print(r.status_code)
print(r.json())
