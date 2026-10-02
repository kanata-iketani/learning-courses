# lesson02 ch02: デコレータを増やしてパスを増やす
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# デコレータ1つにつきパス1つ。関数名は処理の内容が分かる名前にする
@app.get("/")
def home():
    return {"page": "home"}

@app.get("/menu")
def menu():
    return {"page": "menu"}

@app.get("/access")
def access():
    return {"page": "access"}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/").json())
print(client.get("/menu").json())
print(client.get("/access").json())
