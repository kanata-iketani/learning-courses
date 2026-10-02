from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

songs = ["春の歌", "夏の歌", "夏祭り", "秋の空"]

class CommonQueryParams:
    # __init__ の引数がクエリパラメータとして解釈される
    def __init__(self, q: str | None = None, limit: int = 3):
        self.q = q
        self.limit = limit

@app.get("/songs")
def list_songs(params: CommonQueryParams = Depends()):
    # Depends() の省略形: 型注釈 CommonQueryParams が依存になる
    # 渡ってくるのは辞書ではなくインスタンスなので属性でアクセスする
    result = songs
    if params.q is not None:
        result = [s for s in result if params.q in s]
    return result[: params.limit]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for path in ["/songs", "/songs?q=夏&limit=1"]:
    r = client.get(path)
    print(r.json())
