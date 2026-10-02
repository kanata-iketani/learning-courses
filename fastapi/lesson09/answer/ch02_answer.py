from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

users = {1: "佐藤", 2: "鈴木"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in users:
        # f-string で ID を埋め込むと「どの ID がなかったか」まで伝わる
        # detail の値はレスポンスの {"detail": ...} にそのまま入る
        raise HTTPException(status_code=404, detail=f"user {user_id} は存在しません")
    return {"name": users[user_id]}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for user_id in [1, 7]:
    r = client.get(f"/users/{user_id}")
    print(r.status_code)
    print(r.json())
