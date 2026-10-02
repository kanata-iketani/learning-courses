from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# データベースの代わりのリスト (変更しない)
tasks = [
    {"id": 1, "name": "買い物", "done": False},
    {"id": 2, "name": "掃除", "done": True},
]

# id と done はサーバ側で決めるので、入力モデルには name だけを持たせます。
class TaskIn(BaseModel):
    name: str

# model_dump() で辞書にすれば id と done を追加できます。
# 新規作成なので status_code=201 を指定します。
@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    new_task = task.model_dump()
    new_task["id"] = len(tasks) + 1
    new_task["done"] = False
    tasks.append(new_task)
    return new_task

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/tasks", json={"name": "洗濯"})
print(r.status_code)
print(r.json())
print(tasks)
