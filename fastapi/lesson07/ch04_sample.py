# lesson07 ch04: 200 / 201 / 204 / 404 の使い分け
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 200: 取得の成功 (既定)
@app.get("/items")
def list_items():
    return []

# 201: 新しく作成した
@app.post("/items", status_code=201)
def create_item():
    return {"created": True}

# 204: 成功したが返す中身がない (削除でよく使う)
@app.delete("/items/1", status_code=204)
def delete_item():
    return None

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/items").status_code)       # 200
print(client.post("/items").status_code)      # 201
print(client.delete("/items/1").status_code)  # 204
print(client.get("/nothing").status_code)     # 404: URL が存在しない
