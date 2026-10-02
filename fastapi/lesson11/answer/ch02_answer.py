from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# prefix を付けると router 内は "/" や "/{user_id}" だけ書けばよい
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    # 実際のパスは /users/
    return ["佐藤", "鈴木"]

@router.get("/{user_id}")
def read_user(user_id: int):
    # 実際のパスは /users/{user_id}
    return {"id": user_id}

app.include_router(router)

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/users/")
print(r.status_code)
print(r.json())
r = client.get("/users/1")
print(r.status_code)
print(r.json())
