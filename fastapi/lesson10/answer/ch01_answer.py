from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 依存関数はふつうの関数。共通で返したい値をここに集める
def get_shop_info():
    return {"shop": "demo堂", "open": True}

@app.get("/shop")
def read_shop(info: dict = Depends(get_shop_info)):
    # Depends と書くだけで FastAPI が get_shop_info() を呼び、
    # 戻り値を info に入れてくれる(自分で呼ぶコードは不要)
    return info

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/shop")
print(r.status_code)
print(r.json())
