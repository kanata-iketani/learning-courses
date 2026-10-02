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
    return list(books.values())

@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]

# status_code=201: 「作成成功」は 200 ではなく 201 Created で返す
@app.post("/books", status_code=201)
def create_book(book: Book):
    books[book.id] = book
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    # 更新は「対象が存在すること」が前提なので、まずガード節で 404
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    books[book_id] = book
    return book

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/books", json={"id": 3, "title": "Docker入門", "price": 3200})
print(r.status_code)
print(r.json())
r = client.get("/books/3")
print(r.status_code)
print(r.json())
r = client.put("/books/1", json={"id": 1, "title": "Go入門", "price": 2700})
print(r.status_code)
print(r.json())
r = client.put("/books/9", json={"id": 9, "title": "幻の本", "price": 100})
print(r.status_code)
print(r.json())
