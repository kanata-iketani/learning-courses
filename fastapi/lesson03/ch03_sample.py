# lesson03 ch03: 固定パスは可変パスより先に定義する
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 固定パス /users/me を先に書く (後だと {user_id} に "me" が拾われて 422 になる)
@app.get("/users/me")
def read_me():
    return {"user": "me"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

# パスパラメータは複数置ける
@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/users/me").json())
print(client.get("/users/7").json())
print(client.get("/users/7/items/3").json())
