from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# データベースの代わりのリスト (変更しない)
tasks = [
    {"id": 1, "name": "買い物", "done": False},
    {"id": 2, "name": "掃除", "done": True},
]

# 一覧はリストをそのまま返すだけです。
# FastAPI が辞書のリストを JSON の配列に変換してくれます。
@app.get("/tasks")
def list_tasks():
    return tasks

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/tasks")
print(r.status_code)
print(r.json())
