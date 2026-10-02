# lesson07 ch01 演習: response_model の指定

書籍取得 API のレスポンスの形を宣言します。

- `title`(文字列)と `price`(整数)を持つモデル `Book` を定義する
- `GET /books/1` に `response_model=Book` を指定し、関数からは辞書 `{"title": "FastAPI入門", "price": 2500, "memo": "在庫わずか"}` を返す

`memo` は `Book` にないキーなので、レスポンスには含まれません。

**期待出力**

```text
200
{'title': 'FastAPI入門', 'price': 2500}
```
