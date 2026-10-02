# lesson10 ch01: Depends とは
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 依存関数: 共通で使いたい処理をふつうの関数として書く
def get_app_info():
    return {"app_name": "メモ帳API", "version": "1.0"}

@app.get("/about")
def about(info: dict = Depends(get_app_info)):
    # FastAPI が get_app_info() を呼び、戻り値を info に入れてくれる
    return info

@app.get("/status")
def status(info: dict = Depends(get_app_info)):
    # 別のエンドポイントでも同じ依存関数を使い回せる
    return {"app_name": info["app_name"], "ok": True}

client = TestClient(app)
r = client.get("/about")
print(r.status_code)
print(r.json())
r = client.get("/status")
print(r.status_code)
print(r.json())
