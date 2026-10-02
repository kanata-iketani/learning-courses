# lesson06 ch03: Query でクエリパラメータを検証する
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

# q は「2 文字以上 10 文字以内」の文字列だけ受け付ける
@app.get("/search")
def search(q: str = Query(min_length=2, max_length=10)):
    return {"q": q}

# --- 動作確認 ---
client = TestClient(app)
r = client.get("/search?q=apple")
print(r.status_code)
print(r.json())
r2 = client.get("/search?q=a")
print(r2.status_code)  # min_length=2 に違反 → 422
