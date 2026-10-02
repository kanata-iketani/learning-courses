# lesson05 ch04: model_dump でモデルを辞書にする
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

@app.post("/items")
def create_item(item: Item):
    data = item.model_dump()  # モデル → 辞書
    data["id"] = 1            # 辞書にすればキーを追加できる
    return data

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/items", json={"name": "apple", "price": 120})
print(r.status_code)
print(r.json())
