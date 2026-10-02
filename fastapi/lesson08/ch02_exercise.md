# lesson08 ch02 演習: 個別の GET

タスクを 1 件取り出す API を作ります。

- `GET /tasks/{task_id}` でパスパラメータ `task_id`(整数)を受け取る
- リスト `tasks` を for 文で探し、`id` が一致した辞書を返す
- 見つからなければ `{"error": "not found"}` を返す

**期待出力**

```text
200
{'id': 1, 'name': '買い物', 'done': False}
{'error': 'not found'}
```
