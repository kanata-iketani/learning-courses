# lesson07 ch03: 作成の成功は 201 で伝える
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

# 既定では成功はすべて 200
@app.post("/items")
def create_item(item: Item):
    return item

# status_code=201 で「作成した」ことを表せる
@app.post("/items2", status_code=201)
def create_item2(item: Item):
    return item

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/items", json={"name": "apple"})
print(r.status_code)
r2 = client.post("/items2", json={"name": "apple"})
print(r2.status_code)
