from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# BaseModel を継承したクラスが「受け取る JSON の形」の宣言になります。
class Book(BaseModel):
    title: str
    price: int

# 引数の型に Book を指定すると、ボディの JSON が Book に変換されて届きます。
# モデルをそのまま返すと、FastAPI が JSON に変換して返します。
@app.post("/books")
def create_book(book: Book):
    return book

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/books", json={"title": "FastAPI入門", "price": 2500})
print(r.status_code)
print(r.json())
