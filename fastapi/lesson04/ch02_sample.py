# lesson04 ch02: デフォルト値で省略可能にする
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# lang にデフォルト値があるので ?lang=... は省略できる
@app.get("/hello")
def hello(lang: str = "ja"):
    if lang == "en":
        return {"message": "Hello"}
    return {"message": "こんにちは"}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/hello").json())          # 省略 → デフォルトの "ja"
print(client.get("/hello?lang=en").json())  # 指定 → 上書きされる
