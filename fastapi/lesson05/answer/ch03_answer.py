from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Rectangle(BaseModel):
    width: int
    height: int

# 受け取った値は rect.width のように属性で取り出して計算に使います。
# int どうしの掛け算になることが型ヒントで保証されています。
@app.post("/rectangles")
def create_rectangle(rect: Rectangle):
    return {"area": rect.width * rect.height}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/rectangles", json={"width": 7, "height": 5})
print(r.status_code)
print(r.json())
r2 = client.post("/rectangles", json={"width": 3, "height": 3})
print(r2.json())
