# lesson09 ch03: 「見つからなければ404、あれば200」の定番パターン
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

books = {
    1: {"title": "Python入門", "price": 2500},
    2: {"title": "FastAPI入門", "price": 2800},
}

@app.get("/books/{book_id}")
def read_book(book_id: int):
    # ガード節: 異常系を先に片付ける
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]

@app.get("/books/{book_id}/price")
def read_price(book_id: int):
    # 別のエンドポイントでも冒頭は同じ 2 行
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return {"price": books[book_id]["price"]}

client = TestClient(app)
for path in ["/books/1", "/books/2/price", "/books/9"]:
    r = client.get(path)
    print(r.status_code)
    print(r.json())
