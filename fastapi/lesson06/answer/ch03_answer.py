from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

# 既定値の位置に Query(制約) を書くと、クエリパラメータが検証されます。
# min_length=3 なので 2 文字以下のキーワードは 422 になります。
@app.get("/find")
def find(keyword: str = Query(min_length=3)):
    return {"keyword": keyword}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/find?keyword=fastapi")
print(r.status_code)
print(r.json())
r2 = client.get("/find?keyword=ab")
print(r2.status_code)
