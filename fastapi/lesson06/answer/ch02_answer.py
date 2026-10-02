from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# ge=0 は「0 以上」。在庫は 0 個ならあり得るので gt=0 ではなく ge=0 にします。
# max_length=5 で 6 文字以上の名前は 422 になります。
class Product(BaseModel):
    name: str = Field(max_length=5)
    stock: int = Field(ge=0)

@app.post("/products")
def create_product(product: Product):
    return product

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/products", json={"name": "pen", "stock": 0})
print(r.status_code)
print(r.json())
r2 = client.post("/products", json={"name": "pen", "stock": -1})
print(r2.status_code)
r3 = client.post("/products", json={"name": "ボールペンセット", "stock": 3})
print(r3.status_code)
