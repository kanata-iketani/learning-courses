# lesson09 ch02: detail にエラー内容を入れる
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

items = {1: "りんご", 2: "みかん"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        # detail に「何が・なぜ」を入れると、呼ぶ側が原因を特定できる
        raise HTTPException(status_code=404, detail=f"item {item_id} は見つかりません")
    return {"name": items[item_id]}

client = TestClient(app)

r = client.get("/items/2")
print(r.status_code)
print(r.json())

# detail がそのまま {"detail": ...} で返る
r = client.get("/items/99")
print(r.status_code)
print(r.json())
