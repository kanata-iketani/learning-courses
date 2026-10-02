# lesson11 ch02 演習: prefix と tags

prefix と tags 付きの router でユーザー API を作ってください。

- `router = APIRouter(prefix="/users", tags=["users"])` を作る
- `@router.get("/")` で `["佐藤", "鈴木"]` を返す(実際のパスは `/users/`)
- `@router.get("/{user_id}")` で `{"id": user_id}` を返す
- `app.include_router(router)` で合体させる

**期待出力**

```text
200
['佐藤', '鈴木']
200
{'id': 1}
```
