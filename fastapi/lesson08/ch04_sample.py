# lesson08 ch04: PUT で更新する (Update)
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "Python入門", "price": 2000},
    {"id": 2, "title": "FastAPI入門", "price": 2500},
]

class BookIn(BaseModel):
    title: str
    price: int

# 更新には PUT を使う
@app.put("/books/{book_id}")
def update_book(book_id: int, new: BookIn):
    for book in books:
        if book["id"] == book_id:
            book.update(new.model_dump())  # 新しい値で上書き
            return book
    return {"error": "not found"}

# --- 動作確認 ---
client = TestClient(app)
r = client.put("/books/1", json={"title": "Python入門 改訂版", "price": 2200})
print(r.status_code)
print(r.json())
print(client.put("/books/99", json={"title": "x", "price": 1}).json())
