from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# データベースの代わりのリスト (変更しない)
tasks = [
    {"id": 1, "name": "買い物", "done": False},
    {"id": 2, "name": "掃除", "done": True},
]

class TaskIn(BaseModel):
    name: str
    done: bool

# パスパラメータ (task_id) とボディ (new) は同時に受け取れます。
# 辞書の update に model_dump() を渡すと、name と done がまとめて上書きされ、
# id はそのまま残ります。
@app.put("/tasks/{task_id}")
def update_task(task_id: int, new: TaskIn):
    for task in tasks:
        if task["id"] == task_id:
            task.update(new.model_dump())
            return task
    return {"error": "not found"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.put("/tasks/1", json={"name": "買い物", "done": True})
print(r.status_code)
print(r.json())
r2 = client.put("/tasks/99", json={"name": "x", "done": False})
print(r2.json())
