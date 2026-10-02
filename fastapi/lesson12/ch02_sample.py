# lesson12 ch02: 追加 (POST 201) と更新 (PUT 404対応)
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    price: int

app = FastAPI()

books = {
    1: Book(id=1, title="Python入門", price=2500),
    2: Book(id=2, title="FastAPI入門", price=2800),
}

@app.post("/books", status_code=201)
def create_book(book: Book):
    # 追加成功は 201 Created で返すのが REST の作法
    books[book.id] = book
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    # 更新対象がなければ 404 (ガード節)
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    books[book_id] = book
    return book

client = TestClient(app)
r = client.post("/books", json={"id": 3, "title": "Web入門", "price": 2200})
print(r.status_code)
print(r.json())
r = client.put("/books/1", json={"id": 1, "title": "Python入門", "price": 1980})
print(r.status_code)
print(r.json())
r = client.put("/books/99", json={"id": 99, "title": "幻の本", "price": 100})
print(r.status_code)
print(r.json())
