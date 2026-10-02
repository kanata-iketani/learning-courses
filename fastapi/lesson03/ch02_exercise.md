# lesson03 ch02 演習: 型ヒントで int 変換

GET `/items/{item_id}` で、`item_id` を int として受け取り、`{"item_id": item_id, "price": item_id * 100}` を返すエンドポイントを書いてください。動作確認部分は `/items/5` の結果と、数値にできない `/items/apple` のステータスコードを出力します。

**期待出力**

```text
200
{'item_id': 5, 'price': 500}
422
```
