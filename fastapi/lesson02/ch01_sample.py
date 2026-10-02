# lesson02 ch01: 最小のアプリと @app.get("/")
from fastapi import FastAPI
from fastapi.testclient import TestClient

# アプリ本体を作る
app = FastAPI()

# パス "/" への GET を read_root 関数に割り当てる (これがエンドポイント)
@app.get("/")
def read_root():
    return {"message": "Hello"}

# --- 動作確認 ---
client = TestClient(app)
r = client.get("/")
print(r.status_code)
print(r.json())
