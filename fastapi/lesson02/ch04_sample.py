# lesson02 ch04: レスポンスの中身を調べる
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

# --- 動作確認 ---
client = TestClient(app)

# 定義済みのパス: 200 (成功)
r = client.get("/")
print(r.status_code)
print(r.headers["content-type"])  # 本文の形式は JSON
print(r.json())

# 定義していないパス: 404 (見つからない) が自動で返る
r = client.get("/nothing")
print(r.status_code)
print(r.json())
