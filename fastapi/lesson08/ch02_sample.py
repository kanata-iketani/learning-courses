# lesson08 ch02: ID を指定して 1 件取り出す (Read)
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

books = [
    {"id": 1, "title": "Python入門", "price": 2000},
    {"id": 2, "title": "FastAPI入門", "price": 2500},
]

@app.get("/books/{book_id}")
def get_book(book_id: int):
    # for 文で探し、id が一致したものを返す
    for book in books:
        if book["id"] == book_id:
            return book
    # 最後まで見つからなかったとき (本格的なエラーは lesson09 で)
    return {"error": "not found"}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/books/2").json())
print(client.get("/books/99").json())
