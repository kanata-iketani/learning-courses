# lesson08 ch05: DELETE で削除する (Delete)
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

books = [
    {"id": 1, "title": "Python入門", "price": 2000},
    {"id": 2, "title": "FastAPI入門", "price": 2500},
]

@app.get("/books")
def list_books():
    return books

# 削除に成功したら 204 (中身なし) を返す
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)  # 見つかった位置の要素を取り除く
            return

# --- 動作確認 ---
client = TestClient(app)
print(client.delete("/books/1").status_code)  # 204
print(client.get("/books").json())            # 1 冊だけ残る
