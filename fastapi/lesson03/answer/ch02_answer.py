from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# item_id: int と書くだけで、URL の文字列 "5" が数値 5 に変換されて渡ります。
# 変換できない "apple" は、関数が呼ばれる前に FastAPI が 422 で弾いてくれます。
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "price": item_id * 100}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/items/5")
print(r.status_code)
print(r.json())
r = client.get("/items/apple")
print(r.status_code)
