from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# str | None = None で「省略されたら None」の任意パラメータになります。
# bool 型は URL の "true" / "1" などを Python の True に自動変換してくれます。
@app.get("/items")
def read_items(q: str | None = None, in_stock: bool = False):
    return {"q": q, "in_stock": in_stock}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/items").json())
print(client.get("/items?q=pen&in_stock=true").json())
