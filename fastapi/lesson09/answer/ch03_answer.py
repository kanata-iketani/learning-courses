from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

menu = {
    1: {"name": "コーヒー", "price": 480},
    2: {"name": "紅茶", "price": 520},
}

@app.get("/menu/{item_id}")
def read_menu(item_id: int):
    # ガード節: 異常系(404)を先に raise で片付けると
    # 以降は正常系だけになり、else もネストも不要になる
    if item_id not in menu:
        raise HTTPException(status_code=404, detail=f"menu {item_id} は見つかりません")
    return menu[item_id]

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
for item_id in [1, 3]:
    r = client.get(f"/menu/{item_id}")
    print(r.status_code)
    print(r.json())
