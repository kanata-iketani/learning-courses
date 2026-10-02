from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# 入力用はパスワードを受け取り、出力用は持たない、と分けるのが定石です。
class AccountIn(BaseModel):
    email: str
    password: str

class AccountOut(BaseModel):
    email: str

# response_model=AccountOut のおかげで、user をそのまま返しても
# レスポンスには email しか含まれず、パスワードが漏れません。
@app.post("/accounts", response_model=AccountOut)
def create_account(account: AccountIn):
    return account

# --- 動作確認(この下は変更しない) ---
client = TestClient(app)
r = client.post("/accounts", json={"email": "demo@example.com", "password": "secret777"})
print(r.status_code)
print(r.json())
