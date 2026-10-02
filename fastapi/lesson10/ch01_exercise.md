# lesson10 ch01 演習: Depends とは

店の情報を返す依存関数を使って `GET /shop` を作ってください。

- 依存関数 `get_shop_info` を定義し、`{"shop": "demo堂", "open": True}` を返す
- `GET /shop` は引数 `info: dict = Depends(get_shop_info)` で受け取り、`info` をそのまま返す

**期待出力**

```text
200
{'shop': 'demo堂', 'open': True}
```
