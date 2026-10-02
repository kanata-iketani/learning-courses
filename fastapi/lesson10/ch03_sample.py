# lesson10 ch03: クラス依存 (CommonQueryParams パターン)
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

class CommonQueryParams:
    # __init__ の引数がそのままクエリパラメータになる
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 3):
        self.q = q
        self.skip = skip
        self.limit = limit

books = ["Python入門", "Python実践", "FastAPI入門", "Go入門"]

@app.get("/books")
def list_books(params: CommonQueryParams = Depends()):
    # Depends() と省略すると、型注釈のクラスが依存として使われる
    result = books
    if params.q is not None:
        result = [b for b in result if params.q in b]
    return result[params.skip : params.skip + params.limit]

client = TestClient(app)
for path in ["/books", "/books?q=Python", "/books?q=Python&limit=1"]:
    r = client.get(path)
    print(r.json())
