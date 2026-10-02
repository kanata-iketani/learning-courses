# lesson01 ch02: 最小の FastAPI アプリと動作確認
from fastapi import FastAPI
from fastapi.testclient import TestClient

# FastAPI() で作ったこの app が、uvicorn main:app で起動するときの「app」
app = FastAPI()

# 「GET / に来たリクエストをこの関数で処理する」という登録
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

# --- 動作確認: サーバを起動せずに TestClient で呼び出す ---
client = TestClient(app)
r = client.get("/")
print(r.status_code)  # 200 なら成功
print(r.json())       # レスポンスの JSON を辞書として取得
