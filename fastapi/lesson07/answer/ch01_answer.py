from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    price: int

# response_model=Book により、返した辞書は Book の形に整えられます。
# memo は Book にないキーなので、レスポンスから自動で取り除かれます。
@app.get("/books/1", response_model=Book)
def get_book():
    return {"title": "FastAPI入門", "price": 2500, "memo": "在庫わずか"}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.get("/books/1")
print(r.status_code)
print(r.json())
