from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# name はパス /greet に含まれないので、クエリパラメータとして扱われます。
# ?name=demo の値が引数 name に入り、f 文字列で挨拶文を組み立てます。
@app.get("/greet")
def greet(name: str):
    return {"greeting": f"こんにちは、{name}さん"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/greet?name=demo").json())
