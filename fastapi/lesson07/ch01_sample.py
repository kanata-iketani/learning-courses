# lesson07 ch01: response_model でレスポンスの形を宣言する
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

# response_model に指定した形にレスポンスが整えられる
@app.get("/items/1", response_model=Item)
def get_item():
    # secret は Item にないキーなので、レスポンスからは消える
    return {"name": "apple", "price": 120, "secret": "仕入れ値は 60 円"}

# --- 動作確認 ---
client = TestClient(app)
r = client.get("/items/1")
print(r.status_code)
print(r.json())
