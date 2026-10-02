from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# デコレータが「パス → 関数」の対応表を作るので、パスの数だけ組を書きます。
@app.get("/")
def home():
    return {"page": "home"}

# 関数名はパスと無関係ですが、重複しない別の名前にします。
@app.get("/about")
def about():
    return {"page": "about"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/").json())
print(client.get("/about").json())
