from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    name: str

# 「新しく作った」ことを伝えるため、既定の 200 ではなく 201 を指定します。
# デコレータに書くだけで、成功時のステータスコードが変わります。
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    return task

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/tasks", json={"name": "買い物"})
print(r.status_code)
print(r.json())
