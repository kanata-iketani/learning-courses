# lesson04 ch03: int 型クエリと skip / limit パターン
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = ["ノート", "ペン", "消しゴム", "定規", "はさみ"]

# skip 件読み飛ばして limit 件だけ返す (一覧を少しずつ取り出す定番の形)
@app.get("/items")
def read_items(skip: int = 0, limit: int = 2):
    return items[skip : skip + limit]

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/items").json())                 # 先頭から2件
print(client.get("/items?skip=2&limit=2").json())  # 2件飛ばして2件
print(client.get("/items?skip=4").json())          # 残りが1件でもエラーにならない
