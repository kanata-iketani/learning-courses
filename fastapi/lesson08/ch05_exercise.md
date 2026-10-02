# lesson08 ch05 演習: DELETE で削除

タスクを削除する API を作ります。一覧の `GET /tasks` はスターターに用意してあります。

- `DELETE /tasks/{task_id}`(`status_code=204`)を作る
- `enumerate` で位置を調べながらリスト `tasks` を探し、`id` が一致したら `pop` で取り除いて `return` する

**期待出力**

```text
204
200
[{'id': 1, 'name': '買い物', 'done': False}]
```
