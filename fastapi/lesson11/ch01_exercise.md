# lesson11 ch01 演習: APIRouter でエンドポイントをまとめる

APIRouter を使って動物一覧 API を作ってください。

- `router = APIRouter()` を作り、`@router.get("/animals")` で `["犬", "猫"]` を返すエンドポイントを登録する
- `app.include_router(router)` で app に合体させる

**期待出力**

```text
200
['犬', '猫']
```
