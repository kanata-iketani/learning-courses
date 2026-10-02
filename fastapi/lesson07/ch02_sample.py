# lesson07 ch02: 入力用と出力用のモデルを分ける
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# 入力用: パスワードを受け取る
class UserIn(BaseModel):
    name: str
    password: str

# 出力用: パスワードを持たない
class UserOut(BaseModel):
    name: str

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    # そのまま返しても、レスポンスは UserOut の形に絞られる
    return user

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/users", json={"name": "demo", "password": "himitsu123"})
print(r.status_code)
print(r.json())  # password は含まれない
