from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

users = {1: "佐藤", 2: "鈴木"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    # 先にエラーを raise して抜けると、以降は「見つかった場合」だけ書けばよい
    if user_id not in users:
        # raise なので return と違い、ここで処理が完全に止まる
        raise HTTPException(status_code=404)
    return {"name": users[user_id]}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for user_id in [2, 5]:
    r = client.get(f"/users/{user_id}")
    print(r.status_code)
    print(r.json())
