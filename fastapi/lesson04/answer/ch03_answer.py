from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

fruits = ["りんご", "みかん", "ぶどう", "もも", "バナナ"]

# 型ヒント int のおかげで、?skip=2 の "2" が数値 2 になりスライスに直接使えます。
# skip / limit のデフォルト値により、何も付けなければ先頭 3 件が返ります。
@app.get("/fruits")
def read_fruits(skip: int = 0, limit: int = 3):
    return fruits[skip : skip + limit]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/fruits").json())
print(client.get("/fruits?skip=2&limit=2").json())
