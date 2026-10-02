from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# パスの {name} と引数名 name を一致させることで、URL の値が関数に渡ります。
# /users/demo でも /users/guest でも、この1つの関数が処理します。
@app.get("/users/{name}")
def read_user(name):
    return {"hello": name}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/users/demo").json())
print(client.get("/users/guest").json())
