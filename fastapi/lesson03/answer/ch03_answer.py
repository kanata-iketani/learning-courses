from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# パスは定義順に照合されるため、固定パス /users/me を先に書きます。
# 逆順だと "me" が user_id: int に渡って変換に失敗し、422 になります。
@app.get("/users/me")
def read_me():
    return {"user": "current"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/users/me").json())
print(client.get("/users/10").json())
