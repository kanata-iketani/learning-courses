from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# データベースの代わりのリスト (変更しない)
tasks = [
    {"id": 1, "name": "買い物", "done": False},
    {"id": 2, "name": "掃除", "done": True},
]

# id が一致した時点で return すると、for 文ごと関数が終わります。
# for 文を最後まで抜けた = 見つからなかった、なのでエラーの辞書を返します。
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "not found"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/tasks/1")
print(r.status_code)
print(r.json())
r2 = client.get("/tasks/99")
print(r2.json())
