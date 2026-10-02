from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 定義したパスは 200 で返り、content-type は自動で application/json になります。
# 定義していないパスは、自分で書かなくても FastAPI が 404 を返してくれます。
@app.get("/ping")
def ping():
    return {"ping": "pong"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/ping")
print(r.status_code)
print(r.headers["content-type"])
print(r.json())
r = client.get("/nothing")
print(r.status_code)
print(r.json())
