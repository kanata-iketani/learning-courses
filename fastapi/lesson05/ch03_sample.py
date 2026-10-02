# lesson05 ch03: モデルの属性を使って計算する
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Order(BaseModel):
    item: str
    price: int
    quantity: int

@app.post("/orders")
def create_order(order: Order):
    # モデルの値は「モデル名.フィールド名」で取り出して計算に使える
    total = order.price * order.quantity
    return {"item": order.item, "total": total}

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/orders", json={"item": "コーヒー", "price": 480, "quantity": 3})
print(r.status_code)
print(r.json())
