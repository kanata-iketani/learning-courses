from fastapi import FastAPI
from fastapi.testclient import TestClient

# app = FastAPI() が土台。すべてのエンドポイントはこの app に登録していきます。
app = FastAPI()

# @app.get("/") で「GET / → この関数」というエンドポイントが1つできます。
@app.get("/")
def read_root():
    return {"message": "Hello, API"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/")
print(r.status_code)
print(r.json())
