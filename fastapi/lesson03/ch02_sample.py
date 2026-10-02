# lesson03 ch02: 型ヒントで int に自動変換
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    # int に変換済みなので、そのまま計算に使える
    return {"item_id": item_id, "double": item_id * 2}

# --- 動作確認 ---
client = TestClient(app)

r = client.get("/items/3")
print(r.status_code)
print(r.json())  # item_id は数値の 3 (クォートが付かない)

# int にできない値は 422 が自動で返る
r = client.get("/items/abc")
print(r.status_code)
print(r.json()["detail"][0]["msg"])  # エラーの理由
