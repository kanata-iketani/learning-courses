# lesson02 ch03: 辞書・リストを return すれば JSON になる
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 辞書 → JSON オブジェクト。True は JSON の true に変換される
@app.get("/shop")
def shop():
    return {"name": "demo堂", "open": True}

# リスト (中に辞書) → JSON 配列。一覧 API の定番の形
@app.get("/users")
def list_users():
    return [{"name": "sato"}, {"name": "suzuki"}]

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/shop").json())
print(client.get("/users").json())
