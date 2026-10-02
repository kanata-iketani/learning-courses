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

@app.post("/books", status_code=201)
def create_book(book: Book):
    books[book.id] = book
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    books[book_id] = book
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    # 削除も GET/PUT と同じガード節で始める(CRUD 全部で同じ形)
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    # del で辞書から消し、何を消したか分かるレスポンスを返す
    del books[book_id]
    return {"deleted": book_id}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/books", json={"id": 3, "title": "Docker入門", "price": 3200})
print(r.status_code, r.json())
r = client.put("/books/3", json={"id": 3, "title": "Docker入門", "price": 2980})
print(r.status_code, r.json())
r = client.delete("/books/3")
print(r.status_code, r.json())
r = client.get("/books/3")
print(r.status_code, r.json())
r = client.delete("/books/9")
print(r.status_code, r.json())
r = client.get("/books")
print(r.status_code, r.json())
