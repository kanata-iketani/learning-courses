# lesson11 ch01: APIRouter でエンドポイントをまとめる
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

# 本来は items.py など別ファイルに書く部分
router = APIRouter()

items = {1: "ペン", 2: "ノート"}

@router.get("/items")
def list_items():
    return list(items.values())

@router.get("/items/{item_id}")
def read_item(item_id: int):
    return {"name": items[item_id]}

# 本来は main.py に書く部分: router を app に合体させる
app = FastAPI()
app.include_router(router)

client = TestClient(app)
r = client.get("/items")
print(r.status_code)
print(r.json())
r = client.get("/items/1")
print(r.json())
