# lesson09 ch01: HTTPException で 404 を返す
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

items = {1: "りんご", 2: "みかん"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        # raise した時点で処理が止まり、404 レスポンスに変換される
        raise HTTPException(status_code=404)
    return {"name": items[item_id]}

client = TestClient(app)

# 存在する ID → 200
r = client.get("/items/1")
print(r.status_code)
print(r.json())

# 存在しない ID → 404 (detail は既定の "Not Found")
r = client.get("/items/99")
print(r.status_code)
print(r.json())
