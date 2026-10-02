# lesson05 ch04 演習: model_dump とレスポンス

ユーザー登録 API を作ります。

- `name`(文字列)と `age`(整数)を持つモデル `User` を定義する
- `POST /users` で `User` を受け取り、`model_dump()` で辞書にしてから、18 歳以上かどうかの真偽値をキー `adult` として追加して返す

**期待出力**

```text
200
{'name': 'demo', 'age': 20, 'adult': True}
{'name': 'python', 'age': 13, 'adult': False}
```
