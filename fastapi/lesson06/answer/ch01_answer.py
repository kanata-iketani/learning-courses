from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# age: int と宣言するだけで「整数にできない値は 422」になります。
# 検証コードを自分で書く必要はありません。
class Member(BaseModel):
    name: str
    age: int

# フィールドが欠けたリクエストも、モデルの宣言と合わないので 422 になります。
@app.post("/members")
def create_member(member: Member):
    return member

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/members", json={"name": "demo", "age": 13})
print(r.status_code)
print(r.json())
r2 = client.post("/members", json={"name": "demo", "age": "abc"})
print(r2.status_code)
r3 = client.post("/members", json={"name": "demo"})
print(r3.status_code)
