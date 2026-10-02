# lesson11 ch02: prefix と tags
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

# prefix: パスの共通接頭辞 / tags: /docs でのグループ名
router = APIRouter(prefix="/items", tags=["items"])

items = {1: "ペン", 2: "ノート"}

@router.get("/")
def list_items():
    # 実際のパスは prefix が付いて /items/ になる
    return list(items.values())

@router.get("/{item_id}")
def read_item(item_id: int):
    # 実際のパスは /items/{item_id}
    return {"name": items[item_id]}

app = FastAPI()
app.include_router(router)

client = TestClient(app)
r = client.get("/items/")
print(r.status_code)
print(r.json())
r = client.get("/items/2")
print(r.json())

# 登録された実際のパスを確認してみる
print(sorted(app.openapi()["paths"].keys()))
