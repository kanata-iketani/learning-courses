# lesson08 ch03 演習: POST で追加

タスクを追加する API を作ります。

- `name`(文字列)を持つモデル `TaskIn` を定義する
- `POST /tasks`(`status_code=201`)で `TaskIn` を受け取り、`model_dump()` で辞書にしてから、キー `id` に `len(tasks) + 1`、キー `done` に `False` を追加する
- その辞書をリスト `tasks` に `append` してから返す

**期待出力**

```text
201
{'name': '洗濯', 'id': 3, 'done': False}
[{'id': 1, 'name': '買い物', 'done': False}, {'id': 2, 'name': '掃除', 'done': True}, {'name': '洗濯', 'id': 3, 'done': False}]
```
