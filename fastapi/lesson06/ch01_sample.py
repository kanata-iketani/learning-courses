# lesson06 ch01: 型に合わないデータは 422 になる
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}

# --- 動作確認 ---
client = TestClient(app)
# 正しい形 → 200
r = client.post("/items", json={"name": "apple", "price": 120})
print(r.status_code)
# price が整数にできない → 422
r2 = client.post("/items", json={"name": "apple", "price": "たくさん"})
print(r2.status_code)
# どのフィールドが原因かは detail の loc に入っている
print(r2.json()["detail"][0]["loc"])
