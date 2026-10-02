from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

colors = ["赤", "青", "黄", "緑", "白"]

# 依存関数の引数は、エンドポイントに書いたときと同じく
# クエリパラメータ (?skip=2&limit=2) として受け取られる
def pagination(skip: int = 0, limit: int = 3):
    return {"skip": skip, "limit": limit}

@app.get("/colors")
def list_colors(page: dict = Depends(pagination)):
    # 一覧の切り出しロジックは各エンドポイント側に書く
    return colors[page["skip"] : page["skip"] + page["limit"]]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for path in ["/colors", "/colors?skip=2&limit=2"]:
    r = client.get(path)
    print(r.json())
