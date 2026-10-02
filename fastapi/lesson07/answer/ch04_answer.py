from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 取得の成功は既定の 200 のままでよいので、何も指定しません。
@app.get("/ping")
def ping():
    return {"message": "pong"}

# 作成は 201 (Created) で伝えます。
@app.post("/notes", status_code=201)
def create_note():
    return {"created": True}

# 削除は 204 (No Content)。ボディを返さない決まりなので return None にします。
@app.delete("/notes/1", status_code=204)
def delete_note():
    return None

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/ping").status_code)
print(client.post("/notes").status_code)
print(client.delete("/notes/1").status_code)
print(client.get("/nothing").status_code)
