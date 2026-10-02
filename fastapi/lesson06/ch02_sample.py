# lesson06 ch02: Field で値の範囲を検証する
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(max_length=10)  # 10 文字以内
    price: int = Field(gt=0)          # 0 より大きい

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/items", json={"name": "apple", "price": 120})
print(r.status_code)   # 制約を満たす → 200
r2 = client.post("/items", json={"name": "apple", "price": 0})
print(r2.status_code)  # gt=0 に違反 → 422
r3 = client.post("/items", json={"name": "とても長い商品名なので通らない", "price": 120})
print(r3.status_code)  # max_length=10 に違反 → 422
