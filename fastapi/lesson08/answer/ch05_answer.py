from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# データベースの代わりのリスト (変更しない)
tasks = [
    {"id": 1, "name": "買い物", "done": False},
    {"id": 2, "name": "掃除", "done": True},
]

@app.get("/tasks")
def list_tasks():
    return tasks

# pop には「何番目か」が必要なので、enumerate で位置 i も受け取ります。
# 204 (No Content) なのでボディは返さず、return だけで関数を終えます。
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.delete("/tasks/2").status_code)
r = client.get("/tasks")
print(r.status_code)
print(r.json())
