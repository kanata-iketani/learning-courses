# lesson08 ch03: POST で追加する (Create)
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "Python入門", "price": 2000},
    {"id": 2, "title": "FastAPI入門", "price": 2500},
]

# 入力には id を含めない (id はサーバ側で採番する)
class BookIn(BaseModel):
    title: str
    price: int

@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_book = book.model_dump()     # モデル → 辞書
    new_book["id"] = len(books) + 1  # 新しい ID を採番
    books.append(new_book)
    return new_book

# --- 動作確認 ---
client = TestClient(app)
r = client.post("/books", json={"title": "Web API設計", "price": 3000})
print(r.status_code)
print(r.json())
print(books)  # リストに追加されている
