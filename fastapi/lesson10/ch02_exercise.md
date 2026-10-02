# lesson10 ch02 演習: 共通クエリパラメータを Depends でまとめる

色の一覧 API `GET /colors` を、共通クエリパラメータの依存関数で作ってください。

- 依存関数 `pagination(skip: int = 0, limit: int = 3)` を定義し、`{"skip": skip, "limit": limit}` を返す
- `GET /colors` は `page: dict = Depends(pagination)` で受け取り、`colors[skip : skip + limit]` を返す

**期待出力**

```text
['赤', '青', '黄']
['黄', '緑']
```
