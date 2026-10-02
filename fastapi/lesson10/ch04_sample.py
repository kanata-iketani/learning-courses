# lesson10 ch04: 依存の中の依存 (ネスト)
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 1 段目: 設定を返す依存
def get_settings():
    return {"shop": "demo堂"}

# 2 段目: 依存関数の中でさらに Depends を使える
def get_greeting(settings: dict = Depends(get_settings)):
    return f"ようこそ {settings['shop']} へ"

@app.get("/welcome")
def welcome(greeting: str = Depends(get_greeting)):
    # エンドポイントは一番外側の依存だけ書けばよい
    # (get_settings → get_greeting の順に FastAPI が解決する)
    return {"message": greeting}

client = TestClient(app)
r = client.get("/welcome")
print(r.status_code)
print(r.json())
