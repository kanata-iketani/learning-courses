# lesson04 ch01: パスにない引数はクエリパラメータになる
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# q はパス /search に含まれない → クエリパラメータとして受け取る
@app.get("/search")
def search(q: str):
    return {"q": q}

# 複数のクエリパラメータは & でつなぐ
@app.get("/find")
def find(word: str, lang: str):
    return {"word": word, "lang": lang}

# --- 動作確認 ---
client = TestClient(app)
print(client.get("/search?q=fastapi").json())
print(client.get("/find?word=hello&lang=en").json())
