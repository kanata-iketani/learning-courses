# lesson11 ch03 演習: async def エンドポイント

非同期エンドポイント `GET /price` を作ってください。

- 非同期関数 `fetch_price` を `async def` で定義し、`480` を返す
- `GET /price` を `async def` で定義し、`await fetch_price()` の結果を `{"price": 結果}` として返す

**期待出力**

```text
200
{'price': 480}
```
