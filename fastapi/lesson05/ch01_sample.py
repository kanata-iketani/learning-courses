# lesson05 ch01: BaseModel でデータの形を宣言する
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# 受け取るデータの形: name は文字列、age は整数
class User(BaseModel):
    name: str
    age: int

# 引数の型にモデルを指定すると、リクエストボディとして受け取る
@app.post("/users")
def create_user(user: User):
    return user  # モデルを返すと自動で JSON になる

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/users", json={"name": "demo", "age": 13})
print(r.status_code)
print(r.json())
