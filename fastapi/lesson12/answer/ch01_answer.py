from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    price: int

app = FastAPI()

books = {
    1: Book(id=1, title="Go入門", price=3000),
    2: Book(id=2, title="SQL入門", price=2600),
}

@app.get("/books")
def list_books():
    # 辞書の値 (Book のリスト) を返すと FastAPI が JSON の配列にしてくれる
    return list(books.values())

@app.get("/books/{book_id}")
def read_book(book_id: int):
    # lesson09 のガード節: 異常系 (404) を先に片付ける
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for path in ["/books", "/books/2", "/books/9"]:
    r = client.get(path)
    print(r.status_code)
    print(r.json())
