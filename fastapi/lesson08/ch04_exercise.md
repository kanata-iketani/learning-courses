# lesson08 ch04 演習: PUT で更新

タスクを更新する API を作ります。

- `name`(文字列)と `done`(真偽値)を持つモデル `TaskIn` を定義する
- `PUT /tasks/{task_id}` で対象をリスト `tasks` から探し、見つかった辞書を `update(受け取ったモデル.model_dump())` で上書きして返す
- 見つからなければ `{"error": "not found"}` を返す

**期待出力**

```text
200
{'id': 1, 'name': '買い物', 'done': True}
{'error': 'not found'}
```
