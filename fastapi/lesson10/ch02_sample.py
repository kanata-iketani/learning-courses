# lesson10 ch02: 共通クエリパラメータを Depends でまとめる
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# skip と limit はクエリパラメータとして受け取られる
def pagination(skip: int = 0, limit: int = 2):
    return {"skip": skip, "limit": limit}

fruits = ["りんご", "みかん", "ぶどう", "もも", "なし"]
teas = ["緑茶", "紅茶", "麦茶"]

@app.get("/fruits")
def list_fruits(page: dict = Depends(pagination)):
    return fruits[page["skip"] : page["skip"] + page["limit"]]

@app.get("/teas")
def list_teas(page: dict = Depends(pagination)):
    # 一覧系のエンドポイントすべてで同じ依存関数を共有できる
    return teas[page["skip"] : page["skip"] + page["limit"]]

client = TestClient(app)
for path in ["/fruits", "/fruits?skip=1&limit=3", "/teas?limit=1"]:
    r = client.get(path)
    print(r.json())
