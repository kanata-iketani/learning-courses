from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Comment(BaseModel):
    author: str
    body: str

# データを新しく送るので @app.post を使います。
# ボディの JSON は Comment に変換されて届くので、属性で取り出せます。
# 返す辞書のキー名は自由に決められます (body を message に変えて返す)。
@app.post("/comments")
def create_comment(comment: Comment):
    return {"author": comment.author, "message": comment.body}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/comments", json={"author": "demo", "body": "いいね"})
print(r.status_code)
print(r.json())
r2 = client.get("/comments")
print(r2.status_code)
