# lesson08 ch01: 一覧を返す GET (Read)
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# データベースの代わりのリスト (実行のたびにこの初期状態から始まる)
books = [
    {"id": 1, "title": "Python入門", "price": 2000},
    {"id": 2, "title": "FastAPI入門", "price": 2500},
]

# リストを返すと、そのまま JSON の配列になる
@app.get("/books")
def list_books():
    return books

# --- 動作確認 ---
client = TestClient(app)
r = client.get("/books")
print(r.status_code)
print(r.json())
