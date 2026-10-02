# lesson03 ch01: パスパラメータ {item_id}
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# {item_id} の部分が、同じ名前の引数 item_id に渡される
@app.get("/items/{item_id}")
def read_item(item_id):
    # 型ヒントなしなら文字列 (str) のまま
    return {"item_id": item_id}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/items/1").json())    # '1' は文字列として渡る
print(client.get("/items/abc").json())  # どんな値でも同じ関数が処理する
