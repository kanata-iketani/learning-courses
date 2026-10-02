# lesson05 ch01 演習: Pydantic の BaseModel

書籍データを受け取る API を作ります。

- `title`(文字列)と `price`(整数)の 2 つのフィールドを持つモデル `Book` を定義する
- `POST /books` で `Book` を受け取り、そのまま返す

**期待出力**

```text
200
{'title': 'FastAPI入門', 'price': 2500}
```
