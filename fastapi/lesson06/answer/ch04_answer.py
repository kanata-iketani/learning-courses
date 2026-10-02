from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

app = FastAPI()

# ge=1, le=100 で「1 以上 100 以下」だけを受け付けます。
# 範囲外の 0 や 999 は、関数が呼ばれる前に 422 で弾かれます。
@app.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1, le=100)):
    return {"item_id": item_id}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/items/50")
print(r.status_code)
print(r.json())
r2 = client.get("/items/0")
print(r2.status_code)
r3 = client.get("/items/999")
print(r3.status_code)
