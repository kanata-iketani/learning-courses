# lesson12 ch03: 削除 (DELETE) と通し確認
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

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    # 削除もガード節から。対象がなければ 404
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    del books[book_id]
    return {"deleted": book_id}

@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]

client = TestClient(app)
r = client.delete("/books/1")
print(r.status_code)
print(r.json())
# 削除した本の GET は 404 になる
r = client.get("/books/1")
print(r.status_code)
print(r.json())
r = client.delete("/books/99")
print(r.status_code)
print(r.json())
