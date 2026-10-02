# lesson12 ch01: Book モデルと一覧/個別 GET (土台)
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    price: int

app = FastAPI()

# メモリ上のデータ置き場。キーは Book の id
books = {
    1: Book(id=1, title="Python入門", price=2500),
    2: Book(id=2, title="FastAPI入門", price=2800),
}

@app.get("/books")
def list_books():
    return list(books.values())

@app.get("/books/{book_id}")
def read_book(book_id: int):
    # lesson09 のガード節: なければ 404、あれば正常系
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]

client = TestClient(app)
for path in ["/books", "/books/1", "/books/99"]:
    r = client.get(path)
    print(r.status_code)
    print(r.json())
