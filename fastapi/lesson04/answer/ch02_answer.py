from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# size: str = "M" とデフォルト値を書くと、?size=... を省略できるようになります。
# 省略時は "M"、?size=L を付ければ "L" で上書きされます。
@app.get("/coffee")
def coffee(size: str = "M"):
    return {"size": size}

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
print(client.get("/coffee").json())
print(client.get("/coffee?size=L").json())
