from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# 本来は animals.py など別ファイルに書く部分
router = APIRouter()

@router.get("/animals")
def list_animals():
    return ["犬", "猫"]

# include_router を忘れると 404 になる(登録されていないため)
app.include_router(router)

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/animals")
print(r.status_code)
print(r.json())
