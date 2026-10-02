from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

# モデルのままではキーを追加できないので、model_dump() で辞書にします。
# age >= 18 の比較結果 (True / False) をそのまま adult に入れます。
@app.post("/users")
def create_user(user: User):
    data = user.model_dump()
    data["adult"] = user.age >= 18
    return data

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/users", json={"name": "demo", "age": 20})
print(r.status_code)
print(r.json())
r2 = client.post("/users", json={"name": "python", "age": 13})
print(r2.json())
