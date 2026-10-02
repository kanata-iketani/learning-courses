# lesson04 ch04 演習: bool と None

GET `/items` で、`q` (str | None、デフォルト None) と `in_stock` (bool、デフォルト False) を受け取り、`{"q": q, "in_stock": in_stock}` を返すエンドポイントを書いてください。動作確認部分は、何も付けない場合と `?q=pen&in_stock=true` の場合を出力します。

**期待出力**

```text
{'q': None, 'in_stock': False}
{'q': 'pen', 'in_stock': True}
```
