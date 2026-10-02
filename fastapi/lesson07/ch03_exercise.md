# lesson07 ch03 演習: status_code=201 の指定

タスク作成 API を 201 で応答させます。

- `name`(文字列)を持つモデル `Task` を定義する
- `POST /tasks` で `Task` を受け取り、そのまま返す。デコレータに `status_code=201` を指定する

**期待出力**

```text
201
{'name': '買い物'}
```
