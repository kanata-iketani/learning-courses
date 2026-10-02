from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# リストを返すと JSON 配列になります。json.dumps は不要で、FastAPI が変換します。
# 一覧 API は「辞書のリスト」を返すのが定番の形です。
@app.get("/todos")
def list_todos():
    return [{"id": 1, "task": "買い物"}, {"id": 2, "task": "掃除"}]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/todos").json())
