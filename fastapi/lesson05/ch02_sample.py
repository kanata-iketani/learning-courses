# lesson05 ch02: POST でボディを受け取る
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

# @app.post で「POST で呼ばれる関数」になる
@app.post("/echo")
def echo(msg: Message):
    return {"received": msg.text}

# --- 動作確認 ---
client = TestClient(app)
# json= に渡した辞書がリクエストボディになる
r = client.post("/echo", json={"text": "こんにちは"})
print(r.status_code)
print(r.json())

# POST 用の URL を GET で呼ぶと 405 (Method Not Allowed)
r2 = client.get("/echo")
print(r2.status_code)
