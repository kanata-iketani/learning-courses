# lesson06 ch02 演習: Field で制約を付ける

在庫登録 API に制約を付けます。

- `name`(文字列、`Field(max_length=5)` で 5 文字以内)と `stock`(整数、`Field(ge=0)` で 0 以上)を持つモデル `Product` を定義する
- `POST /products` で `Product` を受け取り、そのまま返す

動作確認では「正しいデータ」「stock が負のデータ」「name が長すぎるデータ」の 3 パターンを送ります。

**期待出力**

```text
200
{'name': 'pen', 'stock': 0}
422
422
```
