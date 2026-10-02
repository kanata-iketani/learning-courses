from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

def get_name():
    return "demo"

# 依存関数の引数にも Depends を書ける(ネスト)
def get_message(name: str = Depends(get_name)):
    return f"こんにちは、{name}さん"

@app.get("/greet")
def greet(message: str = Depends(get_message)):
    # get_name → get_message の順に FastAPI が自動で解決するので、
    # エンドポイントは一番外側の get_message だけ指定すればよい
    return {"message": message}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/greet")
print(r.status_code)
print(r.json())
