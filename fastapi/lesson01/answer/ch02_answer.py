from fastapi import FastAPI
from fastapi.testclient import TestClient

# uvicorn で起動するときも TestClient で試すときも、この app が入り口になります。
app = FastAPI()

# 「GET / はこの関数で処理する」と登録します。辞書を返すと自動で JSON になります。
@app.get("/")
def read_root():
    return {"framework": "FastAPI"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/")
print(r.status_code)
print(r.json())
