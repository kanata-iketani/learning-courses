# lesson04 ch04: str | None と bool のクエリパラメータ
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# q は「あってもなくてもよい」。省略されると None になる
@app.get("/search")
def search(q: str | None = None, sale: bool = False):
    if q is None:
        return {"q": None, "sale": sale, "hit": 0}
    return {"q": q, "sale": sale, "hit": 1}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/search").json())                  # q は None のまま
print(client.get("/search?q=pen").json())
print(client.get("/search?q=pen&sale=true").json())  # "true" → True に変換
