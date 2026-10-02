# lesson06 ch04: Path でパスパラメータを検証する
from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

app = FastAPI()

# user_id は 1 以上の整数だけ受け付ける
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=1)):
    return {"user_id": user_id}

# --- 動作確認 ---
client = TestClient(app)
r = client.get("/users/5")
print(r.status_code)
print(r.json())
r2 = client.get("/users/0")
print(r2.status_code)  # ge=1 に違反 → 422
